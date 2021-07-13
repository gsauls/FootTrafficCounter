import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
    
from datetime import datetime
import time

import RPi.GPIO as GPIO
import subprocess

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#function for sending email
def SendReport():
	
	#from and to emails
	fromaddr = "sender email"
	toaddr = "reciever email"
	
	#object from MIME library
	msg = MIMEMultipart()

	#setting msg variables
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Foot Traffic Data"
	
	#body of email
	body = "Test Run"

	#attaching body to msg var
	msg.attach(MIMEText(body, 'plain'))
	
	#getting date from time library
	today = datetime.today()
	todaysDate2 = today.strftime("%m.%d.%y")

	#name of file that is emailing 
	filename = "Hive Foot Traffic Data " + str(todaysDate2) + ".png"

	#setting the file path
	attachment = open("/home/pi/GitRepo/FootTrafficCounter/Hive Foot Traffic Data " + str(todaysDate2) + ".png", "rb")

	#adding the attachment
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(part)

	#server communication and log in
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "sender email password")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

#PIR Sensor detection function
def Sensor():

	#loop work	
	
	#array for counting each section of hours
	list = [0,0,0,0,0,0,0,0,0,0]
 
    
	#Use BCM GPIO reference
	#instead of Physical pin numbers
	GPIO.setmode(GPIO.BCM)

	#Define GPIO to use on Pi
	GPIO_PIR = 4

	print("PIR Module Holding Time Test")

	# Set pin as input
	GPIO.setup(GPIO_PIR, GPIO.IN)
	current_state = 0
	previous_state = 0

	
	firstRun = 0

	#while True:

		#try:

	print("waiting for PIR to settle...")
        
	# Loop until PIR output is 0
	while GPIO.input(GPIO_PIR)==1:
		current_state = 0
	print("Ready")
        
	while True:

		try:
			dailyReport  = 0

			#setting date and time
			today = datetime.today()
			todaysDate = today.strftime("%m/%d/%y")
			todaysDate2 = today.strftime("%m.%d.%y")
        
			#setting label
			obArray = ['7-8AM','8-9AM','9-10AM','10-11AM','11-12PM','12-1PM', '1-2PM', '2-3PM', '3-4PM', '4-5PM']
			y_pos = np.arange(len(obArray))
        
			#building graph
			plt.bar(y_pos, list, align='center')
			plt.xticks(y_pos, obArray, rotation=45)
			plt.tick_params(axis='x', which='major', labelsize=8)
			plt.ylabel('Frequency')
			plt.xlabel('Time Frame')
			plt.title('The HIVE Foot Traffic ' + todaysDate)
        
			x = "Hive Foot Traffic Data " + str(todaysDate2)
        
			#marking data in office
			timeStampRecord = open('%s.csv' %x, "w")
			timeStampRecord.write("Date    ," +"Time  ,\n")
			
			now = datetime.now()
			current_hour = now.strftime("%H")
			#print("current hour is" + current_hour)


			#Loop until user quits with CTRL-C
			while int(current_hour) > 6 and int(current_hour) < 18:

				#Read PIR state
				current_state = GPIO.input(GPIO_PIR)

				start_time = time.time()
				now = datetime.now()
				current_hour = now.strftime("%H")
 
				if current_state == 1 and previous_state ==0:

					#firstRun = 1
                
					#PIR is triggered
					print("Motion Detected")
					print("Current Hour: " + current_hour)

					#start_time = time.time()
					#now = datetime.now()
					#current_hour = now.strftime("%H")
	
					if int(current_hour) == 7:
						list[0] += 1
					elif int(current_hour) == 8:
						list[1] += 1
					elif int(current_hour) == 9:
						list[2] += 1
					elif int(current_hour) == 10:
						list[3] += 1
					elif int(current_hour) == 11:
						list[4] += 1
					elif int(current_hour) == 12:
						list[5] += 1
					elif int(current_hour) == 13:
						list[6] += 1
					elif int (current_hour) == 14:
						list[7] += 1
					elif int(current_hour) == 15:
						list[8] += 1
					elif int(current_hour) == 16:
						list[9] += 1

					#Record previous state
					previous_state = 1
					newList = np.divide(list, 2)
					newList = np.array(newList, dtype=np.int16)
					plt.bar(y_pos, newList, align='center', color=['black','red'])
					current_time = now.strftime("%H:%M")
					timeStampRecord.write(todaysDate + " ," + current_time + "\n")

					#saving
					plt.savefig('%s.png' %x)
					print("Saving..")

				elif current_state==0 and previous_state==1:
					#PIR has returned to ready state
					previous_state = 0
			
				#sending daily report at 4pm changing report flag so it only sends once
				elif int(current_hour) == 17 and dailyReport == 0:
					dailyReport = 1
					print("Sending Report")
					SendReport()

				#resetting report flag at 6am so it will trigger again the next day
				#elif int(current_hour) == 18:
					#dailyReport = 0
	
				# plt.savefig('%s.png' %x)
				# print("saving")


		except KeyboardInterrupt:
			print("Quitting and saving")
			plt.savefig('%s.png' %x)
			timeStampRecord.close()
			#Reset GPIO settings
			GPIO.cleanup()
       


#Activates PIR sensor       
Sensor()
