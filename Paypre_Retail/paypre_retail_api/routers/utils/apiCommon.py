from routers.utils.errorHandling import handleError
from routers.utils.statusCodes import FAILED
from routers.utils.responseMessages import NOT_ADD, ADD_MSG, ALREADY_EXISTS, NOT_UPDATE, UPDATE_MSG, DELETE_MSG, NOT_DELETE, NOT_FOUND, FOUND
import json
import pyodbc
from aioodbc.cursor import Cursor
from typing import List, Tuple, Optional, Dict
from collections.abc import Callable
from pydantic import ValidationError

async def ApiWithProcedure(db: Cursor, query: str, additionalFunction: Callable, queryParams: Optional[Tuple]='') -> Dict:
    try:
        print('queryParams', queryParams)
        print(f"""{query}""", queryParams)
        await db.execute(f"""{query}""", queryParams)
        res:List = await db.fetchall()
        return additionalFunction(res)
    except pyodbc.Error as pe:
         print(str(pe))
         return {
              'response': 'DataBase error ',
              'statusCode': FAILED
         }
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)

async def ApiWithProcedureTrans(db: Cursor, query: str, request: any,transformParam: Callable, additionalFunction: Callable) -> Dict:
    try:
        print(f"""{query}""")
        queryParams:Tuple = transformParam(request)
        await db.execute(f"""{query}""", queryParams)
        res:List = await db.fetchall()
        return additionalFunction(res)
    except ValidationError as pe:
        # handle the validation error
        print(f"Validation error for field type {pe.field_type}: {pe.errors()}")
        
        def pydanticError(e) -> str:
            return f"Validation error for field type {pe.field_type}: {pe.errors()}"
        return handleError(pe, pydanticError)
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)
    
async def ApiWithProcedureGet(db: Cursor, query: str, queryParams: Optional[Tuple]='', additionalFunction: Optional[Callable]=None, dataTransform: Optional[Callable]=None) -> Dict:
    try:
        print('queryParams', queryParams)
        print(f"""{query}""", queryParams)
        await db.execute(f"""{query}""", queryParams)
        res: List = await db.fetchall()
        if additionalFunction: 
            return additionalFunction(res,dataTransform if dataTransform else getData)
        else:
             return additionalFunctionGet(res,dataTransform if dataTransform else getData)
    except Exception as e:
        def errorFunc(e):
            return e
        return handleError(e, errorFunc)

def getData(res: str) -> Dict:
    data = FOUND
    data['data'] = json.loads(res) 
    return data

def additionalFunctionGet(res: List, getData: Callable) -> Dict:
        print('res', res)
        if len(res) == 0:
            return NOT_FOUND
        elif res[0][0] != None:
            return getData(res[0][0])
        else: 
            return NOT_FOUND
    
def additionalFunctionPost(res: List) -> Dict:
        if len(res) == 0:
            return ALREADY_EXISTS
        elif res[0][1] == 0:
            return NOT_ADD
        elif res[0][1] == 2:
            return ALREADY_EXISTS
        else: 
            return ADD_MSG

def additionalFunctionPut(res: List) -> Dict:
        if len(res) == 0:
            return NOT_UPDATE
        elif res[0][1] == 0:
            return NOT_UPDATE
        else: 
            return UPDATE_MSG

def additionalFunctionDelete(res: List) -> Dict:
        if len(res) == 0:
            return NOT_DELETE
        elif res[0][1] == 0:
            return NOT_DELETE
        else: 
            return DELETE_MSG
        
