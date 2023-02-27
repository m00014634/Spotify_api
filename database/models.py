from main import db
from datetime import datetime

# User's table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,autoincrement = True)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=False,primary_key=True,unique =True)
    password = db.Column(db.String,nullable = False)
    phone_number = db.Column(db.String,nullable = False,unique =True)
    reg_date = db.Column(db.DateTime,default = datetime.now())


    # Create user
    def user_registration(self,first_name,last_name,username,password,phone_number):
        new_user = User(first_name=first_name,last_name=last_name,username=username,password=password,phone_number=phone_number)
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
    id = db.Column(db.Integer,autoincrement=True)
    song_name = db.Column(db.String,primary_key=True,nullable = False)
    song_likes = db.Column(db.Integer,nullable = True , default = 0)
    published_date = db.Column(db.DateTime)


    artist_id = db.Column(db.Integer,db.ForeignKey('artists.id',ondelete = 'SET NULL'))


    user = db.relationship('User')
    artist = db.relationship('SongSettings')



    # Create music
    def create_music(self,song_name,published_date,artist_id,users_id,music):
        new_song = Song(song_name=song_name,published_date=published_date,artist_id=artist_id,users_id=users_id)
        song_for_artist = SongSettings()
        song_for_artist.song_path = f'music/{music}'
        self.artist.append(song_for_artist)
        db.session.add(new_song)
        db.session.add(song_for_artist)
        db.session.commit()

    def change_song_name(self,song_name,new_song_name):
        current_song_name = Song.query.get_or_404(song_name)

        if current_song_name == new_song_name:
            return 'Старое название песни должно отличаться от старого'
        current_song_name.song_name = new_song_name
        db.session.commit()

    def delete_music(self,song_name):
        current_song = Song.query.get_or_404(song_name)
        db.session.delete(current_song)
        db.session.commit()



class SongSettings(db.Model):
    __tablename__ = 'songs_to_settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_path = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('songs.id', ondelete='SET NULL'))



