import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from  DatabaseManager import DatabaseClass
from PIL import ImageTk, Image
import hashlib

#----------------------------------------------------------------------------------------------------------------------------------------------------
class MainApp: # Initializing the MainApp class which serves as the controller
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SAMOSA") # Screen Geometry
        self.root.geometry("800x600")
        self.database = DatabaseClass()
        self.current_user = None # stores the users session
        # This dictionary would contain all GUI classes
        self.frames = {
            "login" : LoginFrame(self),
            "orderframe" : OrderFrame(self),
            "settings" : SettingsFrame(self),
            "orderhistory" : OrderHistoryFrame(self),
            "additem": AddItem(self),
            "adminorders" : showOrders(self)
        }

        self.show_frame(self.frames["login"]) # Sets the current screen to show once application starts running
        
        self.root.mainloop()

    def show_frame(self,frame): # Function to show frames and prevent other frames from showing
        for current_frame in self.frames.values():
            current_frame.pack_forget()
        if hasattr(frame,"on_show"):
            frame.on_show()
        frame.pack(fill = "both", expand=True)


#----------------------------------------------------------------------------------------------------------------------------------------------------
class LoginFrame(tk.Frame): # Login frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed

        self.app = app
        self.configure(background="#3a79ee")

        intro = tk.Label(self,text = "Welcome to Adrian's Canteen ",font= ("Arial", 43),bg="#3a79ee", foreground="#fbf025") # Intro text label
        intro.grid(row=0,column = 1,columnspan=3, padx = 10, pady =15)

        self.entry_frame = tk.Frame(self) # Creating new frame for entry widgets
        self.entry_frame.place(x=300,y=220)

        lgntext = tk.Label(self.entry_frame,text = "    Login In / Sign up    ",font= ("Arial", 20)) # Login label
        lgntext.grid(row=0,column = 0, columnspan=2)

        username_label = tk.Label(self.entry_frame,text = "Username",font = ("Arial",10)) # Username label
        username_label.grid(row=1,column = 0)

        self.username_entry =tk.Entry(self.entry_frame,width=20) # Username entry box
        self.username_entry.grid(row=1,column = 1, padx = 12, pady =10)

        password_label = tk.Label(self.entry_frame,text = "Password",font = ("Arial",10)) # Password entry label
        password_label.grid(row=2,column = 0)

        self.password_entry =tk.Entry(self.entry_frame,width=20,show="*") # Password entry box
        self.password_entry.grid(row=2,column = 1, padx = 12, pady =10)

        loginbtn = tk.Button(self.entry_frame, text="Login", command=self.login) # Login button
        loginbtn.grid(row=3,column = 0, pady=10)

        signupbtn = tk.Button(self.entry_frame, text="Sign Up", command=self.signup) # Sign up button
        signupbtn.grid(row=3,column = 1, pady=5)

    def login(self): # The login function to verify users login
        hashed_password = hashlib.sha256(self.password_entry.get().encode()).hexdigest() # Hashing the password
        Username = self.username_entry.get() # Getting the password
        access = self.app.database.Login(self.username_entry.get(),hashed_password) # Running the database check

        if access == "Access granted": # Adding the users current status to the dictionary
            USER_ID = self.app.database.get_user(Username)[0]
            self.app.current_user = {
                "ID" : USER_ID[0],
                "USERNAME" : USER_ID[1],
                "ROLE_ID"   : USER_ID[3]
            }
            print(self.app.current_user)
            self.app.show_frame(self.app.frames["orderframe"]) # Takes user to the order frame
            self.password_entry.delete(0,tk.END)# Clearing the fields
            self.username_entry.delete(0,tk.END)
            self.app.frames["orderhistory"].refresh()
        elif access == "Incorrect password":
            messagebox.showerror("Error Logging In", "Incorrect Password entered") # Incorrect password
        elif access == "Username not found":
            messagebox.showerror("Error Logging In", "Username not found. Try Signing Up") # Username not found
        elif access == "Invalid username":
            messagebox.showerror("Error Logging In", "Username is below 8 characters") # Invalid username


    def signup(self): # Sign up verification
            hashed_password = hashlib.sha256(self.password_entry.get().encode()).hexdigest() # Hash password
            valid_pass = self.app.database.validate(self.password_entry.get()) #validate the password
            security = self.app.database.Signup(self.username_entry.get(),hashed_password) # validate the username
            Username = self.username_entry.get()
            if security and valid_pass: # check if the username and password are valid
                USER_ID = self.app.database.get_user(Username)[0]
                self.app.current_user = {
                    "ID" : USER_ID[0],
                    "USERNAME" : USER_ID[1],
                    "ROLE_ID"   : USER_ID[3]
                }# Log user session
                self.password_entry.delete(0,tk.END)# Clearing the fields
                self.username_entry.delete(0,tk.END)
                self.app.show_frame(self.app.frames["orderframe"])
                self.app.frames["orderhistory"].refresh()
            else: # Username already exist
                self.password_entry.delete(0,tk.END)# Clearing the fields
                self.username_entry.delete(0,tk.END)
                messagebox.showerror("Error Signing Up", "Inputs are below 8 characters or Username already exists")
    #print("Login Frame Initialized")


#----------------------------------------------------------------------------------------------------------------------------------------------------
class OrderFrame(tk.Frame): # Customer frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app # Link to the main app handler
        self.configure(background="red") # background colour
        self.cards = [] # Stores all the cards on the screen
        self.search_text = "" # user input text for searching
        self.category = [] # the categories selected
        self.current_items = [] # Stores all the items on the screen 

        self.cartframe= CartFrame(self,app) # Linking cart frame as a sub class of customer frame
        self.cartframe.place_forget() # Hiding the cart frame

        header_frame = tk.Frame(self,bg ="red") # creating header frame for header
        header_frame.pack(fill="x")


        content_frame = tk.Frame(self, bg="yellow") # Creating content frame for items
        content_frame.pack(fill="both", expand=True)

        toolbar_frame = tk.Frame(content_frame, bg="yellow")
        toolbar_frame.pack(fill="x")

        self.menu_scroll = ScrollableFrame(content_frame, bg="brown")
        self.menu_scroll.pack(fill="both", expand=True)
        

        self.toggle_options = tk.Button(header_frame,text = "☰",bg="red", foreground="#fffffd",anchor="center",font = ("Bold",20),
                                        activebackground="red",
                                        activeforeground="white",
                                        command=self.side_panel,bd=2,
                                        highlightbackground="black",
                                        highlightthickness=5,relief="raised") # creating the toggle button widget
        self.toggle_options.pack(side=tk.LEFT)

        intro = tk.Label(header_frame,text = "Welcome to the order page",font= ("Arial", 27),bg="red", foreground="#fbf025",anchor="center") # Intro text
        intro.pack(padx= 100,side=tk.LEFT) # Intro label


        self.search_entry = tk.Entry(toolbar_frame, width=90) # Search entry box
        self.search_entry.grid(row=0, column=0, padx = 25)

        searchbtn = tk.Button(toolbar_frame, text="Search", command=self.refresh_menu) # Search button
        searchbtn.grid(row=0, column=1,padx = 5)

        sort_btn = tk.Menubutton(toolbar_frame,text = "Sort By ▼", relief="raised") # Adding the sort button menu
        sort_btn.grid(row=0,column=3, padx=5) # Set position
        sort_dropdown = tk.Menu(sort_btn,tearoff=0)
        sort_dropdown.add_command(label = "By Price ASC",command = self.filterprice_asc) # Adding sorting button
        sort_dropdown.add_separator()
        sort_dropdown.add_command(label = "By Price DESC",command = self.filterprice_desc) 
        sort_dropdown.add_separator()
        sort_dropdown.add_command(label = "By Name ASC",command = self.filtername_asc)
        sort_dropdown.add_separator()
        sort_dropdown.add_command(label = "By Name DESC",command = self.filtername_desc)
        sort_dropdown.add_separator()
        sort_btn["menu"] = sort_dropdown # Link button to drop down

        self.filter_frame = tk.LabelFrame(content_frame,text="Select Category")# Frame for filter options
        self.filter_frame.place_forget()

        self.drinks_var = tk.BooleanVar() # Making a variable to check if box is ticked
        drinks = tk.Checkbutton(self.filter_frame,text = "Drinks",variable = self.drinks_var)
        drinks.grid(row=0,column = 0)

        self.meals_var = tk.BooleanVar() # Making a variable to check if box is ticked
        meals = tk.Checkbutton(self.filter_frame,text = "Meals",variable = self.meals_var)
        meals.grid(row=1,column = 0)

        self.snack_var = tk.BooleanVar() # Making a variable to check if box is ticked
        snack = tk.Checkbutton(self.filter_frame,text = "Snacks",variable = self.snack_var)
        snack.grid(row=2,column = 0)

        self.desserts_var = tk.BooleanVar() # Making a variable to check if box is ticked
        desserts_var = tk.Checkbutton(self.filter_frame,text = "Desserts",variable = self.desserts_var)
        desserts_var.grid(row=3,column = 0)

        filter_btn = tk.Button(toolbar_frame,text ="Filter ▼", command = self.filterbutton) # Filter button
        filter_btn.grid(row=0,column=2,padx= 5)

        self.filter_action = tk.Button(self.filter_frame,text ="Filter", command = self.filter_action)
        self.filter_action.grid(row=4,column = 0)
        

        self.refresh_menu() # Refresh the menu once user logs in

    def side_panel(self): # Side panel for the options
        self.toggle_frame = tk.Frame(self,bg="grey") # configuring the button coordinates and position
        self.toggle_frame.place(x=0,y=60,height=350,width=200)
        self.toggle_options.config(text =" X ",font = ("Bold",20))
        self.toggle_options.config(command =self.collapse_panel)

        y_axis = 20

        cart_btn = tk.Button(self.toggle_frame, text="CART",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white",command = self.cart)
        cart_btn.place(x=20,y=y_axis) # Creating and placing the cart button
        y_axis+= 40

        orderhistory_btn = tk.Button(self.toggle_frame, text="ORDER HISTORY",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white",command = self.orderpage)
        orderhistory_btn.place(x=20,y=y_axis) # Creating and pplacing the order history button
        y_axis+=40

        settings_btn = tk.Button(self.toggle_frame, text="SETTINGS",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white",command = self.settings)
        settings_btn.place(x=20,y=y_axis) # Creating and placing the settings button
        y_axis+=40

        if self.app.current_user["ROLE_ID"] == 2: # Checking the status of the user
            add_item_btn = tk.Button(self.toggle_frame, text="ADD ITEM",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white",command = self.additems)
            add_item_btn.place(x=20,y=y_axis) # Creating the add items button for admins
            y_axis+=40

            delete_item_btn = tk.Button(self.toggle_frame, text="DELETE ITEM",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white")
            delete_item_btn.place(x=20,y=y_axis) # Creating the delete items button for admins
            y_axis+=40

            upd_item_btn = tk.Button(self.toggle_frame, text="UPDATE ITEM",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white")
            upd_item_btn.place(x=20,y=y_axis) # Creating the update items button for admins
            y_axis+=40

            view_orders_btn = tk.Button(self.toggle_frame, text="VIEW ORDERS",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white", command = self.admin_orders)
            view_orders_btn.place(x=20,y=y_axis) # Creating the view order items button for admins
            y_axis+=40

        logout_btn = tk.Button(self.toggle_frame, text="LOGOUT",font = ("Bold",15),bd=0,bg="grey",fg="white",activebackground="grey",activeforeground="white",command = self.logout)
        logout_btn.place(x=20,y=y_axis) # Creating the logout button 

    def collapse_panel(self): # Collapsing the toggle options tab
        self.toggle_frame.destroy()
        self.toggle_options.config(text =" ☰ ")
        self.toggle_options.config(command =self.side_panel)

    
    def filterbutton(self): # filter button
        self.filter_frame.place(x=620,y =30)

    def filter_action(self):
        self.filter_frame.place_forget() # Close popup
        self.category.clear() # Reset all the checkboxes list
        if self.meals_var.get() == True:
            self.category.append(1) # Append to categries if the category is ticked
        if self.snack_var.get() == True:
            self.category.append(2) # Append to categries if the category is ticked
        if self.drinks_var.get() == True:
            self.category.append(3) # Append to categries if the category is ticked
        if self.desserts_var.get() == True:
            self.category.append(4) # Append to categries if the category is ticked
        self.refresh_menu() # Refresh menu items

    def settings(self): # button to the settings
        self.collapse_panel()
        self.app.show_frame(self.app.frames["settings"])

    def orderpage(self): # Button to the orderpage
       self.collapse_panel()
       self.app.show_frame(self.app.frames["orderhistory"])

    def additems(self): # Button to the add items page
        self.app.show_frame(self.app.frames["additem"])

    def admin_orders(self):
        self.app.show_frame(self.app.frames["adminorders"])


    def cart(self): # Displaying the cart on the screen
        self.collapse_panel()
        self.cartframe.place(relx=0.5, rely=0.5, anchor="center")
        self.cartframe.lift()
        #print("cart")

    def logout(self): # logout function
        self.collapse_panel() # close side options panel
        self.app.current_user = None # change the session of the user to none
        self.cartframe.clear_cart() # clear the cart
        self.cartframe.cart_items.clear()
        self.app.show_frame(self.app.frames["login"]) # switch to the login frame 

    def display_items(self,items): # displaying the items on the screen in a grid format
        index = 0
        for item in items:
            id = item[0]
            name = item[1] 
            desc = item[2] 
            img = item[3]
            price = item[5]
            col = index % 3 # calculate the column position
            rows = index // 3 # calculate the row position
            card = ItemCard(self.menu_scroll.content_frame,self.cartframe,id,name,desc,img,price) # turning the variables into an item card
            card.grid(row=rows,column=col,padx=30,pady=10) # postioning the card on the grid
            index = index + 1
            self.cards.append(card) # add it to the card list in the class
        
    def refresh_menu(self): # refresh the menu
        word = self.search_entry.get() # get user search word
        self.clear_menu()
        self.current_items = self.app.database.display_menu(word,self.category)# search the database for all items linked to the word
        self.display_items(self.current_items) # display the items

    def clear_menu(self): # clar menu
        for card in self.cards:
            card.destroy()
        self.cards.clear() # destroy all the cards made
        #self.current_items.clear()

    def filterprice_desc(self): # bubble sort algorithm for sorting items
        self.clear_menu() # clear menu screen
        for item in range(len(self.current_items)-1): # loop through the list
            for i in range(len(self.current_items)-1): # loop thriugh the list comparing items and swapping
                if self.current_items[i][5] < self.current_items[i + 1][5]:
                    temp = self.current_items[i]
                    self.current_items[i] = self.current_items[i + 1]
                    self.current_items[i + 1]= temp
        self.display_items(self.current_items) # display items

    def filterprice_asc(self):
        self.clear_menu()
        for item in range(len(self.current_items)-1):
            for i in range(len(self.current_items)-1):
                if self.current_items[i][5] > self.current_items[i + 1][5]:
                    temp = self.current_items[i]
                    self.current_items[i] = self.current_items[i + 1]
                    self.current_items[i + 1]= temp
        self.display_items(self.current_items)

    def filtername_asc(self):
        self.clear_menu()
        for item in range(len(self.current_items)-1):
            for i in range(len(self.current_items)-1):
                if self.current_items[i][1] > self.current_items[i + 1][1]:
                    temp = self.current_items[i]
                    self.current_items[i] = self.current_items[i + 1]
                    self.current_items[i + 1]= temp
        self.display_items(self.current_items)

    def filtername_desc(self):
        self.clear_menu()
        for item in range(len(self.current_items)-1):
            for i in range(len(self.current_items)-1):
                if self.current_items[i][1] < self.current_items[i + 1][1]:
                    temp = self.current_items[i]
                    self.current_items[i] = self.current_items[i + 1]
                    self.current_items[i + 1]= temp
        self.display_items(self.current_items)

#----------------------------------------------------------------------------------------------------------------------------------------------------
class CartFrame(tk.Frame): # Cart frame initialization
    def __init__(self,parent,app):
        super().__init__(parent) # Inherits the OrderFrame window as the place to be displayed
        self.app = app
        self.cutomerframe = parent
        self.cart_items = [] # stores all the cart items
        self.cart_item_cards = [] # stores all the cart item cards
        self.configure(background="brown",width=400,height=400)
        self.pack_propagate(False) # Keep size fixed
        content_frame = tk.Frame(self, bg="yellow") # Creating content frame for items
        content_frame.pack(fill="both", expand=True)
        self.cart_scroll = ScrollableFrame(content_frame, bg="brown") # make the frame scrollable
        self.cart_scroll.pack(fill="both", expand=True)
        
        close_btn = tk.Button(self.cart_scroll.content_frame,text = "Close", command=self.close)
        close_btn.grid(row = 0,column = 0)  # create and place the close button

        checkout_btn = tk.Button(self.cart_scroll.content_frame,text = "Checkout", command=self.checkout)
        checkout_btn.grid(row = 0,column = 1) # create and place checkout button

    def price(self): # Calculate the total price of the cart
        total_price = 0
        for item in self.cart_items:
            price = item[2] * item[3]
            total_price += price
        return total_price
    
    def checkout(self): # Checkout function
        if self.cart_items == []: # if cart is empty invalid transaction
            messagebox.showerror("Invalid Request", "Can not checkout on an empty cart")
        else:
           print(self.cart_items)
           request = messagebox.askyesno("Checkout Request", f"Are you sure you want to check out? You total price is £{self.price()}") # validate checkout request
           if request: # If user has validated checkout begin transaction
                print("YES")
                user_id = self.app.current_user["ID"]
                result = self.app.database.checkout(user_id,self.cart_items)
                print(result)
                if result == "SUCCESS":
                    order_num = self.app.database.get_order_id()
                    messagebox.showinfo("Congratulations!", f"Your order has been made!!. Your Order Number is #{order_num}")
                    self.clear_cart()
                    self.empty_cart_list()
                    self.cutomerframe.refresh_menu()
                    self.app.frames["orderhistory"].refresh()
                    self.close()
                elif result == "FAILED":
                    messagebox.showerror("Invalid Request", "Sorry we are expereincing some errors right now please try again.")          
        self.close()

    def close(self): # close cart
        self.place_forget()

    def display_cart(self): # display the items in the cart like on screen in grid form
        index = 2
        for item in self.cart_items:
            id = item[0]
            name = item[1]
            price = item[2]
            qty = item[3]
            col = index % 2
            rows = index // 2
            cart_card =Cart_item_card(self.cart_scroll.content_frame,self,id,name,price,qty)
            self.cart_item_cards.append(cart_card)
            cart_card.grid(row = rows,column = col, padx= 5,pady=5)
            index += 1

    def clear_cart(self): # clear cart
        for card in self.cart_item_cards: # Loop through and destroy all the card objects
            card.destroy()
        self.cart_item_cards.clear() # Clear the cart list of card objects

    def remove_item(self,item_id):
        for item in self.cart_items: # Find the item by id
            if item[0] == item_id:
                self.cart_items.remove(item) # remove from list
        self.clear_cart() # Destroy all widgets on screen
        self.display_cart() # Redrwaw screen.

    def empty_cart_list(self): # empty cart list
        for item in self.cart_items:
            self.cart_items.remove(item)

#----------------------------------------------------------------------------------------------------------------------------------------------------
class SettingsFrame(tk.Frame): # Settings frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="grey")

        header_frame = tk.Frame(self) # creating and placing frames
        header_frame.pack()
        msg = tk.Label(self,text= "Welcome to the settings page", anchor="center", font=("Arial",20), bg = "grey")
        msg.pack(pady=10)

        content_frame = tk.Frame(self,bg = "grey")
        content_frame.pack(fill="both", expand=True)

        user_label = tk.Label(content_frame,text="  Username:  ",font=("Arial",20),bg="grey")
        user_label.grid(row=0,column=0,padx=10,pady=10)

        self.user_entry = tk.Entry(content_frame,width=40)
        self.user_entry.grid(row=0,column= 1,padx= 20,pady=50)

        password_label1 = tk.Label(content_frame,text="  New password:  ",font=("Arial",20),bg="grey")
        password_label1.grid(row=1,column=0,padx=10,pady=10)
        
        self.password1_entry = tk.Entry(content_frame,width=40,show="*")
        self.password1_entry.grid(row=1,column= 1,padx= 20,pady= 50)

        self.password2_label = tk.Label(content_frame,text="  Re-enter New password:  ",font=("Arial",20),bg="grey")
        self.password2_label.grid(row=3,column=0,padx=10,pady=10)
                
        self.password2_entry = tk.Entry(content_frame,width=40,show="*")
        self.password2_entry.grid(row=3,column= 1,padx= 20,pady=50)

        new_pass_btn = tk.Button(content_frame,text="Change password", command= self.change_password)
        new_pass_btn.grid(row=3,column=2, padx= 10,pady=10)

        back_btn = tk.Button(content_frame,text="Back", command= self.back_menu)
        back_btn.grid(row=4,column=1, padx= 10,pady=30)

    def on_show(self): # filling the username field with the current users name
        user = self.app.current_user

        if user is None:
            return

        self.user_entry.config(state="normal")
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, user["USERNAME"])
        self.user_entry.config(state="readonly")
    

    def back_menu(self): # return to previous page
        self.app.show_frame(self.app.frames["orderframe"])

    def change_password(self): # change the password in database
        first_entry = self.password1_entry.get()
        second_entry = self.password2_entry.get()
        if first_entry == "" or second_entry == "": # check if they are the same
            messagebox.showerror("Error", "Makes sure both fields have been filled")
        else:
            if self.app.database.validate(first_entry) and self.app.database.validate(second_entry):
                if first_entry == second_entry: # hash password and add to database
                    hashed_password = hashlib.sha256(first_entry.encode()).hexdigest() 
                    new_entry = self.app.database.change_password(self.app.current_user["ID"],hashed_password)
                    if new_entry == "SAME PASSWORD":
                        messagebox.showerror("Notice","Your new password is the same as the previous one try something different!")
                    elif new_entry == "PASSWORD CHANGED":
                        messagebox.showinfo("Password changed", "Congratulations you have now changed your password. NOTE: Please don't forget it")
                else:
                    messagebox.showerror("Error","Make sure New passwords entered are the same")
            else:
                messagebox.showerror("Error","Make sure password entered is at least 8 characters")

#----------------------------------------------------------------------------------------------------------------------------------------------------
class OrderHistoryFrame(tk.Frame): # Order history frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="brown")
        self.history_cards = [] # holds all the history cards

        header_frame = tk.Frame(self,bg= "brown")
        header_frame.pack()
        
        content_frame = tk.Frame(self,bg="brown")
        content_frame.pack(fill="both", expand=True)

        self.orderhistory_scroll = ScrollableFrame(content_frame, bg="brown")
        self.orderhistory_scroll.pack(fill="both", expand=True)

        header_frame.columnconfigure(1, weight=5)
        header_frame.columnconfigure(0, weight=2)
        header_frame.columnconfigure(2, weight=2)

        intro = tk.Label(header_frame,text="  Welcome to the Order History Page ",anchor="center", font=("Arial",20), bg = "brown")
        intro.grid(row=0,column=1)

        note = tk.Label(header_frame,text=" NOTE: Always refresh this page for new updates to history ",anchor="center", font=("Arial",10), bg = "grey")
        note.grid(row=1,column=1)

        back_btn = tk.Button(header_frame,text="Back", command= self.back_menu)
        back_btn.grid(row=0,column= 0,padx=5)

        refresh_btn = tk.Button(header_frame,text="Refresh", command= self.refresh)
        refresh_btn.grid(row=0,column=2,padx=5)


    def display(self): # displaying all the cards on the screen just like the orderframe
        user_id = self.app.current_user["ID"] # get user id
        orders = self.app.database.get_orders(user_id) # get all order numbers
        index = 0
        for order in orders: # loop through the orders
            order_num = order[0]
            items = self.app.database.get_order_items(order_num) # get the items
            odr_hist = self.app.database.order_history(items) # convert them to displayable format
            row_num = index // 3
            col_num = index % 3
            status = self.app.database.status(order_num)
            card = order_history_card(self.orderhistory_scroll.content_frame,self,order_num,odr_hist,status) # make them a card object
            card.grid(row=row_num,column=col_num,padx=30,pady=10) # place on screen
            self.history_cards.append(card)
            index+= 1

    def refresh(self): # refresh
        for card in self.history_cards:
            card.destroy()
        self.history_cards.clear()
        self.display()

    def back_menu(self): # retun to previous page
        self.app.show_frame(self.app.frames["orderframe"])

#----------------------------------------------------------------------------------------------------------------------------------------------------
class ScrollableFrame(tk.Frame): # Initialize class
    def __init__(self,parent,bg = "white"):
        super().__init__(parent)
        canvas_frame = tk.Frame(self, bg="brown") # Set the frame for the canvas
        canvas_frame.pack(fill="both", expand=True) # Fill the screen as an overlay

        scrollbar = tk.Scrollbar(canvas_frame,orient="vertical") # Initalize the scrollbar
        scrollbar.pack(side="right",fill="y") # Position it

        self.canvas = tk.Canvas(canvas_frame,yscrollcommand=scrollbar.set,bg=bg) # Connect the scroll bar and the canvas
        scrollbar.config(command=self.canvas.yview) # Configure the scroll bar
        self.content_frame = tk.Frame(self.canvas,bg =bg) # Create a frame on the canvas to write on
        self.canvas_window = self.canvas.create_window((0,0),window=self.content_frame,anchor="nw") # Connect the canvas and the frame to use scroll bar
        self.content_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))) # Connect the canvas and the frame to use scroll bar
        self.canvas.pack(side="left",fill="both",expand=True)

        self.canvas.bind("<Configure>", self.resize_canvas) # Setting canvas size

    def resize_canvas(self,event):
        self.canvas.itemconfig(self.canvas_window, width=event.width) # Configure canvas tro match frame size

#----------------------------------------------------------------------------------------------------------------------------------------------------
class ItemCard(tk.Frame): # Initializes the class
    def __init__(self, parent,cartframe, item_id, name, description, image, price): # All the parameters
        super().__init__(parent) # Inherits from the customer frame class
        self.BG = "orange"
        self.configure(background=self.BG,width =200,height=250)
        self.grid_propagate(False)
        self.cartframe = cartframe
        self.item_id = item_id
        self.name = name
        self.description = description
        self.old_image = image
        self.price = price
        self.popup = None
        self.image = self.image_resize(self.old_image)
        self.quantity = 0

        self.stock_level = self.cartframe.app.database.get_quantity(self.item_id)

        self.warning = ""
        self.display_stock_text()

        self.clickable_widgets(self)

        # creating all the labels for the card
        img = tk.Label(self,image=self.image, anchor="center",justify="center")
        img.grid(row=1,column=0,columnspan=2,padx=15,pady=5)
        self.clickable_widgets(img)

        name = tk.Label(self,text = self.name, anchor="center")
        name.grid(row=0,column=0,columnspan=2,padx=13,pady=5)
        self.clickable_widgets(name)

        desc = tk.Label(self,text = self.description, anchor="center",wraplength=190,justify="center")
        desc.grid(row=2,column=0,columnspan=2,padx=13,pady=5)
        self.clickable_widgets(desc)

        price = tk.Label(self, text=f"£{self.price:.2f}", anchor="center")
        price.grid(row=3,column=0,columnspan=2,padx=13,pady=5)
        self.clickable_widgets(price)

        stock_level_label = tk.Label(self,text=self.warning,anchor="center")
        stock_level_label.grid(row=4,column=0,columnspan=2,padx=13,pady=5)
        self.clickable_widgets(stock_level_label)

    def clickable_widgets(self,widget): # making the whole widget clickable
        if self.stock_level > 10:
            widget.bind("<Button-1>",self.open_popup)
        else:
            self.BG = "grey"
            self.configure(background=self.BG,width =200,height=250)

    def display_stock_text(self): # Displaying the remaining stock in the database
        if self.stock_level > 10:
            self.warning = f"{self.stock_level} portions remaining"
        else:
            self.warning = "Item Unavaiable"

    def open_popup(self,event): # the popup for each item
        if self.popup != None:
            return 
        self.popup = tk.Toplevel(self) # creating a top level frame
        self.popup.title(self.name)
        self.popup.geometry("300x350")
        tk.Label(self.popup, text=self.name).pack(pady=10) # adding all the labels on it
        tk.Label(self.popup, image=self.image).pack(pady=5)
        tk.Label(self.popup, text=f"This item is a {self.description}",wraplength=150).pack(pady=10)
        tk.Label(self.popup, text=f"One portion costs: £{self.price:.2f}").pack(pady=10)
        self.qty = tk.Spinbox(self.popup, from_=0,to=10,width=10,state="normal",justify="center",wrap="True") # adding the spin box for quantity
        self.qty.config(state="readonly") # prevent user input allow only through arrows
        self.qty.pack()
        tk.Button(self.popup,text="Add to chart",command=self.add_to_cart).pack(pady=5)
        tk.Button(self.popup,text="Close",command=self.close_popup).pack(pady=5)# placing the checkout button
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup) # closing the popup

    def close_popup(self): # close popup
        self.popup.destroy()
        self.popup = None

    def image_resize(self,original_img): # resize the img to be displayed
        img = Image.open(original_img).resize((100,100))
        img = ImageTk.PhotoImage(img)
        return img


    def add_to_cart(self): # adding item to cart
        if int(self.qty.get()) > 0 : # Check if the quantity is above 0 and under 10
            cart_item = [self.item_id,self.name,self.price,int(self.qty.get())] # Get the item id name price and quantity
            for item in self.cartframe.cart_items: # Check if there is an instance of that specific item
                if item[0] == self.item_id:
                    if item[3] >= 10 or (item[3] + int(self.qty.get())) > 10: # Check if max order limit per item is reached
                        messagebox.showerror("Invalid Order", "Order quantity exceeds limit of 10") # Show error message
                        self.close_popup()
                        return
                    else:
                        item[3] += int(self.qty.get()) # If max limit is not reached calc quantity
                        self.cartframe.display_cart() # Update display
                        self.close_popup()
                        return
            self.cartframe.cart_items.append(cart_item) # Add new item to cart
            self.cartframe.display_cart() # Update display
            self.close_popup()
        else: 
            messagebox.showerror("Invalid Order", "Order quantity is below 1") # Display error message.
            self.close_popup()

#----------------------------------------------------------------------------------------------------------------------------------------------------
class Cart_item_card(tk.Frame): # creating the card for the cart cards
    def __init__(self, parent,cartframe, item_id, name, price,quantity):
        super().__init__(parent)
        self.configure(background="orange",width =180,height=100)
        self.grid_propagate(False)
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.popup = None
        self.cartframe = cartframe
        # adding the labels
        name = tk.Label(self,text = self.name, anchor="center")
        name.grid(row=0,column=0,columnspan=2,padx=13,pady=5)

        value = self.price * self.quantity
        price = tk.Label(self, text=f"Price: £{value:.2f}", anchor="center")
        price.grid(row=2,column=0,columnspan=2,padx=13,pady=5)

        quantity = tk.Label(self, text=f"Quantity: {self.quantity}", anchor="center")
        quantity.grid(row=1,column=0,columnspan=2,padx=13,pady=5)

        remove_btn = tk.Button(self,text = "Remove",command=self.remove_item)
        remove_btn.grid(row=1,column=3)

    def remove_item(self): # removing the items
        self.cartframe.remove_item(self.item_id)
       
#----------------------------------------------------------------------------------------------------------------------------------------------------
class order_history_card(tk.Frame): # creating the order history cards
    def __init__(self,parent,screen,order_number,order_list,status,admin = False):
        super().__init__(parent)
        self.parent = parent
        self.status = status
        self.configure(background="orange",width =200,height=200)
        self.grid_propagate(False)
        self.order_number = order_number
        self.order_list = order_list
        self.popup = None
        self.status = status
        self.screen = screen

        self.clickable_widgets(self) # making the widgets clickable

        order_text = tk.Label(self,text = f"ORDER #{self.order_number} Details",font=15,anchor="center",bg = "orange")
        order_text.pack(pady= 10,padx= 10)
        self.clickable_widgets(order_text)

        if self.status[0] == 1:
            print(self.status)
            self.configure(background="green")

        if admin:
            confirm_btn = tk.Button(self,text = "Confirm Order", command = self.change_status)
            confirm_btn.pack()

    def clickable_widgets(self,widget): # making the widgets clickable
        widget.bind("<Button-1>",self.open_popup)

    def open_popup(self,event): # popup for the order history
        if self.popup != None:
            return 
        self.popup = tk.Toplevel(self) # creating the top level window
        self.popup.title(f"Order Number #{self.order_number}")
        self.popup.geometry("300x350")
        self.popup.config(bg ="white")

        header_frame = tk.Frame(self.popup,bg="white") # main header
        header_frame.pack(fill="x")

        content_frame = tk.Frame(self.popup,bg="white") # content frame
        content_frame.pack(fill="both", expand=True)
        
        self.popup_scroll = ScrollableFrame(content_frame, bg="white") # making the content frame scrollable
        self.popup_scroll.pack(fill="both", expand=True)

        title_label = tk.Label(header_frame,text= f"Order Receipt #{self.order_number}",bg = "white") # title the popup widget
        title_label.pack(pady=10)

        grid_frame = tk.Frame(self.popup_scroll.content_frame,bg="black",bd=0) # the grid for the black lines
        grid_frame.pack(fill="x",padx=15,pady=5)

        grid_frame.columnconfigure(0, weight=3) # Item Name
        grid_frame.columnconfigure(1, weight=1) # Qty
        grid_frame.columnconfigure(2, weight=1) # Price

        name_label = tk.Label(grid_frame, text = "Item Name",bg = "white",anchor = "w")
        name_label.grid(row=0, column=0, sticky="nsew", padx=(0, 1), pady=(0, 2))

        qty_label = tk.Label(grid_frame, text = "Quantity",bg = "white",anchor = "e")
        qty_label.grid(row=0, column=1, sticky="nsew", padx=(0, 1), pady=(0, 2))

        price_label = tk.Label(grid_frame, text = "Price",bg = "white",anchor = "e")
        price_label.grid(row=0, column=2, sticky="nsew", padx=(0, 1), pady=(0, 2))

        row = 1
        total_price = 0
        for order in self.order_list: # loop through the returned items list and display all the info
            name = order[0]
            qty = order[1]
            price = order[2]
            # creating the lines and border
            item_name = tk.Label(grid_frame,text = name,bg = "white",anchor = "w")   
            item_name.grid(row=row, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1))

            item_qty = tk.Label(grid_frame,text = qty,bg = "white",anchor = "e")   
            item_qty.grid(row=row, column=1, sticky="nsew", padx=(0, 1), pady=(0, 1))

            item_price = tk.Label(grid_frame,text = f"£{price}",bg = "white",anchor = "e")   
            item_price.grid(row=row, column=2, sticky="nsew", padx=(0, 1), pady=(0, 1))

            row += 1
            total_price += price

        totals_frame = tk.Frame(self.popup,bg = "white") # totals frame
        totals_frame.pack(fill="x",padx=15,pady=15)

        tk.Label(totals_frame,text = "TOTAL:",bg = "white").pack(side="left")
        tk.Label(totals_frame,text = f"£{total_price}",bg = "white").pack(side="right")
        self.popup.protocol("WM_DELETE_WINDOW",self.close_popup)

    def change_status(self):
        self.config(background="green")
        self.screen.update_stat(self.order_number)

    def close_popup(self):
        self.popup.destroy()
        self.popup = None    

#----------------------------------------------------------------------------------------------------------------------------------------------------
class AddItem(tk.Frame): # Add Item frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="#ab6f8a")
        header_frame = tk.Frame(self)
        header_frame.pack()
        msg = tk.Label(self,text= "Welcome to the add items page", anchor="center", font=("Arial",20), bg = "grey")
        msg.pack(pady=10)
        content_frame = tk.Frame(self,bg = "#ab6f8a")
        content_frame.pack(fill="both", expand=True)
        #creating labels
        item_name_label = tk.Label(content_frame,text="  Name:  ",font=("Arial",10))
        item_name_label.grid(row=0,column=0,padx=10,pady=10)

        self.name_entry = tk.Entry(content_frame,width=40)
        self.name_entry.grid(row=0,column= 1,padx= 10,pady=25)

        description_label = tk.Label(content_frame,text="  Description:  ",font=("Arial",10))
        description_label.grid(row=1,column=0,padx=10,pady=10)
        
        self.description_entry = tk.Entry(content_frame,width=40)
        self.description_entry.grid(row=1,column= 1,padx= 10,pady= 25)

        image_label = tk.Label(content_frame,text="  Image  ",font=("Arial",10))
        image_label.grid(row=2,column=0,padx=10,pady=10)
                
        self.image_entry = tk.Entry(content_frame,width=40)
        self.image_entry.grid(row=2,column= 1,padx= 10,pady=25)

        qty_label = tk.Label(content_frame,text = "Quantity", font = ("Arial,10"))
        qty_label.grid(row=3, column=0, padx = 10, pady = 25)

        self.qty = tk.Spinbox(content_frame, from_=0,to=100,width=10,state="normal",justify="center",wrap="True")
        self.qty.config(state="readonly")
        self.qty.grid(row=3, column = 1, padx= 10, pady= 25)

        price_label = tk.Label(content_frame,text="  Price  ",font=("Arial",10))
        price_label.grid(row=4,column=0,padx=10,pady=10)
    
        self.price = tk.Spinbox(content_frame, from_=0,to=10,width=10,state="normal",justify="center",wrap="True",increment = 0.1)
        self.price.config(state="readonly")
        self.price.grid(row=4, column = 1, padx= 10, pady= 25)

        category_label = tk.Label(content_frame, text = " Category ", font = ("Arial,10"))
        category_label.grid(row = 5, column = 0,padx = 10, pady = 25)
        self.category = ["Drinks", "Meals", "Snacks", "Desserts"]
        self.selection = ttk.Combobox(content_frame,values= self.category)
        self.selection.config(state= "readonly")
        self.selection.set("Select a Category")
        self.selection.grid(row=5, column = 1)
        
        back_btn = tk.Button(content_frame,text="Back", command= self.backbutton)
        back_btn.grid(row=6,column=1, padx= 10,pady=30)
        
        add_btn = tk.Button(content_frame,text="Add Item", command= self.additem)
        add_btn.grid(row=6,column=2, padx= 10,pady=30)

    def backbutton(self): # return to the previous page
        self.app.show_frame(self.app.frames["orderframe"])

    def additem(self):
        name = self.name_entry.get()
        desc = self.description_entry.get()
        image = self.image_entry.get()
        qty = self.qty.get()
        price = self.price.get()
        Category = self.selection.get()
        details = [name,desc,image,qty,price,Category]
        for i in details:
            if i == "" or i == "0.0" or i == "0" or i == "Select a Category":
                return messagebox.showerror("Invalid Inputs", "Make sure all fields are filled")
        #print(name,desc,image,qty,price,Category)
        if self.app.database.add_items(name,desc,image,qty,price,Category) == "Item Added":
            self.name_entry.delete(0,tk.END)
            self.description_entry.delete(0,tk.END)
            self.image_entry.delete(0,tk.END)
            messagebox.showinfo("Congratulations","Item has successfully been added to the Database")
        elif self.app.database.add_items(name,desc,image,qty,price,Category) == "Item name Exists":
            messagebox.showerror("Error", "Item name already exists")
        #print(self.app.database.add_items(name,desc,image,qty,price,Category))
        self.app.frames["orderframe"].refresh_menu()

#----------------------------------------------------------------------------------------------------------------------------------------------------
class showOrders(tk.Frame): # show all orders page initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="#62239c")
        self.order_cards = []

        header_frame = tk.Frame(self)
        header_frame.pack()
        msg = tk.Label(self,text= "Welcome to the orders page", anchor="center", font=("Arial",20), bg = "grey")
        msg.pack(pady=10)

        self.content_frame = tk.Frame(self,bg = "#ab6f8a")
        self.content_frame.pack(fill="both", expand=True)

        self.showOrders_scroll = ScrollableFrame(self.content_frame, bg="brown")
        self.showOrders_scroll.pack(fill="both", expand=True)

        back_btn = tk.Button(self,text="Back", command= self.backbutton)
        back_btn.pack(pady=30)

        self.display()

    def display(self):
        all_orders = self.app.database.admin_orders_db()
        print(all_orders)
        index = 0
        for order in all_orders:
            order_num = order[0]
            items = self.app.database.get_order_items(order_num) # get the items
            odr_hist = self.app.database.order_history(items) # convert them to displayable format
            row_num = index // 3
            col_num = index % 3
            status = self.app.database.status(order_num)
            card = order_history_card(self.showOrders_scroll.content_frame,self,order_num,odr_hist,status,admin = True) # make them a card object
            card.grid(row=row_num,column=col_num,padx=30,pady=10) # place on screen
            self.order_cards.append(card)
            index+= 1


    def update_stat(self, o_id):
        print(f"The inital status is {self.app.database.status(o_id)}")
        self.app.database.chg_stat(o_id)
        print("Status changed ")
        print(f"The final status is {self.app.database.status(o_id)}")


    def backbutton(self): # return to the previous page
        self.app.show_frame(self.app.frames["orderframe"])
        self.app.frames["orderframe"].collapse_panel()
MainApp()