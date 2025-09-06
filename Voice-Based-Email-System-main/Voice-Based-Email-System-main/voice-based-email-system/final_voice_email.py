import smtplib
import speech_recognition as sr
from email.message import EmailMessage
import imaplib
import email
import pyttsx3

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

username = "kirubakaran30357@gmail.com"
password = "ljnp wcsu xtrp zbes"

# Fix pyttsx3 init
k2k = pyttsx3.init()


def cute_jerry(text):
    k2k.say(text)
    k2k.runAndWait()


def login(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    return mail


def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("programing is listening.......")
        audio = recognizer.listen(source)
    try:
        speech = recognizer.recognize_google(audio)
        print("You said: {}".format(speech))
        return speech
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def mic():
    listenser = sr.Recognizer()
    with sr.Microphone() as source:
        listenser.adjust_for_ambient_noise(source, duration=10)
        print("programing is listening.......")
        audio = listenser.listen(source)
        data = listenser.recognize_google(audio)
        print("You said", data)
        return data.lower()


email_list = {"python": "luvky2k007@gmail.com",
              "java": "subaharani2007@gmail.com",
              "dotnet": "kirubakaran30357@ksriet.com"}


def send_mail(receiver, subject, body):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("kirubakaran30357@gmail.com", "ljnp wcsu xtrp zbes")
    email = EmailMessage()
    email["From"] = "kirubakaran30357@gmail.com"
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(body)
    server.send_message(email)


def main_poc():
    cute_jerry("To whom do you want to send this mail?")
    name = mic()

    if name not in email_list:
        cute_jerry("Sorry, I don't know this contact.")
        return

    receiver = email_list[name]
    cute_jerry("Speak the subject of the email")
    subject = mic()
    cute_jerry("Speak the message of the email")
    body = mic()
    send_mail(receiver, subject, body)
    cute_jerry("Your email has been send!!")


def read_latest_email(mail):
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]

    typ, data = mail.fetch(latest_email_id, '(RFC822)')
    email_message = email.message_from_bytes(data[0][1])

    subject = email_message['Subject']
    sender = email_message['From']

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                break
    else:
        body = email_message.get_payload(decode=True).decode()

    print("Subject: ", subject)
    print("From: ", sender)
    print("Body: ", body)
    cute_jerry(subject)
    cute_jerry(sender)
    cute_jerry(body)



def little_tom():
    cute_jerry("Welcome to the Voice-Based Email System.")
    cute_jerry("What would you like to do?")
    print("1. Read latest email")
    print("2. Send email")
    choice = recognize_speech_from_mic()
    if choice == "read":
        print("Reading latest email...")
        mail = login(username, password)
        read_latest_email(mail)
    elif choice == "send":
        main_poc()
    else:
        print("Invalid choice. Please try again.")
        little_tom()


# Call the renamed function
little_tom()
