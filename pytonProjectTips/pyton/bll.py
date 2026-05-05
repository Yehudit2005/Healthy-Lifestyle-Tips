from db_connection import get_connection
from models import Tip
from models import Tip

#קבלת כל הטיפים
def getAllTips():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tips")
    columns = [col[0] for col in cursor.description]  # שמות העמודות
    rows = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in rows]  # ממיר כל שורה ל-dict
    cursor.close()
    conn.close()
    return result

#סינון טיפים לפי קטגוריה
def getTipsByCategory(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT  *
                   FROM tips t
                   JOIN categories c ON t.category_id = c.id
                   WHERE c.name = ?
                   """, (category,))
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    conn.close()
    return result

#קבלת פרטי טיפ ספיציפי
def getTipById(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT t.title, t.description FROM tips t WHERE t.id = ?",
        (id,))
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()  # במקום fetchall
    cursor.close()
    conn.close()
    if row is None:
        return None  # או להעיף HTTPException(404)
    return dict(zip(columns, row))  # מחזיר dict בודד

#הוספת טיפ
def addTip(tip: Tip):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tips (category_id, title, description) OUTPUT INSERTED.id VALUES (?, ?, ?)",
        (tip.category_id, tip.title, tip.description)
    )
    tip_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return tip_id

#מחיקת טיפ
def deleteTip(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE  FROM tips  WHERE id = ?",
        (id,)
    )
    conn.commit()
    #יכנס לתוך המשתנה כמה שורות השתנו בעקבות הפעולה
    deleted=cursor.rowcount
    cursor.close()
    conn.close()
    return deleted


#עדכון טיפ
def updateTip(id: int, newCategory: int = None, newTitle: str = None, newDescription: str = None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   UPDATE tips
                   SET category_id = COALESCE(?, category_id),
                       title       = COALESCE(?, title),
                       description = COALESCE(?, description)
                   WHERE id = ?
                   """, (newCategory, newTitle, newDescription, id))

    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()

    return updated






