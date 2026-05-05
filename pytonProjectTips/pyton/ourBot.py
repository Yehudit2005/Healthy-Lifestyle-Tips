import sys
import io
import os
from google import genai


# הגדרת עברית
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'


# הגדרת הלקוח
client = genai.Client(
   api_key="AIzaSyBr2ypwbmfANTOT4H5jCYsv7mYO33a60WI"
)




def get_bot_response(user_question):
   """פונקציה שמקבלת שאלה ומחזירה תשובה"""
   try:
       response = client.models.generate_content(
           model="models/gemini-2.5-flash",
           contents=user_question
       )
       return response.text
   except Exception as e:
       return f"שגיאה: {str(e)}"




def chat_bot():
   """פונקציה ראשית להפעלת הבוט"""
   print("=" * 50)
   print("🤖 ברוכים הבאים לבוט Gemini!")
   print("=" * 50)
   print("כתבי את השאלה שלך (או 'יציאה' כדי לצאת)\n")


   while True:
       # קבלת קלט מהמשתמש
       user_input = input("👤 את: ").strip()


       # בדיקה אם המשתמש רוצה לצאת
       if user_input.lower() in ['יציאה', 'exit', 'quit', 'bye']:
           print("\n👋 להתראות! תודה שהשתמשת בבוט!")
           break


       # בדיקה שהקלט לא ריק
       if not user_input:
           print("⚠️ בבקשה כתבי שאלה\n")
           continue


       # קבלת תשובה מהבוט
       print("\n🤖 הבוט חושב...")
       response = get_bot_response(user_input)
       print(f"🤖 בוט: {response}\n")
       print("-" * 50)




if __name__ == "__main__":
   # בדיקת חיבור ראשונית
   print("מתחבר לשירות Gemini...")
   test_response = get_bot_response("Hi")


   if "שגיאה" not in test_response:
       print("✅ החיבור תקין!\n")
       # הפעלת הבוט
       chat_bot()
   else:
       print(f"❌ שגיאה בחיבור: {test_response}")


