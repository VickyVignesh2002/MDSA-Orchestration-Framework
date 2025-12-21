from chatbot_app.chatbot import MDSAChatbot

chatbot = MDSAChatbot(enable_tools=True, enable_rag=False)
response = chatbot.chat("Calculate 50 + 75")
print(response['response'])  # Shows calculation result