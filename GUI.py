import tkinter as tk
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

class LoginFrame(tk.Frame): # login frame initialization
    def __init__(self,app):
        super().__init__(app.root) # inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="#3a79ee")

        intro = tk.Label(self,text = "Welcome to Adrian's Canteen ",font= ("Arial", 43),bg="#3a79ee", foreground="#fbf025")
        intro.grid(row=0,column = 1,columnspan=2, padx = 10, pady =15)

        self.entry_frame = tk.Frame(self)
        self.entry_frame.place(x=280,y=220)

        lgntext = tk.Label(self.entry_frame,text = "    Login In / Sign up    ",font= ("Arial", 20))
        lgntext.grid(row=0,column = 0, columnspan=2)

        username_label = tk.Label(self.entry_frame,text = "Username",font = ("Arial",10))
        username_label.grid(row=1,column = 0)

        username_entry =tk.Entry(self.entry_frame,width=20)
        username_entry.grid(row=1,column = 1, padx = 12, pady =10)

        password_label = tk.Label(self.entry_frame,text = "Password",font = ("Arial",10))
        password_label.grid(row=2,column = 0)

        password_entry =tk.Entry(self.entry_frame,width=20)
        password_entry.grid(row=2,column = 1, padx = 12, pady =10)

        loginbtn = tk.Button(self.entry_frame, text="Login", command=self.login)
        loginbtn.grid(row=3,column = 0, pady=10)

        signupbtn = tk.Button(self.entry_frame, text="Sign Up", command=self.signup)
        signupbtn.grid(row=3,column = 1, pady=5)

    def login(self):
        # Normally you'd check the database here.
        self.app.show_frame(self.app.frames["customerframe"])

    def signup(self):

         self.app.show_frame(self.app.frames["customerframe"])
    print("Login Frame Initialized")

class CustomerFrame(tk.Frame): # customer frame initialization
    def __init__(self,app):
        super().__init__(app.root) # inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="red")

        header_frame = tk.Frame(self)
        header_frame.pack()

        content_frame = tk.Frame(self, bg="red")
        content_frame.pack(fill="both", expand=True)

        intro = tk.Label(header_frame,text = "Menu ",font= ("Arial", 43),bg="red", foreground="#fbf025",anchor="center")
        intro.pack(pady=10)

        search_entry = tk.Entry(content_frame, width=90)
        search_entry.grid(row=0, column=0, padx = 40)

        searchbtn = tk.Button(content_frame, text="Search", command=self.search)
        searchbtn.grid(row=0, column=1,)

        filter_btn = tk.Menubutton(content_frame,text = "Filter ▼", relief="raised")
        filter_btn.grid(row=0,column=2)
        dropdown = tk.Menu(filter_btn,tearoff=0)
        self.drinks_var = tk.BooleanVar()
        dropdown.add_checkbutton(label = "Drinks",variable = self.drinks_var)
        dropdown.add_command(label = "By Price",command = self.filterprice)
        dropdown.add_separator()
        dropdown.add_command(label = "By Name",command = self.filtername)
        filter_btn["menu"] = dropdown
# for the filter use a label frame to hide options and user has to press search
# for sorting use a ttk.combobox

        logoutbtn = tk.Button(content_frame, text="Logout", command=self.logout)
        logoutbtn.grid(row=1,column = 1, padx = 12, pady =10)

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
MainApp()

