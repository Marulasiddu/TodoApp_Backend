from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from flask_cors import CORS
from marshmallow import fields
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/todoapp'
db = SQLAlchemy(app)
CORS(app)


###Models####
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    todoDescription = db.Column(db.String(100))
    status = db.Column(db.String(100))
    # created = db.Column(db.DateTime, default=datetime.now())

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,title,todoDescription,status):
        self.title = title
        self.todoDescription = todoDescription
        self.status = status
        # self.created = created
    def __repr__(self):
        return '' % self.id
db.create_all()

class TodoSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Todo
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    todoDescription = fields.String(required=True)
    status = fields.String(required=True)
    # created = fields.String(required=False)
    
@app.route('/todos', methods = ['GET'])
def index():
    get_todos = Todo.query.all()
    todo_schema = TodoSchema(many=True)
    todos = todo_schema.dump(get_todos)
    return make_response(jsonify( todos))
    
@app.route('/maketodo', methods = ['POST'])
def create_todo():
    data = request.get_json()
    todo_schema = TodoSchema()
    todo = todo_schema.load(data)
    result = todo_schema.dump(todo.create())
    return make_response(jsonify({"todo": result}),200)

@app.route('/todos/<id>', methods = ['PUT'])
def update_todo_by_id(id):
    data = request.get_json()
    get_todo = Todo.query.get(id)
    if data.get('title'):
        get_todo.title = data['title']
    if data.get('todoDescription'):
        get_todo.todoDescription = data['todoDescription']
    if data.get('status'):
        get_todo.status = data['status']
    db.session.add(get_todo)
    db.session.commit()
    todo_schema = TodoSchema(only=['id', 'title', 'todoDescription', 'status'])
    todo = todo_schema.dump(get_todo)
    return make_response(jsonify({"todo":todo}))


@app.route('/todos/<id>', methods = ['DELETE'])
def delete_todo_by_id(id):
    get_todo = Todo.query.get(id)
    db.session.delete(get_todo)
    db.session.commit()
    return make_response("todo deleted",204)


if __name__ == "__main__":
    app.run()
    
    