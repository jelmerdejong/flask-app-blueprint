from project import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from dataclasses import dataclass #Python 3.7+ and Flask 1.1+ https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json

@dataclass
class Texts(db.Model):
    id: int
    identify_id: str
    texts: str
    predicted_text: str

    __tablename__ = 'texts'
    
    id = db.Column(db.Integer, primary_key=True)
    identify_id = db.Column(db.String(25), nullable=True)
    texts = db.Column(db.Text, nullable=False)
    predicted_text = db.Column(db.Text, nullable=True)
    
    def __init__(self,identify_id, texts, predicted_text=None):
        self.identify_id= identify_id
        self.texts = texts
        self.predicted_text = predicted_text 
    
