from FurhatClient import FurhatClient
import os
import google.generativeai as genai

genai.configure(api_key="")

class LLMModule:
    def __init__(self, furhatClient: FurhatClient, userdata: dict, doctor_info: dict):
        """Constructor: Initializes LLMModule with FurhatClient, user data, and doctor info."""
        print("Initializing LLMModule...")
        self.furhatClient = furhatClient
        self.userdata = userdata
        self.doctor_info = doctor_info
        self.exercise_completed = set()  # Track completed exercises

    def __del__(self):
        """Destructor: Cleans up LLMModule"""
        print("Destroying LLMModule...")

    # Breathing Exercise Functions
    def breathing_54321(self):
        self.exercise_completed.add("54321")
        return (
            "Let's try the **54321 Breathing Exercise**:\n"
            "1. Take a deep breath in.\n"
            "2. Slowly count backward from 5 while exhaling.\n"
            "3. Repeat this process 3-5 times.\n"
            "Do you feel a bit better now?"
        )

    def breathing_478(self):
        self.exercise_completed.add("478")
        return (
            "Let's try the **478 Breathing Exercise**:\n"
            "1. Breathe in for 4 seconds.\n"
            "2. Hold your breath for 7 seconds.\n"
            "3. Exhale slowly for 8 seconds.\n"
            "Repeat this for 3-5 cycles.\n"
            "How do you feel now?"
        )

    def breathing_equal(self):
        self.exercise_completed.add("Equal")
        return (
            "Let's try the **Equal Breathing Exercise**:\n"
            "1. Inhale deeply for 4 seconds.\n"
            "2. Exhale for 4 seconds, keeping it even.\n"
            "3. Repeat this for several minutes.\n"
            "Are you feeling more relaxed?"
        )

    def breathing_444(self):
        self.exercise_completed.add("444")
        return (
            "Let's try the **444 Breathing Exercise**:\n"
            "1. Inhale deeply for 4 seconds.\n"
            "2. Hold your breath for 4 seconds.\n"
            "3. Exhale slowly for 4 seconds.\n"
            "Repeat this for a few cycles.\n"
            "How do you feel now?"
        )

    def breathing_555(self):
        self.exercise_completed.add("555")
        return (
            "Let's try the **555 Breathing Exercise**:\n"
            "1. Inhale for 5 seconds.\n"
            "2. Hold your breath for 5 seconds.\n"
            "3. Exhale slowly for 5 seconds.\n"
            "Repeat this process a few times.\n"
            "Do you feel calmer now?"
        )

    # Function to call the correct breathing exercise dynamically
    def get_breathing_exercise(self,exercise_name):
        exercises = {
            "54321": self.breathing_54321,
            "478": self.breathing_478,
            "Equal": self.breathing_equal,
            "444": self.breathing_444,
            "555": self.breathing_555
        }
        return exercises.get(exercise_name)()
    
        #if exercise_name in self.exercise_completed:
            #return f"You've already completed the **{exercise_name} Breathing Exercise**. Let me know if you'd like to try a different one!"
        #else:
            #return exercises.get(exercise_name, lambda: "Sorry, I don't know that exercise.")()


    def start(self):
        """Starts the LLM process, using FurhatClient."""
        print("Starting LLM module...")
        self.furhatClient.speak("LLM Module started.")


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
                "  - 54321 Breathing\n"
                "  - 478 Breathing\n"
                "  - Equal Breathing\n"
                "  - 444 Breathing\n"
                "  - 555 Breathing\n"
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
                "Hi\n",
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

        response = chat_session.send_message("HI")
        print(response.text)

        response = chat_session.send_message("What do you do?")
        print(response.text)

        response = chat_session.send_message("I think i am not feeling well")
        print(response.text)

        # Continuous loop for user interaction
        while True:
            user_input = input("You: ")  # Get user input
            if user_input.lower() in ["exit", "quit", "bye"]:  # Exit condition
                print("Mindy: I'm glad I could help. Take care and reach out anytime you need assistance. Have a peaceful day!")
                break
            
            response = chat_session.send_message(user_input)  # Send user input to the model
            print(f"Mindy: {response.text}")  # Print the model's response

            # Check for breathing exercises dynamically
            for exercise in ["54321", "478", "Equal", "444", "555"]:
                if exercise in response.text and exercise not in self.exercise_completed:
                    print(f"Mindy: {self.get_breathing_exercise(exercise)}")
                    # Update LLM context about exercise completion
                    chat_session.history.append({
                        "role": "user",
                        "parts": [f"I've completed the {exercise} breathing exercise."]
                    })
                    break
            else:
                if any(ex in response.text for ex in ["54321", "478", "Equal", "444", "555"]):
                    print("Mindy: You've already done this exercise. Let me know if you'd like to try something else!")
           
            # Check for breathing exercises based on keywords
            if "54321" in response.text:
                print(f"Mindy: {self.breathing_54321()}")
            elif "478" in response.text:
                print(f"Mindy: {self.breathing_478()}")
            elif "Equal" in response.text:
                print(f"Mindy: {self.breathing_equal()}")
            elif "444" in response.text:
                print(f"Mindy: {self.breathing_444()}")
            elif "555" in response.text:
                print(f"Mindy: {self.breathing_555()}")

