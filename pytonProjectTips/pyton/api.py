import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import bll
from models import Tip
from google import genai
import os








app = FastAPI()


# הגדרת CORS - מאפשר ל-HTML לתקשר עם השרת
app.add_middleware(
 CORSMiddleware,
 allow_origins=["*"],
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)


# הגדרת הלקוח של Gemini
# שימי לב: מומלץ לשמור את ה-Key במשתנה סביבה, אבל שמתי אותו כאן כדי שזה יעבוד לך מיד
client = genai.Client(api_key="AIzaSyDp1qijskZJNSr63lb1r4YCv0X1FYkHHcw")


# מודל עבור בקשת הצ'אט
class ChatRequest(BaseModel):
 question: str


@app.get("/tips")
def getAllTips():
   try:
       return bll.getAllTips()
   except HTTPException:
       raise
   except Exception as e:
       print(e)
       raise HTTPException(500, "אירעה שגיאה בשרת, נסי שוב מאוחר יותר")


@app.get("/tips/category/{category}")
def getTipsByCategory(category: str):
   try:
       return bll.getTipsByCategory(category)
   except HTTPException:
       raise
   except Exception as e:
       print(e)
       raise HTTPException(500, "אירעה שגיאה בשליפת טיפים לפי קטגוריה")


@app.get("/tips/{id}")
def getTipById(id: int):
   try:
       tip = bll.getTipById(id)
       return tip
   except HTTPException:
       raise
   except Exception as e:
       print(e)
       raise HTTPException(500, "אירעה שגיאה בשליפת הטיפ")
@app.post("/tips")
def addTip(tip: Tip):
   try:
       tip_id = bll.addTip(tip)
       return {"message": "Tip added successfully", "id": tip_id}
   except HTTPException:
       raise
   except Exception as e:
       print(e)
       raise HTTPException(500, "אירעה שגיאה בהוספת הטיפ")


@app.delete("/tips/{id}")
def deleteTip(id: int):
   try:
       bll.deleteTip(id)
       return {"message": "Tip deleted successfully"}
   except HTTPException:
       raise
   except Exception as e:
       print(e)
       raise HTTPException(500, "אירעה שגיאה במחיקת הטיפ")


@app.put("/tips/{id}")
def updateTip(
   id: int,
   category: Optional[int] = None,
   title: Optional[str] = None,
   description: Optional[str] = None
):
   try:
       updated = bll.updateTip(id, category, title, description)
       if updated == 0:
           raise HTTPException(404, "טיפ לא נמצא")
       return {"message": "Tip updated successfully"}
   except HTTPException:
       raise
   except Exception as e:
       print(e)
       raise HTTPException(500, "אירעה שגיאה בעדכון הטיפ")

# --- Endpoint חדש עבור הבוט ---

# --- פונקציות עזר לבוט ---
def get_bot_response(user_question):
  try:
      # הגדרת ההנחיה המגבילה
      system_instruction = """
     אתה עוזר וירטואלי באתר המוקדש לטיפים לאורח חיים בריא, טיפוח ובריאות בלבד.




     עליך לפעול לפי הכללים הבאים:
     1. ענה אך ורק על שאלות בנושאי: תזונה נכונה, כושר, שינה, טיפוח הגוף והפנים, ובריאות כללית.
     2. אם השאלה של המשתמש אינה קשורה ישירות לאורח חיים בריא או טיפוח (למשל: פוליטיקה, טכנולוגיה, היסטוריה, בישול כללי וכו'),
        עליך לענות אך ורק בנוסח הבא: "שאלתך אינה קשורה לתוכן האתר שלנו, רוצה לברר אודות דבר נוסף?"
     3. היה אדיב וממוקד.
     """

      # שילוב ההנחיה עם השאלה של המשתמש
      full_prompt = f"{system_instruction}\n\nשאלת המשתמש: {user_question}"


      response = client.models.generate_content(
          model="models/gemini-2.5-flash",
          contents=full_prompt
      )

      if response and response.text:
          return response.text
      return "מצטער, לא הצלחתי לעבד את התשובה."

  except Exception as e:
      print(f"Error: {e}")
      return "שאלתך אינה קשורה לתוכן האתר שלנו, רוצה לברר אודות דבר נוסף?"


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
 """הפונקציה שה-HTML יקרא לה בכל פעם שמשתמש שולח הודעה"""
 bot_answer = get_bot_response(request.question)
 return {"response": bot_answer}


if __name__ == '__main__':
 uvicorn.run(app, host="127.0.0.1", port=8000)

