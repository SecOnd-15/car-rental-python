import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from tkinter import messagebox
from datetime import datetime

class RentCarFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        
        self.configure(bg="#f0f0f0")
        self.total_price = 0
        self.base_price = 0
        self.selected_services = []
        
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Rent a Car", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=(20, 0))

        self.car_plate_label = tk.Label(form_frame, text="Car Plate Number:", bg="#f0f0f0", font=("Helvetica", 12))
        self.car_plate_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.car_plate_combobox = ttk.Combobox(form_frame, values=DatabaseManager.GetAvailableCars(), state="readonly", font=("Helvetica", 12))
        self.car_plate_combobox.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        self.car_plate_combobox.bind("<<ComboboxSelected>>", lambda event: self.calculate_total_price())

        self.renter_name_label = tk.Label(form_frame, text="Renter's Full Name:", bg="#f0f0f0", font=("Helvetica", 12))
        self.renter_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.customer_names = DatabaseManager.GetAllCustomerNames()
        self.renter_name_var = tk.StringVar()
        self.renter_name_combobox = ttk.Combobox(form_frame, textvariable=self.renter_name_var, font=("Helvetica", 12))
        self.renter_name_combobox['values'] = self.customer_names
        self.renter_name_combobox.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        self.renter_name_combobox.configure(state="normal")
        self.renter_name_combobox.bind("<KeyRelease>", self.on_keyrelease)

        self.payment_method_label = tk.Label(form_frame, text="Payment Method:", bg="#f0f0f0", font=("Helvetica", 12))
        self.payment_method_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.payment_method_combobox = ttk.Combobox(form_frame, values=["Down Payment", "Cash in Direct"], state="readonly", font=("Helvetica", 12))
        self.payment_method_combobox.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.rental_period_label = tk.Label(form_frame, text="Rental Period (Days):", bg="#f0f0f0", font=("Helvetica", 12))
        self.rental_period_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.rental_period_var = tk.StringVar()
        self.rental_period_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.rental_period_var)
        self.rental_period_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        
        self.start_date_label = tk.Label(form_frame, text="Start Date (DD/MM/YY):", bg="#f0f0f0", font=("Helvetica", 12))
        self.start_date_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.start_date_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.start_date_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")
        self.start_date_entry.bind("<KeyRelease>", lambda event: self.calculate_rental_days())

        
        self.end_date_label = tk.Label(form_frame, text="End Date (DD/MM/YY):", bg="#f0f0f0", font=("Helvetica", 12))
        self.end_date_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.end_date_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.end_date_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")
        self.end_date_entry.bind("<KeyRelease>", lambda event: self.calculate_rental_days())


        self.total_price_label = tk.Label(form_frame, text="Total Price ($):", bg="#f0f0f0", font=("Helvetica", 12))
        self.total_price_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.total_price_var = tk.StringVar()
        self.total_price_var.set(f"${self.total_price:.2f}")
        self.total_price_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.total_price_var)
        self.total_price_entry.grid(row=6, column=1, pady=5, padx=10, sticky="w")

        services_container = tk.Frame(form_frame, bg="#e0e0e0")
        services_container.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky="nsew")

        services_canvas = tk.Canvas(services_container, bg="#e0e0e0", highlightthickness=0)
        services_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(services_container, orient="vertical", command=services_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        services_canvas.configure(yscrollcommand=scrollbar.set)
        services_canvas.bind('<Configure>', lambda e: services_canvas.configure(scrollregion=services_canvas.bbox("all")))

        self.services_frame = tk.Frame(services_canvas, bg="#e0e0e0")
        services_canvas.create_window((0, 0), window=self.services_frame, anchor="nw")

        services_title = tk.Label(self.services_frame, text="Additional Services:", bg="#e0e0e0", font=("Helvetica", 12, "bold"))
        services_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        service_data = DatabaseManager.GetAllServicesDataForRent()
        self.service_vars = {}

        for i, (service, price) in enumerate(service_data.items()):
            label = tk.Label(self.services_frame, text=f"{service} (${price:.2f}):", bg="#e0e0e0", font=("Helvetica", 11))
            label.grid(row=i + 1, column=0, sticky="w", pady=2)

            var = tk.IntVar(value=0)
            self.service_vars[service] = var

            rb_no = tk.Radiobutton(self.services_frame, text="No", variable=var, value=0, bg="#e0e0e0", font=("Helvetica", 10), command=self.on_service_change)
            rb_no.grid(row=i + 1, column=1, sticky="w", padx=(10, 0))

            rb_yes = tk.Radiobutton(self.services_frame, text="Yes", variable=var, value=1, bg="#e0e0e0", font=("Helvetica", 10), command=self.on_service_change)
            rb_yes.grid(row=i + 1, column=2, sticky="w")

        self.rent_car_button = tk.Button(self, text="Rent Car", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.rent_car_button_functions)
        self.rent_car_button.pack(pady=(20, 0))

        self.tree = ttk.Treeview(self, columns=("Plate", "Make", "Model", "Year", "Fuel", "Trans", "Price", "Seats", "Availability"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.load_data_from_db()

    def calculate_total_price(self):
        plate_number = self.car_plate_combobox.get()
        price = DatabaseManager.GetCarRentalPrice(plate_number)
        if price is not None:
            self.base_price = price
            self.total_price = self.base_price
            self.total_price_var.set(f"${self.total_price:.2f}")
            self.selected_services = []
            self.rental_period_entry.delete(0, tk.END)
            self.rental_period_entry.insert(0, "1")
            self.reset_all_services()

            for var in self.service_vars.values():
                var.set(0)

            # Load selected car into the Treeview
            self.load_selected_car_to_tree(plate_number)
            self.calculate_rental_days()


    def on_service_change(self):
        selected_services = self.get_selected_services()
        total_additional_price = 0

        for service in selected_services:
            additional = DatabaseManager.GetServicePrice(service)
            if additional:
                total_additional_price += additional

        self.total_price = self.base_price + total_additional_price
        self.selected_services = selected_services
        self.total_price_var.set(f"${self.total_price:.2f}")
        self.calculate_rental_days()

    def get_selected_services(self):
        return [service for service, var in self.service_vars.items() if var.get() == 1]

    def rent_car_button_functions(self):
        car_plate = self.car_plate_combobox.get()
        renter_name = self.renter_name_var.get()
        payment_method = self.payment_method_combobox.get()
        rental_period = self.rental_period_var.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        try:
            self.check_and_add_if_new_user(name=renter_name)

            self.validation(car_plate, renter_name, rental_period, payment_method)

            if DatabaseManager.get_customer_reputation(renter_name) < 20:
                result = messagebox.askyesno(
                    "Bad Reputation",
                    f"{renter_name} has a bad reputation. Do you still want to rent the car?"
                )
                if not result:
                    return

            car_price = DatabaseManager.GetCarRentalPrice(car_plate)
            total_price = float(car_price) * int(rental_period)

            self.total_price_entry.config(state="normal")
            self.total_price_entry.delete(0, tk.END)
            self.total_price_entry.insert(0, f"{total_price:.2f}")
            self.total_price_entry.config(state="readonly")

            selected_services = self.get_selected_services()
            total_additional_price = 0

            for service in selected_services:
                additional = DatabaseManager.GetServicePrice(service)
                if additional:
                    total_additional_price += additional

            total_price += float(total_additional_price)

            DatabaseManager.rent_car_and_services(
                car_plate=car_plate,
                renter_name=renter_name,
                rental_period=rental_period,
                total_price=total_price,
                payment_method=payment_method,
                services=selected_services,
                starting_date=start_date,
                ending_date=end_date
            )

            self.warningText.config(text="Car rented successfully!", fg="green")
            self.load_data_from_db()
            self.clear()

            self.customer_names = DatabaseManager.GetAllCustomerNames()
            self.renter_name_combobox['values'] = self.customer_names

        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def validation(self, car_plate, renter_name, rental_period, payment_method):
        if not car_plate.strip():
            raise ValueError("Car plate is required.")
        if not renter_name.strip():
            raise ValueError("Renter's full name is required.")
        if not rental_period.strip() or not rental_period.isdigit() or int(rental_period) <= 0:
            raise ValueError("Valid rental period is required.")
        if not payment_method.strip():
            raise ValueError("Payment method is required.")

    def load_data_from_db(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for car in DatabaseManager.GetAllCars():
            self.tree.insert("", "end", values=car)

    def on_keyrelease(self, event):
        value = self.renter_name_var.get().strip().lower()
        filtered = [n for n in self.customer_names if value in n.lower()] if value else self.customer_names
        self.renter_name_combobox['values'] = filtered
        self.renter_name_combobox.selection_clear()

    def check_and_add_if_new_user(self, name):
        if not DatabaseManager.ExistingCustomerExists(name):
            DatabaseManager.AddExistingCustomer(name)

    def clear(self):
        self.car_plate_combobox.set('')
        self.renter_name_combobox.set('')
        self.payment_method_combobox.set('')
        
        self.rental_period_entry.delete(0, tk.END)
        
        self.total_price_entry.config(state="normal")
        self.total_price_entry.delete(0, tk.END)
        self.total_price_entry.config(state="readonly")
        
        for var in self.service_vars.values():
            var.set(0)
        
        self.total_price_var.set("$0.00")
        self.base_price = 0
        self.total_price = 0
        self.selected_services = []
        
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        
        self.reset_car_plate_combobox()

    def reset_car_plate_combobox(self):
        self.car_plate_combobox['values'] = DatabaseManager.GetAvailableCars()
        self.car_plate_combobox.set('')

    def update_total_price(self):
        car_plate = self.car_plate_combobox.get()
        rental_period = self.rental_period_entry.get()

        try:
            base_price = DatabaseManager.GetCarRentalPrice(car_plate)
            days = int(rental_period)

            if base_price is None:
                raise ValueError("Invalid car or no price found.")

            service_total = sum(
                DatabaseManager.GetServicePrice(service) or 0
                for service in self.get_selected_services()
            )

            total = base_price * days + service_total
            self.total_price = total
            self.total_price_var.set(f"${total:.2f}")

        except (ValueError, TypeError):
            self.total_price_var.set("$0.00")

    def reset_all_services(self):
        for var in self.service_vars.values():
            var.set(0)
        self.on_service_change()

    def load_selected_car_to_tree(self, plate_number):

        self.tree.delete(*self.tree.get_children())
        car = DatabaseManager.GetCarByPlate(plate_number)
        if car:
            self.tree.insert("", "end", values=car)

    def calculate_rental_days(self):
        start_date_str = self.start_date_entry.get().strip()
        end_date_str = self.end_date_entry.get().strip()

        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%y")

            if end_date < start_date:
                self.rental_period_var.set("")
                self.total_price_var.set("$0.00")
                return

            days = (end_date - start_date).days + 1
            self.rental_period_var.set(str(days))
            self.update_total_price()

        except ValueError:
            self.rental_period_var.set("")
            self.total_price_var.set("$0.00")