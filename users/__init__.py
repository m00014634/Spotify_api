from flask import Blueprint,request
from flask_restx import Resource,Api


bp = Blueprint('users',__name__,url_prefix='/users')
api = Api(bp)


user_model = api.parser()
user_model.add_argument('username',type=str,required = True)
user_model.add_argument('first_name',type=str,required =True)
user_model.add_argument('last_name',type=str,required =True)
user_model.add_argument('phone_number',type=str,required =True)


@api.route('/user')
class GetAllUsersOrCreate(Resource):

    @api.expect(user_model)
    def post(self):
        args = user_model.parse_args()
        username = args.get('username')
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        phone_number = args.get('phone_number')


