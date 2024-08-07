from tkinter import *
from tkinter import simpledialog,messagebox
import os,datetime,smtplib,json,requests,pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


sender_email ="xyz@mail.com"
email_password = "xyz"

class StartQuiz():
    def __init__(self):
        self.user()
        start_btn.destroy()
        self.wait_label = Label(text="Generating Quiz, Please Wait. . .",bg="#635985",font=("Arial",12,"bold"))
        self.wait_label.grid(row = 1, column =1,padx=20,pady=20)
        self.num = 0
        self.correct = 0
        self.incorrect = 0
        self.answers = []
        self.getData()
        self.history()
        self.now()
    def now(self):
        return datetime.datetime.now().date()
        
    def user(self):
        self.name = simpledialog.askstring(title="Simple Quiz Game",prompt="Enter you name : ")
        if self.name is None:
            self.name = "Unknown Player"
        
    def scorecard(self):
        a = [self.data[i]["question"] for i in range(self.num)]
        b = [self.data[i]["correct_answer"] for i in range(self.num)]
        c = self.answers
        result = {"Question":a,"Correct Answers":b,"Your Answers":c}
        result_csv = pd.DataFrame(result)
        result_csv.to_csv("scorecard.csv",index=False)
    
    def getData(self):
        try:
            self.data = requests.get(url="https://opentdb.com/api.php?amount=25&type=boolean").json()["results"]
            window.after(2000,self.changeUI)
        except Exception as e:
            messagebox.showerror("Error", f"Error while generating questions : {e}")
            
    
    def changeUI(self):
        self.wait_label.destroy()
        self.a = PhotoImage(file="true.png")
        self.b = PhotoImage(file="false.png")
        self.changeQn()
        self.incorrect_img = Button(image=self.b,fg="white",bg="#635985",command = self.checkFalse,highlightthickness=0,width=100,height=100)
        self.incorrect_img.grid(row=1,column=1,padx=20,pady=20,sticky="W")
        self.correct_img = Button(image=self.a,fg="white",bg="#635985",command =self.checkTrue,highlightthickness=0,width=100,height=100)    
        self.correct_img.grid(row=1,column=1,padx=20,pady=20,sticky="E")
        self.quit_now = Button(text="QUIT NOW",fg="white",bg="red",command =self.quit,highlightthickness=0,width=15)    
        self.quit_now.grid(row=2,column=1,padx=20,pady=20)

    def checkTrue(self):
        self.answers.append("True")
        if self.data[self.num]["correct_answer"] == "True":
            self.correct+=1
        else:
            self.incorrect+=1
        self.num+=1
        self.changeQn()

    def checkFalse(self):
        self.answers.append("False")
        if self.data[self.num]["correct_answer"] == "False":
            self.correct+=1
        else:
            self.incorrect+=1
        self.num+=1
        self.changeQn()
        
    def changeQn(self):
        if self.num < len(self.data):
            canvas2.itemconfig(question,text=self.data[self.num]["question"],font=("Arial",12))
        else:
            self.quit()

    def quit(self):
        self.incorrect_img.destroy()
        self.correct_img.destroy()
        self.quit_now.destroy()
        canvas2.itemconfig(question,text=f"Correct Answers : {self.correct}\nIncorrect Answers : {self.incorrect}",font=("Arial",12))
        if self.correct > highScore():
             data = {"Name":self.name,"Score":self.correct}
             with open("score.json", "w") as file:
                json.dump(data,file)
        self.scorecard()
        self.mail_btn = Button(text="Get Scorecard",fg="white",bg="green",command =self.mail_score,highlightthickness=0,width=17,font=("Arial",20,"bold"))    
        self.mail_btn.grid(row=2,column=1,padx=20,pady=20)
        
    def history(self):
        if os.path.exists("history.csv"):
            pass
        else:
            hist_data = {"Date":[],"Name":[],"Score":[],"Email":[]}
            hist_data = pd.DataFrame(hist_data)
            a = hist_data.to_csv("history.csv",index=False)
    
    def mail_score(self):
        self.mail_to = simpledialog.askstring(title="Simple Quiz Game", prompt="Enter your mail id: ")
        if self.mail_to is not None:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = self.mail_to
            msg['Subject'] = "Simple Quiz Game Scorecard"

            body = f"Hello {self.name}, thanks for playing our game.\nYour score is {self.correct} out of 25. We have attached the scorecard with this mail."
            msg.attach(MIMEText(body, 'plain'))

            filename = "scorecard.csv"
            attachment = open(filename, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login(user=sender_email, password=email_password)
                    connection.sendmail(from_addr=sender_email, to_addrs=self.mail_to, msg=msg.as_string())
                messagebox.showinfo("Email Sent", f"Scorecard sent successfully to {self.mail_to}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {e}")
            his_file = pd.read_csv("history.csv")
            new = {"Date":self.now(),"Name":self.name,"Score":self.correct,"Email":self.mail_to}
            new = pd.DataFrame([new])
            his_file = pd.concat([his_file,new],ignore_index=True)
            his_file.to_csv("history.csv",index=False)
def highScore():
    try:
        with open("score.json", "r") as file:
            hs_data = json.load(file)
    except FileNotFoundError:
        with open("score.json", "w") as file:
            hs_data = {"Name":"","Score":0}
            json.dump(hs_data,file)
    return hs_data["Score"]

window =Tk()
window.minsize(450,650)
window.config(bg="#635985",padx=100,pady=30)

canvas = Canvas(width=300,height=350,bg="#443C68",highlightthickness=0)
canvas.grid(row=0,column=1)
canvas.create_text(120,305,text=f"Your Score : \nHigh Score : {highScore()}",fill="white",font=("Arial",12,"bold"))
canvas2 = Canvas(width=250,height=250,bg="#18122B",highlightthickness=0)
canvas2.grid(row=0,column=1,sticky="N",pady=30)
question = canvas2.create_text(120,100,width=200,text="\nSIMPLE QUIZ GAME",fill="white",font=("Arial",30,"bold"))

start_btn = Button(text="START",fg="White",bg="black",command=StartQuiz,highlightthickness=0,width=10,height=1)
start_btn.grid(row=1,column=1,padx=20,pady=20)

window.mainloop()