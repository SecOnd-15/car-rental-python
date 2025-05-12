import tkinter as tk
from tkinter import ttk, messagebox
from Database.DatabaseInstance import db_manager

class ReturnRentFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(bg="#f0f0f0")

        tk.Label(self, text="Return Rental", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Customer Email", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.customer_email_var = tk.StringVar()
        self.customer_email_combobox = ttk.Combobox(form_frame, textvariable=self.customer_email_var, font=("Helvetica", 12), width=30)
        self.customer_email_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.customer_email_combobox.bind("<<ComboboxSelected>>", self.load_rental_info)

        self.return_button = tk.Button(self, text="Mark as Returned", font=("Helvetica", 14), bg="#00998F", fg="white")
        self.return_button.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Plate", "Start", "End", "Total", "Status"), show="headings")
        for col in ("Plate", "Start", "End", "Total", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        

    def refresh(self):
        self.warningText.config(text="", fg="red")
        self.tree.delete(*self.tree.get_children())
        emails = db_manager.Get.get_all_customer_emails(cursor=db_manager.cursor)
        self.customer_email_combobox['values'] = emails
        self.customer_email_combobox.set("")

    def load_rental_info(self, event=None):
        self.tree.delete(*self.tree.get_children())
        email = self.customer_email_var.get()
        rentals = db_manager.Get.get_active_rentals_by_email(cursor=db_manager.cursor, email=email)
        for rental in rentals:
            self.tree.insert("", "end", values=(
                rental['plate_number'],
                rental['rental_date'],
                rental['return_date'],
                f"${rental['total_amount']:.2f}",
                rental['status']
            ))

    def mark_returned(self):
        selected = self.tree.selection()
        if not selected:
            self.warningText.config(text="Please select a rental.", fg="red")
            return
        item = self.tree.item(selected[0])
        plate = item['values'][0]
        email = self.customer_email_var.get()

        try:
            db_manager.Edit.mark_rental_returned(cursor=db_manager.cursor, conn=db_manager.conn, plate_number=plate, email=email)
            db_manager.Edit.edit_car_availability(cursor=db_manager.cursor, conn=db_manager.conn, licensePlate=plate, newStatus="Available")
            self.warningText.config(text="Rental marked as returned.", fg="green")
            self.load_rental_info()
        except Exception as e:
            self.warningText.config(text=str(e), fg="red")
