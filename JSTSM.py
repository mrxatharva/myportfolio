import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ----------------- GLOBAL DATA -----------------
ADMIN_USER = "ADMIN"
ADMIN_PASS = "admin"
tiffin_data = []
PDF_FILE = "Monthly_Tiffin_Bill.pdf"

# ----------------- LOGIN WINDOW -----------------
def login():
    if entry_user.get() == ADMIN_USER and entry_pass.get() == ADMIN_PASS:
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Admin Login", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(login_window, text="Username").pack()
entry_user = tk.Entry(login_window)
entry_user.pack()

tk.Label(login_window, text="Password").pack()
entry_pass = tk.Entry(login_window, show="*")
entry_pass.pack()

tk.Button(login_window, text="Login", command=login, width=15).pack(pady=10)

# ----------------- MAIN APP -----------------
def main_app():
    root = tk.Tk()
    root.title("Jay Shankar Tiffin Service - Mess Manager")
    root.geometry("900x650")

    def add_entry():
        day = entry_day.get()
        qty = entry_qty.get()

        if day == "" or qty == "":
            messagebox.showerror("Error", "Enter day and tiffins")
            return

        tiffin_data.append((day, int(qty)))
        table.insert("", tk.END, values=(day, qty))
        entry_day.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        calculate_total()

    def calculate_total():
        rate = entry_rate.get()
        if rate == "":
            return
        total_tiffins = sum(q[1] for q in tiffin_data)
        amount = total_tiffins * float(rate)
        lbl_total_tiffins.config(text=f"Total Tiffins: {total_tiffins}")
        lbl_amount.config(text=f"Total Amount: ₹ {amount}")

    def create_pdf():
        if not tiffin_data:
            messagebox.showerror("Error", "No data to generate bill")
            return

        c = canvas.Canvas(PDF_FILE, pagesize=A4)
        text = c.beginText(40, 800)

        text.setFont("Helvetica-Bold", 14)
        text.textLine("Jay Shankar Tiffin Service")
        text.textLine("Monthly Tiffin Bill")
        text.textLine("-" * 40)

        text.setFont("Helvetica", 11)
        text.textLine(f"Customer Name: {entry_name.get()}")
        text.textLine(f"Month: {entry_month.get()}")
        text.textLine(f"Tiffin Rate: ₹{entry_rate.get()}")
        text.textLine("")

        total_tiffins = 0
        for d, q in tiffin_data:
            text.textLine(f"Day {d} : {q} Tiffins")
            total_tiffins += q

        total_amount = total_tiffins * float(entry_rate.get())
        text.textLine("")
        text.textLine(f"Total Tiffins: {total_tiffins}")
        text.textLine(f"Total Amount: ₹ {total_amount}")

        c.drawText(text)
        c.showPage()
        c.save()

        messagebox.showinfo("Success", "Monthly PDF Bill Generated")

    def print_bill():
        if not os.path.exists(PDF_FILE):
            messagebox.showerror("Error", "Generate PDF first")
            return
        os.startfile(PDF_FILE, "print")

    # ----------------- UI -----------------

    tk.Label(root, text="🍱 Jay Shankar Tiffin Service", font=("Arial", 20, "bold")).pack(pady=10)

    info = tk.Frame(root)
    info.pack()

    tk.Label(info, text="Customer Name").grid(row=0, column=0)
    entry_name = tk.Entry(info)
    entry_name.grid(row=0, column=1)

    tk.Label(info, text="Month").grid(row=0, column=2)
    entry_month = tk.Entry(info)
    entry_month.grid(row=0, column=3)

    tk.Label(info, text="Rate per Tiffin").grid(row=0, column=4)
    entry_rate = tk.Entry(info)
    entry_rate.grid(row=0, column=5)

    daily = tk.Frame(root)
    daily.pack(pady=10)

    tk.Label(daily, text="Day").grid(row=0, column=0)
    entry_day = tk.Entry(daily, width=10)
    entry_day.grid(row=0, column=1)

    tk.Label(daily, text="Tiffins").grid(row=0, column=2)
    entry_qty = tk.Entry(daily, width=10)
    entry_qty.grid(row=0, column=3)

    tk.Button(daily, text="Add Entry", command=add_entry).grid(row=0, column=4, padx=10)

    table = ttk.Treeview(root, columns=("Day", "Tiffins"), show="headings", height=12)
    table.heading("Day", text="Day")
    table.heading("Tiffins", text="Tiffins Taken")
    table.pack(pady=10)

    summary = tk.Frame(root)
    summary.pack()

    lbl_total_tiffins = tk.Label(summary, text="Total Tiffins: 0", font=("Arial", 12, "bold"))
    lbl_total_tiffins.grid(row=0, column=0, padx=20)

    lbl_amount = tk.Label(summary, text="Total Amount: ₹ 0", font=("Arial", 12, "bold"))
    lbl_amount.grid(row=0, column=1, padx=20)

    tk.Button(root, text="Generate PDF Bill", command=create_pdf, width=25).pack(pady=5)
    tk.Button(root, text="Print Bill", command=print_bill, width=25).pack(pady=5)

    root.mainloop()

login_window.mainloop()
