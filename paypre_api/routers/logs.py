
from fastapi.routing import APIRouter
# from schemas import PostBranch,PutBranch
from aioodbc.cursor import Cursor
from routers.config import get_cursor,logs_collection
from fastapi import Depends
from typing import Optional,List,Dict
from fastapi import Query

router = APIRouter(prefix='/logs', tags=['Logs'])


@router.get('')
async def get_logs(UserId:Optional[int] = Query(None))->Dict:
    try:
        # Execute the MongoDB query
        if UserId:
            logs = logs_collection.find({'user_id': UserId}, {'_id': 0, 'message': 1}).sort('timestamp').limit(5)
        else:
            logs = logs_collection.find({},{'_id': 0, 'message': 1}).sort('timestamp',-1).limit(5)
            
        # Extract the 'message' field from each document
        messages = [{'message': log['message']} for log in logs]
        # messages = logs

        return {
            'statusCode': 1,
            'response':'Data Found',
            'data': messages
        }
    except Exception as e:
        print("Exception Error",str(e))
        return {
            'statusCode': 0,
            'response': str(e),
        }
        
