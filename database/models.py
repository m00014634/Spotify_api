from main import db


# User's table

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String,nullable = False)


    # Create user
    def user_registration(self,first_name,last_name,username,phone_number):
        new_user = User(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()