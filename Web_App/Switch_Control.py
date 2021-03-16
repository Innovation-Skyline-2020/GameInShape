# Import the required Libraries
from Web_App.models import BoundingBoxes

# from GameSetup import BoundingBoxFace, BoundingBoxSwitchList
from skimage.exposure import is_low_contrast
import cv2
import imutils
import time
import numpy as np

from Web_App.Direct_Keys import *
###############################################################################
bbox = BoundingBoxes.objects.last()
BoundingBoxFace = string_to_list(bbox.Face)
BoundingBoxSwitchList = string_to_listoflists(bbox.Switches)

# Utility Function that Calculates and returns the Center of rectangle.


def FindCenter(rectangle_box):

    x, y, w, h = rectangle_box

    # (x, y) -> Top Left Coordinates of the Box
    # w -> Width of the Box
    # h -> Height of the Box

    centre_x = int(x+w/2)
    centre_y = int(y+h/2)

    return (centre_x, centre_y)

# Utility function that draw rectangle in frame


def DrawBox(rectangle_box, frame):

    # Pixel values of Color in (B,G,R) format
    Color = (0, 255, 255)

    Line_thickness = 1
    x, y, w, h = rectangle_box
    Top_Left_Coordinates = (x, y)
    Bottom_Right_Coordinates = (x+w, y+h)

    # It draws rectangle on the frame at provided coordinates
    cv2.rectangle(frame, Top_Left_Coordinates,
                  Bottom_Right_Coordinates, Color, Line_thickness)


# Utility Function that returns frames
def GetFrame(capture):

    _, frame = capture.read()

    # Flip a 2D array. "1" means flipping around y-axis
    frame = cv2.flip(frame, 1)

    frame = cv2.resize(frame, dsize=(900, 700))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    check = True
    # Here we try to check either surrounding to user have not low intensity of light
    # if light present surrounding to user is less than 30% we not take picture of it
    if is_low_contrast(gray, fraction_threshold=0.30):
        
        check=False
    
    return check,frame

###############################################################################
# We define some global parameters so that its easier for us to tweak when required.

# Bounding box for Face of the User and
# List of Bounding boxes of Switches

# Mortal_Kombat

# BoundingBoxFace = (252, 197, 222, 344)

# BoundingBoxSwitchList = [(727, 372, 68, 72), (43, 340, 54, 65),
#                          (682, 507, 126, 94), (34, 507, 158, 87), (679, 104, 200, 200)]

# Madalin_Stunt_Cars_2


# BoundingBoxFace = (341, 207, 149, 271)

# BoundingBoxSwitchList = [(842, 65, 55, 94), (697, 344, 54, 72), (
#     24, 280, 43, 51), (222, 336, 27, 58), (209, 601, 61, 77), (591, 626, 46, 54)]


# Center of the Face
# FaceCenter = FindCenter(BoundingBoxFace)

# We will activate the Switch, If Noise Level caused due to change in the pixels exceeds this Threshold value
Threshold = 400

# It is the coordinates of the bottom-left corner of the text string in the image
Coord_Text = (50, 50)

# It is the Type(style) of font being used
Font_Type = cv2.FONT_HERSHEY_SIMPLEX

# Font scale factor that is multiplied by the font-specific base size
Font_Scale = 1.25

# It is font color in BGR(Blue,Green,Red) format
Text_Color = (255, 0, 255)

# It is the thickness of the line in px
Thickness = 2


# List of Actions for which switches(except the last one) are being mapped into.
CorrespondGameKeyName = SwitchNames[GameName]

# Used for writing corresponding CorrespondGameKeyName on screen
Count = 0
###############################################################################


class VirtualSwitch():

    def __init__(self, BoundingBoxFace, BoundingBoxSwitch=None, Threshold=100, SwitchingDelay=0.0001):

        self.Threshold = Threshold

        # For Avoiding the Continuous Pressing of Switch
        self.SwitchingDelay = SwitchingDelay

        self.LastSwitchTime = time.time()

        # Using the most efficient and accurate BackgroundSubstracter

        # It removes the Background noise and leaves only movable objects in a grayscale images
        self.backgroundobject = cv2.bgsegm.createBackgroundSubtractorMOG()

        # Creating kernal matrix (4X4) which is used for morphological operations that is for a broad set of image processing operations that process images based on shapes.
        self.kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (4, 4))

        if BoundingBoxSwitch:
            self.BoundingBoxSwitch = BoundingBoxSwitch

        else:
            self.Setup(BoundingBoxFace)

    def Setup(self, BoundingBoxFace):
        """
            This sets up the Boundary Box for the Switch based on user Response
        """

        # Timer for capturing base image, get reading in posture
        Setup_Time = 5

        # Keeping track of Time
        start_time = time.time()

        # Device index is just the number to specify which camera
        # Usually We have only one camera
        Device_index = 0

        # To get a video capture object for the camera.
        capture = cv2.VideoCapture(Device_index)

        while True:

            _, frame = capture.read()

            # Flip a 2D array. "1" means flipping around y-axis
            frame = cv2.flip(frame, 1)

            frame = cv2.resize(frame, dsize=(900, 700))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            # Here we try to check either surrounding to user have not low intensity of light
            # if light present surrounding to user is less than 30% we not take picture of it
            if is_low_contrast(gray, fraction_threshold=0.30):
                    
                text = "Low contrast: Yes Please visit where you have atleast 30 % light "
                
                color = (0, 0, 255)
                
                cv2.putText(frame, text, (10, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.8,color, 2) 


            current_time = (time.time() - start_time)

            if current_time > Setup_Time:
                break

            Text = " You still have " + \
                str(int(Setup_Time - current_time)+1) + " Seconds!"

            cv2.putText(frame, Text,
                        Coord_Text, Font_Type, Font_Scale, Text_Color, Thickness)

            DrawBox(BoundingBoxFace, frame)

            cv2.imshow("Get Ready for Setup !!", frame)

            cv2.waitKey(1)

        # It simply destroys all the windows we created.
        cv2.destroyAllWindows()

        cv2.putText(frame, 'Select region for {} Switch'.format(CorrespondGameKeyName[Count-1]), Coord_Text,
                    Font_Type, Font_Scale, Text_Color, Thickness)

        # crosshair of selection rectangle will be shown.
        self.BoundingBoxSwitch = cv2.selectROI(frame, showCrosshair=True)

        #  Use `space` or `enter` to finish selection, use key `c` to cancel selection.
        cv2.destroyAllWindows()

    def isActivated(self, frame):
        """
            This returns `True` if Switch is pressed that is it is activated.
        """

        # Checking if Bounding Box of the Switch goes outside the Frame
        try:

            # Picking up the switch region from the Frame
            x, y, w, h = self.BoundingBoxSwitch
            Switch_Region = frame[y:y+h, x:x+w]

            # Applying the Background Subtractor on this region of Switch
            Switch_Region_after_BGS = self.backgroundobject.apply(
                Switch_Region)

            # Morphological transformations are some simple operations based on the image shape.

            # We are performing Erosion followed by dilation
            # Dilation -> Adding imporatant imformation which lost during BackgroundSubstracter process
            # Erosion -> Remove unnessary noise which may possible add during dilation

            Switch_Region_Final = cv2.morphologyEx(
                Switch_Region_after_BGS, cv2.MORPH_OPEN, self.kernel, iterations=2)

        except:
            return False

        else:

            # Checking number of pixels changed by finding all the pixels that have value of 255
            # 255 pixel value represents complete White.
            switch_thresh = np.sum(Switch_Region_Final == 255)

            Text = "Number of Pixels changed : " + str(switch_thresh)

            cv2.putText(frame, Text,
                        Coord_Text, Font_Type, Font_Scale, Text_Color, Thickness)

            # This shows our Region of Interest which is acting as Virtual Switch
            DrawBox(self.BoundingBoxSwitch, frame)

            if (time.time() - self.LastSwitchTime) < self.SwitchingDelay:
                DrawBox(self.BoundingBoxSwitch, frame)

            # Checking whether Switch is activated or not
            if (switch_thresh > Threshold) and ((time.time() - self.LastSwitchTime) > self.SwitchingDelay):

                DrawBox(self.BoundingBoxSwitch, frame)

                # Since Switch is activated, We Update the Last Time Switch Activation time.
                self.LastSwitchTime = time.time()

                return True

            return False


class Buttons:

    """
    For storing Switch objects and for deciding which Switch is to be pressed based on current frame.
    """

    def __init__(self, BoundingBoxFace, NumberofSwitches=0, Train=False):

        self.Train = Train

        if Train:
            self.NumberofSwitches = NumberofSwitches
            self.BoundingBoxFace = BoundingBoxFace
            self.FaceCenter = FindCenter(self.BoundingBoxFace)

            # To store Bounding Boxes of all the Switches
            self.BoundingBoxSwitchList = []

        else:
            self.NumberofSwitches = NumberofSwitches
            self.BoundingBoxFace = BoundingBoxFace

            self.FaceCenter = FindCenter(self.BoundingBoxFace)

            self.BoundingBoxSwitchList = BoundingBoxSwitchList

        # Calling the Function to setup the Bounding Boxes for Switches
        self.SetupSwitchBoundingBox()

        # Calling the Actions object
        self.action = Actions(self.FaceCenter, 5)

    # For Setup of Bounding Boxes for the Switches which are our regions of interest to provide action

    def SetupSwitchBoundingBox(self):

        # To store all the switch objects
        self.Switches = []

        # To store Bounding Boxes of all the Switches wrt to the Center of Bounding Box of the User's face.
        self.BoundingBoxWrtCenterList = []

        # Creating Bounding Boxes using our Virtual Switch Class.
        for i in range(self.NumberofSwitches):

            if self.Train:
                global Count
                Count = Count+1
                Switch_i = VirtualSwitch(self.BoundingBoxFace)

                self.BoundingBoxSwitchList.append(Switch_i.BoundingBoxSwitch)

            else:

                BBoxSwitch = self.BoundingBoxSwitchList[i]
                Switch_i = VirtualSwitch(self.BoundingBoxFace, BBoxSwitch)

            self.Switches.append(Switch_i)

            # Evaluating the Position of Bounding Boxes Position wrt Center of Bounding Box of the User's face.
            self.BoundingBoxWrtCenterList.append(self.BoundingBoxWrtCenter(
                Switch_i.BoundingBoxSwitch))

        if self.Train:
            # Save this Printed Data For Later Use
            print(
                f'BoundingBoxFace = {self.BoundingBoxFace} \nBoundingBoxSwitches = {self.BoundingBoxSwitchList}')

    # Finds the relative position of the Bounding Box with respect to Center of User's Face.

    def BoundingBoxWrtCenter(self, BoundingBox):
        x_Center, y_Center = self.FaceCenter
        x, y, w, h = BoundingBox
        X, Y = x - x_Center, y - y_Center
        New_Position = (X, Y, w, h)
        return New_Position

    # Updates the Bounding Box to the new position with respect to Center of User's Face.
    def BoundingBoxUpdate(self, BoundingBox):
        x_Center, y_Center = self.FaceCenter
        x, y, w, h = BoundingBox
        X, Y = x + x_Center, y + y_Center
        New_Position = (X, Y, w, h)
        return New_Position

    # Presses the Buttons when Switches are activated.
    def run(self, frame, PresentCenter):

        self.PresentCenter = PresentCenter

        for each_switch in range(self.NumberofSwitches):

            switch, bbox = self.Switches[each_switch], self.BoundingBoxWrtCenterList[each_switch]

            switch.bbox = self.BoundingBoxUpdate(bbox)

            pressed = switch.isActivated(frame)

            if pressed and (each_switch != self.NumberofSwitches-1):
                self.action.PressValue(each_switch)

            if pressed and (each_switch == self.NumberofSwitches-1):

                if (GameName == 'Mortal_Kombat'):

                    from GesturePredictor import getPredictedClass

                    pred = getPredictedClass()

                    if pred[0] == 0:    # Swing
                        self.action.PressValue(6)
                    if pred[0] == 1:    # Palm
                        self.action.PressValue(4)
                    if pred[0] == 2:    # Fist
                        self.action.PressValue(5)

                if (GameName == 'Madalin_Stunt_Cars_2'):
                    self.action.PressValue(each_switch)

        #this activate when user do some jumping,or forward or backward motion            
        if (GameName == 'Mortal_Kombat'):
            self.action.MovementAction(PresentCenter)


class Actions():

    """ Used for mapping the Virtual Switches with respective keys for Actions in the games.
    """

    def __init__(self, FaceCenter, ActionThreshold):

        self.FaceCenter = FaceCenter
        self.ActionThreshold = ActionThreshold

        self.Previous = FaceCenter
        self.Middle = FaceCenter

        # Key for Up or Down movement of the User.
        self.VerticalKey = None

        # Key for Left or Right movement of the User.
        self.HorizontalKey = None

        # Reference line which is horizontal & passing through face. (Y Coordinate)
        self.ReferenceLine = FaceCenter[1]

        # To jump Up or Down.
        self.VerticalThreshold = 45

        # To move towards Left or Right.
        self.HorizontalThreshold = 20

       # Mapping the Switch index value to a corresponding Key to perform Action in the game.

        self.Value2KeyMap = Value2KeyMap_Games[GameName]

    def PressValue(self, value):

        if self.HorizontalKey != None:
            return

        key = self.Value2Key(value)
        self.PressAndReleaseTheKey(key)

    def Value2Key(self, value):

        key = self.Value2KeyMap[value]
        return key

    def PressAndReleaseTheKey(self, key, ContDelay=0.00001, DiscontDelay=0.00009, isContinued=False):

        # First, We Press the Key
        PressTheKey(key)

        if isContinued:
            # There is no Delay
            pass

        else:
            # There is some delay between Press and Release
            time.sleep(DiscontDelay)
            ReleaseTheKey(key)

        # Setting the delay for continous press
        time.sleep(ContDelay)

    # It monitors the User's Movement action
    def MovementAction(self, position):

        self.Current = position

        ChangeInX = self.Current[0] - self.Previous[0]
        ChangeInY = self.Current[1] - self.ReferenceLine

        if abs(self.Current[0] - self.Middle[0]) > self.HorizontalThreshold:

            index = 1
            if ChangeInX > 0:
                index = 2

            for j in range(index):
                self.HorizontalAction(ChangeInX)

        if np.absolute(ChangeInY) > self.VerticalThreshold:

            self.VerticalAction(ChangeInY)

        self.Previous = position

    # For monitoring User's Horizontal Action
    def HorizontalAction(self, Delta):

        if np.absolute(Delta) < self.ActionThreshold:

            self.Middle = self.Current

            if self.HorizontalKey != None:

                ReleaseTheKey(self.HorizontalKey)

                self.HorizontalKey = None
            return

        # Move to the Left
        if Delta < 0:
            self.HorizontalKey = A_key

        # Move to the Right
        else:
            self.HorizontalKey = D_key

        self.PressAndReleaseTheKey(self.HorizontalKey, True)

    #  For monitoring User's Vertical motion Action
    def VerticalAction(self, Delta):

        if (Delta < 75) and (self.VerticalKey == S_key):

            ReleaseTheKey(self.VerticalKey)

            self.VerticalKey = None
            
        if (Delta >-45) and (self.VerticalKey == W_key):

            ReleaseTheKey(self.VerticalKey)

            self.VerticalKey = None
                 

        isContinued = False

        # Monitering Jump
        if Delta < -45:
            self.VerticalKey = W_key

        # Monitering Duck
        elif Delta > 75:
            self.VerticalKey = S_key
            isContinued = True

        else:
            return

        self.PressAndReleaseTheKey(self.VerticalKey, isContinued)


Count = 0
