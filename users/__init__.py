from flask import Blueprint
from flask_restx import Resource,Api
from database.models import User

bp = Blueprint('users',__name__,url_prefix='/users')
api = Api(bp)


user_model = api.parser()
user_model.add_argument('first_name',type=str,required =True)
user_model.add_argument('last_name',type=str,required =True)
user_model.add_argument('username',type=str,required = True)
user_model.add_argument('phone_number',type=str,required =True)


new_user_model = api.parser()
new_user_model.add_argument('new_username',type=str,required =True)
new_user_model.add_argument('new_phone_number',type=str,required =True)

@api.route('/user')
class GetAllUsersOrCreate(Resource):

    # Создать пользователя
    @api.expect(user_model)
    def post(self):
        args = user_model.parse_args()
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        username = args.get('username')
        phone_number = args.get('phone_number')
        try:
            User().user_registration(first_name, last_name, username, phone_number)
            return {'status':1,'message':'Пользователь успешно создан'}
        except:
            return {'status':0,'message':'Такое имя пользователя уже существует'}

    # Посмотреть пользователей
    def get(self):
        all_users = User.query.all()
        if all_users:
            result = [{i.id: i.username} for i in all_users]
            return {'status':1,'users':result}
        return []

@api.route('/<int:user_id>')
class GetOrChangeExactUser(Resource):

    # Посмотреть на определенного пользователя
    def get(self,user_id):
        current_user = User.query.get_or_404(user_id)

        if current_user:
            return {'status':1,'user':{'first_name':current_user.first_name,
                                       'last_name':current_user.last_name,
                                       'username':current_user.username,
                                       'phone_number':current_user.phone_number,
                                       'reg_date':str(current_user.reg_date)}}

        return {'status':0,'message':'Пользователь не найден'}

    # Изменение данных определенного пользователя
    @api.expect(new_user_model)
    def put(self,user_id):
        args = new_user_model.parse_args()
        new_username = args.get('new_username')
        new_phone_number = args.get('new_phone_number')
        User().change_username(user_id,new_username)
        User().change_phone_number(user_id,new_phone_number)

        return {'status':1,'message':'Данные пользователя успешно изменены'}