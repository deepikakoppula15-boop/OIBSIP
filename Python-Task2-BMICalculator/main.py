import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import ttk
import matplotlib.pyplot as plt


# Create database
def create_database():
    try:
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT,
                date TEXT
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error:
        print("Database error while creating the database.")


# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_label.config(
        text="",
        fg="black"
    )


# Calculate BMI
def calculate_bmi():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            result_label.config(
                text="Weight and height must be greater than 0.",
                fg="red"
            )
            return

        if name.strip() == "":
            result_label.config(
                text="Please enter your name.",
                fg="red"
            )
            return

        # BMI calculation
        bmi = weight / (height ** 2)

        # BMI category
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        # Color-coded result
        if category == "Normal":
            result_color = "green"
        elif category == "Obese":
            result_color = "red"
        else:
            result_color = "orange"

        result_label.config(
            text=f"BMI: {round(bmi, 2)}\nCategory: {category}",
            fg=result_color
        )

        # Save record to database
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()
        connection.close()

    except ValueError:
        result_label.config(
            text="Please enter numbers only.",
            fg="red"
        )

    except sqlite3.Error:
        result_label.config(
            text="Database error. Please try again.",
            fg="red"
        )


# Show BMI graph
def show_graph():
    try:
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT date, bmi FROM bmi_records")

        records = cursor.fetchall()
        connection.close()

        if not records:
            result_label.config(
                text="No BMI records available for graph.",
                fg="red"
            )
            return

        dates = [record[0] for record in records]
        bmi_values = [record[1] for record in records]

        plt.figure(figsize=(8, 5))
        plt.plot(dates, bmi_values, marker="o")

        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI History")

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    except sqlite3.Error:
        result_label.config(
            text="Database error while loading graph.",
            fg="red"
        )


# View BMI history
def view_history():
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_window.geometry("700x400")

    table = ttk.Treeview(
        history_window,
        columns=("Name", "Weight", "Height", "BMI", "Category", "Date"),
        show="headings"
    )

    table.pack(fill="both", expand=True)

    for column in ("Name", "Weight", "Height", "BMI", "Category", "Date"):
        table.heading(column, text=column)

    try:
        connection = sqlite3.connect("bmi_database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT name, weight, height, bmi, category, date "
            "FROM bmi_records"
        )

        records = cursor.fetchall()
        connection.close()

        for record in records:
            table.insert("", tk.END, values=record)

    except sqlite3.Error:
        result_label.config(
            text="Database error while loading history.",
            fg="red"
        )


# Main window
window = tk.Tk()

window.title("BMI Calculator")
window.geometry("400x700")


# Title
title = tk.Label(
    window,
    text="BMI CALCULATOR",
    font=("Arial", 20)
)
title.pack(pady=20)


# Name
name_label = tk.Label(
    window,
    text="Name"
)
name_label.pack()

name_entry = tk.Entry(window)
name_entry.pack(pady=5)


# Weight
weight_label = tk.Label(
    window,
    text="Weight (kg)"
)
weight_label.pack()

weight_entry = tk.Entry(window)
weight_entry.pack(pady=5)


# Height
height_label = tk.Label(
    window,
    text="Height (m)"
)
height_label.pack()

height_entry = tk.Entry(window)
height_entry.pack(pady=5)


# Calculate button
calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi
)
calculate_button.pack(pady=10)


# Clear button
clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_fields
)
clear_button.pack(pady=5)


# Result
result_label = tk.Label(
    window,
    text="",
    font=("Arial", 14)
)
result_label.pack(pady=10)


# History button
history_button = tk.Button(
    window,
    text="View History",
    command=view_history
)
history_button.pack(pady=10)


# Graph button
graph_button = tk.Button(
    window,
    text="Show BMI Graph",
    command=show_graph
)
graph_button.pack(pady=10)


# BMI Category Guide
guide_title = tk.Label(
    window,
    text="BMI Category Guide",
    font=("Arial", 12, "bold")
)
guide_title.pack(pady=10)

guide_label = tk.Label(
    window,
    text="Below 18.5  → Underweight\n"
         "18.5 - 24.9 → Normal\n"
         "25 - 29.9   → Overweight\n"
         "30 or above → Obese",
    font=("Arial", 10),
    justify="left"
)
guide_label.pack(pady=5)


# Create database
create_database()


# Start application
window.mainloop()