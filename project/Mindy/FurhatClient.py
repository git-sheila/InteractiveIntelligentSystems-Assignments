from furhat_remote_api import FurhatRemoteAPI
class FurhatClient:
    def __init__(self):
        """Constructor: Initializes FurhatClient"""
        self.furhat = FurhatRemoteAPI("localhost")
        print("Initializing FurhatClient...")

    def __del__(self):
        """Destructor: Cleans up FurhatClient"""
        print("Destroying FurhatClient...")

    def init(self):
        """Initializes any required components"""
        self.furhat.set_voice(name='Anna')
        print("FurhatClient initialized.")

    def speak(self, message: str):
        """Simulates speaking a message."""
        self.furhat.set_led(red=255, green=191, blue=128) #ombre yellow
        self.furhat.say(text=message, blocking=True)
        print(f"Furhat speaks: {message}")
        self.furhat.set_led(red=0, green=0, blue=0) #black or no light

    def listen(self) -> str:
        """Simulates listening and returns a sample input."""
        self.furhat.set_led(red=144, green=238, blue=144) #gentle green
        response = self.furhat.listen()
        message = getattr(response, 'message', '') 
        if(message):
            print(f"Furhat listened: {message}")
        self.furhat.set_led(red=0, green=0, blue=0)
        return message

    def getResponse(self, query: str) -> str:
        """Single function to speak and listen"""
        self.furhat.say(text=query, blocking=True)
        response = self.furhat.listen()
        message = getattr(response, 'message', '') 
        print(f"Furhat response: {message}")
        return message
    
    def attendLocation(self, loc: str):
        self.furhat.attend(location=loc)
    
    def gesture_inhale(self, inhale_time: int):
        print("Inhaling for " + str(inhale_time) + " seconds.")
        self.furhat.set_led(red=102, green=205, blue=170) #Soothing Aqua
        self.furhat.gesture(body={
            "frames": [
                {
                    "time": [0.25], #start of breathing in=0.25
                    "params": {
                        "NECK_TILT": -1.0,       # Final neck lift for exaggerated breath
                    }
                },            {
                    "time": [inhale_time/8], #inhale_time/8=0.5
                    "params": {
                        "NECK_TILT": -7.0,       # Final neck lift for exaggerated breath
                    }
                },
                {
                    "time": [inhale_time/4], #inhale_time/4=1.0
                    "params": {
                        "NECK_TILT": -15.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_UP_LEFT": 0.4,      # Raised brows to indicate tension
                        "BROW_UP_RIGHT": 0.4,
                        "EYE_SQUINT_LEFT": 0.5,  # Eye squint for focus
                        "EYE_SQUINT_RIGHT": 0.5,
                        #"PHONE_AAH": 0.4,        # Slightly open mouth for inhale
                        "SMILE_CLOSED": 1      # Adjust lips subtly
                        #"SMILE_OPEN": 0.0
                    }
                },
                {
                    "time": [inhale_time/2], #middle of breathing in   #inhale_time/2=2.0
                    "params": {
                        "NECK_TILT": -15.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_UP_LEFT": 0.4,      # Raised brows to indicate tension
                        "BROW_UP_RIGHT": 0.4,
                        "EYE_SQUINT_LEFT": 0.5,  # Eye squint for focus
                        "EYE_SQUINT_RIGHT": 0.5,
                        #"PHONE_AAH": 0.4,        # Slightly open mouth for inhale
                        "SMILE_CLOSED": 1      # Adjust lips subtly
                        #"SMILE_OPEN": 0.0
                    }
                },
                {
                    "time": [inhale_time - 0.25], #End of breathing in and start of bolding breath #inhale_time - 0.25=3.75
                    "params": {
                        "NECK_TILT": -3.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_DOWN_LEFT": 0.4,   # Shift brows to a downward focus
                        "BROW_DOWN_RIGHT": 0.4,
                        #"PHONE_BIGAAH": 0.6,     # Stronger mouth opening for emphasis
                        "EYE_SQUINT_LEFT": 0.7,  # Increased squint for intensity
                        "EYE_SQUINT_RIGHT": 0.7,
                        "SMILE_CLOSED": 1.0,        # Slightly open smile for realism
                        #"SMILE_OPEN": 0.0,
                        "BROW_IN_LEFT": 0.2,       # Inward brow motion for more tension
                        "BROW_IN_RIGHT": 0.2,      # Inward brow motion on the other side
                        #"PHONE_EE": 0.1 
                    }
                },
                {
                    "time": [inhale_time],  #inhale_time=4.0
                    "params": {
                        "NECK_TILT": -1.0,       # Final neck lift for exaggerated breath
                        "SMILE_CLOSED": 1.0        # Slightly open smile for realism                    
                    }
                },
                {
                    "time": [inhale_time + 0.25], #inhale_time + 0.25=4.25
                    "params": {
                        "reset": False            # Return to neutral
                    }
                }
            ],
            "class": "furhatos.gestures.Gesture"
        },
    blocking=True)


    def gesture_hold(self, hold_time: int):
        print("Hold breath for " + str(hold_time) + " seconds.")
        self.furhat.set_led(red=221, green=160, blue=221) #Soft lavender
        self.furhat.gesture(body={
            "frames": [
                            {
                    "time": [0.0], #Start of bolding breath
                    "params": {
                        "NECK_TILT": -1.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_DOWN_LEFT": 0.4,   # Shift brows to a downward focus
                        "BROW_DOWN_RIGHT": 0.4,
                        #"PHONE_BIGAAH": 0.6,     # Stronger mouth opening for emphasis
                        "EYE_SQUINT_LEFT": 1,  # Increased squint for intensity
                        "EYE_SQUINT_RIGHT": 1,
                        "SMILE_CLOSED": 1.0,        # Slightly open smile for realism
                        #"SMILE_OPEN": 0.0,
                        "BROW_IN_LEFT": 0.4,       # Inward brow motion for more tension
                        "BROW_IN_RIGHT": 0.4,      # Inward brow motion on the other side
                        #"PHONE_EE": 0.1 
                    }
                },
                {
                    "time": [hold_time/4], #hold_time/4=1.0
                    "params": {
                        "NECK_TILT": -3.0
                    }
                },
                {
                    "time": [hold_time/2], #hold_time/2=2.0
                    "params": {
                        "NECK_TILT": -4.0
                    }
                },
                {
                    "time": [hold_time*3/4], #hold_time*3/4=3.0
                    "params": {
                        "NECK_TILT": -3.0
                    }
                },
                {
                    "time": [hold_time], #End of bolding breath #hold_time=4.0
                    "params": {
                        "NECK_TILT": -2.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_DOWN_LEFT": 0.4,   # Shift brows to a downward focus
                        "BROW_DOWN_RIGHT": 0.4,
                        #"PHONE_BIGAAH": 0.6,     # Stronger mouth opening for emphasis
                        "EYE_SQUINT_LEFT": 1,  # Increased squint for intensity
                        "EYE_SQUINT_RIGHT": 1,
                        "SMILE_CLOSED": 1.0,        # Slightly open smile for realism
                        #"SMILE_OPEN": 0.0,
                        "BROW_IN_LEFT": 0.4,       # Inward brow motion for more tension
                        "BROW_IN_RIGHT": 0.4,      # Inward brow motion on the other side
                        #"PHONE_EE": 0.1 
                    }
                },
                {
                    "time": [hold_time + 0.25],#hold_time + 0.25
                    "params": {
                        "reset": False            # Return to neutral
                    }
                }
            ],
            "class": "furhatos.gestures.Gesture"
        },
    blocking=True)

    def gesture_smile(self):
        """ Start a smile in face
        Args:
            None
        Returns:
            None
        """
        print("Smile gesture")
        self.furhat.gesture(name="Smile")
    
    def gesture_bigsmile(self):
        """ Start a big smile in face
        Args:
            None
        Returns:
            None
        """
        print("Big Smile gesture")
        self.furhat.gesture(name="BigSmile")


    def gesture_exhale(self, exhale_time: int):
        print("Exhaling for " + str(exhale_time) + " seconds.")
        self.furhat.set_led(red=255, green=182, blue=193) #Muted peach
        self.furhat.gesture(body={
            "frames": [
                            {
                    "time": [0.0], #End of bolding breath
                    "params": {
                        "NECK_TILT": -3.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_DOWN_LEFT": 0.2,   # Shift brows to a downward focus
                        "BROW_DOWN_RIGHT": 0.2,
                        #"PHONE_BIGAAH": 0.6,     # Stronger mouth opening for emphasis
                        "EYE_SQUINT_LEFT": 0.4,  # Increased squint for intensity
                        "EYE_SQUINT_RIGHT": 0.4,
                        "SMILE_CLOSED": 1.0,        # Slightly open smile for realism
                        #"SMILE_OPEN": 0.0,
                        "BROW_IN_LEFT": 0.2,       # Inward brow motion for more tension
                        "BROW_IN_RIGHT": 0.2,      # Inward brow motion on the other side
                        #"PHONE_EE": 0.1 
                    }
                },
                {
                    "time": [0.25], #Start to release breath
                    "params": {
                        "NECK_TILT": 1.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_DOWN_LEFT": 0.3,   # Shift brows to a downward focus
                        "BROW_DOWN_RIGHT": 0.3,
                        #"PHONE_BIGAAH": 0.6,     # Stronger mouth opening for emphasis
                        "EYE_SQUINT_LEFT": 0.5,  # Increased squint for intensity
                        "EYE_SQUINT_RIGHT": 0.5,
                        "SMILE_CLOSED": 1,        # Slightly open smile for realism
                        "PHONE_OOH_Q": 0
                    }
                },
                {
                    "time": [0.25], 
                    "params": {
                        "PHONE_OOH_Q": 0.4
                    }
                },
                {
                    "time": [exhale_time/4 + 0.25], #exhale_time/4 + 0.25 = 1.25
                    "params": {
                        "PHONE_OOH_Q": 0.7
                    }
                },
                {
                    "time": [exhale_time/2], #exhale_time/2 = 2.0
                    "params": {
                        "PHONE_OOH_Q": 1
                    }
                },
                {
                    "time": [exhale_time*3/4], #exhale_time*3/4=3.0
                    "params": {
                        "PHONE_OOH_Q": 1
                    }
                },
                {
                    "time": [exhale_time], #end #exhale_time=4.0
                    "params": {
                        "NECK_TILT": 0.0,       # Final neck lift for exaggerated breath
                        "GAZE_TILT": 0.0,
                        "BROW_DOWN_LEFT": -0.1,   # Shift brows to a downward focus
                        "BROW_DOWN_RIGHT": -0.1,
                        "PHONE_AAH": 0.1,     # Stronger mouth opening for emphasis
                        "EYE_SQUINT_LEFT": 0.1,  # Increased squint for intensity
                        "EYE_SQUINT_RIGHT": 0.1,
                        "SMILE_CLOSED": 0.1,        # Slightly open smile for realism
                        "PHONE_OOH_Q": 0.1
                    }
                },            
                {
                    "time": [exhale_time + 0.5], #exhale_time + 0.5=4.5
                    "params": {
                        "reset": True            # Return to neutral
                    }
                }
            ],
            "class": "furhatos.gestures.Gesture"
        },
        blocking=True)
        self.furhat.set_led(red=0, green=0, blue=0) #black or no color

    def gesture_blink(self):
        """ Start a Blink gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Blink gesture")
        self.furhat.gesture(name="Blink")

    def gesture_browfrown(self):
        """ Start a BrowFrown gesture in face
        Args:
            None
        Returns:
            None
        """
        print("BrowFrown gesture")
        self.furhat.gesture(name="BrowFrown")

    def gesture_browraise(self):
        """ Start a BrowRaise gesture in face
        Args:
            None
        Returns:
            None
        """
        print("BrowRaise gesture")
        self.furhat.gesture(name="BrowRaise")

    def gesture_closeeyes(self):
        """ Start a CloseEyes gesture in face
        Args:
            None
        Returns:
            None
        """
        print("CloseEyes gesture")
        self.furhat.gesture(name="CloseEyes")

    def gesture_expressanger(self):
        """ Start an ExpressAnger gesture in face
        Args:
            None
        Returns:
            None
        """
        print("ExpressAnger gesture")
        self.furhat.gesture(name="ExpressAnger")

    def gesture_expressdisgust(self):
        """ Start an ExpressDisgust gesture in face
        Args:
            None
        Returns:
            None
        """
        print("ExpressDisgust gesture")
        self.furhat.gesture(name="ExpressDisgust")

    def gesture_expressfear(self):
        """ Start an ExpressFear gesture in face
        Args:
            None
        Returns:
            None
        """
        print("ExpressFear gesture")
        self.furhat.gesture(name="ExpressFear")

    def gesture_expresssad(self):
        """ Start an ExpressSad gesture in face
        Args:
            None
        Returns:
            None
        """
        print("ExpressSad gesture")
        self.furhat.gesture(name="ExpressSad")

    def gesture_gazeaway(self):
        """ Start a GazeAway gesture in face
        Args:
            None
        Returns:
            None
        """
        print("GazeAway gesture")
        self.furhat.gesture(name="GazeAway")

    def gesture_nod(self):
        """ Start a Nod gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Nod gesture")
        self.furhat.gesture(name="Nod")

    def gesture_oh(self):
        """ Start an Oh gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Oh gesture")
        self.furhat.gesture(name="Oh")

    def gesture_roll(self):
        """ Start a Roll gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Roll gesture")
        self.furhat.gesture(name="Roll")

    def gesture_shake(self):
        """ Start a Shake gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Shake gesture")
        self.furhat.gesture(name="Shake")

    def gesture_surprise(self):
        """ Start a Surprise gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Surprise gesture")
        self.furhat.gesture(name="Surprise")

    def gesture_thoughtful(self):
        """ Start a Thoughtful gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Thoughtful gesture")
        self.furhat.gesture(name="Thoughtful")

    def gesture_wink(self):
        """ Start a Wink gesture in face
        Args:
            None
        Returns:
            None
        """
        print("Wink gesture")
        self.furhat.gesture(name="Wink")