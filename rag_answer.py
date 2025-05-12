import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")  

def generate_answer(context, question):
    prompt = f"""Answer the following question based on the given context very well and elaborated.Give each answer in minimum of 20 lines. 
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {question}
"""
    response = model.generate_content(prompt)
    return response.text
