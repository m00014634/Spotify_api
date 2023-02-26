from flask import Blueprint
from flask_restx import Resource,Api
from database.models import Song
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os

bp = Blueprint('songs',__name__,url_prefix='/songs')
api= Api(bp)

upload_parser = api.parser()
upload_parser.add_argument('file',location='files',type=FileStorage)
upload_parser.add_argument('song_name',type=str,required = True)
upload_parser.add_argument('artist_id',type=int,required = True)
upload_parser.add_argument('users_id',type=int,required = True)


song_model = api.parser()
song_model.add_argument('new_song_name')

file_model = api.parser()
file_model.add_argument('file',location='files',type=FileStorage)

# All Songs [GET /api/song/all]
@api.route('/song')
class GetAllSongsOrCreate(Resource):
    # Получить все данные песен
    def get(self):
        all_songs = Song.query.all()

        if all_songs:
            result = [{'song_id':i.id,
                       'song_name':i.song_name,
                       'song_likes':i.song_likes,
                       'publshed_date':str(i.published_date),
                       'user_id':i.users_id,
                       'artist_id':i.artist_id}
                      for i in all_songs]

            return result

        return {'status':0,'message':'Нет музыки'}

    # Post Song [POST/api/song/post]
    # Добавить песню
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        artist_song = args.get('file')
        song_name = args.get('song_name')
        published_date = datetime.now()
        artist_id = args.get('artist_id')
        users_id = args.get('users_id')


        filename = secure_filename(artist_song.filename)
        artist_song.save(os.path.join('media/',filename))
        Song().create_music(song_name,published_date,artist_id,users_id,filename)
        return {'status':1,'message':'Музыка успешно добавлена'}


#Exаct Song [GET/ api/song/exect/ {song_id}]
@api.route('/<string:song_name>')
class GetOrChangeOrDeletePostById(Resource):
    # Получить песню
    def get(self,song_name):
        current_song = Song.query.get_or_404(song_name)
        if current_song:

            return {'status':1,'song':{'song_name':current_song.song_name,
                                       'song_likes':current_song.song_likes,
                                       'published_date':str(current_song.published_date),
                                       'artist_id':current_song.artist_id,
                                       'users_id':current_song.users_id,
                                       }}

        return {'status':0,'message':'Музыка не найдена'}

    # Put Song [PUT/api/song/put/{song_id}]
    # Изменить песню
    @api.expect(song_model)
    def put(self,song_name):
        args = song_model.parse_args()
        new_song_name = args.get('new_song_name')
        Song().change_song_name(song_name,new_song_name)

        return {'status':1,'message':'Название песни успешно изменена'}

    # Delete Song [DELETE/api/song/delete/{song_id}]
    # Удалить песню
    def delete(self,song_name):
        current_song = Song.query.get_or_404(song_name)

        if current_song:
            Song.delete_music(current_song,song_name)
            return {'status':1,'message':'Песня успешно удалена'}

        return {'status':0,'message':'Песня не удалена'}

