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
