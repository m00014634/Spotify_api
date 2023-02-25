from main import db


# User's table

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=False,unique =True)
    phone_number = db.Column(db.String,nullable = False,unique =True)


    # Create user
    def user_registration(self,first_name,last_name,username,phone_number):
        new_user = User(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()


    # Change username
    def change_username(self,user_id,new_username):
        user = User.query.get_or_404(user_id)
        if user.username == new_username:
            return 'Новое имя должно отличаться от старого'
        user.username = new_username
        db.session.commit()

    # Change phone number
    def change_phone_number(self,user_id,new_phone_number):
        user = User.query.get_or_404(user_id)
        if user.phone_number == new_phone_number:
            return 'Новый номер должен отличаться от старого'
        user.phone_number = new_phone_number
        db.session.commit()