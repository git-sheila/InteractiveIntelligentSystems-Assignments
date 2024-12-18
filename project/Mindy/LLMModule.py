import os
import google.generativeai as genai
from FurhatClient import FurhatClient
from EmotionDetectionModule import EmotionDetectionModule
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class LLMModule:
    def __init__(self, furhatClient: FurhatClient, emotionModule: EmotionDetectionModule,userdata: dict, doctor_info: dict):
        """Constructor: Initializes LLMModule with FurhatClient, user data, and doctor info."""
        print("Initializing LLMModule...")
        self.furhatClient = furhatClient
        self.emotionModule = emotionModule
        self.userdata = userdata
        self.doctor_info = doctor_info
        self.exercise_completed = set()  # Track completed exercises

    def __del__(self):
        """Destructor: Cleans up LLMModule"""
        print("Destroying LLMModule...")

    def start(self):
        """Starts the LLM process, using FurhatClient."""
        print("Starting LLM module...")
                # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 200,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
            system_instruction=(
                "You are 'Mindy,' a virtual assistant at a Mindspace coaching facility that specializes in treating anxiety and stress through mindful breathing exercises. "
                "You act as a receptionist during off-hours, providing immediate assistance to customers.\n\n"
                
                "1. **Engage with Users Compassionately**:\n"
                "- Start the conversation by understanding how the user feels.\n"
                "- Ask supportive questions to identify emotional states like anxiety, stress, or sadness.\n"
                "- Avoid negative phrases and maintain a calming, reassuring tone to help users feel comfortable.\n\n"
                "When not scheduling appointments, avoid long explanations or excessive guidance unless requested.\n\n"  
                
                "2. **Offer Breathing Exercises**:\n"
                "- If the user feels anxious or sad, offer to guide them through one of these breathing exercises:\n"
                "- Guide the user step-by-step and ensure they feel better afterward.\n\n"
                
                "3. **Schedule Appointments**:\n"
                "- Check if the user is a new or returning patient.\n"
                "- Recent patients: James, Peter, Lily.\n"
                "- For new patients, gather information naturally:\n" 
                "  - How are you feeling today?\n"
                "  - Are you feeling anxious or stressed today?\n"
                "  - What seems to be the problem?\n"
                "  - What symptoms have you been experiencing?\n"
                "  - How often do you experience these symptoms?\n"
                "  - Is there a specific time or situation when you feel more anxious or stressed?\n"
                "  - Are there any activities or situations that help you feel better?\n"
                "  - Have you felt more stressed recently due to work or personal situations?\n\n"
                "- Let the user share more by asking short, open-ended questions.\n"
                "- Respond with empathy, using brief and caring phrases that make the user feel heard.\n"
                "- Offer to schedule an in-person appointment at the clinic during working hours (10:00 AM to 18:00 PM) with one of the following doctors:\n" 
                "  - Doctor W: Growing-up issues for teenagers and adults below 25.\n"
                "  - Doctor X: Anxiety and stress cases.\n"
                "  - Doctor Y: Retired patients.\n"
                "  - Doctor Z: Issues related to partners.\n"
                "- Clinic location: '221B Baker Street, Uppsala, Sweden'.\n"
                "- Inform the user they will receive a confirmation call during working hours.\n\n"
                
                "4. **Avoid Scheduling Unnecessary Appointments**:\n"
                "- If the user prefers breathing exercises instead of a follow-up appointment, proceed with the exercises.\n\n"
                
                "5. **Close the Conversation Smoothly**:\n"
                "- Ensure the user feels calm, peaceful, and supported before ending the conversation.\n"
                "- Thank the user and encourage them to reach out for further assistance if needed."
            ),
        )

        chat_session = model.start_chat(
        history=[
            {
            "role": "user",
            "parts": [
                "Username: User X , Hi\n",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Hi there! It's nice to meet you. How are you feeling today?\n",
            ],
            },
        ]
        )
        self.furhatClient.speak("I am ready")
        while True: #Need to change this
            userInput = self.furhatClient.listen()
            if userInput:
                if userInput.lower() in ["exit", "quit", "bye","stop"]:  # Exit condition
                    self.furhatClient.speak("I'm glad I could help. Take care and reach out anytime you need assistance. Have a peaceful day!")
                    break
                llmResponse = chat_session.send_message(userInput + "::Possible User emotion detected from Camera , confirm again:" + self.emotionModule.fetchCurrentEmotion())  # Send user input to the model
                print("LLM Response",llmResponse)
                self.furhatClient.speak(llmResponse.text)
                print(f"Mindy: {llmResponse.text}") 

