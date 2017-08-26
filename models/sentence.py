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
