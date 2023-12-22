import tkinter as tk
from PIL import Image, ImageTk

def signup_page():
    main_window.destroy()
    import signup

main_window = tk.Tk()
main_window.title("SIKALA SCHOOL EMPLOYEE MANAGEMENT SYSTEM")
main_window.iconbitmap('emp.ico')
main_window.geometry("1300x600")
main_window.resizable(0, 0)

bgImage = Image.open("2023landing.jpg")
photo = ImageTk.PhotoImage(bgImage)
bgLabel = tk.Label(main_window, image=photo)
bgLabel.place(x=0, y=0)

name_label = tk.Label(main_window, text="SIKALA SCHOOL EMPLOYEE MANAGEMENT SYSTEM", font=("Helvetica", 16), bg="white", fg="black")
name_label.place(relx=0.5, rely=0.1, anchor="center")

click_here = tk.Button(main_window, text="CLICK HERE TO CONTINUE", bg="white", fg="black", command=signup_page) 
click_here.place(x=450, y=450, width=300, height=40)

main_window.mainloop()
    