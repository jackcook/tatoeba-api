from flask import Flask, jsonify
from flask_mysqldb import MySQL

class Contribution:
    id = 0
    user_id = 0
    sentence_id = 0
    sentence_lang = ""
    text = ""
    action = ""
    type = ""
    timestamp = ""
    user = None
    
    def __init__(self, row):
        self.id = row[11]
        self.sentence_id = row[0]
        self.sentence_lang = row[1]
        self.text = row[5].decode("utf-8")
        self.action = row[6]
        self.type = row[10]
        self.timestamp = row[8].isoformat()
    
    def dict(self):
        return {
            "id": self.id,
            "sentence_id": self.sentence_id,
            "sentence_lang": self.sentence_lang,
            "text": self.text,
            "action": self.action,
            "type": self.type,
            "timestamp": self.timestamp,
            "user": self.user.dict()
        }

class User:
    id = 0
    username = ""
    image = ""
    
    def __init__(self, row):
        self.id = row[0]
        self.username = row[1]
        self.image = row[14]
    
    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "image": self.image
        }

app = Flask(__name__)
sql = MySQL()

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "tatoeba"
app.config["MYSQL_HOST"] = "localhost"
sql.init_app(app)

@app.route("/contributions")
def contributions():
    cursor = sql.connection.cursor()
    cursor.execute("SELECT * FROM contributions ORDER BY datetime DESC")
    result = cursor.fetchall()
    contributions = []
    
    for row in result:
        contribution = Contribution(row)
        cursor.execute("SELECT * FROM users WHERE id = %d" % row[7])
        contribution.user = User(cursor.fetchall()[0])
        contributions.append(contribution.dict())
    
    return jsonify(contributions)

if __name__ == "__main__":
    app.run(debug=True)
