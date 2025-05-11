import tkinter as tk
from Dashboard.DashboardMenu import DashboardMenu
from Session.PseudoSession import Session
import matplotlib.pyplot as plt
import sys

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.framesWithTables = {"AddCars", "EditCarRentalPrice", "CarMaintenance", "StaffManagement", "CarApproval", "CarDeletionApproval", "ServiceApproval", "RentCar"}
        self.title("Dashboard")
        self.state('zoomed')
        self.geometry(f"800x600+{(self.winfo_screenwidth()//2)-425}+{(self.winfo_screenheight()//2)-350}")

        self.header_frame = tk.Frame(self, bg="#f5f5f5", pady=20, padx=20, bd=1, relief="sunken", highlightbackground="#00998F", highlightthickness=0.5)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        welcome_label = tk.Label(self.header_frame, text=f"Welcome, {Session.session_name}!", 
                                 font=("Helvetica", 14, "bold"), bg="#f5f5f5")
        welcome_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # User Info: ID and Role
        user_id_label = tk.Label(self.header_frame, text=f"User ID: {Session.session_id}", 
                                 font=("Helvetica", 10), bg="#f5f5f5")
        user_id_label.grid(row=1, column=0, sticky="w", padx=(0, 10))

        role_label = tk.Label(self.header_frame, text=f"Role: {Session.session_role}", 
                              font=("Helvetica", 10), bg="#f5f5f5")
        role_label.grid(row=1, column=1, sticky="w")


        

        # Dashboard Menu
        self.menu = DashboardMenu(self, app=self)
        self.menu.grid(row=1, column=0, sticky="nsew")

       
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=1, column=1, sticky="nsew")

        # Frames dictionary
        self.frames = {
         
           
        }

       
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        
        self.currentFrame = None
        self.ChangeFrame("Statistic")  

        # 10% ang menu
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()


       
    # Matplot goofy ah bug remove; tanan chart kung i close ang window
    def on_closing(self):
        plt.close('all')
        

    def ChangeFrame(self, frame_name):
        """Switch between frames"""
        self.currentFrame = frame_name
        self.frames[frame_name].tkraise()

        if frame_name in self.framesWithTables:
            self.frames[frame_name].load_data_from_db()
        




