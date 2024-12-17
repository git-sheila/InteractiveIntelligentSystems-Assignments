class FurhatClient:
    def __init__(self):
        """Constructor: Initializes FurhatClient"""
        print("Initializing FurhatClient...")

    def __del__(self):
        """Destructor: Cleans up FurhatClient"""
        print("Destroying FurhatClient...")

    def init(self):
        """Initializes any required components"""
        print("FurhatClient initialized.")

    def speak(self, message: str):
        """Simulates speaking a message."""
        print(f"Furhat speaks: {message}")

    def listen(self) -> str:
        """Simulates listening and returns a sample input."""
        user_input = input("Listening... Enter user response: ")
        print(f"Furhat listened: {user_input}")
        return user_input

    def getResponse(self, query: str) -> str:
        """Generates a response based on input query."""
        response = f"Response to '{query}'"
        print(f"Furhat generated response: {response}")
        return response

    def setGesture(self):
        """Simulates setting a gesture."""
        print("Furhat set a gesture.")
