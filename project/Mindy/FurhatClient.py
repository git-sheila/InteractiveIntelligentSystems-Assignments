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
