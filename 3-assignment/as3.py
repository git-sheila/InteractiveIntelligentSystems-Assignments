'''from furhat_remote_api import FurhatRemoteAPI

# Connect to the Furhat robot
furhat = FurhatRemoteAPI("localhost")

# Select a character for Furhat
#furhat.set_character(name="Emma")  # Replace "Emma" with the desired character name

# Set a voice for Furhat
furhat.set_voice(name="Matthew")  # Replace "Matthew" with the desired voice name

# Have Furhat greet the user
furhat.say(text="Hello! It's wonderful to meet you!")
furhat.say(text="How are you feeling today?")
# Instruct Furhat to smile and nod
furhat.gesture(name="Smile")
furhat.gesture(name="Nod")

# Ask a question to the user



result = furhat.listen()  # Listen to the user's response
print(f"User response: {result}")
'''
from furhat_remote_api import FurhatRemoteAPI

# Connect to the Furhat robot
furhat = FurhatRemoteAPI("localhost")

# Start the scripted conversation
def scripted_conversation():
    # Greeting
    furhat.say(text="Hello there, human! I’m Furhat, your friendly virtual companion. How’s your day going?", blocking=True)
    user_response = furhat.listen()
    print(f"User: {user_response}")

    # Response to user's day
    furhat.say(text="Oh, you know, just another day making humans smile and nod—literally.", blocking=True)
    furhat.gesture(name="Smile")
    furhat.gesture(name="Nod")

    # Ask about food
    furhat.say(text="So, I’m curious—do you have a favorite food?", blocking=True)
    user_response = furhat.listen()
    print(f"User: {user_response}")

    # Respond to favorite food
    furhat.say(text="Ah, a great question! While I don't eat, I hear binary biscuits are quite the delicacy. Do you like those?", blocking=True)
    user_response = furhat.listen()
    print(f"User: {user_response}")

    # Discuss binary biscuits and user's comfort food
    furhat.say(text="It’s a thing in my world! Crunchy 0s and 1s. So satisfying. But tell me—what’s your go-to comfort food?", blocking=True)
    user_response = furhat.listen()
    print(f"User: {user_response}")

    # Respond to user's comfort food
    furhat.say(text=f"Excellent choice. Did you know that {user_response} is scientifically proven to boost happiness?", blocking=True)
    furhat.say(text="No, but I thought it sounded convincing.", blocking=True)

    # Humor: Knock-knock joke
    furhat.say(text="Speaking of comedy—knock, knock!", blocking=True)
    furhat.say(text="Who’s there?", blocking=True)
    furhat.say(text="AI.", blocking=True)
    furhat.say(text="AI who?", blocking=True)
    furhat.say(text="AI can’t believe you fell for that.", blocking=True)
    furhat.gesture(name="Smirk", blocking=True)

    # Wrap up
    furhat.say(text="Haha! You’re quite the comedian. Thank you! I’m here all week. Now, how else can I assist you today?", blocking=True)

# Run the conversation
scripted_conversation()
