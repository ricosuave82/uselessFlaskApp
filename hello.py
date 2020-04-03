from flask import Flask, request
from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
api = Api(app=flask_app, version="1.0", title="Ah some app")

name_space = api.namespace('names', description='Main APIs')

model = api.model('Name Model',
                  {'name': fields.String(required=True,
                                         description="Name of the person",
                                         help="Name cannot be blank.")})

list_of_names = {}

@name_space.route("/<int:id>")
class MainClass(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the person'})
    def get(self, id):
        try:
            name = list_of_names[id]
            return {
                "status": "Person retrieved",
                "name": list_of_names[id]
            }
        except KeyError as e:
            name_space.abort(
                500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            name_space.abort(
                400, e.__doc__, status="Could not retrieve information", statusCode="400")

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the person'})
    @api.expect(model)
    def post(self, id):
        try:
            list_of_names[id] = request.json['name']
            return {
                "status": "New person added",
                "name": list_of_names[id]
            }
        except KeyError as e:
            name_space.abort(
                500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            name_space.abort(
                400, e.__doc__, status="Could not save information", statusCode="400")
