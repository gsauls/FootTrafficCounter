import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

smtp_server = 'smtp.gmail.com'
smtp_port = 587

#fill in custom info here
gmail = 'sender email'
password = 'sender password'

message = MIMEMultipart('mixed')
message['From'] = 'Contact <{sender}>'.format(sender = gmail)

#fill in custom info here
message['To'] = 'reciever email'
message['CC'] = 'cc reciever email'
message['Subject'] = 'Hello'
msg_content = '<h4> Hi there, <br> This is a testing message.</h4>\n'

body = MIMEText(msg_content, 'html')
message.attach(body)

#fill in file attachment path here starting at /home
attachmentPath = "/home/pi..."

try:
    with open(attachmentPath, "rb") as attachment:
        p = MIMEApplication(attachment.read(), _subtype="pdf")
        p.add_header('Content-Disposition',"attachment; filename= %s" % attachmentPath.split("\\")[-1])
        message.attach(p)
except Exception as e:
    print(str(e))
    
    
context = ssl.create_default_context()

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(gmail, password)
    server.sendmail(gmail, " ", " " )
    server.quit()
    
print("email sent")
