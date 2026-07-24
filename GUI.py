import tkinter as tk

#----------------------------------------------------------------------------------------------------------------------------------------------------
class MainApp: # Initializing the MainApp class which serves as the controller
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SAMOSA") # Screen Geometry
        self.root.geometry("800x600")

        # This dictionary would contain all GUI classes
        self.frames = {
            "login" : LoginFrame(self),
            "customerframe" : CustomerFrame(self),
            "settings" : SettingsFrame(self),
            "orderhistory" : OrderHistoryFrame(self)
        }

        self.show_frame(self.frames["login"]) # Sets the current screen to show once application starts running

        self.root.mainloop()

    def show_frame(self,frame): # Function to show frames and prevent other frames from showing
        for current_frame in self.frames.values():
            current_frame.pack_forget()
        frame.pack(fill = "both", expand=True)


#----------------------------------------------------------------------------------------------------------------------------------------------------
class LoginFrame(tk.Frame): # Login frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="#3a79ee")

        intro = tk.Label(self,text = "Welcome to Adrian's Canteen ",font= ("Arial", 43),bg="#3a79ee", foreground="#fbf025") # Intro text label
        intro.grid(row=0,column = 1,columnspan=2, padx = 10, pady =15)

        self.entry_frame = tk.Frame(self) # Creating new frame for entry widgets
        self.entry_frame.place(x=280,y=220)

        lgntext = tk.Label(self.entry_frame,text = "    Login In / Sign up    ",font= ("Arial", 20)) # Login label
        lgntext.grid(row=0,column = 0, columnspan=2)

        username_label = tk.Label(self.entry_frame,text = "Username",font = ("Arial",10)) # Username label
        username_label.grid(row=1,column = 0)

        self.username_entry =tk.Entry(self.entry_frame,width=20) # Username entry box
        self.username_entry.grid(row=1,column = 1, padx = 12, pady =10)

        password_label = tk.Label(self.entry_frame,text = "Password",font = ("Arial",10)) # Password entry label
        password_label.grid(row=2,column = 0)

        self.password_entry =tk.Entry(self.entry_frame,width=20) # Password entry box
        self.password_entry.grid(row=2,column = 1, padx = 12, pady =10)

        loginbtn = tk.Button(self.entry_frame, text="Login", command=self.login) # Login button
        loginbtn.grid(row=3,column = 0, pady=10)

        signupbtn = tk.Button(self.entry_frame, text="Sign Up", command=self.signup) # Sign up button
        signupbtn.grid(row=3,column = 1, pady=5)

    def login(self):
        # Normally you'd check the database here.
        self.app.show_frame(self.app.frames["customerframe"])

    def signup(self):

         self.app.show_frame(self.app.frames["customerframe"])
    print("Login Frame Initialized")


#----------------------------------------------------------------------------------------------------------------------------------
class CustomerFrame(tk.Frame): # Customer frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="red")

        self.cartframe= CartFrame(self) # Linking cart frame as a sub class of customer frame
        self.cartframe.place_forget() # Hiding the cart frame

        header_frame = tk.Frame(self,bg ="red") # crating header frame for header
        header_frame.pack()

        content_frame = tk.Frame(self, bg="red") # Creating content frame for items
        content_frame.pack(fill="both", expand=True)

        intro = tk.Label(header_frame,text = "Menu Items",font= ("Arial", 43),bg="red", foreground="#fbf025",anchor="center") # Intro text
        intro.grid(row=0,column=1,columnspan=2)

        self.search_entry = tk.Entry(content_frame, width=90) # Search entry box
        self.search_entry.grid(row=0, column=0, padx = 25)

        searchbtn = tk.Button(content_frame, text="Search", command=self.search) # Search button
        searchbtn.grid(row=0, column=1,padx = 5)

        sort_btn = tk.Menubutton(content_frame,text = "Sort By ▼", relief="raised") # Adding the sort button menu
        sort_btn.grid(row=0,column=3, padx=5) # Set position
        sort_dropdown = tk.Menu(sort_btn,tearoff=0)
        sort_dropdown.add_command(label = "By Price",command = self.filterprice) # Adding sorting button
        sort_dropdown.add_separator()
        sort_dropdown.add_command(label = "By Name",command = self.filtername)
        sort_btn["menu"] = sort_dropdown # Link button to drop down

        options_btn = tk.Menubutton(header_frame,text = "▼ OPTIONS", relief="raised",bg="red") # Creating a menu drop down for options
        options_btn.grid(row=0,column=8,padx= 10)
        options_dropdown= tk.Menu(options_btn,tearoff=0)
        options_dropdown.add_command(label="CART",command=self.cart) # Adding all the options with commands
        options_dropdown.add_command(label="ORDER HISTORY",command=self.orderpage)
        options_dropdown.add_command(label="SETTINGS",command=self.settings)
        options_dropdown.add_command(label="LOGOUT",command=self.logout)
        options_btn["menu"] = options_dropdown # Likning the button with the menu

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

        filter_btn = tk.Button(content_frame,text ="Filter ▼", command = self.filterbutton) # Filter button
        filter_btn.grid(row=0,column=2,padx= 5)

        self.filter_close = tk.Button(self.filter_frame,text ="Close", command = self.filterclose)
        self.filter_close.grid(row=4,column = 0)

    def filterbutton(self):
        self.filter_frame.place(x=620,y =30)

    def filterclose(self):
        print("closing")
        self.filter_frame.place_forget()

    def settings(self):
        self.app.show_frame(self.app.frames["settings"])

    def orderpage(self):
       self.app.show_frame(self.app.frames["orderhistory"])

    def cart(self):
        self.cartframe.place(relx=0.5, rely=0.5, anchor="center")
        self.cartframe.lift()
        print("cart")
    def logout(self):
        # Normally you'd check the database here.
        self.app.show_frame(self.app.frames["login"])  

    def search(self):
        pass      

    def filterprice(self):
        pass

    def filtername(self):
        pass
    print("Customer Frame Initialized")

class CartFrame(tk.Frame): # Cart frame initialization
    def __init__(self,parent):
        super().__init__(parent) # Inherits the CustomerFrame window as the place to be displayed
        self.configure(background="brown",width=400,height=400)
        self.pack_propagate(False) # Keep size fixed

        close_btn = tk.Button(self,text = "Close", command=self.close)
        close_btn.place(x=180,y=370)

    def close(self):
        self.place_forget()

class SettingsFrame(tk.Frame): # Settings frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="grey")

        header_frame = tk.Frame(self)
        header_frame.pack()

        msg = tk.Label(self,text= "Welcome to the settings page", anchor="center", font=("Arial",20), bg = "grey")
        msg.pack(pady=10)

        content_frame = tk.Frame(self,bg = "grey")
        content_frame.pack(fill="both", expand=True)

        user_label = tk.Label(content_frame,text="  Username:  ",font=("Arial",20),bg="grey")
        user_label.grid(row=0,column=0,padx=10,pady=10)

        user_entry = tk.Entry(content_frame,width=40)
        user_entry.grid(row=0,column= 1,padx= 20,pady=50)

        password_label = tk.Label(content_frame,text="  Current password:  ",font=("Arial",20),bg="grey")
        password_label.grid(row=1,column=0,padx=10,pady=10)
        
        password_entry = tk.Entry(content_frame,width=40)
        password_entry.grid(row=1,column= 1,padx= 20,pady= 50)

        new_password_label = tk.Label(content_frame,text="  New password:  ",font=("Arial",20),bg="grey")
        new_password_label.grid(row=3,column=0,padx=10,pady=10)
                
        new_password_entry = tk.Entry(content_frame,width=40)
        new_password_entry.grid(row=3,column= 1,padx= 20,pady=50)

        new_pass_btn = tk.Button(content_frame,text="Change password")#, command= self.change_password)
        new_pass_btn.grid(row=3,column=2, padx= 10,pady=10)

        back_btn = tk.Button(content_frame,text="Back", command= self.back_menu)
        back_btn.grid(row=4,column=1, padx= 10,pady=30)

    def back_menu(self):
        self.app.show_frame(self.app.frames["customerframe"])



class OrderHistoryFrame(tk.Frame): # Order history frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="brown")

        hearder_frame = tk.Frame(self,bg= "brown")
        hearder_frame.pack()

        content_frame = tk.Frame(self,bg="brown")
        content_frame.pack(fill="both", expand=True)

        intro = tk.Label(hearder_frame,text="  Welcome to your order history  ",anchor="center", font=("Arial",20), bg = "brown")
        intro.pack()

        back_btn = tk.Button(hearder_frame,text="Back", command= self.back_menu)
        back_btn.pack(pady=30)

    def back_menu(self):
        self.app.show_frame(self.app.frames["customerframe"])
MainApp()

