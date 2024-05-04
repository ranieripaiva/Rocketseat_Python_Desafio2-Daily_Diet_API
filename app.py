from datetime import datetime
from flask import Flask, request, jsonify
from database import db
from models.user import User
from models.dieta import Dieta
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

# Autenticação do User
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

# Logout na API com usuário logado
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})

# Criar novo usuário no banco
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

# Listar usuário especifico cadastrado no banco de dados
@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
  user = User.query.get(id_user)

  if user:
    return {"username": user.username}

  return jsonify({"message": "Usuario não encontrado"}), 404

# Atualizar usuário cadastrado no banco de dados
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

# Excluir usuário cadastrado no banco de dados
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
@login_required
def creat_dieta():
  data = request.json
  title = data.get("title")
  description = data.get("description")
  dt_dieta = datetime.strptime(str(data.get("dt_dieta")), '%Y-%m-%d %H:%M:%S')
   
  if title and description and dt_dieta:
    dieta = Dieta(title=title, description=description, dt_dieta=dt_dieta)  
    db.session.add(dieta)
    db.session.commit()    
    return jsonify({"message": "Dieta cadastrada com sucesso"})
  
  return jsonify({"message": "Dados invalidos"}), 400


@app.route('/dietas', methods=['GET'])
def get_dietas():
  dietas = Dieta.query.all()
  return jsonify([dieta.serialize() for dieta in dietas])

# obter dieta especifica
@app.route('/dietas/<int:id_dieta>', methods=['GET'])
def get_dieta(id_dieta):
  dieta = Dieta.query.get(id_dieta)
  
  if dieta:
    return {"Title": dieta.title, "Description": dieta.description, "Data": dieta.dt_dieta }
  
  return jsonify({"message": "Dieta não encontrada"}), 404

# Atualização da dieta
@app.route('/dietas/<int:id_dieta>', methods=["PUT"])
@login_required
def update_dieta(id_dieta):
  data = request.json
  dieta = Dieta.query.get(id_dieta)

  if dieta:
    dieta.title = data.get("title")
    dieta.description = data.get("description")
    dieta.dt_dieta = datetime.strptime(str(data.get("data")), '%Y-%m-%d %H:%M:%S')
    dieta.dieta = data.get("dieta")
    db.session.commit()

    return jsonify({"message": f"Dieta {id_dieta} atualizado com sucesso"})

  return jsonify({"message": "Dieta não encontrado"}), 404

# Deletar uma dieta especifica
@app.route('/dietas/<int:id_dieta>', methods=['DELETE'])
def delete_dieta(id_dieta):
  dieta = Dieta.query.get(id_dieta)
  if dieta:
    db.session.delete(dieta)
    db.session.commit()
    return jsonify({"message": f"Dieta {id_dieta} deletado com sucesso"})

  return jsonify({"message": "Dieta não encontrado"}), 404

  
if __name__ == "__main__":
  app.run(debug=True)
