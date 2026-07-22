import tkinter as tk

#----------------------------------------------------------------------------------------------------------------------------------------------------
class MainApp: # initializing the MainApp class which serves as the controller
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SAMOSA")
        self.root.geometry("800x600")
        

        self.frames = { # this dictionary would contain all GUI classes
            "login" : LoginFrame(self),
            "customerframe" : CustomerFrame(self)
        }
        

        self.show_frame(self.frames["login"]) # sets the current screen to show once application starts running

        self.root.mainloop()

    def show_frame(self,frame): # function to show frames and prevent other frames from showing
        for current_frame in self.frames.values():
            current_frame.pack_forget()
        frame.pack(fill = "both", expand=True)


#----------------------------------------------------------------------------------------------------------------------------------------------------
class LoginFrame(tk.Frame): # login frame initialization
    def __init__(self,app):
        super().__init__(app.root) # inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="#3a79ee")

        intro = tk.Label(self,text = "Welcome to Adrian's Canteen ",font= ("Arial", 43),bg="#3a79ee", foreground="#fbf025") # intro text label
        intro.grid(row=0,column = 1,columnspan=2, padx = 10, pady =15)

        self.entry_frame = tk.Frame(self) # creating new frame for entry widgets
        self.entry_frame.place(x=280,y=220)

        lgntext = tk.Label(self.entry_frame,text = "    Login In / Sign up    ",font= ("Arial", 20)) # login label
        lgntext.grid(row=0,column = 0, columnspan=2)

        username_label = tk.Label(self.entry_frame,text = "Username",font = ("Arial",10)) # username label
        username_label.grid(row=1,column = 0)

        username_entry =tk.Entry(self.entry_frame,width=20) # username entry box
        username_entry.grid(row=1,column = 1, padx = 12, pady =10)

        password_label = tk.Label(self.entry_frame,text = "Password",font = ("Arial",10)) # password entry label
        password_label.grid(row=2,column = 0)

        password_entry =tk.Entry(self.entry_frame,width=20) # password entry box
        password_entry.grid(row=2,column = 1, padx = 12, pady =10)

        loginbtn = tk.Button(self.entry_frame, text="Login", command=self.login) # login button
        loginbtn.grid(row=3,column = 0, pady=10)

        signupbtn = tk.Button(self.entry_frame, text="Sign Up", command=self.signup) # sign up button
        signupbtn.grid(row=3,column = 1, pady=5)

    def login(self):
        # Normally you'd check the database here.
        self.app.show_frame(self.app.frames["customerframe"])

    def signup(self):

         self.app.show_frame(self.app.frames["customerframe"])
    print("Login Frame Initialized")


#----------------------------------------------------------------------------------------------------------------------------------
class CustomerFrame(tk.Frame): # customer frame initialization
    def __init__(self,app):
        super().__init__(app.root) # inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="red")

        self.cartframe= CartFrame(self) # linking cart frame as a sub class of customer frame
        self.cartframe.place_forget() # hiding the cart frame

        header_frame = tk.Frame(self,bg ="red") # crating header frame for header
        header_frame.pack()

        content_frame = tk.Frame(self, bg="red") # creating content frame for items
        content_frame.pack(fill="both", expand=True)

        intro = tk.Label(header_frame,text = "Menu Items",font= ("Arial", 43),bg="red", foreground="#fbf025",anchor="center") # intro text
        intro.grid(row=0,column=1,columnspan=2)

        search_entry = tk.Entry(content_frame, width=90) # search entry box
        search_entry.grid(row=0, column=0, padx = 25)

        searchbtn = tk.Button(content_frame, text="Search", command=self.search) # search button
        searchbtn.grid(row=0, column=1,padx = 5)

        filter_btn = tk.Menubutton(content_frame,text = "Filter ▼", relief="raised") # adding the filter button menu
        filter_btn.grid(row=0,column=2,padx= 5) # set postion
        dropdown = tk.Menu(filter_btn,tearoff=0)
        self.drinks_var = tk.BooleanVar() # making a variable to check if box is ticked
        dropdown.add_checkbutton(label = "Drinks",variable = self.drinks_var) # adding button checkbox
        filter_btn["menu"] = dropdown # linking button and dropdown

        sort_btn = tk.Menubutton(content_frame,text = "Sort By ▼", relief="raised") # adding the sort button menu
        sort_btn.grid(row=0,column=3, padx=5) # set position
        sort_dropdown = tk.Menu(sort_btn,tearoff=0)
        sort_dropdown.add_command(label = "By Price",command = self.filterprice) # adding sorting button
        sort_dropdown.add_separator()
        sort_dropdown.add_command(label = "By Name",command = self.filtername)
        sort_btn["menu"] = sort_dropdown # link button to drop down
# for the filter use a label frame to hide options and user has to press search
# for sorting use a ttk.combobox

        options_btn = tk.Menubutton(header_frame,text = "▼ OPTIONS", relief="raised",bg="red") # creating a menu drop down for options
        options_btn.grid(row=0,column=8,padx= 10)
        options_dropdown= tk.Menu(options_btn,tearoff=0)
        options_dropdown.add_command(label="CART",command=self.cart) # adding all the options with commands
        options_dropdown.add_command(label="ORDER HISTORY",command=self.orderpage)
        options_dropdown.add_command(label="SETTINGS",command=self.settings)
        options_dropdown.add_command(label="LOGOUT",command=self.logout)
        options_btn["menu"] = options_dropdown # likning the button with the menu

    def settings(self):
        pass
    def orderpage(self):
        pass
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

class CartFrame(tk.Frame): # customer frame initialization
    def __init__(self,parent):
        super().__init__(parent) # inherits the main root window as the place to be displayed
        self.configure(background="brown",width=400,height=400)
        self.pack_propagate(False)
        close_btn = tk.Button(self,text = "Close", command=self.close)
        close_btn.place(x=180,y=370)
        


    def close(self):
        self.place_forget()
MainApp()

