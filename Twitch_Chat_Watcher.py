import socket
import time
import ctypes
import winsound
from pynput.keyboard import Key, Controller

# Generic function to hold a key for a certain amount of time doesn't work for games
def Hold_Key(Key, Time):
	TimeHeld = 0
	while TimeHeld < Time:
		keyboard.press(Key)
		time.sleep(.5)
		keyboard.release('w')
		TimeHeld += 1
	print("Finished Holding " + Key)

# Smash that like button doesn't work for games
def Press_Key(Key):
	print("Pressing " + Key)
	keyboard.press(Key)

# Direct input bull that I stole from the top Stack Overflow question
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# These functions work for games
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'howdyhightower'
channel = '#blue_shark9'

# Read token from config file
Config = open('Config.txt', 'r')
Line = Config.readline()
token = Line
print(Line)

# Connecting
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# The first response is always the same greeting.
response = sock.recv(2048).decode('utf-8')
print(response)
keyboard = Controller()

# We want to constantly listen
while True:
	response = sock.recv(2048).decode('utf-8')

	# Get chat username and clean it up
	ChatUsername = response.split("!",  1)
	Chatter = ChatUsername[0].replace(":","")
	#print(Chatter)

	# Clean up what they said
	try:
		ChatMessage = response.split(":", 1)[1].split(":", 1)
	except:
		print("Error")
	if len(ChatMessage) > 1:
		ParsedChatMessage = ChatMessage[1]
	# Strip newline characters
		ParsedChatMessage = ParsedChatMessage.replace("\r\n", "")
		print(ParsedChatMessage)

		if ParsedChatMessage == "W":
			PressKey(0x11)
			time.sleep(60)
			ReleaseKey(0x11)
		elif ParsedChatMessage == "A":
			PressKey(0x1E)
			time.sleep(1)
			ReleaseKey(0x1E)
		elif ParsedChatMessage == "S":
			PressKey(0x1F)
			time.sleep(1)
			ReleaseKey(0x1F)
		elif ParsedChatMessage == "D":
			PressKey(0x20)
			time.sleep(1)
			ReleaseKey(0x20)
		elif ParsedChatMessage == "Jump":
			PressKey(0x39)
			time.sleep(1)
			ReleaseKey(0x39)

		# This is how you send a message to chat
		#sock.send(bytearray('PRIVMSG ' + channel + ' :' + 'Hi ' + Chatter + '\r\n', 'utf-8'))
		# Beep when a message has been received	
		frequency = 1000
		duration = 1000
		winsound.Beep(frequency, duration)

# Done I guess
sock.close()

