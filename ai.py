import google.generativeai as genai

genai.configure(api_key="AIzaSyAJFUHLcfT1_lzPSv8A5jy6vthRBvAIbU0")

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])


def get_info(*, prompt):
    response = chat.send_message(prompt)
    return response.text
