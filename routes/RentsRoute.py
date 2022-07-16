from fastapi import APIRouter, Depends

from models.RentsModel import RentSchema
from controllers.RentsController import rent_movie, get_rent_history


from fastapi_login import LoginManager
from config.database import connect

rents_router = APIRouter(prefix="/api/rents")

users_collection = connect('users')

SECRET = "super-secret-key"
manager = LoginManager(SECRET, token_url='/api/users/login')


@manager.user_loader()
async def query_user(username):
    document = await users_collection.find_one({'username': username})
    return document


@rents_router.post('/{id}')
async def customer_rent_dvd(id: str, data: RentSchema, user=Depends(manager)):
    document = await rent_movie(id, data, user)
    return {
        "status": 'success',
        "description": 'rent movie add !'
    }


@rents_router.get('/{id}')
async def customer_renting_history(id: str, user=Depends(manager)):
    document = await get_rent_history(id, user)
    return {
        "status": 'success',
        "description": f'data rent by ID : {id}',
        'data': document
    }
