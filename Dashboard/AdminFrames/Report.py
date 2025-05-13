import tkinter as tk
from tkinter import ttk
from Database.DatabaseInstance import db_manager  # Can be kept or removed for now

class ReportFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.configure(bg="#f4f7fc")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Configure internal grid: 2 rows, 3 columns
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)
        self.grid_rowconfigure(1, weight=2)  # Treeview row

        # Title
        tk.Label(self, text="Car Rental Report", font=("Segoe UI", 26, "bold"),
                 bg="#f4f7fc", fg="#333").grid(row=0, column=0, columnspan=3, pady=20)

        # --- [1st Row] - Summary Boxes ---

        # [0,0] Top Users
        self.top_users_frame = tk.Frame(self, bg="#e0ecff", bd=1, relief="solid")
        self.top_users_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tk.Label(self.top_users_frame, text="Top Users", font=("Segoe UI", 14, "bold"), bg="#e0ecff").pack(pady=10)
        for name, count in [("Alice Johnson", "15 rentals"), ("Bob Smith", "12 rentals"), ("Carol Davis", "11 rentals")]:
            tk.Label(self.top_users_frame, text=f"{name} - {count}", bg="#e0ecff", font=("Segoe UI", 12)).pack(anchor="w", padx=10)

        # [0,1] Top Cars
        self.top_cars_frame = tk.Frame(self, bg="#fff4cc", bd=1, relief="solid")
        self.top_cars_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(self.top_cars_frame, text="Top Cars", font=("Segoe UI", 14, "bold"), bg="#fff4cc").pack(pady=10)
        for car, count in [("Toyota Camry", "18 rentals"), ("Tesla Model 3", "14 rentals"), ("Honda Accord", "13 rentals")]:
            tk.Label(self.top_cars_frame, text=f"{car} - {count}", bg="#fff4cc", font=("Segoe UI", 12)).pack(anchor="w", padx=10)

        # [0,2] Projected Income
        self.projected_income_frame = tk.Frame(self, bg="#dfffe0", bd=1, relief="solid")
        self.projected_income_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        tk.Label(self.projected_income_frame, text="Projected Income", font=("Segoe UI", 14, "bold"), bg="#dfffe0").pack(pady=10)
        tk.Label(self.projected_income_frame, text="$25,600.00", font=("Segoe UI", 18, "bold"),
                 bg="#dfffe0", fg="#2e7d32").pack(pady=10)

        # --- [2nd Row] - TreeView ---
        self.tree_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        self.tree_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(self.tree_frame, columns=("User", "Car", "Date", "Amount"), show="headings")
        self.tree.heading("User", text="User")
        self.tree.heading("Car", text="Car")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Add fake data
        fake_data = [
            ("Alice Johnson", "Toyota Camry", "2025-05-01", "$320"),
            ("Bob Smith", "Honda Accord", "2025-05-03", "$280"),
            ("Carol Davis", "Tesla Model 3", "2025-05-05", "$450"),
            ("Dan Wilson", "Ford Explorer", "2025-05-06", "$390"),
            ("Eva Lee", "BMW X5", "2025-05-07", "$610"),
        ]
        for record in fake_data:
            self.tree.insert("", "end", values=record)