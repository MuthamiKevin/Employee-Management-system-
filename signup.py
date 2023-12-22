from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# Function to clear entry fields
def clear():
    firstEntry.delete(0, END)
    secondEntry.delete(0, END)
    emailEntry.delete(0, END)
    phoneEntry.delete(0, END)
    departmentEntry.delete(0, END)
    idnumberEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    check.set(0)

#
def connect_database():
    if (firstEntry.get() == '' or secondEntry.get() == '' or emailEntry.get() == '' or
            phoneEntry.get() == '' or departmentEntry.get() == '' or idnumberEntry.get() == '' or
            usernameEntry.get() == '' or passwordEntry.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    elif check.get() == 0:
        messagebox.showerror('Error', 'Accept terms and conditions')
    else:
        
        try:
            con = sqlite3.connect("employeedata.db") 
            mycursor = con.cursor()
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Database connectivity issue: {str(e)}')
            return
        create_table_query = '''CREATE TABLE IF NOT EXISTS employees (
                                first_name TEXT,
                                last_name TEXT,
                                email TEXT,
                                phone TEXT,
                                department TEXT,
                                idnumber INTEGER,
                                username TEXT,
                                password TEXT)'''

        try:
            mycursor.execute(create_table_query)
            con.commit()
        except sqlite3.Error as e:
            messagebox.showerror('Error', f'Database error: {str(e)}')

        username = usernameEntry.get()
        check_username_query = "SELECT * FROM employees WHERE username = ?"
        mycursor.execute(check_username_query, (username,))
        row = mycursor.fetchone()

        if row is not None:
            messagebox.showerror('Error', 'Username already exists')
        else:
            # Insert new user data into the database
            insert_query = '''INSERT INTO employees (first_name, last_name, email, phone, department, idnumber, username, password)
                              VALUES (?, ?, ?, ?, ?, ?, ?,?)'''
            data = (firstEntry.get(), secondEntry.get(), emailEntry.get(), phoneEntry.get(), departmentEntry.get(), idnumberEntry.get(),
                    usernameEntry.get(), passwordEntry.get())
            try:
                mycursor.execute(insert_query, data)
                con.commit()
                messagebox.showinfo('Success', 'Registration successful')
                clear()
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'Database error: {str(e)}')
        con.close()


def login_page():
    signup_window.destroy()
    import signin

signup_window = Tk()
signup_window.geometry('1140x822')
signup_window.resizable(0, 0)
signup_window.title('Sikala School Employee Management System Signup Page')

bgImage = Image.open("new2.jpg")
photo = ImageTk.PhotoImage(bgImage)
bgLabel = Label(signup_window, image=photo)
bgLabel.place(x=0, y=0)

frame = Frame(signup_window, bg='white')
frame.place(x=690, y=89)
frame.config(width=480, height=600)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI light', 18, 'bold'), bg='white', fg='black')
heading.grid(row=0, column=0, padx=5, pady=5)

firstLabel = Label(frame, text='First Name', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
firstLabel.grid(row=1, column=0, sticky='W', padx=15, pady=(2, 0))
firstEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
firstEntry.grid(row=2, column=0, sticky='W', padx=15)

secondLabel = Label(frame, text='Last Name', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
secondLabel.grid(row=3, column=0, sticky='W', padx=15, pady=(2, 0))
secondEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
secondEntry.grid(row=4, column=0, sticky='W', padx=15)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
emailLabel.grid(row=5, column=0, sticky='W', padx=15, pady=(2, 0))
emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
emailEntry.grid(row=6, column=0, sticky='W', padx=15)

phoneLabel = Label(frame, text='Phone Number', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
phoneLabel.grid(row=7, column=0, sticky='W', padx=15, pady=(2, 0))
phoneEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
phoneEntry.grid(row=8, column=0, sticky='W', padx=15)

departmentLabel = Label(frame, text='Department', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
departmentLabel.grid(row=9, column=0, sticky='W', padx=15, pady=(2, 0))
departmentEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
departmentEntry.grid(row=10, column=0, sticky='W', padx=15)

idnumberLabel = Label(frame, text='ID Number', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
idnumberLabel.grid(row=11, column=0, sticky='W', padx=15, pady=(2, 0))
idnumberEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
idnumberEntry.grid(row=12, column=0, sticky='W', padx=15)

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
usernameLabel.grid(row=13, column=0, sticky='W', padx=15, pady=(2, 0))
usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
usernameEntry.grid(row=14, column=0, sticky='W', padx=15)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI light', 10, 'bold'), bg='white', fg='black')
passwordLabel.grid(row=15, column=0, sticky='W', padx=15, pady=(2, 0))
passwordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI light', 10, 'bold'), fg='black', bg='white')
passwordEntry.grid(row=16, column=0, sticky='W', padx=15)

check = IntVar()

termsandconditions = Checkbutton(frame, text='I agree to the terms & conditions',
                                  font=('Microsoft Yahei UI light', 8, 'bold'), fg='black',
                                  bg='white', activeforeground='black', activebackground='white', cursor='hand2', variable=check)
termsandconditions.grid(row=17, column=0, padx=20, pady=5)

createButton = Button(frame, text='Create Account', font=('Open sans', 16, 'bold'), bd=0, bg='white',
                      fg='black', activeforeground='black', activebackground='white', width=17, command=connect_database)
createButton.grid(row=18, column=0, pady=2)

alreadyaccount = Label(frame, text="Already have an account?", font=('Open sans', 9, 'bold'), bg='white', fg='black')
alreadyaccount.grid(row=19, column=0, sticky='w', padx=25, pady=10)

loginButton = Button(frame, text='Log in', font=('Open sans', 9, 'bold underline'), bg='white',
                     fg='blue', bd=0, cursor='hand2', activeforeground='blue', activebackground='white', command=login_page)
loginButton.place(x=185, y=535)
signup_window.mainloop()
