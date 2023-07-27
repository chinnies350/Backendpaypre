from collections.abc import Callable
from routers.utils.statusCodes import FAILED
from typing import Dict

def handleError(error, callback: Callable) -> Dict:
    return  {'statusCode': FAILED ,
                'response' :callback(str(error))}