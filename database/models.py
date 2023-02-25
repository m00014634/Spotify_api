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



# Artist's table
class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    nickname = db.Column(db.String,nullable = False)
    artist_subscribes = db.Column(db.Integer,default = 0)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='SET NULL'))

    # Register artist
    def register_artist(self,nickname,user_id):
        artist = Artist(nickname=nickname,user_id = user_id)
        db.session.add(artist)
        db.session.commit()

    # Change artist data
    def change_artist(self,artist_id,new_nickname):
        current_artist_nickname = Artist.query.get_or_404(artist_id)
        if current_artist_nickname == new_nickname:
            return 'Новое имя должно отличаться от старого'
        current_artist_nickname.nickname = new_nickname
        db.session.commit()


    # subsribes
    def  artist_subscribes_detect(self,user_id):
        current_artist = Artist.query.get_or_404(user_id)
        current_artist.artist_subscribes += 1
        db.session.commit()




# Song's table
class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_name = db.Column(db.String,nullable = False)
    song_likes = db.Column(db.Integer,nullable = True , default = 0)
    published_date = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer,db.ForeignKey('artists.id',ondelete = 'SET NULL'))
    users_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete = 'SET NULL'))
    user = db.relationship('User')
    artist = db.relationship('Artist')