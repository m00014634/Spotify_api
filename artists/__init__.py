from flask import Blueprint
from flask_restx import Resource,Api
from database.models import Artist


bp = Blueprint('artists',__name__,url_prefix='/artists')
api = Api(bp)


artist_model = api.parser()
artist_model.add_argument('nickname',type = str,required = True)
artist_model.add_argument('user_id',type = int,required = True)

new_artist_model = api.parser()
new_artist_model.add_argument('new_nickname', type = str, required =True )

@api.route('/artist')
class GetAllArtistsOrCreate(Resource):
    # Создать артиста
    @api.expect(artist_model)
    def post(self):
        args = artist_model.parse_args()
        nickname = args.get('nickname')
        user_id = args.get('user_id')


        Artist().register_artist(nickname,user_id)
        return {'status': 1, 'message': 'Артист успешно создан'}


    # Получить всех артистов
    def get(self):
        all_artists = Artist.query.all()

        if all_artists:
            result = [{'artist_id':i.id,
                       'nickname':i.nickname,
                       'subscribes':i.artist_subscribes,
                       'user_id':i.user_id}
                      for i in all_artists]
            return {'status':1,'message':result}

        return {'status':0,'message':'Артистов пока нет'}


@api.route('/<int:artist_id>')
class GetOrChangeArtistById(Resource):
    def get(self,artist_id):
        current_artist = Artist.query.get_or_404(artist_id)
        if current_artist:
            return {'status':1,'artist': {'nickname':current_artist.nickname,'subscribes':current_artist.artist_subscribes}}

        return {'status':0,'message':'Артист не найден'}

    @api.expect(new_artist_model)
    def put(self,artist_id):
        args = new_artist_model.parse_args()
        new_nickname = args.get('new_nickname')
        Artist().change_artist(artist_id,new_nickname)
        return {'status':1,'message':'Никнейм артиста успешно изменено'}