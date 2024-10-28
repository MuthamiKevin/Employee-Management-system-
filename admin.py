import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
from PIL import ImageTk
from datetime import datetime

class AdminPanel:
    def __init__(self, role):
        self.role = role
        # Only admins can delete employees, for example
        if self.role == "Admin":
            self.delete_employee_button = tk.Button(delete_employee_tab, text="Delete Employee", command=self.delete_employee)
            self.delete_employee_button.pack()

class AdminViewProjects:
    def __init__(self):
        self.admin_view_projects = tk.Tk()
        self.admin_view_projects.title("Admin View Projects")
        self.create_widgets()
        self.load_submitted_projects()

    def create_widgets(self):
        self.project_tree = ttk.Treeview(self.admin_view_projects, columns=("Employee ID", "Project Name", "Start Date", "End Date", "Status", "Comments"))
        self.project_tree.heading("#1", text="Employee ID")
        self.project_tree.heading("#2", text="Project Name")
        self.project_tree.heading("#3", text="Start Date")
        self.project_tree.heading("#4", text="End Date")
        self.project_tree.heading("#5", text="Status")
        self.project_tree.heading("#6", text="Comments")
        self.project_tree.pack(padx=10, pady=10)

        refresh_button = tk.Button(self.admin_view_projects, text="Refresh", command=self.load_submitted_projects)
        refresh_button.pack(pady=10)

    def load_submitted_projects(self):
        self.project_tree.delete(*self.project_tree.get_children())

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT employee_id, project_name, start_date, end_date, status, comments
            FROM projects
        """)

        submitted_projects = cursor.fetchall()

        for project in submitted_projects:
            self.project_tree.insert("", "end", values=project)

        conn.close()

    def run(self):
        self.admin_view_projects.mainloop()

class AdminLeaveRequests:
    def __init__(self):
        self.admin_leave_requests = tk.Tk()
        self.admin_leave_requests.title("Admin Leave Requests")
        self.create_widgets()
        self.load_leave_requests()

    def create_widgets(self):
        self.leave_tree = ttk.Treeview(self.admin_leave_requests, columns=("NO","Employee ID", "Reason", "Start Date", "End Date"))
        self.leave_tree.heading("#1", text="NO")
        self.leave_tree.heading("#2", text="username")
        self.leave_tree.heading("#3", text="Reason")
        self.leave_tree.heading("#4", text="Start Date")
        self.leave_tree.heading("#5", text="End Date")
        self.leave_tree.pack(padx=10, pady=10)

        accept_button = tk.Button(self.admin_leave_requests, text="Accept", command=self.accept_leave_request)
        accept_button.pack(side=tk.LEFT, padx=10)

        decline_button = tk.Button(self.admin_leave_requests, text="Decline", command=self.decline_leave_request)
        decline_button.pack(side=tk.RIGHT, padx=10)

    def load_leave_requests(self):
        self.leave_tree.delete(*self.leave_tree.get_children())

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        # Fetch all leave requests
        cursor.execute("CREATE TABLE IF NOT EXISTS leave_requests (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id TEXT, reason TEXT, start_date TEXT, end_date TEXT, status TEXT)")
        cursor.execute("SELECT * FROM leave_requests")
        leave_requests = cursor.fetchall()

        for leave_request in leave_requests:
            self.leave_tree.insert("", "end", values=leave_request)

        conn.close()

    def accept_leave_request(self):
        selected_item = self.leave_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a leave request.")
            return

        leave_id = self.leave_tree.item(selected_item, "values")[0]

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE leave_requests SET status='Accepted' WHERE id=?", (leave_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Leave Request Accepted", "Leave request has been accepted.")
        self.load_leave_requests()

    def decline_leave_request(self):
        selected_item = self.leave_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a leave request.")
            return

        leave_id = self.leave_tree.item(selected_item, "values")[0]

        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE leave_requests SET status='Declined' WHERE id=?", (leave_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Leave Request Declined", "Leave request has been declined.")
        self.load_leave_requests()

    def run(self):
        self.admin_leave_requests.mainloop()


class AssignProjectForm:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Assign Project")
        self.root.geometry('300x250')
        self.create_projects_table()

        self.create_widgets()

    def create_projects_table(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT,
                project_name TEXT,
                start_date TEXT,
                end_date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def create_widgets(self):
        tk.Label(self.root, text="Select Employee:").grid(row=0, column=0, pady=10)
        self.employee_combobox = ttk.Combobox(self.root, values=self.get_employee_names())
        self.employee_combobox.grid(row=0, column=1, pady=10)

        tk.Label(self.root, text="Project Name:").grid(row=1, column=0, pady=10)
        self.project_name_entry = tk.Entry(self.root)
        self.project_name_entry.grid(row=1, column=1, pady=10)

        tk.Label(self.root, text="Start Date:").grid(row=2, column=0, pady=10)
        current_date = datetime.now().date()
        self.start_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, mindate=current_date)
        self.start_date_entry.grid(row=2, column=1, pady=10)

        tk.Label(self.root, text="End Date:").grid(row=3, column=0, pady=10)
        self.end_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, mindate=current_date)
        self.end_date_entry.grid(row=3, column=1, pady=10)

        tk.Button(self.root, text="Assign", command=self.assign_project).grid(row=4, column=0, columnspan=2, pady=20)
    def get_employee_names(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM employees")
        employee_names = [f"{first_name} {last_name}" for first_name, last_name in cursor.fetchall()]
        conn.close()
        return employee_names

    def assign_project(self):
        employee_name = self.employee_combobox.get()
        project_name = self.project_name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not all((employee_name, project_name, start_date, end_date)):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        employee_id = self.get_employee_id(employee_name)

        if employee_id:
            self.insert_project_data(employee_id, project_name, start_date, end_date)
        else:
            messagebox.showerror("Error", "Employee not found.")

    def get_employee_id(self, employee_name):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT idnumber FROM employees WHERE first_name || ' ' || last_name=?", (employee_name,))
        employee_id = cursor.fetchone()
        conn.close()
        return employee_id[0] if employee_id else None

    def insert_project_data(self, employee_id, project_name, start_date, end_date):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO projects (employee_id, project_name, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """, (employee_id, project_name, start_date, end_date))

        conn.commit()
        conn.close()

        messagebox.showinfo("Project Assigned", f"Project '{project_name}' assigned to the employee.")

        self.root.destroy()
    

class AdminPanel:
    def __init__(self):
        self.admin_panel = tk.Tk()
        self.admin_panel.title("Sikala School Employee Managemnt System Admin Panel")
        self.admin_panel.geometry("1500x600")

        self.bgImage = ImageTk.PhotoImage(file='seco.jpg')
        self.bgLabel = tk.Label(self.admin_panel, image=self.bgImage)
        self.bgLabel.place(x=350, y=70)

        self.create_notebook()

    def create_notebook(self):
        notebook = ttk.Notebook(self.admin_panel)

        view_employees_tab = tk.Frame(notebook)
        delete_employee_tab = tk.Frame(notebook)
        assign_projects_tab = tk.Frame(notebook)
        review_leave_request_tab = tk.Frame(notebook)
        check_attendance_tab = tk.Frame(notebook)
        log_out_tab = tk.Frame(notebook)

        notebook.add(view_employees_tab, text="View Employees")
        notebook.add(delete_employee_tab, text="Delete Employee")
        notebook.add(assign_projects_tab, text="Assign Projects")
        notebook.add(review_leave_request_tab, text="Review Leave Request")
        notebook.add(check_attendance_tab, text="Check Attendance")
        notebook.add(log_out_tab, text="Log Out")

        notebook.pack()

        view_employees_button = tk.Button(view_employees_tab, text="View Employees", command=self.view_employees)
        delete_employee_button = tk.Button(delete_employee_tab, text="Delete Employee", command=self.delete_employee)
        assign_projects_button = tk.Button(assign_projects_tab, text="Assign Projects", command=self.assign_project)
        review_leave_request_button = tk.Button(review_leave_request_tab, text="Review Leave Request", command=self.review_leave_request)
        check_attendance_button = tk.Button(check_attendance_tab, text="Check attendance", command=self.check_attendance)
        view_projects_button = tk.Button(assign_projects_tab, text="View Submitted Projects", command=self.view_submitted_projects)
        add_employee_button = tk.Button(view_employees_tab, text="Add Employee", command=self.add_employee)
        log_out_button = tk.Button(log_out_tab, text="Log Out", command=self.main_window)

        view_employees_button.pack()
        delete_employee_button.pack()
        assign_projects_button.pack()
        review_leave_request_button.pack()
        check_attendance_button.pack()
        view_projects_button.pack()
        log_out_button.pack()

    def main_window(self):
        self.admin_panel.destroy()
        import main

    def add_employee(self):
        add_employee_window = tk.Toplevel(self.admin_panel)
        add_employee_window.title("Add Employee")
        add_employee_window.geometry("400x400")
        
        first_name_label = tk.Label(add_employee_window, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(add_employee_window)
        first_name_entry.pack()

        last_name_label = tk.Label(add_employee_window, text="Last Name:")
        last_name_label.pack()
        last_name_entry = tk.Entry(add_employee_window)
        last_name_entry.pack()

        email_label = tk.Label(add_employee_window, text="Email:")
        email_label.pack()
        email_entry = tk.Entry(add_employee_window)
        email_entry.pack()

        phone_label = tk.Label(add_employee_window, text="Phone:")
        phone_label.pack()
        phone_entry = tk.Entry(add_employee_window)
        phone_entry.pack()

        department_label = tk.Label(add_employee_window, text="Department:")
        department_label.pack()
        department_entry = tk.Entry(add_employee_window)
        department_entry.pack()

        id_number_label = tk.Label(add_employee_window, text="ID Number:")
        id_number_label.pack()
        id_number_entry = tk.Entry(add_employee_window)
        id_number_entry.pack()

        username_label = tk.Label(add_employee_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(add_employee_window)
        username_entry.pack()

        password_label = tk.Label(add_employee_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(add_employee_window, show="*")
        password_entry.pack()


        def perform_addition():
          
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            department = department_entry.get()
            id_number = id_number_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not all((first_name, last_name, email, phone, department, id_number, username, password)):
                messagebox.showerror("Error", "All fields must be filled.")
                return

            conn = sqlite3.connect("employeedata.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO employees (first_name, last_name, email, phone, department, idnumber, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, department, id_number, username, password))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Employee added successfully.")
            add_employee_window.destroy()

        add_button = tk.Button(add_employee_window, text="Add Employee", command=perform_addition)
        add_button.pack()    

    def view_submitted_projects(self):
        admin_view_projects = AdminViewProjects()
        admin_view_projects.run()

    def check_attendance(self):
        check_attendance_window = tk.Toplevel(self.admin_panel)
        check_attendance_window.title("Check Attendance")
        check_attendance_window.geometry('1000x400')
        self.show_attendance_data(check_attendance_window)

    
    def check_attendance(self):
        check_attendance_window = tk.Toplevel(self.admin_panel)
        check_attendance_window.title("Check Attendance")
        check_attendance_window.geometry('1000x400')
        self.show_attendance_data(check_attendance_window)

    def show_attendance_data(self, parent):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT attendance_date FROM attendance")
        dates = [date[0] for date in cursor.fetchall()]

        conn.close()

        date_label = tk.Label(parent, text="Select Date:")
        date_label.pack()

        date_combobox = ttk.Combobox(parent, values=dates)
        date_combobox.pack()

        def fetch_attendance():
            selected_date = date_combobox.get()

            if not selected_date:
                messagebox.showerror("Error", "Please select a date.")
                return

            conn = sqlite3.connect("employeedata.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM attendance WHERE attendance_date=?", (selected_date,))
            attendance_data = cursor.fetchall()

            conn.close()

            if attendance_data:
                tree = ttk.Treeview(parent, columns=("id", "Employee ID", "Username", "Attendance Date", "Time In", "Time Out", "Status"))
                tree.heading("#0", text="id")
                tree.heading("#1", text="Emp id")
                tree.heading("#2", text="Username")
                tree.heading("#3", text="Attendance Date")
                tree.heading("#4", text="Time In")
                tree.heading("#5", text="Time Out")
                tree.heading("#6", text="Status")

                for row in attendance_data:
                    tree.insert("", "end", values=row)

                tree.pack(expand=True, fill="both")
            else:
                messagebox.showinfo("Attendance", f"No attendance data available for {selected_date}.")

        fetch_button = tk.Button(parent, text="Fetch Attendance", command=fetch_attendance)
        fetch_button.pack()


    def print_attendance(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM attendance")
        attendance_data = cursor.fetchall()

        conn.close()

        if attendance_data:
            print("Attendance Data:")
            for row in attendance_data:
                print(row)
        else:
            print("No attendance data available.")

    def run(self):
        self.admin_panel.mainloop()

    def assign_project(self):
        assign_project_form = AssignProjectForm()
        assign_project_form.run()

    def view_employees(self):
        view_employees_window = tk.Toplevel(self.admin_panel)
        view_employees_window.title("View Employees")
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        employee_tree = ttk.Treeview(view_employees_window, columns=("First Name", "Last Name", "Email", "Phone", "Department", "ID Number", "Username"))

        employee_tree.heading("#1", text="First Name")
        employee_tree.heading("#2", text="Last Name")
        employee_tree.heading("#3", text="Email")
        employee_tree.heading("#4", text="Phone")
        employee_tree.heading("#5", text="Department")
        employee_tree.heading("#6", text="ID Number")
        employee_tree.heading("#7", text="Username")

        for employee in employees:
            employee_tree.insert("", "end", values=employee)

        employee_tree.pack()
        conn.close()

    def delete_employee(self):
        conn = sqlite3.connect("employeedata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM employees")
        employee_usernames = [row[0] for row in cursor.fetchall()]
        conn.close()

        delete_employee_window = tk.Toplevel(self.admin_panel)
        delete_employee_window.title("Delete Employee")
        delete_employee_window.geometry("300x200")

        username_label = tk.Label(delete_employee_window, text="Select Employee Username:")
        username_label.pack()

        username_combobox = ttk.Combobox(delete_employee_window, values=employee_usernames)
        username_combobox.pack()

        def perform_delete():
            selected_username = username_combobox.get()
            if not selected_username:
                messagebox.showerror("Error", "Please select an employee.")
                return

            # Ask for confirmation
            confirmation = messagebox.askyesno("Confirmation", f"Do you really want to delete the employee '{selected_username}'?")

            if confirmation:
                conn = sqlite3.connect("employeedata.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employees WHERE username=?", (selected_username,))
                employee = cursor.fetchone()

                if employee is None:
                    messagebox.showerror("Error", "Employee with the selected username not found.")
                else:
                    cursor.execute("DELETE FROM employees WHERE username=?", (selected_username,))
                    conn.commit()
                    messagebox.showinfo("Success", "Employee deleted successfully.")
                conn.close()

        delete_button = tk.Button(delete_employee_window, text="Delete Employee", command=perform_delete)
        delete_button.pack()

    def run(self):
        self.admin_panel.mainloop()

    def review_leave_request(self):
        admin_leave_requests_app = AdminLeaveRequests()
        admin_leave_requests_app.run()

    def run(self):
        self.admin_panel.mainloop()

def accept_leave_request(self):
    if not self.leave_balance_sufficient(employee_id):
        messagebox.showerror("Insufficient Leave Balance")
        return
    # Approval process here...
def export_data_to_csv(self, table_name):
    conn = sqlite3.connect("employeedata.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    with open(f"{table_name}.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    conn.close()

if __name__ == "__main__":
    admin_app = AdminPanel()
    admin_app.run()
