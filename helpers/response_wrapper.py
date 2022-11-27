from typing import Any
import helpers.constants as constants

def wrap_response(status: int, error: bool, message: Any = None, data: Any = None) -> object:
    """_summary_

    Args:
        data (Any): The response data to the api
        stauts (int): The status code of the response
        Error (bool): Ture/False to indicte error while processing
        Message (Any): Message associated with the response

    Returns:
        object: The response wrapped in an object
    """
    response = {}
    if data: response[constants.data] = data
    if message: response[constants.message] = message
    response[constants.status] = status
    response[constants.error] = error
    return response