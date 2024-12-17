from FurhatClient import FurhatClient

class LLMModule:
    def __init__(self, furhatClient: FurhatClient, userdata: dict, doctor_info: dict):
        """Constructor: Initializes LLMModule with FurhatClient, user data, and doctor info."""
        print("Initializing LLMModule...")
        self.furhatClient = furhatClient
        self.userdata = userdata
        self.doctor_info = doctor_info

    def __del__(self):
        """Destructor: Cleans up LLMModule"""
        print("Destroying LLMModule...")

    def start(self):
        """Starts the LLM process, using FurhatClient."""
        print("Starting LLM module...")
        self.furhatClient.speak("LLM Module started.")
