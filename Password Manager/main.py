from tkinter import *
from tkinter import messagebox
from random import choice,shuffle
import pandas as pd
import os

def generatePass():
    symbols = ['@', '#', '&', '%', '*']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
    uppercase_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    password = []
    for a in range(0,int(uppercase_input.get())):
        password.append(choice(uppercase_letters))
    for a in range(0,int(lowercase_input.get())):
        password.append(choice(lowercase_letters))
    for a in range(0,int(numbers_input.get())):
        password.append(choice(numbers))
    for a in range(0,int(symbols_input.get())):
        password.append(choice(symbols))
    shuffle(password)
    final_password = ''.join(password)
    password_input.delete(0, END)
    password_input.insert(0, final_password)
    copyToClipboard(password_input.get())
    
def copyToClipboard(text):
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()
    
def savePass():
    data = {"Platform":platform_input.get(),"UserId":userId_input.get(),"Password":password_input.get()}
    #to Password.csv
    if os.path.exists("Passwords.csv"):
        a = pd.read_csv("Passwords.csv")
    else:
        a = pd.DataFrame(columns=["Platform", "UserId", "Password"])
    new_input = pd.DataFrame([data])
    a = pd.concat([a,new_input],ignore_index=True)
    a.to_csv("Passwords.csv",index=False)
    
    password_input.delete(0,END)
    platform_input.delete(0,END)
    userId_input.delete(0,END)
    
    messagebox.showinfo(title="Password Manager",message="Password saved successfully.")

def cancelUserId():
    userId_input.delete(0,END)

def cancelPlatform():
    platform_input.delete(0,END)
    
def defMail():
    userId_input.delete(0,END)
    userId_input.insert(0,"105singhanshuman@gmail.com")

def defPhone():
    userId_input.delete(0,END)
    userId_input.insert(0,"8822786312")

def search():
    try:
        pass_file = pd.read_csv("Passwords.csv")
        req_row = pass_file[pass_file.Platform == platform_input.get()]
        messagebox.showinfo(title="Password Manager",message=f"User id : {req_row.UserId.to_string(index=False)}\nPassword : {req_row.Password.to_string(index=False)}")
    except FileNotFoundError:
        messagebox.showwarning(title="Password Manager",message="No password file found!")

window = Tk()
window.minsize(900, 600)
window.config(bg="white")
window.title("Password Manager")
window.config(padx=150)

canvas = Canvas(window, width=200, height=200, bg="white", highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

Platform_label = Label(text="Platform : ", bg="white")
Platform_label.grid(row=1, column=0,sticky="E")
platform_input = Entry(window, width=35)
platform_input.grid(row=1, column=1,pady=10)

userId_label = Label(text="User Id : ", bg="white")
userId_label.grid(row=2, column=0,sticky="E")
userId_input = Entry(window, width=35)
userId_input.grid(row=2, column=1,pady=10)

btn = Button(text="X",fg="white",bg="red",command=cancelUserId,height=1,highlightthickness=0,width=1)
btn.grid(row=2,column=2,padx=3,sticky="W")
btn = Button(text="X",fg="white",bg="red",command=cancelPlatform,height=1,highlightthickness=0,width=1)
btn.grid(row=1,column=2,padx=3,sticky="W")
btn = Button(text="Default Mail",fg="white",bg="blue",command=defMail,height=1,highlightthickness=0,width=12)
btn.grid(row=2,column=3,padx =3,sticky="W")
btn = Button(text="Search",fg="white",bg="green",command=search,height=1,highlightthickness=0,width=12)
btn.grid(row=1,column=3,padx =3,sticky="W")
btn = Button(text="Default Phone No.",fg="white",bg="blue",command=defPhone,height=1,highlightthickness=0,width=14)
btn.grid(row=2,column=4,padx=3,sticky="W")

numbers_label = Label(text="No. of Numbers : ", bg="white")
numbers_label.grid(row=3, column=0,sticky="E")
numbers_input = Entry(window, width=35)
numbers_input.grid(row=3, column=1,pady=10)
numbers_input.insert(0,4)

uppercase_label = Label(text="No. of Uppercase Letters : ", bg="white")
uppercase_label.grid(row=4, column=0,sticky="E")
uppercase_input = Entry(window, width=35)
uppercase_input.grid(row=4, column=1,pady=10)
uppercase_input.insert(0,2)
lowercase_label = Label(text="No. of Lowercase Letters : ", bg="white")
lowercase_label.grid(row=5, column=0,sticky="E")
lowercase_input = Entry(window, width=35)
lowercase_input.grid(row=5, column=1,pady=10)
lowercase_input.insert(0,2)

symbols_label = Label(text="No. of Symbols : ", bg="white")
symbols_label.grid(row=6, column=0,sticky="E")
symbols_input = Entry(window, width=35)
symbols_input.grid(row=6, column=1,pady=10)
symbols_input.insert(0,2)

password_label = Label(text="Password : ", bg="white",font=("Arial",14,"bold"))
password_label.grid(row=7, column=0,sticky="E")
password_input = Entry(window, width=35)
password_input.grid(row=7, column=1,pady=10)

btn = Button(text="Generate Pasword",fg="white",bg="blue",command=generatePass)
btn.grid(row=8,column=1,pady=5,padx=3)

btn = Button(text="Save Password",fg="white",bg="green",command=savePass)
btn.grid(row=9,column=1,pady=5)

window.mainloop()