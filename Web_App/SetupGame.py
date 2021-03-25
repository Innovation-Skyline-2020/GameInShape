# Importing relevant libraries
from skimage.exposure import is_low_contrast
import cv2
import time
import numpy as np
import imutils

# Import all the functionalities from Switch_Control and Direct_Keys
from Web_App.Direct_Keys import *
from Web_App.Switch_Control import *


class StartSetup(object):
    def __init__(self):
        self.url = cv2.VideoCapture(0)

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):

        # For allowing web cam to open
        time.sleep(0.3)

        # Represents the Time given for the player to come to position to play game
        SetupTime = 5

        StartTime = time.time()

        # To Draw a rectangle/box around the frame with relevant text displayed
        while True:


            check,frame = GetFrame(self.url)
    
            # if we donot have sufficient light surrounding to user it will inform user
            if check==False :
        
                text = "For better Gaming Experience, make sure you have sufficient light in your environment!"
        
                color = (0, 0, 255)
        
                cv2.putText(frame, text, (10, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.8,color, 2)
            
            CurrentTime = (time.time() - StartTime)
            if CurrentTime > SetupTime:
                break

            text = " You still have " + \
                str(int(SetupTime - CurrentTime)+1) + " Seconds!"

            cv2.putText(frame, text, Coord_Text,
                        Font_Type, Font_Scale, Text_Color, 4)

            cv2.imshow("Get Ready for Setup !!", frame)
            cv2.waitKey(1)

        cv2.destroyAllWindows()

        cv2.putText(frame, 'Make a box around Face', (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # bounding box for face
        bbox = cv2.selectROI(frame, False)

        # It destroys all the windows we created.
        cv2.destroyAllWindows()
        self.url.release()

        NoOfSwitches = NoOfSwitchesDict[GameName]

        buttons = Buttons(bbox, NoOfSwitches, Train=True)

        BoundingBoxFace = buttons.BoundingBoxFace

        BoundingBoxSwitchList = buttons.BoundingBoxSwitchList

        return ([BoundingBoxFace, BoundingBoxSwitchList])
