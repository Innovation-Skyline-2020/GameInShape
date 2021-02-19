# Importing relevnt libraries
import cv2
import time
import numpy as np

# Import all the functionalities from Switch_Control and Direct_Keys
from Web_App.Direct_Keys import *
from Web_App.Switch_Control import *
from Web_App.GesturePredictor import *
from Web_App.models import BoundingBoxes

########################################################################################


def Start():

    # Getting the Recently stored Bounding Boxes from the Database
    bbox = BoundingBoxes.objects.last()

    # Conversion to required format.
    BoundingBoxFace = string_to_list(bbox.Face)
    BoundingBoxSwitchList = string_to_listoflists(bbox.Switches)

    # here we take number of switches respected to particular game
    NoOfSwitches = NoOfSwitchesDict[GameName]

    # Calling the Buttons class
    button = Buttons(BoundingBoxFace, NoOfSwitches, Train=False)

    # Here we use builtin CSRT traker of opencv for tracking user's face.
    tracker = cv2.TrackerCSRT_create()

    # Device index is just the number to specify which camera
    # Usually We have only one camera
    Device_index = 0

    # To get a video capture object for the camera.
    capture = cv2.VideoCapture(Device_index)

    # Represents the Time given for the player to come to position to play game
    SetupTime = 5

    StartTime = time.time()

    # To Draw a rectangle/box around the frame with relevant text displayed
    while True:

        frame = GetFrame(capture)

        CurrentTime = (time.time() - StartTime)
        if CurrentTime > SetupTime:
            break

        text = " You have " + \
            str(int(SetupTime - CurrentTime)+1) + " Seconds !"

        cv2.putText(frame, text, Coord_Text,
                    Font_Type, Font_Scale, Text_Color, 4)

        DrawBox(BoundingBoxFace, frame)

        cv2.imshow("Get Ready for Playing the Game !!", frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()

    # Initialising the Tracker for the User's Face
    tracker.init(frame, BoundingBoxFace)

    ####################################
    # Quantitites that help in Hand Gesture Recognition

    x, y, w, h = (679, 104, 200, 200)
    (left, top) = (x+w, y)
    (right, bottom) = (x, y+h)
    aWeight = 0.5

    # initialize num of frames
    num_frames = 0
    start_recording = False
    ##########################################

    # Once the Setup time finishes, the user actions will be recorded, and will be mapped to key in game.
    while True:

        frame = GetFrame(capture)

        # It will update frame with respect to traker positon
        Success, BoundingBoxRectangleFace = tracker.update(frame)

        # Updating BoundingBoxFace on when Success is True
        if Success:
            BoundingBoxFace = [int(x) for x in BoundingBoxRectangleFace]

        DrawBox(BoundingBoxFace, frame)

        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # draw the segmented region and display the frame
                cv2.drawContours(
                    clone, [segmented + (right, top)], -1, (0, 0, 255))
                if start_recording:
                    cv2.imwrite('Temp.png', thresholded)
                    resizeImage('Temp.png')

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

        # increment the number of frames
        num_frames += 1

        # Using the previously defined run function
        button.run(frame, FindCenter(BoundingBoxFace))

        # Original video frames
        cv2.imshow("Tracking", frame)
        # cv2.resizeWindow("Tracking", 1000, 600)

        # If the user presses "q", then stop looping
        if cv2.waitKey(1) == ord("q"):
            break

        start_recording = True

    # It shut downs the webcam
    capture.release()

    # It destroys all the windows we created.
    cv2.destroyAllWindows()
