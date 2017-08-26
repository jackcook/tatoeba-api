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
