import tkinter as tk
class MainApp: # initializing the MainApp class which serves as the controller
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SAMOSA")
        self.root.geometry("800x800")

        self.frames = { # this dictionary would contain all GUI classes
            "login" : LoginFrame(self)
        }
        

        self.show_frame(self.frames["login"]) # sets the current screen to show once application starts running

        self.root.mainloop()

    def show_frame(self,frame): # function to show frames nad prevent other frames from showing
        for frame in self.frames.values():
            frame.pack_forget()

        frame.pack(fill = "both", expand=True)

class LoginFrame(tk.Frame): # login frame initialization
    def __init__(self,app):
        super().__init__(app.root) # inherits the main root window as the place to be displayed
        self.app = app
        tk.Label(self, # label saying login
                 text="Login Page",
                  font=("Arial",20)).pack(pady=20)

        tk.Button(self, # button to login
                  text="Login",
                  command=self.login).pack()
        
    def login(self):
        # Normally you'd check the database here.

        self.app.show_frame(self.app.customer_frame)




MainApp()
