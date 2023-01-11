from flask import Flask, request
from flask_bcrypt import Bcrypt

from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from functions import Connect, findAll, findOne, findIncompleted, findCompleted

app = Flask(__name__)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_SECRET_KEY"] = "lol"

jwt = JWTManager(app)

bcrypt = Bcrypt()
    
@app.route("/", methods=['get'])
def home():
    conn = Connect()
    cursor = conn.cursor()
    
    sql = f"SELECT * FROM todosapi"
    cursor.execute(sql)
    result = cursor.fetchone()
    
    return {"message":result}

## REGISTER USER
@app.route("/register", methods=['post'])
def register():
    username = (request.json['username']).strip()
    password = (request.json['password']).strip()
    if username != "" and password != "" :
        try:
            if not findOne('users', 'username', username):
                    password=bcrypt.generate_password_hash(password).decode('utf-8')
                    conn = Connect()
                    cursor = conn.cursor()
    
                    sql = f"INSERT INTO users(username,password) VALUES('{username}', '{password}')"
                    cursor.execute(sql)
                    conn.commit()
                    
                    user = findOne('users','username',username)
                    return {"user":user}, 201
            return {"message":"username already exist! choose another one"},403
        except Exception as ex:
            return{"message":"An error occured"}, 500
    return {"message":"username and password are required"}

## LOGIN USER XX
@app.route("/login", methods=['post'])
def login():
    username = (request.json['username']).strip()
    password = (request.json['password']).strip()
    if username != "" and password != "" :
        try:
            user = findOne('users', 'username', username)
            if not user or not bcrypt.check_password_hash(user["password"], password):
                return {"message":"Invalid credential"}, 403

            user["token"] = create_access_token(identity=username)
            user["refresh_token"] = create_refresh_token(identity=username)
            
            return {"user":user},200
        except TypeError as ex:
            return{"{}".format(ex)}, 500
    return {"username and password are required"},403

## REFRESH TOKEN XX
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return {"token":access_token}, 200

## GET ALL TODO xx
@app.route('/todos')
@jwt_required()
def get_todos():
    try:
        todos = findAll()
        return {'todos':todos}, 200
    except TypeError as ex:
        return{"message":"{}".format(ex)}, 500

## GET A TODO xx
@app.route('/todos/<todo_id>')
def get_todo(todo_id):
    try:
        todo = findOne('todosapi', 'id', todo_id)
        if todo:
            return{'todo':todo}, 200
        return {"message":"todo not found"}, 404
    except TypeError as ex:
        return{"message":"{}".format(ex)}, 500

## ADD A TODO xx
@app.route("/todos", methods=['post'])
def add_todo():
    title = (request.json['title']).strip()
    if title != "":
        try:
            if not findOne('todosapi', 'title', title):
                conn = Connect()
                cursor = conn.cursor()

                sql = f"INSERT INTO todosapi(title,completed) VALUES('{title}', '0')"
                cursor.execute(sql)
                conn.commit()
                
                todo=findOne('todosapi', 'title', title)
                return {"todo":todo},201
            return {"message":"todo already exist! Add another one"},403
        except :
            return{"message":"An error occured"}, 500
    return {"message":"title is required"}, 403


## UPDATE A TODO
@app.route("/todos/<int:todo_id>", methods=['put'])
def update_todo(todo_id):
    title = (request.json['title']).strip()
    if title != "":
            if findOne('todosapi', 'id', todo_id):
                if not findOne('todosapi', 'title', title):
                    conn = Connect()
                    cursor = conn.cursor()

                    sql = f"UPDATE todosapi SET title='{title}' WHERE id = '{todo_id}'"
                    cursor.execute(sql)
                    conn.commit()
                    
                    todo=findOne('todosapi', 'id', todo_id)
                    return {"todo":todo},201
                return{"message":"Todo already exist! choose another title"}
            return {"message":"todo not found"},403

    return {"message":"title is required"}, 403


## GET COMPLETED TODO
@app.route("/todos/complete")
def get_complete_todo():
    try:
        todo=findCompleted()
        if not todo:
            return{"todos":[]}
        return{"todos":todo}, 200
    except TypeError as ex:
        return{"message":"{}".format(ex)}, 500

## GET INCOMPLETED TODO
@app.route("/todos/incomplete")
def get_incomplete_todo():
    try:
        todo=findIncompleted()
        if not todo:
            return{"todos":[]}
        return{"todos":todo}, 200
    except TypeError as ex:
        return{"message":"{}".format(ex)}, 500

## COMPLETE A TODO
@app.route("/todos/complete/<int:todo_id>", methods=['post'])
def complete_todo(todo_id):
    if todo_id:
            if findOne('todosapi', 'id', todo_id):
                conn = Connect()
                cursor = conn.cursor()

                sql = f"UPDATE todosapi SET completed = 1 WHERE id = {todo_id}"
                cursor.execute(sql)
                conn.commit()
                
                todo=findOne('todosapi', 'id', todo_id)
                return{"todo":todo}, 200
            return {"message":"todo not found"},403

    return {"message":"id is required"}, 403


if __name__ == '__main__':
    app.run(Debug=True)