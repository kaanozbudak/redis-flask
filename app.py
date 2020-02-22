from flask import Flask, request
from settings import APP_HOST, APP_PORT, DEBUG
import logging.config
import json
from controllers import controller
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Logging
logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('DATA-MANUFACTURING')


# 0.0.0.0:5000/keys/
class Keys(Resource):
    # if api calls all keys
    def get(self):
        try:
            if request.args.get('filter') is not None:
                request_filter = request.args.get('filter')
                result = controller.get_keys(request_filter)
                logger.info('Getting all with filter -->' + str(request_filter))
            else:
                ###
                # * means get all keys without search expression
                ###
                result = controller.get_keys('*')
                logger.info('Getting all keys')
            _response = {
                "result": result[0],
                "result_type": result[1]
            }
            response = app.response_class(
                response=json.dumps(_response),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            response = app.response_class(
                response='request data wrong --->' + str(e),
                status=400,
                mimetype='application/json'
            )
            logger.error('request data wrong --->' + str(e))
        return response

    # if api creating new key, or updating existing key
    def put(self):
        try:
            request_data = request.get_json()
            key = request_data['key']
            value = request_data['value']
            if request.args.get('expire_in') is not None:
                expire_time = request.args.get('expire_in')  # type --> seconds
                result = controller.set_value_expire_time(key, value, expire_time)
            else:
                result = controller.set_value(key, value)
            _response = {
                "result": result[0],
                "result_type": result[1]
            }
            response = app.response_class(
                response=json.dumps(_response),
                status=201,
                mimetype='application/json'
            )
            logger.info('Putting new key')

        except Exception as e:
            response = app.response_class(
                response='request data wrong --->' + str(e),
                status=400,
                mimetype='application/json'
            )
            logger.error('request data wrong --->' + str(e))
        return response

    # if api calls delete all keys
    def delete(self):
        try:
            result = controller.delete_all_keys()
            _response = {
                "result": result[0],
                "result_type": result[1]
            }
            response = app.response_class(
                response=json.dumps(_response),
                status=200,
                mimetype='application/json'
            )
            logger.info('Deleting all keys')

        except Exception as e:
            response = app.response_class(
                response='request data wrong --->' + str(e),
                status=400,
                mimetype='application/json'
            )
            logger.error('request data wrong --->' + str(e))
        return response


# 0.0.0.0:5000/keys/parameter/
class Key(Resource):
    # if api calls get a key
    def get(self, parameter):
        try:
            result = controller.get_value(parameter)
            if result[0] is not None:
                _response = {
                    "result": result[0],
                    "result_type": result[1]
                }
                response = app.response_class(
                    response=json.dumps(_response),
                    status=200,
                    mimetype='application/json'
                )
                logger.info('Getting a key which -->' + str(parameter))
            else:
                response = app.response_class(
                    response='Not found',
                    status=204,
                    mimetype='application/json'
                )
        except Exception as e:
            response = app.response_class(
                response='request data wrong --->' + str(e),
                status=400,
                mimetype='application/json'
            )
            logger.error('request data wrong --->' + str(e))

        return response

    # if api calls is a key exist
    def head(self, parameter):
        """
            HEAD does not return response body
            200 --> exist
            204 --> no content, do not exist
        """
        try:
            _response = controller.key_exist(parameter)
            response = app.response_class(
                status=_response,
                mimetype='application/json'
            )
            logger.info('Key checking is exist which' + str(parameter))
        except Exception as e:
            response = app.response_class(
                response='request data wrong --->' + str(e),
                status=400,
                mimetype='application/json'
            )
            logger.error('request data wrong --->' + str(e))
        return response

    # if api calls delete a key
    def delete(self, parameter):
        try:
            result = controller.delete_key(parameter)
            _response = {
                "result": bool(result[0]),
                "result_type": result[1]
            }
            response = app.response_class(
                response=json.dumps(_response),
                status=200,
                mimetype='application/json'
            )
            logger.info('Deleting a key which --->' + str(parameter))
        except Exception as e:
            response = app.response_class(
                response='request data wrong --->' + str(e),
                status=400,
                mimetype='application/json'
            )
            logger.error('request data wrong --->' + str(e))
        return response


api.add_resource(Keys, '/keys/')
api.add_resource(Key, '/keys/<string:parameter>/')

if __name__ == '__main__':
    # App host, port, debug mode imported from settings py
    app.run(host=APP_HOST, port=APP_PORT, debug=DEBUG)
