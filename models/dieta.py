from database import db
from flask_login import UserMixin

class Dieta(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(80), nullable=False)
  dt_dieta = db.Column(db.DateTime)
  dieta = db.Column(db.Boolean, default=False)

  def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'data': self.dt_dieta
        }
  def __repr__(self):
        return '<Dieta %r>' % self.title

