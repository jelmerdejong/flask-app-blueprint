from app import db


class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)
