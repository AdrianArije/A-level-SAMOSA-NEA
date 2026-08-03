import tkinter as tk
from tkinter import messagebox
from  DatabaseManager import DatabaseClass
from PIL import ImageTk, Image

#----------------------------------------------------------------------------------------------------------------------------------------------------
class MainApp: # Initializing the MainApp class which serves as the controller
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SAMOSA") # Screen Geometry
        self.root.geometry("800x600")
        self.database = DatabaseClass()
        # This dictionary would contain all GUI classes
        self.frames = {
            "login" : LoginFrame(self),
            "customerframe" : CustomerFrame(self),
            "settings" : SettingsFrame(self),
            "orderhistory" : OrderHistoryFrame(self)
        }

        self.show_frame(self.frames["customerframe"]) # Sets the current screen to show once application starts running
        
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

    def login(self):
        access = self.app.database.Login(self.username_entry.get(),self.password_entry.get())

        #self.password_entry.delete(0,tk.END)# Clearing the fields
        #self.username_entry.delete(0,tk.END)

        if access == "Access granted":
            self.app.show_frame(self.app.frames["customerframe"])
        elif access == "Incorrect password":
            messagebox.showerror("Error Logging In", "Incorrect Password entered")
        elif access == "Username not found":
            messagebox.showerror("Error Logging In", "Username not found. Try Signing Up")
        elif access == "Invalid username":
            messagebox.showerror("Error Logging In", "Username is below 8 characters")

    def signup(self):
            security = self.app.database.Signup(self.username_entry.get(),self.password_entry.get())

            self.password_entry.delete(0,tk.END)# Clearing the fields
            self.username_entry.delete(0,tk.END)

            if security:
                self.app.show_frame(self.app.frames["customerframe"])
                
            else:
                messagebox.showerror("Error Signing Up", "Inputs are below 8 characters or Username already exists")
    #print("Login Frame Initialized")


#----------------------------------------------------------------------------------------------------------------------------------
class CustomerFrame(tk.Frame): # Customer frame initialization
    def __init__(self,app):
        super().__init__(app.root) # Inherits the main root window as the place to be displayed
        self.app = app
        self.configure(background="red")
        self.cards = []
        self.search_text = ""
        self.category = []
        self.current_items = []

        self.cartframe= CartFrame(self) # Linking cart frame as a sub class of customer frame
        self.cartframe.place_forget() # Hiding the cart frame

        header_frame = tk.Frame(self,bg ="red") # crating header frame for header
        header_frame.pack()

        content_frame = tk.Frame(self, bg="yellow") # Creating content frame for items
        content_frame.pack(fill="both", expand=True)

        toolbar_frame = tk.Frame(content_frame, bg="yellow")
        toolbar_frame.pack(fill="x")

        canvas_frame = tk.Frame(content_frame, bg="yellow")
        canvas_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(canvas_frame,orient="vertical")
        scrollbar.pack(side="right",fill="y")

        self.canvas = tk.Canvas(canvas_frame,yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.canvas.yview)
        self.item_frame = tk.Frame(self.canvas,bg = "brown")
        self.canvas.create_window((0,0),window=self.item_frame,anchor="nw")
        self.canvas_window = self.canvas.create_window((0,0),window=self.item_frame,anchor="nw")
        self.item_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.pack(side="left",fill="both",expand=True)
        

        intro = tk.Label(header_frame,text = "Menu Items",font= ("Arial", 43),bg="red", foreground="#fbf025",anchor="center") # Intro text
        intro.grid(row=0,column=1,columnspan=2)

        self.search_entry = tk.Entry(toolbar_frame, width=90) # Search entry box
        self.search_entry.grid(row=0, column=0, padx = 25)

        searchbtn = tk.Button(toolbar_frame, text="Search", command=self.refresh_menu) # Search button
        searchbtn.grid(row=0, column=1,padx = 5)

        sort_btn = tk.Menubutton(toolbar_frame,text = "Sort By ▼", relief="raised") # Adding the sort button menu
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

        self.desserts_var = tk.BooleanVar() # Making a variable to check if box is ticked
        desserts_var = tk.Checkbutton(self.filter_frame,text = "Desserts",variable = self.desserts_var)
        desserts_var.grid(row=3,column = 0)

        filter_btn = tk.Button(toolbar_frame,text ="Filter ▼", command = self.filterbutton) # Filter button
        filter_btn.grid(row=0,column=2,padx= 5)

        self.filter_action = tk.Button(self.filter_frame,text ="Filter", command = self.filter_action)
        self.filter_action.grid(row=4,column = 0)

        self.refresh_menu()
        self.canvas.bind("<Configure>", self.resize_canvas)

    def resize_canvas(self,event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def filterbutton(self):
        self.filter_frame.place(x=620,y =30)

    def filter_action(self):
        self.filter_frame.place_forget() # Close popup
        if self.meals_var.get() == True:
            self.category.append(1) # Append to categries if the category is ticked
        if self.snack_var.get() == True:
            self.category.append(2) # Append to categries if the category is ticked
        if self.drinks_var.get() == True:
            self.category.append(3) # Append to categries if the category is ticked
        if self.desserts_var.get() == True:
            self.category.append(4) # Append to categries if the category is ticked
        self.refresh_menu() # Refresh menu items
        self.category.clear() # Reset all the checkboxes list

    def settings(self):
        self.app.show_frame(self.app.frames["settings"])

    def orderpage(self):
       self.app.show_frame(self.app.frames["orderhistory"])

    def cart(self):
        self.cartframe.place(relx=0.5, rely=0.5, anchor="center")
        self.cartframe.lift()
        #print("cart")
    def logout(self):
        # Normally you'd check the database here.
        self.app.show_frame(self.app.frames["login"]) 

    def display_items(self,items):
        index = 0
        for item in items:
            id = item[0]
            name = item[1] 
            desc = item[2] 
            img = item[3]
            price = item[5]
            col = index % 3
            rows = index // 3
            card = ItemCard(self.item_frame,id,name,desc,img,price)
            card.grid(row=rows,column=col,padx=30,pady=10)
            #print(col,rows)
            index = index + 1
            self.cards.append(card)
        
    def refresh_menu(self):
        word = self.search_entry.get()
        self.clear_menu()
        self.current_items = self.app.database.display_menu(word,self.category)
        self.display_items(self.current_items)

    def clear_menu(self):
        for card in self.cards:
            card.destroy()
        self.cards.clear()
        #self.current_items.clear()

    def filterprice(self):
        self.clear_menu()
        for item in range(len(self.current_items)-1):
            for i in range(len(self.current_items)-1):
                if self.current_items[i][5] > self.current_items[i + 1][5]:
                    temp = self.current_items[i]
                    self.current_items[i] = self.current_items[i + 1]
                    self.current_items[i + 1]= temp
        self.display_items(self.current_items)


    def filtername(self):
        pass
    #print("Customer Frame Initialized")

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

class ItemCard(tk.Frame): # Initializes the class
    def __init__(self, parent, item_id, name, description, image, price): # All the parameters
        super().__init__(parent) # Inherits from the customer frame class
        self.configure(background="orange",width =200,height=230)
        self.grid_propagate(False)
        
        self.item_id = item_id
        self.name = name
        self.description = description
        self.old_image = image
        self.price = price
        self.popup = None
        self.image = self.image_resize(self.old_image)
        self.quantity = 0

        self.clickable_widgets(self)
        
        img = tk.Label(self,image=self.image, anchor="center",justify="center")
        img.grid(row=1,column=0,columnspan=2,padx=13,pady=5)
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

        

    def clickable_widgets(self,widget):
        widget.bind("<Button-1>",self.open_popup)

    def open_popup(self,event):
        if self.popup != None:
            return 
        self.popup = tk.Toplevel(self)
        self.popup.title(self.name)
        self.popup.geometry("300x350")
        tk.Label(self.popup, text=self.name).pack(pady=10)
        tk.Label(self.popup, image=self.image).pack(pady=5)
        tk.Label(self.popup, text=f"This item is a {self.description}",wraplength=150).pack(pady=10)
        tk.Label(self.popup, text=f"One portion costs: £{self.price:.2f}").pack(pady=10)
        self.qty = tk.Spinbox(self.popup, from_=0,to=10,width=10,command = self.quantity_value,state="normal",justify="center",wrap="True")
        self.qty.pack()
        tk.Button(self.popup,text="Add to chart").pack(pady=5)
        tk.Button(self.popup,text="Close",command=self.close_popup).pack(pady=5)
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

    def close_popup(self):
        self.popup.destroy()
        self.popup = None

    def image_resize(self,original_img):
        img = Image.open(original_img).resize((100,100))
        img = ImageTk.PhotoImage(img)
        return img

    def quantity_value(self):
        self.quantity = int(self.qty.get())
        #print(f"Quantity is now {self.quantity}")
        
MainApp()