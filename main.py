from flask import Flask, jsonify, request
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

class Sentence:
    id = 0
    lang = ""
    text = ""
    user_id = 0
    created_at = ""
    updated_at = ""
    translations = None
    
    def __init__(self, row):
        self.id = row[0]
        self.lang = row[1]
        self.text = row[2]
        self.user_id = row[4]
        self.created_at = row[5]
        self.updated_at = row[6]
    
    def dict(self):
        data = {
            "id": self.id,
            "lang": self.lang,
            "text": self.text.decode("utf-8"),
            "user_id": self.user_id
        }
        
        if self.created_at is not None:
            data["created_at"] = self.created_at.isoformat()
        
        if self.updated_at is not None:
            data["updated_at"] = self.updated_at.isoformat()
        
        if self.translations is not None:
            data["translations"] = self.translations
        
        return data

class Translation:
    id = 0
    sentence_id = 0
    translation_id = 0
    
    def __init__(self, row):
        self.id = row[0]
        self.sentence_id = row[1]
        self.translation_id = row[2]
    
    def dict(self):
        return {
            "id": self.id,
            "sentence_id": self.sentence_id,
            "translation_id": self.translation_id
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

@app.route("/sentences")
def sentences():
    sid = request.args.get("id")
    
    if sid is not None:
        cursor = sql.connection.cursor()
        cursor.execute("SELECT * FROM sentences WHERE id = " + sid)
        data = Sentence(cursor.fetchall()[0]).dict()
        return jsonify(data)
    else:
        query = request.args.get("q")
        offset = request.args.get("offset")
        from_lang = request.args.get("from")
        
        offset_num = 0
        
        try:
            offset_num = int(offset)
        except:
            offset_num = 0
            
        where_languages = ""
        
        if from_lang is not None:
            where_languages = " AND lang = '" + from_lang + "'"
        
        cursor = sql.connection.cursor()
        cursor.execute("SELECT * FROM sentences WHERE text LIKE '%" + query + "%'" + where_languages + " LIMIT 10 OFFSET " + str(offset_num))
        result = cursor.fetchall()
        sentences = []
        
        for row in result:
            sentence = Sentence(row)
            cursor.execute("SELECT * FROM sentences_translations WHERE sentence_id = %d" % sentence.id)
            translations_result = cursor.fetchall()
            translations = []
            
            for translation_row in translations_result:
                translation = Translation(translation_row)
                cursor.execute("SELECT * FROM sentences WHERE id = %d" % translation.translation_id)
                translation_sentence = Sentence(cursor.fetchall()[0])
                translations.append(translation_sentence.dict())
            
            sentence.translations = translations
            sentences.append(sentence.dict())
        
        return jsonify(sentences)

if __name__ == "__main__":
    app.run(debug=True)
