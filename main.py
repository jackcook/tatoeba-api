from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from models import *

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
