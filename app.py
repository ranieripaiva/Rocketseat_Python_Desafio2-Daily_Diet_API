from flask import Flask, request, jsonify
from database import db
from models.user import User
from models.dieta import Dieta
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

dietas = []
dieta_id_control = 1

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    #Login
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({"message": "Autenticação realizada com sucesso!"}), 200
  
  return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})

@app.route('/user', methods=["POST"])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario cadastrado com sucesso"})

  return jsonify({"message": "Dados invalidos"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
  user = User.query.get(id_user)

  if user:
    return {"username": user.username}

  return jsonify({"message": "Usuario não encontrado"}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
  data = request.json
  user = User.query.get(id_user)

  if user and data.get("password"):
    user.password = data.get("password")
    db.session.commit()

    return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"})

  return jsonify({"message": "Usuario não encontrado"}), 404

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)

  if id_user == current_user.id:
    return jsonify({"message": "Deleção não permitida"}), 403

  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})

  return jsonify({"message": "Usuario não encontrado"}), 404


@app.route('/dietas', methods=['POST'])
def creat_dieta():
  global dieta_id_control
  data = request.get_json()
  new_dieta = Dieta(id=dieta_id_control, title=data['title'], description=data.get('description',''), dt_dieta=data['dt_dieta'])
  dieta_id_control += 1
  dietas.append(new_dieta)
  print(dietas)
  return jsonify({"message":"Nova dieta criada com sucesso", "id": new_dieta.id})

@app.route('/dietas', methods=['GET'])
def get_dietas():
  dieta_list = [dieta.to_dict() for dieta in dietas]

  output = {
    "Dietas": dieta_list,
    "total_dietas": len(dieta_list)
  }
  return jsonify(output)


@app.route('/dietas/<int:id>', methods=['GET'])
def get_dieta(id):
  for d in dietas:
    if d.id == id:
      return jsonify(d.to_dict())

  return jsonify({"message": "Não foi possível encontrar a dieta"}), 404

@app.route('/dietas/<int:id>', methods=["PUT"])
def update_dieta(id):
  dieta = None
  for d in dietas:
    if d.id == id:
      dieta = d
  if dieta == None:
    return jsonify({"message": "Não foi possível encontrar a dieta"}), 404

  data = request.get_json()
  dieta.title = data['title']
  dieta.description = data['description']
  dieta.dieta = data['dieta']
  return jsonify({"message": "Dieta atualizada com sucesso"})


@app.route('/dietas/<int:id>', methods=['DELETE'])
def delete_dieta(id):
  dieta = None
  for d in dietas:
    if d.id == id:
      dieta = d
      break
    
  if not dieta:
    return jsonify({"message": "Não foi possível encontrar a dieta"}), 404

  dietas.remove(dieta)
  return jsonify({"message": "Dieta deletada com sucesso"})

if __name__ == "__main__":
  app.run(debug=True)
