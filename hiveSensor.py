
#This function activates the PIR sensor
def Sensor():
    import matplotlib.pyplot as plt; plt.rcdefaults()
    import numpy as np
    import matplotlib.pyplot as plt
    
    #used to print out time for each motion trip
    from datetime import datetime
    #used for PIR sensor
    import time
    import RPi.GPIO as GPIO
    #unsure what this line of code is for exactly
    import subprocess
    
    
    list1 = [0,0,0,0,0,0,0,0]
 
    
    #Use BCM GPIO reference
    # instead of Physical pin numbers
    GPIO.setmode(GPIO.BCM)
    #Define GPIO to use on Pi
    GPIO_PIR = 4

    print ("PIR Module Holding Time Test")

    # Set pin as input
    GPIO.setup(GPIO_PIR, GPIO.IN)
    current_state = 0
    previous_state = 0

    try:
        print("waiting for PIR to settle...")
        
        # Loop until PIR output is 0
        while GPIO.input(GPIO_PIR)==1:
            current_state = 0
        print("Ready")
        
        #setting date and time
        today = datetime.today()
        todaysDate = today.strftime("%m/%d/%y")
        todaysDate2 = today.strftime("%m.%d.%y")
        
        #setting label
        obArray = ['8AM<9AM','9AM<10AM','10AM<11AM','11AM<12PM','12PM<1PM', '1PM<2PM', '2PM<3PM', '3PM<4PM']
        y_pos = np.arange(len(obArray))
        
        #building graph
        plt.bar(y_pos, list1, align='center')
        plt.xticks(y_pos, obArray, rotation=45)
        plt.tick_params(axis='x', which='major', labelsize=8)
        plt.ylabel('Frequency')
        plt.xlabel('Time Frame')
        plt.title('The HIVE Foot Traffic ' + todaysDate)
        
        x = "Hive Foot Traffic Data " + str(todaysDate2)
        
        #marking data in office
        timeStampRecord = open('%s.csv' %x, "w")
        timeStampRecord.write("Date    ," +"Time  ,\n")
        #Loop until user quits with CTRL-C
        while True:
            #Read PIR state
            current_state = GPIO.input(GPIO_PIR) 
            if current_state ==1 and previous_state ==0:
                #PIR is triggered
                start_time = time.time()
                now = datetime.now()
                current_hour = now.strftime("%H")
                if int(current_hour) == 12:
                    list1[4] += 1
                elif int(current_hour) == 13:
                    list1[5] += 1
                elif int(current_hour) == 14:
                    list1[6] += 1
                elif int(current_hour) == 15:
                    list1[7] += 1
                elif int(current_hour) == 8:
                    list1[0] += 1
                elif int(current_hour) == 9:
                    list1[1] += 1
                elif int(current_hour) == 10:
                    list1[2] += 1
                elif int(current_hour) == 11:
                    list1[3] += 1
                #Record previous state
                previous_state = 1
                newList = np.divide(list1, 2)
                newList = np.array(newList, dtype=np.int16)
                plt.bar(y_pos, newList, align='center', color=['blueviolet','yellow'])
                current_time = now.strftime("%H:%M")
                timeStampRecord.write(todaysDate + " ," + current_time + "\n")
            elif current_state==0 and previous_state==1:
                #PUR has returned to ready state
                previous_state = 0




    except KeyboardInterrupt:
        print("Quit")
        plt.savefig('%s.png' %x)
        timeStampRecord.close()
        #Reset GPIO settings
        GPIO.cleanup()
       
#
#CALL FUNCTIONS HERE      
#


#Activates PIR sensor       
Sensor()