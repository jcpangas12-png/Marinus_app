import tkinter as tk
from tkinter import ttk, messagebox
import os

# Set up local file storage in the user's Documents folder
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "RhinoFundraiser")
os.makedirs(SAVE_DIR, exist_ok=True)
FILE_PATH = os.path.join(SAVE_DIR, "donations_log.txt")
TARGET_GOAL = 100000.00  # R100,000 Fundraising Goal

def calculate_totals():
    """Reads the local text file to calculate total funds raised."""
    total = 0.0
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    if "Amount: R" in line:
                        try:
                            # Split the line to extract the numerical value safely
                            parts = line.split("Amount: R")
                            if len(parts) > 1:
                                amount_str = parts[1].split(" |")[0]
                                total += float(amount_str)
                        except (IndexError, ValueError):
                            continue
        except Exception as e:
            print(f"Error reading records: {e}")
    return total

def update_ui_metrics():
    """Updates the dynamic progress bar and text metrics on the screen."""
    current_total = calculate_totals()
    lbl_total_raised.config(text=f"Total Raised: R{current_total:,.2f}")
    
    # Calculate percentage progress for the bar (capped at 100%)
    percentage = min((current_total / TARGET_GOAL) * 100, 100) if TARGET_GOAL > 0 else 0
    progress_bar["value"] = percentage
    lbl_percentage.config(text=f"{percentage:.1f}% of R{TARGET_GOAL:,.0f} goal")

def handle_donation():
    """Validates inputs and appends the record to local storage."""
    donor = entry_donor.get().strip()
    amount_raw = entry_amount.get().strip()
    branch = combo_branch.get()

    if not donor or not amount_raw:
        messagebox.showerror("Error", "Please fill in all input fields.")
        return

    try:
        amount = float(amount_raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount greater than R0.")
        return

    # Create data record line
    record = f"Donor: {donor} | Amount: R{amount:.2f} | Branch: {branch}\n"

    try:
        with open(FILE_PATH, "a", encoding="utf-8") as file:
            file.write(record)
        
        messagebox.showinfo("Success", f"Thank you {donor}! Your donation has been recorded.")
        
        # Clear fields and update interface metrics instantly
        entry_donor.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        update_ui_metrics()
        
    except Exception as e:
        messagebox.showerror("Storage Error", f"Could not save record to disk: {str(e)}")

# --- Setup Mobile Window Canvas Shape ---
root = tk.Tk()
root.title("MVJ Rhino App")
root.geometry("380x650")  # Emulates a typical mobile aspect ratio
root.resizable(False, False)
root.configure(bg="#1e293b")  # Dark corporate theme

# Header
lbl_brand = tk.Label(root, text="Marinus van Jaarsveld\nAttorneys", font=("Helvetica", 10, "bold"), fg="#94a3b8", bg="#1e293b")
lbl_brand.pack(pady=10)

lbl_title = tk.Label(root, text="Rhino Conservation\nFundraiser", font=("Helvetica", 16, "bold"), fg="#f8fafc", bg="#1e293b")
lbl_title.pack(pady=5)

# --- PROGRESS CONTAINER (Widget Dashboard) ---
frame_progress = tk.LabelFrame(root, text=" Campaign Progress ", fg="#38bdf8", bg="#0f172a", bd=1, relief="solid", padx=15, pady=15)
frame_progress.pack(fill="x", padx=20, pady=15)

lbl_total_raised = tk.Label(frame_progress, text="Total Raised: R0.00", font=("Helvetica", 14, "bold"), fg="#4ade80", bg="#0f172a")
lbl_total_raised.pack(anchor="w")

# Visual progress bar loading
progress_bar = ttk.Progressbar(frame_progress, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(fill="x", pady=10)

lbl_percentage = tk.Label(frame_progress, text="0.0% of goal", font=("Helvetica", 9), fg="#94a3b8", bg="#0f172a")
lbl_percentage.pack(anchor="e")

# --- DONATION FORM ---
frame_form = tk.LabelFrame(root, text=" Quick Secure Donation ", fg="#38bdf8", bg="#1e293b", bd=0, padx=5)
frame_form.pack(fill="x", padx=20, pady=10)

tk.Label(frame_form, text="Donor Name / Organisation:", fg="#cbd5e1", bg="#1e293b", font=("Helvetica", 10)).pack(anchor="w", pady=(5, 2))
entry_donor = tk.Entry(frame_form, font=("Helvetica", 11), bg="#334155", fg="white", insertbackground="white", bd=0)
entry_donor.pack(fill="x", ipady=6, pady=5)

tk.Label(frame_form, text="Donation Amount (ZAR):", fg="#cbd5e1", bg="#1e293b", font=("Helvetica", 10)).pack(anchor="w", pady=(5, 2))
entry_amount = tk.Entry(frame_form, font=("Helvetica", 11), bg="#334155", fg="white", insertbackground="white", bd=0)
entry_amount.pack(fill="x", ipady=6, pady=5)

tk.Label(frame_form, text="Select Supporting Branch:", fg="#cbd5e1", bg="#1e293b", font=("Helvetica", 10)).pack(anchor="w", pady=(5, 2))
combo_branch = ttk.Combobox(frame_form, values=["Randburg", "Pretoria", "Modimolle"], state="readonly", font=("Helvetica", 10))
combo_branch.current(0)
combo_branch.pack(fill="x", ipady=4, pady=5)

# Action Submission Button
btn_submit = tk.Button(root, text="PROCEED TO PAY", font=("Helvetica", 12, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", bd=0, cursor="hand2", command=handle_donation)
btn_submit.pack(fill="x", padx=20, ipady=10, pady=25)

# Initialize application metrics on startup
update_ui_metrics()

root.mainloop()
