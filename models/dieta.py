class Dieta:
  def __init__(self, id, title, description, dt_dieta, dieta=False) -> None:
    self.id = id
    self.title = title
    self.description = description
    self.dt_dieta = dt_dieta
    self.dieta = dieta

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,      
      "description": self.description,
      "data": self.dt_dieta,
      "dieta": self.dieta      
    }

