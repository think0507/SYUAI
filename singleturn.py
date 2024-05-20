# single_turn.py
import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyCHVdmi7nY5oKsP6c7WokDRtNLlHR0iL5Q")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("")
print(response.text)