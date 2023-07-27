from routers.utils.statusCodes import SUCCESS, FAILED
from typing import Dict

NULL_MSG= {
        "statusCode": FAILED,
        "response": "Please Provide all the details"
    }

ADD_MSG={
        "statusCode": SUCCESS,
        "response": "Data Added Successfully"
    }

UPDATE_MSG={
        "statusCode": SUCCESS,
        "response": "Data Updated Successfully"
    }

DELETE_MSG={
        "statusCode": SUCCESS,
        "response": "Deleted Successfully"
    }

EMAIL_SEND={
        "statusCode": SUCCESS,
        "response": "Email Sent Successfully"
    }

SMS_SEND={
        "statusCode": SUCCESS,
        "response": "Sms Sent Successfully"
    }

OTP={
        "statusCode": SUCCESS,
        "response": "OTP Sent Successfully"
    }

NOT_FOUND={
        "statusCode": FAILED,
        "response": "No Data Found",
        'data': []
    }

NOT_ADD={
        "statusCode": FAILED,
        "response": "Data Not Added"
    }

NOT_UPDATE={
        "statusCode": FAILED,
        "response": "Data Not Updated"
    }

NOT_DELETE={
        "statusCode": FAILED,
        "response": "Data Not Deleted"
    }

DEACTIVATE_MSG={
        "statusCode": SUCCESS,
        "response": "Deactivated Successfully"
    }

ACTIVATE_MSG={
        "statusCode": SUCCESS,
        "response": "Activated Successfully"
    }

EXPIRED={
        "statusCode": FAILED,
        "response": "Validity Expired"
    }

INCORRECT_PASSWORD={
        "statusCode": FAILED,
        "response": "Incorrect Username or Password"
    }

ALREADY_EXISTS = {
    'statusCode': SUCCESS,
    'response': 'Data Already Exists'
}

FOUND = {
    'statusCode': SUCCESS,
    'response': 'Data Found'
}

WELCOME_MESSAGE = {
    'statusCode': SUCCESS,
    'response': 'API Running successfully Yashwanth'
}
