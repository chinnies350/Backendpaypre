from routers.utils.statusCodes import SUCCESS, FAILED
from typing import Dict

NULL_MSG: Dict = {
        "statusCode": FAILED,
        "response": "Please Provide all the details"
    }

ADD_MSG: Dict ={
        "statusCode": SUCCESS,
        "response": "Data Added Successfully"
    }

UPDATE_MSG: Dict ={
        "statusCode": SUCCESS,
        "response": "Data Updated Successfully"
    }

DELETE_MSG: Dict ={
        "statusCode": SUCCESS,
        "response": "Deleted Successfully"
    }

EMAIL_SEND: Dict ={
        "statusCode": SUCCESS,
        "response": "Email Sent Successfully"
    }

SMS_SEND: Dict ={
        "statusCode": SUCCESS,
        "response": "Sms Sent Successfully"
    }

OTP: Dict={
        "statusCode": SUCCESS,
        "response": "OTP Sent Successfully"
    }

NOT_FOUND: Dict={
        "statusCode": FAILED,
        "response": "No Data Found",
        'data': []
    }

NOT_ADD: Dict={
        "statusCode": FAILED,
        "response": "Data Not Added"
    }

NOT_UPDATE: Dict={
        "statusCode": FAILED,
        "response": "Data Not Updated"
    }

NOT_DELETE: Dict={
        "statusCode": FAILED,
        "response": "Data Not Deleted"
    }

DEACTIVATE_MSG: Dict={
        "statusCode": SUCCESS,
        "response": "Deactivated Successfully"
    }

ACTIVATE_MSG: Dict={
        "statusCode": SUCCESS,
        "response": "Activated Successfully"
    }

EXPIRED: Dict={
        "statusCode": FAILED,
        "response": "Validity Expired"
    }

INCORRECT_PASSWORD: Dict={
        "statusCode": FAILED,
        "response": "Incorrect Username or Password"
    }

ALREADY_EXISTS: Dict= {
    'statusCode': SUCCESS,
    'response': 'Data Already Exists'
}

FOUND: Dict= {
    'statusCode': SUCCESS,
    'response': 'Data Found'
}

WELCOME_MESSAGE: Dict= {
    'statusCode': SUCCESS,
    'response': 'API Running successfully'
}