import tkinter as tk
from tkinter import ttk, messagebox
from Database.DatabaseInstance import db_manager

class ReturnRentFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(bg="#f0f0f0")
        self.total_price = 0

        tk.Label(self, text="Return Rental", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=10)
        
        # Rent ID
        self.rent_id_label = tk.Label(form_frame, text="Rent ID:", bg="#f0f0f0", font=("Helvetica", 12))
        self.rent_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.rent_id_combobox = ttk.Combobox(
            form_frame,
            values=["Select Rent ID"],
            state="readonly",
            font=("Helvetica", 12)
        )
        self.rent_id_combobox.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        # Return Date (DD/MM/YY)
        self.return_date_label = tk.Label(form_frame, text="Return Date (DD/MM/YY):", bg="#f0f0f0", font=("Helvetica", 12))
        self.return_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.return_date_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        self.return_date_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.total_price_label = tk.Label(form_frame, text="Total Price ($):", bg="#f0f0f0", font=("Helvetica", 12))
        self.total_price_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.total_price_var = tk.StringVar()
        self.total_price_var.set(f"${self.total_price:.2f}")
        self.total_price_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.total_price_var)
        self.total_price_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")


        # Container for damage section
        damage_container = tk.Frame(form_frame, bg="#e0e0e0")
        damage_container.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky="nsew")

        # Scrollable canvas
        damage_canvas = tk.Canvas(damage_container, bg="#e0e0e0", highlightthickness=0)
        damage_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(damage_container, orient="vertical", command=damage_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        damage_canvas.configure(yscrollcommand=scrollbar.set)

        # Internal frame inside canvas
        self.damage_frame = tk.Frame(damage_canvas, bg="#e0e0e0")
        damage_canvas.create_window((0, 0), window=self.damage_frame, anchor="nw")

        # Enable scroll region update
        self.damage_frame.bind("<Configure>", lambda e: damage_canvas.configure(scrollregion=damage_canvas.bbox("all")))

        # Section title
        damage_title = tk.Label(self.damage_frame, text="Reported Damages:", bg="#e0e0e0", font=("Helvetica", 12, "bold"))
        damage_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # Hardcoded damage types and prices
        damage_data = {
            "Scratch": 50.00,
            "Dented Bumper": 100.00,
            "Broken Mirror": 75.00,
            "Flat Tire": 30.00,
            "Windshield Crack": 120.00
        }

        self.damage_vars = {}

        # Add radio buttons for each damage
        for i, (damage, price) in enumerate(damage_data.items()):
            label = tk.Label(self.damage_frame, text=f"{damage} (${price:.2f}):", bg="#e0e0e0", font=("Helvetica", 11))
            label.grid(row=i + 1, column=0, sticky="w", pady=2)

            var = tk.IntVar(value=0)
            self.damage_vars[damage] = var

            rb_no = tk.Radiobutton(
                self.damage_frame, text="No", variable=var, value=0,
                bg="#e0e0e0", font=("Helvetica", 10)
            )
            rb_no.grid(row=i + 1, column=1, sticky="w", padx=(10, 0))

            rb_yes = tk.Radiobutton(
                self.damage_frame, text="Yes", variable=var, value=1,
                bg="#e0e0e0", font=("Helvetica", 10)
            )
            rb_yes.grid(row=i + 1, column=2, sticky="w")



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
