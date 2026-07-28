import sqlite3

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

