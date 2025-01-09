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
        self.furhat.say(text=message, blocking=True)
        print(f"Furhat speaks: {message}")

    def listen(self) -> str:
        """Simulates listening and returns a sample input."""
        response = self.furhat.listen()
        message = getattr(response, 'message', '') 
        print(f"Furhat listened: {message}")
        return message

    def getResponse(self, query: str) -> str:
        """Generates a response based on input query."""
        self.furhat.say(text=query, blocking=True)
        response = self.furhat.listen()
        message = getattr(response, 'message', '') 
        print(f"Furhat response: {message}")
        return message

    def setGesture(self):
        """Simulates setting a gesture."""
        print("Furhat set a gesture.")
    
    def gesture_inhale(self, inhale_time: int):
        print("Inhaling for " + inhale_time + " seconds.")
        self.furhat.gesture(body={
            "frames": [
                {
                    "time": [0.25], #start of breathing in
                    "params": {
                        "NECK_TILT": -1.0,       # Final neck lift for exaggerated breath
                    }
                },            {
                    "time": [0.5],
                    "params": {
                        "NECK_TILT": -7.0,       # Final neck lift for exaggerated breath
                    }
                },
                {
                    "time": [1.0], 
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
                    "time": [2.0], #middle of breathing in
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
                    "time": [3.75], #End of breathing in and start of bolding breath
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
                    "time": [4.0],
                    "params": {
                        "NECK_TILT": -1.0,       # Final neck lift for exaggerated breath
                        "SMILE_CLOSED": 1.0        # Slightly open smile for realism                    
                    }
                },
                {
                    "time": [4.25],
                    "params": {
                        "reset": False            # Return to neutral
                    }
                }
            ],
            "class": "furhatos.gestures.Gesture"
        })


    def gesture_hold(self, hold_time: int):
        print("Hold breath for " + hold_time + " seconds.")
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
                    "time": [1.0], 
                    "params": {
                        "NECK_TILT": -3.0
                    }
                },
                {
                    "time": [2.0], 
                    "params": {
                        "NECK_TILT": -4.0
                    }
                },
                {
                    "time": [3.0], 
                    "params": {
                        "NECK_TILT": -3.0
                    }
                },
                {
                    "time": [4.0], #End of bolding breath
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
                    "time": [4.25],
                    "params": {
                        "reset": False            # Return to neutral
                    }
                }
            ],
            "class": "furhatos.gestures.Gesture"
        })

    def gesture_exhale(self, exhale_time: int):
        print("Exhaling for " + exhale_time + " seconds.")
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
                    "time": [1.25],
                    "params": {
                        "PHONE_OOH_Q": 0.7
                    }
                },
                {
                    "time": [2.0], 
                    "params": {
                        "PHONE_OOH_Q": 1
                    }
                },
                {
                    "time": [3.0], 
                    "params": {
                        "PHONE_OOH_Q": 1
                    }
                },
                {
                    "time": [4.0], #end
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
                    "time": [4.5],
                    "params": {
                        "reset": True            # Return to neutral
                    }
                }
            ],
            "class": "furhatos.gestures.Gesture"
        })

