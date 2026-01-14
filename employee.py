import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from PIL import ImageTk

def view_own_information(username, parent):
    conn = sqlite3.connect("employeedata.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, phone, department, IDnumber FROM employees WHERE username=?", (username,))
    employee_info = cursor.fetchone()

    conn.close()

    if employee_info:
        first_name, last_name, email, phone, department, id_number = employee_info
        info_text = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone: {phone}\nDepartment: {department}\nID Number: {id_number}"
        messagebox.showinfo("Your Information", info_text)
    else:
        messagebox.showerror("Error", "Employee information not found.")


class UpdateEmployee:
    def __init__(self, emp_id, parent):
        self.emp_id = emp_id
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Update Employee Info")

        tk.Label(self.window, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Last Name:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Phone Number:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Department:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.window, text="ID Number:").grid(row=5, column=0, padx=10, pady=5)

        self.first_name_entry = tk.Entry(self.window)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.last_name_entry = tk.Entry(self.window)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        self.phone_number_entry = tk.Entry(self.window)
        self.phone_number_entry.grid(row=3, column=1, padx=10, pady=5)
        self.department_entry = tk.Entry(self.window)
        self.department_entry.grid(row=4, column=1, padx=10, pady=5)
        self.id_number_entry = tk.Entry(self.window)
        self.id_number_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.window, text="Update Info", command=self.update_employee_info).grid(row=6, column=0, columnspan=2, pady=10)

        self.load_employee_data()

    def load_employee_data(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name, email, phone, department, IDnumber FROM employees WHERE username=?", (self.emp_id,))
        employee_info = cursor.fetchone()
        conn.close()

        if employee_info:
            first_name, last_name, email, phone, department, id_number = employee_info
            self.first_name_entry.insert(0, first_name)
            self.last_name_entry.insert(0, last_name)
            self.email_entry.insert(0, email)
            self.phone_number_entry.insert(0, phone)
            self.department_entry.insert(0, department)
            self.id_number_entry.insert(0, id_number)

    def update_employee_info(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_number_entry.get()
        department = self.department_entry.get()
        id_number = self.id_number_entry.get()

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET first_name=?, last_name=?, email=?, phone=?, department=?, IDnumber=? WHERE username=?",
            (first_name, last_name, email, phone, department, id_number, self.emp_id)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Employee details updated successfully.")
        self.window.destroy()
class AssignProjectForm:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.root = tk.Toplevel()
        self.root.title("submit feedback")
        self.root.geometry('250x270')

        # Create the projects table if it doesn't exist
        self.create_projects_table()

        self.create_widgets()

    def create_projects_table(self):
        # Connect to the SQLite database
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        # Create the projects table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT,
                project_name TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                comments TEXT
            )
        """)

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

    def create_widgets(self):
        tk.Label(self.root, text="Project Name:").grid(row=0, column=0, pady=10)
        self.project_name_entry = tk.Entry(self.root)
        self.project_name_entry.grid(row=0, column=1, pady=10)

        tk.Label(self.root, text="Start Date:").grid(row=1, column=0, pady=10)
        current_date = datetime.now().date()
        one_week_ago = current_date - timedelta(weeks=1)

        self.start_date_entry = DateEntry(
            self.root,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            mindate=one_week_ago,  # Set the mindate to one week ago
        )
        self.start_date_entry.grid(row=1, column=1, pady=10)

        tk.Label(self.root, text="End Date:").grid(row=2, column=0, pady=10)
        self.end_date_entry = DateEntry(
            self.root,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            mindate=current_date,  # Set the mindate to the current date
        )
        self.end_date_entry.grid(row=2, column=1, pady=10)

        tk.Label(self.root, text="Status:").grid(row=3, column=0, pady=10)
        self.status_var = tk.StringVar()
        self.status_var.set("Pending")
        status_menu = tk.OptionMenu(self.root, self.status_var, "Pending", "Done")
        status_menu.grid(row=3, column=1, pady=10)

        tk.Label(self.root, text="Comments:").grid(row=4, column=0, pady=10)
        self.comments_entry = tk.Entry(self.root)
        self.comments_entry.grid(row=4, column=1, pady=10)

        tk.Button(self.root, text="Submit", command=self.submit_project).grid(row=5, column=0, columnspan=2, pady=20)

    def submit_project(self):
        project_name = self.project_name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        status = self.status_var.get()
        comments = self.comments_entry.get()

        if not all((project_name, start_date, end_date, status)):
            messagebox.showerror("Error", "All required fields must be filled.")
            return

        self.insert_project_data(project_name, start_date, end_date, status, comments)

    def insert_project_data(self, project_name, start_date, end_date, status, comments):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO projects (employee_id, project_name, start_date, end_date, status, comments)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.employee_id, project_name, start_date, end_date, status, comments))

        conn.commit()
        conn.close()

        messagebox.showinfo("Project Assigned", f"Project '{project_name}' assigned to the employee.")

        self.root.destroy()
class ApplyLeaveForm:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Apply Leave Form")
        self.root.geometry('300x250')
        self.create_leave_requests_table()

        self.create_widgets()

    def create_leave_requests_table(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                reason TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT DEFAULT 'Pending'
            )
        """)

        conn.commit()
        conn.close()

    def create_widgets(self):
        tk.Label(self.root, text="Reason").grid(row=0, column=0, pady=10)
        self.reason_entry = tk.Entry(self.root)
        self.reason_entry.grid(row=0, column=1, pady=10)

        tk.Label(self.root, text="Start Date").grid(row=1, column=0, pady=10)
        current_date = datetime.now().date()
        self.start_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, mindate=current_date)
        self.start_date_entry.grid(row=1, column=1, pady=10)

        tk.Label(self.root, text="End Date").grid(row=2, column=0, pady=10)
        self.end_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, mindate=current_date)
        self.end_date_entry.grid(row=2, column=1, pady=10)

        # Button to submit leave request
        tk.Button(self.root, text="Submit", command=self.submit_leave).grid(row=3, column=0, columnspan=2, pady=10)

        # Button to check leave request status
        tk.Button(self.root, text="Check Status", command=self.check_leave_status).grid(row=4, column=0, columnspan=2, pady=10)

    def submit_leave(self):
        reason = self.reason_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not all((reason, start_date, end_date)):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        self.submit_leave_request(reason, start_date, end_date)

    def submit_leave_request(self, reason, start_date, end_date):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO leave_requests (username, reason, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """, (self.username, reason, start_date, end_date))

        conn.commit()
        conn.close()

        messagebox.showinfo("Leave Request", "Leave request submitted successfully.")

    def check_leave_status(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        # Fetch the status of the latest leave request for the employee
        cursor.execute("""
            SELECT status FROM leave_requests
            WHERE username = ?
            ORDER BY id DESC
            LIMIT 1
        """, (self.username,))

        status = cursor.fetchone()

        conn.close()

        if status:
            messagebox.showinfo("Leave Status", f"Your leave request status: {status[0]}")
        else:
            messagebox.showinfo("Leave Status", "No leave request found.")

    def run(self):
        self.root.mainloop()
class AttendanceApp:
    def __init__(self, employee_id, username):
        self.employee_id = employee_id
        self.username = username
        self.root = tk.Tk()
        self.root.title("Employee Attendance")
        self.root.geometry('300x250')

        # Create attendance table if not exists
        self.create_attendance_table()

        self.create_widgets()

    def create_attendance_table(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                username TEXT,
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                attendance_date TEXT,
                time_in TEXT,
                time_out TEXT,
                status TEXT
            )
        """)

        conn.commit()
        conn.close()

    def create_widgets(self):
        tk.Label(self.root, text="Select Date:").grid(row=0, column=0, pady=10)
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, pady=10)

        tk.Button(self.root, text="Time In", command=self.get_time_in).grid(row=1, column=0, pady=10)
        self.time_in_entry = tk.Entry(self.root)
        self.time_in_entry.grid(row=1, column=1, pady=10)

        tk.Button(self.root, text="Time Out", command=self.get_time_out).grid(row=2, column=0, pady=10)
        self.time_out_entry = tk.Entry(self.root)
        self.time_out_entry.grid(row=2, column=1, pady=10)

        tk.Label(self.root, text="Status:").grid(row=3, column=0, pady=10)
        self.status_combobox = ttk.Combobox(self.root, values=["Present", "Absent", "Late"])
        self.status_combobox.grid(row=3, column=1, pady=10)
        self.status_combobox.set("Present")

        tk.Button(self.root, text="Submit Attendance", command=self.submit_attendance).grid(row=4, column=0,
                                                                                             columnspan=2, pady=20)

    def get_time_in(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_in_entry.delete(0, tk.END)
        self.time_in_entry.insert(0, current_time)

    def get_time_out(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_out_entry.delete(0, tk.END)
        self.time_out_entry.insert(0, current_time)

    def submit_attendance(self):
        selected_date = self.date_entry.get()
        current_date = datetime.now().strftime("%Y-%m-%d")

        if selected_date != current_date:
            messagebox.showerror("Error", "Please choose the current date for attendance.")
            return

        time_in = self.time_in_entry.get()
        time_out = self.time_out_entry.get()
        status = self.status_combobox.get()

        if not all((time_in, status)) and not all((time_out, status)):
            messagebox.showerror("Error", "Please fill in at least the time in or time out, and status.")
            return

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attendance (username, attendance_date, time_in, time_out, status, employee_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.username, current_date, time_in, time_out, status, self.employee_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Attendance Submitted", f"Attendance for {current_date} marked as {status}")

        self.root.destroy()

    def run(self):
        self.root.mainloop()

class EmployeeApp:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.employee_app = tk.Tk()
        self.employee_app.title(f"Employee Dashboard - {employee_id}")
        self.create_widgets()
        self.load_assigned_projects()

    def create_widgets(self):
        project_tree_label = tk.Label(self.employee_app, text="Assigned Projects:")
        project_tree_label.pack(pady=10)

        self.project_tree = ttk.Treeview(self.employee_app, columns=("Project Name", "Start Date", "End Date"))
        self.project_tree.heading("#1", text="Project Name")
        self.project_tree.heading("#2", text="Start Date")
        self.project_tree.heading("#3", text="End Date")
        self.project_tree.pack(padx=10)

        refresh_button = tk.Button(self.employee_app, text="Refresh", command=self.load_assigned_projects)
        refresh_button.pack(pady=10)

    def load_assigned_projects(self):
        self.project_tree.delete(*self.project_tree.get_children())

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT project_name, start_date, end_date
            FROM projects
            WHERE employee_id = ?
        """, (self.employee_id,))

        assigned_projects = cursor.fetchall()

        for project in assigned_projects:
            self.project_tree.insert("", "end", values=project)

        conn.close()

    def run(self):
        self.employee_app.mainloop()


class EmployeePanel:
    def __init__(self, username):
        self.username = username
        self.employee_panel = tk.Tk()
        self.employee_panel.title("Sikala School Employee Management System Employee Panel")
        self.employee_panel.geometry("1500x600")
        self.employee_panel.configure(bg='ivory4')
        self.bgImage = ImageTk.PhotoImage(file='22delete.png')
        self.bgLabel = tk.Label(self.employee_panel, image=self.bgImage)
        self.bgLabel.place(x=0, y=0)

        self.create_notebook()

    def create_notebook(self):
        notebook = ttk.Notebook(self.employee_panel)

        personal_info_tab = tk.Frame(notebook)
        update_info_tab = tk.Frame(notebook)
        leave_request_tab = tk.Frame(notebook)
        attendance_tab = tk.Frame(notebook)
        view_projects_tab = tk.Frame(notebook)
        log_out_tab=tk.Frame(notebook)

        personal_info_button = tk.Button(personal_info_tab, text="View Personal Information", command=self.view_personal_info)
        update_info_button = tk.Button(update_info_tab, text="Update Personal Information", command=self.update_personal_info)
        request_leave_button = tk.Button(leave_request_tab, text="Request Leave", command=self.request_leave)
        sign_attendance_button = tk.Button(attendance_tab, text="Sign Attendance", command=self.sign_attendance)
        view_projects_button = tk.Button(view_projects_tab, text="View Projects", command=self.view_projects)
        submit_project_button = tk.Button(view_projects_tab, text="submit feedback", command=self.submit_project)
        log_out_button = tk.Button(log_out_tab, text="Log out", command=self.main_window)
        

        personal_info_button.pack()
        update_info_button.pack()
        request_leave_button.pack()
        sign_attendance_button.pack()
        view_projects_button.pack()
        submit_project_button.pack()
        log_out_button.pack()

        notebook.add(personal_info_tab, text="View Personal Info")
        notebook.add(update_info_tab, text="Update Personal Info")
        notebook.add(leave_request_tab, text="Request Leave")
        notebook.add(attendance_tab, text="Sign Attendance")
        notebook.add(view_projects_tab, text="View Projects")
        notebook.add(log_out_tab, text="Log Out")
        notebook.pack()

    def view_personal_info(self):
        view_own_information(self.username, self.employee_panel)

    def update_personal_info(self):
        UpdateEmployee(self.username, self.employee_panel)

    def request_leave(self):
        ApplyLeaveForm(self.username)

    def sign_attendance(self):
        AttendanceApp(self.username,self.username)

    def view_projects(self):
        EmployeeApp(self.username).run()

    def run(self):
        self.employee_panel.mainloop()

    def main_window(self):
        self.employee_panel.destroy()   
        import main
    def submit_project(self):
        AssignProjectForm(self.username)
        

