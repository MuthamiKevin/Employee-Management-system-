from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
from employee import EmployeePanel
from admin import AdminPanel

def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)
def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)
def forget_password():
    def change_password():
        if username_entry.get() == '' or password_entry.get() == '' or confirmpassword_entry.get() == '':
            messagebox.showerror('Error', 'All fields are required', parent=window)
        elif password_entry.get() != confirmpassword_entry.get():
            messagebox.showerror('Error', 'Mismatch of passwords', parent=window)
        else:
            con = sqlite3.connect('employeedata.db')
            mycursor = con.cursor()
            query = 'SELECT * FROM employees WHERE username=?'
            mycursor.execute(query, (username_entry.get(),))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror('Error', 'Wrong username', parent=window)
            else:
                query = 'UPDATE employees SET password=? WHERE username=?'
                mycursor.execute(query, (password_entry.get(), username_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Successful password reset', parent=window)
                window.destroy()

    window = Toplevel()
    window.title('Change password')
    window.resizable(0, 0)

    bgPic = ImageTk.PhotoImage(file='front.jpg')
    bgLabel = Label(window, image=bgPic)
    bgLabel.grid()

    heading = Label(window, text='RESET PASSWORD', font=('arial', 18, 'bold'), bg='white', fg='magenta2')
    heading.place(x=480, y=60)

    usernameLabel = Label(window, text='Username', font=('Arial', 12, 'bold'), bg='white', fg='magenta2')
    usernameLabel.place(x=470, y=120)
    username_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    username_entry.place(x=470, y=150)
    Frame(window, width=250, height=2, bg='magenta2').place(x=470, y=170)

    passwordLabel = Label(window, text='Password', font=('Arial', 12, 'bold'), bg='white', fg='magenta2')
    passwordLabel.place(x=470, y=200)
    password_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    password_entry.place(x=470, y=230)
    Frame(window, width=250, height=2, bg='magenta2').place(x=470, y=250)

    confirmpasswordLabel = Label(window, text='Confirm Password', font=('Arial', 12, 'bold'), bg='white', fg='magenta2')
    confirmpasswordLabel.place(x=470, y=290)
    confirmpassword_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    confirmpassword_entry.place(x=470, y=330)
    Frame(window, width=250, height=2, bg='magenta2').place(x=470, y=350)

    submitButton = Button(window, text='Submit', bd=0, bg='magenta2', fg='white', font=('open sans', '16', 'bold'),
                          width=19, cursor='hand2', activebackground='magenta2', activeforeground='white', command=change_password)
    submitButton.place(x=470, y=390)

    window.mainloop()

def open_employee_panel():
    
    username = usernameEntry.get()  # Get the username from the entry widget
    if username == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All the fields are required!')
    else:
        try:
            con = sqlite3.connect('employeedata.db')
            mycursor = con.cursor()
            query = 'SELECT * FROM employees WHERE username=? AND password=?'
            mycursor.execute(query, (username, passwordEntry.get()))
            employee_row = mycursor.fetchone()

            query = 'SELECT * FROM admin WHERE username=? AND password=?'
            mycursor.execute(query, (username, passwordEntry.get()))
            admin_row = mycursor.fetchone()

            con.close()

            if employee_row:
                messagebox.showinfo('Welcome', 'Employee Login successful')
                login_window.destroy()
                app = EmployeePanel(username)  # Pass the username to EmployeePanel
                app.run()
            elif admin_row:
                messagebox.showinfo('Welcome', 'Admin Login successful')
                
                open_admin_panel()
            else:
                messagebox.showerror('Error', 'Invalid Username or Password')

        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Database connectivity issue: {str(e)}')

def open_admin_panel():
    login_window.destroy()
    app = AdminPanel()
    app.run
   
   
def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All the fields are required!')
    else:
        try:
            con = sqlite3.connect('employeedata.db')
            mycursor = con.cursor()
            query = 'SELECT * FROM employees WHERE username=? AND password=?'
            mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
            employee_row = mycursor.fetchone()

            query = 'SELECT * FROM admin WHERE username=? AND password=?'
            mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
            admin_row = mycursor.fetchone()

            con.close()

            if employee_row:
               
                open_employee_panel()
            elif admin_row:
                messagebox.showinfo('Welcome', 'Admin Login successful')
               
                open_admin_panel()
            else:
                messagebox.showerror('Error', 'Invalid Username or Password')

        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Database connectivity issue: {str(e)}')

def signup_page():
    login_window.destroy()
    import signup

def username_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
login_window.title('Sikala School Employee Management System Login Page')

bgImage = ImageTk.PhotoImage(file='front22.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI light', 20, 'bold'), bg='white', fg='black')
heading.place(x=620, y=120)

usernameEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI light', 10, 'bold'), bd=0, fg='black', bg='white')
usernameEntry.place(x=600, y=180)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', username_enter)

Frame(login_window, width=250, height=2, bg='black').place(x=600, y=200)

passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI light', 10, 'bold'), bd=0, fg='black', bg='white')
passwordEntry.place(x=600, y=250)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

Frame(login_window, width=250, height=2, bg='black').place(x=600, y=270)
openeye=PhotoImage(file='openeye.png')
eyeButton=Button(login_window,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eyeButton.place(x=820,y=240)


forgetButton = Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white',
                      cursor='hand2', font=('Microsoft Yahei UI light', 9, 'bold'),
                      fg='black', activeforeground='black', command=forget_password)
forgetButton.place(x=715, y=285)

loginButton = Button(login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='black',
                    activeforeground='white', activebackground='black', cursor='hand2', bd=0, width=17, command=login_user)
loginButton.place(x=600, y=350)

signupLabel = Label(login_window, text='Dont have an account?', font=('Microsoft Yahei UI light', 9, 'bold'), bg='white',
                    fg='black')
signupLabel.place(x=600, y=400)

newaccountButton = Button(login_window, text='Create new one', font=('Open Sans', 9, 'bold underline'), fg='blue', bg='white',
                          activeforeground='blue', activebackground='white', cursor='hand2', bd=0, command=signup_page)
newaccountButton.place(x=755, y=400)

login_window.mainloop()
