from app import db

class User(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

db.create_all()
