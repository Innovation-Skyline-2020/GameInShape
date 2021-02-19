# Import the required Libraries
import ctypes
# It provides C compatible data types, and allows calling functions in DLLs or shared libraries.

# Using a python builtin API to send Input
SendInput = ctypes.windll.user32.SendInput

# We define some global parameters so that its easier for us to tweak when required.
INITIAL_VALUE = 0
FINAL_VALUE = 1

# Each key on a PC keyboard has a Scan Code rather than an ASCII code associated with it.
# When a key is pressed it sends the Scan Code for the key that was pressed, to the Keyboard Interface Circuit on the Computers System Board.
# These Scan codes are only applicable to non-U.S. keyboard installations.

#  When a key(A_key) is pressed then corresponding Hexagonal value(0x1E) which is the Scan Code.
#  Here are the Scan Codes of A-Z & 4 Arrow Keys :

A_key = 0x1E
B_key = 0x30
C_key = 0x2E
D_key = 0x20
E_key = 0x12
F_key = 0x21
G_key = 0x22
H_key = 0x23
I_key = 0x17
J_key = 0x24
K_key = 0x25
L_key = 0x26
M_key = 0x32
N_key = 0x31
O_key = 0x18
P_key = 0x19
Q_key = 0x10
R_key = 0x13
S_key = 0x1F
T_key = 0x14
U_key = 0x16
V_key = 0x2F
W_key = 0x11
X_key = 0x2D
Y_key = 0x15
Z_key = 0x2C

key_0 = 0x01
key_1 = 0x02
key_2 = 0x03
key_3 = 0x04
key_4 = 0x05
key_5 = 0x06
key_6 = 0x07
key_7 = 0x08
key_8 = 0x09
key_9 = 0x0A

Up_arrow_key = 0x48
Left_arrow_key = 0x4B
Right_arrow_key = 0x4D
Down_arrow_key = 0x50

Shift_key = 0x36  # Right Shift Key
Space_key = 0x39
SemiColon_key = 0x27  # ;


class KeyBoardInput(ctypes.Structure):

    _fields_ = [
        # "qwe" is unsigned short int type variable
        ("qwe", ctypes.c_ushort),

        # "werty" is unsigned short int type variable
        ("werty", ctypes.c_ushort),

        # "tyui" is unsigned long int type variable
        ("tyui", ctypes.c_ulong),

        # "check" is unsigned long int type variable
        ("check", ctypes.c_ulong),

        # "diot" is pointer of unsigned long int variable
        ("diot", ctypes.POINTER(ctypes.c_ulong))]


class HardwareInput(ctypes.Structure):

    _fields_ = [
        # "asd" is unsigned long int type variable
        ("asd", ctypes.c_ulong),

        # "dfghj" is signed short int type variable
        ("dfghj", ctypes.c_short),

        # "jkdg" is unsigned short int type variable
        ("jkdg", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):

    _fields_ = [
        # 'x_axis' is  long int data type variable
        ("x_axis", ctypes.c_long),

        # "y_axis" is long int data type variable
        ("y_axis", ctypes.c_long),

        # "mouseData" is unsigned long int data type variable
        ("mouseData", ctypes.c_ulong),

        # "dwFlags" is unsigned long int data type variable
        ("dwFlags", ctypes.c_ulong),

        # "time" is unsigned long int data type variable
        ("time", ctypes.c_ulong),

        # "dioter" is unsigned long pointer variable
        ("dioter", ctypes.POINTER(ctypes.c_ulong))]


# Creating a Union of all the above three Structures
class InputTakingUnion(ctypes.Union):

    _fields_ = [("KBI", KeyBoardInput),
                ("MI", MouseInput),
                ("HI", HardwareInput)]


# Creating a new structure which has both above union and unsigned long int data type
class InputTaking(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("union", InputTakingUnion)]


def PressTheKey(HexagonalKeyCode):

    value = ctypes.c_ulong(INITIAL_VALUE)
    Input = InputTakingUnion()

    Input.KBI = KeyBoardInput(
        INITIAL_VALUE, HexagonalKeyCode, 0x0008, INITIAL_VALUE, ctypes.pointer(value))

    send = InputTaking(ctypes.c_ulong(FINAL_VALUE), Input)

    # Using the API to Press the Key based on the Provided Hexagonal Key Code.
    ctypes.windll.user32.SendInput(
        FINAL_VALUE, ctypes.pointer(send), ctypes.sizeof(send))


def ReleaseTheKey(HexagonalKeyCode):

    value = ctypes.c_ulong(INITIAL_VALUE)
    Input = InputTakingUnion()

    # "|" this is Bitwise OR operation
    Input.KBI = KeyBoardInput(INITIAL_VALUE, HexagonalKeyCode, 0x0008 | 0x0002,
                              INITIAL_VALUE, ctypes.pointer(value))

    send = InputTaking(ctypes.c_ulong(FINAL_VALUE), Input)

    # Using the API to  Release the Pressed Key based on the Provided Hexagonal Key Code.
    ctypes.windll.user32.SendInput(
        FINAL_VALUE, ctypes.pointer(send), ctypes.sizeof(send))


# Dictionary to store Number of Bounding Boxes required in respective game.
NoOfSwitchesDict = {'Mortal_Kombat': 5, 'Madalin_Stunt_Cars_2': 6}

SwitchNames = {'Mortal_Kombat': ["Front Punch",
                                 "Back Punch", "Front Kick", "Back Kick", "Throw, Block, Interact"],

               'Madalin_Stunt_Cars_2': ["Move Up", "Move Down", "Move Left", "Move Right", "Accelerate", "Hand Brake"]}


Value2KeyMap_Games = {'Mortal_Kombat': {0: J_key,  # Front Punch
                                        1: I_key,  # Back Punch
                                        2: K_key,  # Front Kick
                                        3: L_key,  # Back Kick

                                        4: Space_key,       # Throw    -> Palm
                                        5: O_key,           # Block    -> Fist
                                        6: SemiColon_key,   # Interact -> Swing
                                        },

                      'Madalin_Stunt_Cars_2': {0: W_key,  # Move Up
                                               1: S_key,  # Move Down
                                               2: A_key,  # Move Left
                                               3: D_key,  # Move Right

                                               4: Shift_key,       # Accelerate
                                               5: Space_key,       # Hand Brake

                                               }, }

# This should come from the Web Page when Button is pressed.
GameName = 'Madalin_Stunt_Cars_2'

# Some Utility Functions


def list_to_string(l):
    s = ""
    for i in l:
        s += (str(i) + ",")
    return s


def string_to_list(s):
    s = s[:-1]
    a = [int(x) for x in s.split(",")]
    return a


def listoflists_to_string(l):
    s = ""
    for i in l:
        s += (list_to_string(i) + "|")
    return s


def string_to_listoflists(s):
    Final = []

    s = s[:-1]
    a = [x for x in s.split("|")]

    for each in a:
        Final.append(string_to_list(each))

    return Final


""" 
Note: The references used are :-

1) http://www.philipstorr.id.au/pcbook/book3/scancode.htm
2) https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
"""
