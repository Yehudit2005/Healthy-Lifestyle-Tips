# models.py
from pydantic import BaseModel

class Tip(BaseModel):
    title: str
    description: str
    category_id: int
