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
