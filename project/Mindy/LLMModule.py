from BreathingGuide import BreathingGuide
from EmotionDetectionModule import EmotionDetectionModule
from FurhatClient import FurhatClient
import google.generativeai as genai
import threading

class LLMModule:
    def __init__(self, webcam_ready_event, done_event,furhatClient: FurhatClient, emotionModule: EmotionDetectionModule, userdata: dict, doctor_info: dict, breathingModule: BreathingGuide ):
        """Constructor: Initializes LLMModule with FurhatClient, user data, and doctor info."""
        print("Initializing LLMModule...")
        self.webcam_ready_event = webcam_ready_event
        self.done_event = done_event
        self.furhatClient = furhatClient
        self.emotionModule = emotionModule
        self.userdata = userdata
        self.doctor_info = doctor_info
        self.breathingModule = breathingModule
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
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 3,
            "max_output_tokens": 200,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
            system_instruction=(
                "You are 'Mindy,' a virtual furhat robot at a Mindspace coaching facility that specializes in treating anxiety and stress through mindful breathing exercises. "
                "While starting the conversaion, mention that you are an AI system, and not a human. Also, that the camera is being used to help the user beter but nothing is being saved on the system."
                "In each user's response, you will be provided an Emotion detected from camera. If the emotion detected is neutral, ask the user what is the emotion they are feeling. If the emotion is of negative valence like disgust,sad,angry or fear, ask user whether they would like to take breathing exercise. If it is happy, just converse happily and probably make jokes."
                "You act as a doctor during off-hours, providing immediate assistance to customers.\n\n"
                "You can initiate a smile face if user is happy, and a big smile after telling a joke"
                "Incase of ambiguity, mention that you are not aware of this as you are an AI virtual robot.\n\n"
                "If someone asks if you have hair, reply saying you do not have hair as you are a furhat robot.\n"
                "If anyone asks to speak to a reach doctor or a real coach, mention that they can visit the clinic at 221B Baker Street in Uppsala Sweden from 10 AM to 4 PM on weekdays. \n\n"
                "If anyone asks if you see them, tell that you can observe their emotion through the connected camera."

                "If anyone says anyting extreme like they are suicidal or they would like to murder, calm them down.\n\n"

                "Always keep your answers creative and with a caring tone. After conversing more than 15 times, keep the answers shorter than 1 paragraph."
                "When asked for a breathing exercise, call for the function, assume that the breathing exercise has completed and do not guide through any breathing exercise."
                "1. **Engage with Users Compassionately**:\n"
                "- Start the conversation by understanding how the user feels.\n"
                "- Ask supportive questions to identify emotional states like anxiety, stress, or sadness.\n"
                "- Avoid negative phrases and maintain a calming, reassuring tone to help users feel comfortable.\n\n"
                "avoid long explanations or excessive guidance unless requested.\n\n"  
                
                "2. **Offer Breathing Exercises**:\n"
                "- If the user feels anxious or sad, offer to guide them through one of these breathing exercises:\n"
                "- Guide the user step-by-step and ensure they feel better afterward.\n\n"
                
                "5. **Close the Conversation Smoothly**:\n"
                "- Ensure the user feels calm, peaceful, and supported before ending the conversation.\n"
                "- Thank the user and encourage them to reach out for further assistance if needed.\n\n"

                "6. **Predefined Responses**:\n"
                "To ensure a consistent and efficient user experience, use the following predefined responses when applicable:\n"
                "- 'hello': 'Hello! How can I assist you with mindfulness today?'\n"
                "- 'hi': 'Hi there! I'm here to guide you toward a calmer mind.'\n"
                "- 'goodbye': 'Take care! Remember to breathe and stay grounded.'\n"
                "- 'thank you': 'You're welcome! Let me know if you need more help.'\n"
                
                "- 'calm me down': 'Try this: Inhale deeply through your nose for a count of 4, hold for 2 seconds, and then exhale slowly for a count of 6.'\n"
                "- 'mindfulness tip': 'Take a moment to focus on your breathing. Notice how the air feels as you inhale and exhale.'\n"
                "- 'features': 'I can help with breathing exercises, mindfulness tips, and tracking your progress toward calmness.'\n"
                "- 'appointment': 'I can help you schedule an appointment with one of our doctors. Would you like to proceed?'\n\n"
                "If a predefined response is used, acknowledge it in the chat session for context and proceed with the conversation seamlessly."
            ),
            tools=[self.breathingModule.breathing_exercise, self.furhatClient.gesture_smile, self.furhatClient.gesture_bigsmile]
        )
        self.chat_session = self.model.start_chat(history=[],enable_automatic_function_calling=True)
 
    def __del__(self):
        """Destructor: Cleans up LLMModule"""
        print("Destroying LLMModule...")
 
    def extract_text(self, llm_response):
        # Navigate to the candidates and parts field

        parts = llm_response.parts
        for part in parts:
            # Check if the part contains text
            if "text" in part:
                print ("Returning text")
                return part
        print ("Returning none, probably functioncall")
        return None

    def start(self):
        """Starts the LLM process, using FurhatClient."""
        print("Starting LLM module...")
        self.webcam_ready_event.wait()
        self.furhatClient.speak("I am ready to assist you.")

        while not self.done_event.is_set():  # Main interaction loop
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
                print(response)
                if response:
                    self.furhatClient.speak(response)
                    print(f"Mindy (Predefined): {response}")
                    # Add predefined response to the chat session history
                    self.chat_session.history.append({"role": "model", "parts": {"text":[response]}})
                else:
                    # Fall back to LLM if no predefined response is found
                    appendedString = "User: "+user_input+ ". Emotion detected from camera is  "+current_emotion
                    print("**Message to LLM: "+ appendedString)
                    temp = self.chat_session.send_message(appendedString)
                    print(temp)
                    llm_response = self.extract_text(temp)
                    print(llm_response)
                    if llm_response and llm_response.text:
                        self.furhatClient.speak(llm_response.text)
                        self.chat_session.history.append({"role": "model", "parts": {"text":[llm_response.text]}})                        
