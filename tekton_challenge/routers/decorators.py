from functools import wraps

from fastapi import HTTPException
from requests import HTTPError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from tekton_challenge.repositories.errors import NotFoundError


def error_handler(func):
    """
    Decorator to handle errors in the router calls and return the common responses
    :param func: router function
    :return: router function response or HttpException with the corresponding error message
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundError as pn:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(pn))
        except HTTPError as he:
            response = he.response
            raise HTTPException(status_code=response.status_code, detail=str(response.json()))
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return wrapper
