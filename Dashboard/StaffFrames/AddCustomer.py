import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class AddCustomerFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        
        self.configure(bg="#f0f0f0")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Customer Management", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="First Name", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.first_name_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="Last Name", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.last_name_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="Email", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.email_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.email_entry.grid(row=3, column=0, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="Phone Number", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.phone_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=2, sticky="w")
        
        tk.Label(form_frame, text="Address", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.address_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=64)
        self.address_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        self.add_customer_button = tk.Button(self, text="Add Customer", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken")
        self.add_customer_button.pack(pady=(20, 0))

      
        self.tree = ttk.Treeview(
            self,
            columns=("First Name", "Last Name", "Email", "Phone", "Address"),
            show="headings"
        )

        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.heading("Address", text="Address")

        for col in ("First Name", "Last Name", "Email", "Phone", "Address"):
            self.tree.column(col, width=150)

        self.load_customer_data()

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)


       

    def load_customer_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        customers = db_manager.Get.get_all_customers(cursor=db_manager.cursor)
        for customer in customers:
            self.tree.insert("", "end", values=(
                customer['first_name'],
                customer['last_name'],
                customer['email'],
                customer['phone_number'],
                customer['address']
            ))

    