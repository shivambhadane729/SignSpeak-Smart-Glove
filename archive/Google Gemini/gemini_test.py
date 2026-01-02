from google import genai

# Initialize client (API key already tested as valid)
client = genai.Client(api_key="AIzaSyCONb4jZcVo_48KT0MEkcHONDeY1iN87WU")

gesture_words = "HELLO THANK YOU"

prompt = (
    "You are an assistive AI for sign language users.\n"
    "Convert the following detected gesture words into a natural spoken sentence.\n\n"
    f"Words: {gesture_words}"
)

response = client.models.generate_content(
    model="gemini-1.0-pro",
    contents=prompt
)

print("Gemini Output:")
print(response.text)
