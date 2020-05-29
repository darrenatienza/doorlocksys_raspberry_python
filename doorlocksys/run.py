#!/user/bin/env python
from libs.logic.DevActBLL import DevActBLL
from libs.logic.UserBLL import UserBLL
import time
import RPi.GPIO as GPIO
from libs.sensors.fingerprint import Fingerprint
from libs.sensors.I2C_LCD_driver import lcd
from libs.logic.DoorAccessLogBLL import DoorAccessLogBLL
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
relay_pin = 17


#create new instance of bll which access the data
deviceActionBll = DevActBLL()
fingerprint = Fingerprint()
mylcd = lcd()
userbll = UserBLL()
dooraccesslogBll = DoorAccessLogBLL()
def main():
    GPIO.setup(relay_pin, GPIO.OUT) # GPIO Assign mode
    while True:
        val = deviceActionBll.get_active_device_action()
        if(val.action_name == "Delete All Fingerprint"):
             ## Remove finger print
            print("Deleting Fingerprint!")
            mylcd.lcd_clear()
            ## Wait for the finger print
            mylcd.lcd_display_string('Deleting Finger',1)
            mylcd.lcd_display_string('print',2)
            count = fingerprint.getTemplateCount()
            print(count)
            for pos in range(count):
                lcdStr = ('print pos.{0}').format(pos)
                 ## avoid deleting finger print position 0, can cause  multiple re enroll of new finger print
                if(pos > 0):
                    user = userbll.get_by_fingerprintid(pos)
                    if(user.id == 0):
                        mylcd.lcd_display_string(lcdStr,2)
                        fingerprint.delete_finger(pos)
                        time.sleep(2)
                        deviceActionBll.setDeviceAction("Capture Finger Print")
                    else:
                        deviceActionBll.setDeviceAction("Open Door")
                 

        elif(val.action_name == "Open Door"):
            ## Opening of door
            ## Tries to verify finger print
            print("Verifying Fingerprint!")
            mylcd.lcd_clear()
            ## Wait for the finger print
            mylcd.lcd_display_string('Waiting to scan...',1)
            mylcd.lcd_display_string('Place your finger here',2)
            is_exists = fingerprint.verify_finger()
            ## If true, means that finger print has found
            if(is_exists == True):
               
                ##Todo: save to access logs
                user = userbll.get_by_fingerprintid(fingerprint.getPositionNumber())
                if(user.id > 0):
                     ## Found Finger Print
                    print("Fingerprint Found!")
                    mylcd.lcd_clear()
                    ## Wait for the finger print
                    mylcd.lcd_display_string('Fingerprint found!',1)
                    mylcd.lcd_display_string('Door open..',2)
                    # Save to database
                    dooraccesslogBll.add(user.id,"Door Open")
                    deviceActionBll.setDeviceAction("Close Door 10s")

                   
                else:
                    mylcd.lcd_clear()
                    ## Wait for the finger print
                    mylcd.lcd_display_string('No record',1)
                    mylcd.lcd_display_string('found...',2)
            else:
                mylcd.lcd_clear()
                ## Wait for the finger print
                mylcd.lcd_display_string('Invalid',1)
                mylcd.lcd_display_string('Fingerprint!',2)
        elif(val.action_name == "Force Open Door"):
            ## Supply signal to relay for doorlock activation
            GPIO.output(relay_pin, GPIO.HIGH) # ON
            ## Lock door after 10 seconds
            mylcd.lcd_clear()
            mylcd.lcd_display_string('Door will lock',1)
            mylcd.lcd_display_string('after 10 seconds',2)
            time.sleep(10)
            # Save to database
            #dooraccesslogBll.add(user.id,"Door close")
            deviceActionBll.setDeviceAction("Open Door")
            ## Supply signal to relay for doorlock deactivation
            GPIO.output(relay_pin, GPIO.LOW) # OFF
        elif(val.action_name == "Close Door 10s"):
            ## Supply signal to relay for doorlock activation
            GPIO.output(relay_pin, GPIO.HIGH) # ON
            ## Lock door after 10 seconds
            mylcd.lcd_clear()
            mylcd.lcd_display_string('Door will lock',1)
            mylcd.lcd_display_string('after 10 seconds',2)
            time.sleep(10)
            # Save to database
            #dooraccesslogBll.add(user.id,"Door close")
            deviceActionBll.setDeviceAction("Open Door")
            ## Supply signal to relay for doorlock deactivation
            GPIO.output(relay_pin, GPIO.LOW) # OFF
        elif(val.action_name == "Close Door"):
            ## Opening of door
            ## Tries to verify finger print
            print("Verifying Fingerprint!")
            mylcd.lcd_clear()
            ## Wait for the finger print
            mylcd.lcd_display_string('Waiting to scan...',1)
            mylcd.lcd_display_string('Place your finger here',2)
            is_exists = fingerprint.verify_finger()
            ## If false, means that finger print has found
            if(is_exists == True):
               
                ##Todo: save to access logs
                user = userbll.get_by_fingerprintid(fingerprint.getPositionNumber())
                if(user.id > 0):
                     ## Found Finger Print
                    print("Fingerprint Found!")
                    mylcd.lcd_clear()
                    ## Wait for the finger print
                    mylcd.lcd_display_string('Fingerprint found!',1)
                    mylcd.lcd_display_string('Door close..',2)
                    # Save to database
                    dooraccesslogBll.add(user.id,"Door close")
                    deviceActionBll.setDeviceAction("Open Door")

                     ## Supply signal to relay for doorlock deactivation
                    GPIO.output(relay_pin, GPIO.LOW) # OFF
                else:
                    mylcd.lcd_clear()
                    ## Wait for the finger print
                    mylcd.lcd_display_string('No record',1)
                    mylcd.lcd_display_string('found...',2)
            else:
                mylcd.lcd_clear()
                ## Wait for the finger print
                mylcd.lcd_display_string('Invalid',1)
                mylcd.lcd_display_string('Fingerprint!',2)
        elif(val.action_name == "Capture Finger Print"):
            ## Registering Finger print
            ## Tries to enroll new finger
            print("Enrolling Fingerprint!")
            mylcd.lcd_clear()
            ## Wait for the finger print
            mylcd.lcd_display_string('Waiting to scan...',1)
            mylcd.lcd_display_string('Place your finger here',2)
            ## 
            is_exists = fingerprint.verify_finger()
            if(is_exists == True):
                ## invalid finger print verification
                mylcd.lcd_clear()
                mylcd.lcd_display_string('Finger',1)
                mylcd.lcd_display_string('Already exists..',2)
            else:
                ## verify finger print again
                mylcd.lcd_clear()
                mylcd.lcd_display_string('Remove finger...')
                time.sleep(2)
                mylcd.lcd_clear()
                mylcd.lcd_display_string('place same',1)
                mylcd.lcd_display_string('finger again...',2)
                is_match = fingerprint.verify_finger_again()
                if(is_match == False):
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Finger do not",1)
                    mylcd.lcd_display_string("match!",2)
                else:
                    ## enroll finger print
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Enrolling Finger",1)
                    mylcd.lcd_display_string("print..",2)
                    result = fingerprint.enroll_finger()
                    fprintid = result[0]
                    if(fprintid > 0):
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string('Finger enrolled',1)
                        mylcd.lcd_display_string('successfully!',2)
                        ## save to database
                        userbll.edit(fprintid)
                        deviceActionBll.setDeviceAction("Open Door")
        else:
            ## enroll finger print
            mylcd.lcd_clear()
            mylcd.lcd_display_string("No actions",1)
            mylcd.lcd_display_string("allowed...",2)
            print("Action not allowed!")

        time.sleep(3)

def finger():
    
    pass   


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        mylcd.lcd_clear()
        GPIO.cleanup()