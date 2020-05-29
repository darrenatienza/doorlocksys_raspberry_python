from pyfingerprint.pyfingerprint import PyFingerprint
import lcd
import time
class Fingerprint:


    def __init__(self):
        self.mylcd = lcd.lcd()
        self.pos = 0
        try:
            self.f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            
            if (self.f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)


    def verify_finger(self):
        try:
            ## Wait that finger is read
            while (self.f.readImage() == False ):
                    pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            self.f.convertImage(0x01)
            ## Checks if finger is already enrolled
            result = self.f.searchTemplate()
            positionNumber = result[0]
            ## Check if finger print already exists
            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                self.pos = positionNumber                
                return True
            ## Return True if verfication pass
            return False, 0
    
        except:
            pass
    def getPositionNumber(self):
        return self.pos
        
    def verify_finger_again(self):
        try:
             ## Wait that finger is read again
            while ( self.f.readImage() == False ):
                pass
            
            ## Converts read image to characteristics and stores it in charbuffer 2
            self.f.convertImage(0x02)
    
            ## Compares the charbuffers
            if ( self.f.compareCharacteristics() == 0 ):
                print('Finger do not match')
                return False
                ## raise Exception('Fingers do not match')

            ## Return True if verfication pass
            return True
                
        except:
            pass
    def getTemplateCount(self):
        return self.f.getTemplateCount()

    def enroll_finger(self):       
        try:
            ## Creates a template
            self.f.createTemplate()
            ## Saves template at new position number
    
            positionNumber = self.f.storeTemplate()
            self.f.loadTemplate(positionNumber, 0x01)
            char_store = str (self.f.downloadCharacteristics(0x01))
            char_store1= char_store.translate(None, ',[]')
            return positionNumber, char_store1

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

    def delete_finger(self, fingerprintid):
        try:
            positionNumber = int(fingerprintid)
            if(self.f.deleteTemplate(positionNumber) == True):
                print('Template deleted!')
        except:
            pass