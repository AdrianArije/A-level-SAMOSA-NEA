import sqlite3
from datetime import datetime, timezone

class DatabaseClass:
    def __init__(self):
        self.connection = sqlite3.connect("Database.db")
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def validate(self,text):
        self.text = text
        if len(self.text) >= 8:
            return True
        else:
            return False

    def Signup(self,username, password):
        self.username = username
        self.password = password

        if self.validate(self.username):
            duplicate =self.cursor.execute("""SELECT * FROM Users
                                WHERE Username = (?)
                                """,(self.username,)).fetchall()
            if duplicate:
                return False
            else:
                if self.validate(self.password):
                    self.cursor.execute("""
                        INSERT INTO Users (Username,PasswordHash,Role_Id)
                        VALUES (?,?,?)
    """,(self.username,self.password, 1))
                else: 
                    return False
            self.connection.commit()
            return True

    def Login(self,username,password): ## Initialize functions
        self.username = username
        self.password = password

        if self.validate(self.username): # Validate username
            find_user = self.cursor.execute("""
                SELECT * FROM Users 
                WHERE Username = (?)
""",(self.username,)).fetchone() # Search Database
            if find_user:
                passcode = find_user[2] # Retrieve password
                if passcode == self.password: # Compare password
                    return "Access granted"
                else:
                    return "Incorrect password"
            else:
                return "Username not found"
        else:
            return "Invalid username"

    def get_user(self,username):
        result = self.cursor.execute("SELECT * FROM Users WHERE Username IS ?",(username,)).fetchall()
        return result

    def display_menu(self,word,category):
        placeholders = ",".join(["?"] * len(category))
        if word != "" and category != []:
            items = self.cursor.execute(f"""
            SELECT * FROM MenuItems 
            WHERE Item_Name LIKE ? AND Category_ID IN ({placeholders})
            """,(f"%{word}%",*category)).fetchall()
        elif word == "" and category != []:
           items = self.cursor.execute(f"""
           SELECT * FROM MenuItems 
           WHERE Category_ID IN ({placeholders})
           """,(category)).fetchall()
        elif word != "" and category == []:
            items = self.cursor.execute("""
            SELECT * FROM MenuItems 
            WHERE Item_Name LIKE (?)
            """,(f"%{word}%",)).fetchall()
        else:
            items = self.cursor.execute("""
                    SELECT * FROM MenuItems
            """).fetchall() 
        return items

    def change_password(self,user,password):
        current_password = self.cursor.execute("""
        SELECT PasswordHash From USERS
        WHERE User_ID = ?        
""",(user,)).fetchall()
        if current_password[0][0] == password:
            return "SAME PASSWORD"
        else:
            self.cursor.execute("""
                    UPDATE Users SET PasswordHash = ?
                    WHERE User_ID = ?   
            """,(password,user))
            return "PASSWORD CHANGED" 

    def get_order_id(self):
        id = self.cursor.execute("SELECT MAX(Order_ID) FROM Orders").fetchall()
        return id[0][0]

    def get_quantity(self,item_id):
        qty = self.cursor.execute("SELECT Quantity FROM MenuItems WHERE Item_ID = ?",(item_id,)).fetchall()
        return qty[0][0]

    def create_order(self,user_id,price,datetime,state):
        self.cursor.execute("""
        INSERT INTO Orders (User_ID,Total_Price, DateTime,Status)
        VALUES(?,?,?,?)
                    """,(user_id,price,datetime,state))

    def add_orderitems(self,item_list):
        order_id = self.get_order_id()
        for item in item_list:
            item_id = item[0]
            item_quantity = item[3]
            item_price = item[3] * item[2]
            self.cursor.execute("""
                    INSERT INTO OrderItems (Orders_ID,Item_ID, Quantity,Price)
                    VALUES(?,?,?,?)
                                """,(order_id,item_id,item_quantity,item_price))

    def update_stock(self,item_list):
        for item in item_list:
            ID = item[0]
            quantity = item[3]
            stock_level = self.get_quantity(ID)
            remaining_stock = stock_level - quantity
            self.cursor.execute("""UPDATE MenuItems 
            SET Quantity = ?
             WHERE Item_ID = ? """,(remaining_stock,ID))

    def checkout(self,user_id,cart_items):
        ordertime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        overall_price = 0
        for item in cart_items:
            ID = item[0]
            name = item[1]
            price = item[2] * item[3]
            quantity = item[3]
            stock_level = self.get_quantity(ID)

            if quantity > stock_level:
                return "FAILED"
            
            overall_price += price
        
        try:
            self.create_order(user_id,overall_price,ordertime,False)
            self.add_orderitems(cart_items)
            self.update_stock(cart_items)
            self.connection.commit()
            return "SUCCESS"
        except:
            self.connection.rollback()
            return "FAILED"

    def get_orders(self,user_id):
        result = self.cursor.execute("SELECT Order_ID FROM Orders WHERE User_ID = ?",(user_id,)).fetchall() # get list of users orders
        return result

    def get_order_items(self,order_number):
        data = self.cursor.execute("SELECT Item_ID, Quantity, Price FROM OrderItems WHERE Orders_ID = ?",(order_number,)).fetchall() # get item_id, quantity and price
        return data

    def order_history(self,item_list):
        overall_order = [] # list format
        for item in item_list:
            item_id = item[0]
            item_qty = item[1]
            item_price = item[2]
            item_name = self.cursor.execute("SELECT Item_Name FROM MenuItems WHERE Item_ID = ?",(item_id,)).fetchall() # item name
            invoice = (item_name,item_qty,item_price)
            overall_order.append(invoice)
        return overall_order


    def add_items(self,name,desc,image,qty,price,cty):
        check_validity = self.cursor.execute("""
        SELECT * FROM MenuItems
        WHERE Item_Name = ?
        """,(name,)).fetchall()
        cty_id = self.cursor.execute("SELECT Category_ID FROM Categories WHERE Category_Name = ?",(cty,)).fetchone()
        if check_validity:
            return "Item name Exists"
        else:
            self.cursor.execute("""INSERT INTO MenuItems (Item_Name,Item_Description,Image,Quantity,Price,Category_ID)
            VALUES (?,?,?,?,?,?)""",(name,desc,"Images/No-image.jpg",qty,price,cty_id[0]))
            self.connection.commit()
            return "Item Added"
            


    def admin_orders_db(self):
        total_orders = self.cursor.execute("SELECT Order_ID FROM Orders").fetchall()
        return total_orders


    def status(self,id):
        st = self.cursor.execute("""
                SELECT Status FROM Orders WHERE Order_ID == ?
""",(id,)).fetchone()
        return st


    def chg_stat(self,id):
        self.cursor.execute("UPDATE Orders SET Status = True WHERE Order_ID = ?",(id,))
        self.connection.commit()

    