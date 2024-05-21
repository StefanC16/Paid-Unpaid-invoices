import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json


class InvoiceReminderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Manager de plati PK 1.0")
        self.geometry("800x600")
        style = Style(theme="flatly")
        style.configure("Custom.TEntry", foreground="gray")

        # Create input boxes for invoice number, date, and total amount
        self.invoice_number_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=20, style="Custom.TEntry")
        self.invoice_number_input.insert(0, "Nr. facturii")
        self.invoice_number_input.bind("<FocusIn>", self.clear_placeholder)
        self.invoice_number_input.bind("<FocusOut>", self.restore_placeholder)
        self.invoice_number_input.grid(row=0, column=0, padx=10, pady=5)

        self.invoice_date_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=20, style="Custom.TEntry")
        self.invoice_date_input.insert(0, "Data")
        self.invoice_date_input.bind("<FocusIn>", self.clear_placeholder)
        self.invoice_date_input.bind("<FocusOut>", self.restore_placeholder)
        self.invoice_date_input.grid(row=0, column=1, padx=10, pady=5)

        self.invoice_amount_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=20, style="Custom.TEntry")
        self.invoice_amount_input.insert(0, "Valoare")
        self.invoice_amount_input.bind("<FocusIn>", self.clear_placeholder)
        self.invoice_amount_input.bind("<FocusOut>", self.restore_placeholder)
        self.invoice_amount_input.grid(row=0, column=2, padx=10, pady=5)

        # Create a button to add invoices
        ttk.Button(self, text="Adauga", command=self.add_invoice).grid(
            row=1, column=0, columnspan=3, pady=5)

        # Create a frame to hold the listboxes for the columns
        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # Create and grid the labels for column headers
        self.header1 = tk.Label(
            self.listbox_frame, text="Nr. facturii", font=("Helvetica 18 bold", 16))
        self.header1.grid(row=0, column=0, sticky="ew")

        self.header2 = tk.Label(
            self.listbox_frame, text="Data", font=("TkDefaultFont", 16))
        self.header2.grid(row=0, column=1, sticky="ew")

        self.header3 = tk.Label(
            self.listbox_frame, text="Valoare", font=("TkDefaultFont", 16))
        self.header3.grid(row=0, column=2, sticky="ew")

        # Create and grid the listboxes for each column
        self.invoice_list1 = tk.Listbox(self.listbox_frame, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.SINGLE)
        self.invoice_list1.grid(row=1, column=0, sticky="nsew")

        self.invoice_list2 = tk.Listbox(self.listbox_frame, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.SINGLE)
        self.invoice_list2.grid(row=1, column=1, sticky="nsew")

        self.invoice_list3 = tk.Listbox(self.listbox_frame, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.SINGLE)
        self.invoice_list3.grid(row=1, column=2, sticky="nsew")

        # Configure grid columns to expand with window resizing
        self.listbox_frame.columnconfigure(0, weight=1)
        self.listbox_frame.columnconfigure(1, weight=1)
        self.listbox_frame.columnconfigure(2, weight=1)

        # Create buttons for marking as paid and deleting invoices
        ttk.Button(self, text="Finalizat!", style="success.TButton",
                   command=self.mark_paid).grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(self, text="Stergere", style="danger.TButton",
                   command=self.delete_invoice).grid(row=4, column=0, columnspan=3, pady=10)
        ttk.Button(self, text="Raport", style="info.TButton",
                   command=self.view_stats).grid(row=5, column=0, columnspan=3, pady=10)

        self.load_invoices()

    def view_stats(self):
        unfinished_count = 0
        unpaid_sum = 0
        total_count = self.invoice_list1.size()
        for i in range(total_count):
            if self.invoice_list1.itemcget(i, "fg") == "red":
                unfinished_count += 1
                try:
                    unpaid_sum += float(self.invoice_list3.get(i))
                except ValueError:
                    pass
        messagebox.showinfo(
            "Raport", f"Din {total_count} facturi totale\nSunt neplatite: {unfinished_count} facturi\nSuma totala neincasata: {unpaid_sum:.2f}")

    def add_invoice(self):
        invoice_number = self.invoice_number_input.get()
        invoice_date = self.invoice_date_input.get()
        invoice_amount = self.invoice_amount_input.get()

        if invoice_number != "Nr. facturii" and invoice_date != "Data" and invoice_amount != "Valoare":
            if self.is_valid_amount(invoice_amount):
                self.invoice_list1.insert(tk.END, invoice_number)
                self.invoice_list1.itemconfig(tk.END, fg="red")
                self.invoice_list2.insert(tk.END, invoice_date)
                self.invoice_list2.itemconfig(tk.END, fg="red")
                self.invoice_list3.insert(tk.END, invoice_amount)
                self.invoice_list3.itemconfig(tk.END, fg="red")
                self.save_invoices()

                self.invoice_number_input.delete(0, tk.END)
                self.invoice_date_input.delete(0, tk.END)
                self.invoice_amount_input.delete(0, tk.END)
            else:
                messagebox.showerror(
                    "Error", "Valoarea trebuie sa fie alcatuita numai din cifre!")

    def is_valid_amount(self, amount):
        try:
            float(amount)
            return True
        except ValueError:
            return False

    def mark_paid(self):
        selected_index = self.invoice_list1.curselection()
        if selected_index:
            index = selected_index[0]
            self.invoice_list1.itemconfig(index, fg="green")
            self.invoice_list2.itemconfig(index, fg="green")
            self.invoice_list3.itemconfig(index, fg="green")
            self.save_invoices()

    def delete_invoice(self):
        selected_index = self.invoice_list1.curselection()
        if selected_index:
            index = selected_index[0]
            self.invoice_list1.delete(index)
            self.invoice_list2.delete(index)
            self.invoice_list3.delete(index)
            self.save_invoices()

    def clear_placeholder(self, event):
        if event.widget.get() in ["Nr. facturii", "Data", "Valoare"]:
            event.widget.delete(0, tk.END)
            event.widget.configure(style="TEntry")

    def restore_placeholder(self, event):
        if event.widget.get() == "":
            if event.widget == self.invoice_number_input:
                event.widget.insert(0, "Nr. facturii")
            elif event.widget == self.invoice_date_input:
                event.widget.insert(0, "Data")
            elif event.widget == self.invoice_amount_input:
                event.widget.insert(0, "Valoare")
            event.widget.configure(style="Custom.TEntry")

    def load_invoices(self):
        try:
            with open("invoices.json", "r") as f:
                data = json.load(f)
                for invoice in data:
                    self.invoice_list1.insert(tk.END, invoice["number"])
                    self.invoice_list1.itemconfig(
                        tk.END, fg=invoice.get("color", "red"))
                    self.invoice_list2.insert(tk.END, invoice["date"])
                    self.invoice_list2.itemconfig(
                        tk.END, fg=invoice.get("color", "red"))
                    self.invoice_list3.insert(tk.END, invoice["amount"])
                    self.invoice_list3.itemconfig(
                        tk.END, fg=invoice.get("color", "red"))
        except FileNotFoundError:
            pass

    def save_invoices(self):
        data = []
        for i in range(self.invoice_list1.size()):
            number = self.invoice_list1.get(i)
            date = self.invoice_list2.get(i)
            amount = self.invoice_list3.get(i)
            color = self.invoice_list1.itemcget(i, "fg")
            paid = color == "green"
            data.append({"number": number, "date": date,
                        "amount": amount, "color": color, "paid": paid})
        with open("invoices.json", "w") as f:
            json.dump(data, f)


if __name__ == '__main__':
    app = InvoiceReminderApp()
    app.mainloop()
