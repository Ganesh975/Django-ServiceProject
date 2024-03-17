from django.core.mail import send_mail
import smtplib

def send_notification_email(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)




    

'''
    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.ehlo()
    server.starttls()
    server.login('missionimpossible4546@gmail.com', 'lemluekcftaaolcj')  
    server.sendmail('missionimpossible4546@gmail.com', 'ganeshyarrampati999@gmail.com', 'hello')  
    server.quit()'''
