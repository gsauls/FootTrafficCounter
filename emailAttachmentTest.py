import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

smtp_server = 'smtp.gmail.com'
smtp_port = 587

gmail = 'piraspberry668@gmail.com'
password = 'Raspberry123!'

message = MIMEMultipart('mixed')
message['From'] = 'Contact <{sender}>'.format(sender = gmail)
message['To'] = 'gsauls3421@gmail.com'
message['CC'] = 'gsauls3421@gmail.com'
message['Subject'] = 'Hello'

msg_content = '<h4> Hi there, <br> This is a testing message.</h4>\n'
body = MIMEText(msg_content, 'html')
message.attach(body)

attachmentPath = "/home/pi/Desktop/Hive Foot Traffic Data 06.17.21.png"

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