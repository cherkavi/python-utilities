import logging

import werkzeug
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException

import settings

api = Api(version='1.0',
          title='db-react-bridge',
          description='facade with business logic for directories')

log = logging.getLogger(__name__)


# @api.errorhandler(Exception)
# def default_error_handler(e):
#     # log.exception(message)
#     return {'message': 'unexpected exception'}, 500

# @api.errorhandler(NoResultFound)
# def database_not_found_error_handler(e):
#     # log.warning(traceback.format_exc())
#     return {'message': 'no data found'}, 404


for each_code in (list(range(400, 420)) + list(range(501, 520))):
    # class Exception400(HTTPException):
    #     code = 400
    #     # description = ()
    class_exception_by_code: type = type(f'Exception{each_code}',
                                         (HTTPException,),
                                         {"__doc__": f"exception for code {each_code}",
                                          "code": each_code})

    # werkzeug.http.HTTP_STATUS_CODES[402]='xxxx'
    werkzeug.exceptions._aborter.mapping[each_code] = class_exception_by_code

