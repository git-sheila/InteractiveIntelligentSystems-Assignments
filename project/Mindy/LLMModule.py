import os
import google.generativeai as genai
from FurhatClient import FurhatClient
from EmotionDetectionModule import EmotionDetectionModule

genai.configure(api_key="AIzaSyCob6ycjeEkPlWdBlRhqyCXO7ondVlYzY4")

class LLMModule:
    def __init__(self, furhatClient: FurhatClient, emotionModule: EmotionDetectionModule, userdata: dict, doctor_info: dict):
        """Constructor: Initializes LLMModule with FurhatClient, user data, and doctor info."""
        print("Initializing LLMModule...")
        self.furhatClient = furhatClient
        self.emotionModule = emotionModule
        self.userdata = userdata
        self.doctor_info = doctor_info
        self.exercise_completed = set()  # Track completed exercises

        # Predefined responses dictionary
        self.predefined_responses = {
            "hello": "Hello! How can I assist you with mindfulness today?",
            "hi": "Hi there! I'm here to guide you toward a calmer mind.",
            "goodbye": "Take care! Remember to breathe and stay grounded.",
            "thank you": "You're welcome! Let me know if you need more help.",
            "breathing exercise": "Let's begin with the 4-7-8 technique: Inhale for 4 seconds, hold for 7, and exhale for 8. Shall we start?",
            "calm me down": "Try this: Inhale deeply through your nose for a count of 4, hold for 2 seconds, and then exhale slowly for a count of 6.",
            "mindfulness tip": "Take a moment to focus on your breathing. Notice how the air feels as you inhale and exhale.",
            "features": "I can help with breathing exercises, mindfulness tips, and tracking your progress toward calmness.",
            "appointment": "I can help you schedule an appointment with one of our doctors. Would you like to proceed?"
        }

        # Configure LLM model and start chat session
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 200,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
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
                "- Thank the user and encourage them to reach out for further assistance if needed.\n\n"

                "6. **Predefined Responses**:\n"
                "To ensure a consistent and efficient user experience, use the following predefined responses when applicable:\n"
                "- 'hello': 'Hello! How can I assist you with mindfulness today?'\n"
                "- 'hi': 'Hi there! I'm here to guide you toward a calmer mind.'\n"
                "- 'goodbye': 'Take care! Remember to breathe and stay grounded.'\n"
                "- 'thank you': 'You're welcome! Let me know if you need more help.'\n"
                "- 'breathing exercise': 'Let's begin with the 4-7-8 technique: Inhale for 4 seconds, hold for 7, and exhale for 8. Shall we start?'\n"
                "- 'calm me down': 'Try this: Inhale deeply through your nose for a count of 4, hold for 2 seconds, and then exhale slowly for a count of 6.'\n"
                "- 'mindfulness tip': 'Take a moment to focus on your breathing. Notice how the air feels as you inhale and exhale.'\n"
                "- 'features': 'I can help with breathing exercises, mindfulness tips, and tracking your progress toward calmness.'\n"
                "- 'appointment': 'I can help you schedule an appointment with one of our doctors. Would you like to proceed?'\n\n"
                "If a predefined response is used, acknowledge it in the chat session for context and proceed with the conversation seamlessly."
            ),
        )
        self.chat_session = self.model.start_chat(history=[])

    def __del__(self):
        """Destructor: Cleans up LLMModule"""
        print("Destroying LLMModule...")

    # def predefined_response(self, user_input):
        """Returns a predefined response if a match is found."""
    #    return self.predefined_responses.get(user_input.lower())

    def llm_response(self, user_input, emotion="neutral"):
        """Generates a response using the LLM."""
        # Use the existing chat session for context
        appendedString = "User: "+user_input+ "Emotion detected from camera is  "+emotion
        print("************SD  "+ appendedString)
        llm_response = self.chat_session.send_message(appendedString)
        return llm_response.text

    def start(self):
        """Starts the LLM process, using FurhatClient."""
        print("Starting LLM module...")
        self.furhatClient.speak("I am ready to assist you.")

        while True:  # Main interaction loop
            user_input = self.furhatClient.listen()
            if user_input:
                if user_input.lower() in ["exit", "quit", "bye", "stop"]:  # Exit condition
                    self.furhatClient.speak(
                        "I'm glad I could help. Take care and reach out anytime you need assistance. Have a peaceful day!"
                    )
                    self.chat_session.send_message("User has ended the session.")  # Log exit in chat history
                    break

                # Get the current emotion from the EmotionDetectionModule
                current_emotion = self.emotionModule.fetchCurrentEmotion()

                # Try predefined response first
                #predefined_response = self.predefined_response(user_input)
                response = self.predefined_responses.get(user_input.lower())
                if response:
                    self.furhatClient.speak(response)
                    print(f"Mindy (Predefined): {response}")
                    # Add predefined response to the chat session history
                    self.chat_session.history.append({"role": "model", "parts": [response]})
                    self.chat_session.history.append({"role": "system", "parts": [f"Predefined response '{user_input}' used and acknowledged."]})
                else:
                    # Fall back to LLM if no predefined response is found
                    print("userInput", user_input)
                    print("current emotion", current_emotion)
                    llm_response = self.llm_response(user_input, current_emotion)
                    print(f"LLM Response: {llm_response}")
                    self.furhatClient.speak(llm_response)

