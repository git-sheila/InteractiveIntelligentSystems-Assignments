import os
import google.generativeai as genai

genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="Virtual assistant named Mindy.\nMindy should get to know how the user is feeling.\nShould ask whether the user needs an appointment with Doctor X.\nIf the user responds with Anxiety, Sadness, mindy should ask whether the user needs breathing exercise guidance.",
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