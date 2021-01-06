from flask import Flask, request, jsonify;
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'you_will_never_guess'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'todoapp'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['CORS_HEADERS'] = 'Content-Type'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
now = datetime.now()

@app.route('/todo', methods=['POST', 'GET'])
def addTodo():
    cur = mysql.connection.cursor()
    item = request.get_json()['item']
    description = request.get_json()['description']
    status = request.get_json()['status']
    created = datetime.utcnow()

    cur.execute("INSERT INTO todoitems (item, description, status, datetime) VALUES ('" +
    str(item) + "', '" +
    str(description) + "', '" +
    str(status) + "', '" +
    str(created) + "')")

    mysql.connection.commit()

    result = {
        "item" : item,
        "description" : description,
        "status" : status,
        "datetime" : created
    }
    return jsonify({"result": result})




if __name__ == "__main__":
    app.run(debug=True)
