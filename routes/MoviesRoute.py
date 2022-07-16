from turtle import update
from fastapi import APIRouter, Depends

from models.MoviesModel import MovieSchema, RateSchema
from controllers.MoviesController import add_data, update_data, rate_revew_data, remove_review


from fastapi_login import LoginManager
from config.database import connect

movies_router = APIRouter(prefix="/api/movies")

users_collection = connect('users')

SECRET = "super-secret-key"
manager = LoginManager(SECRET, token_url='/api/users/login')


@manager.user_loader()
async def query_user(username):
    document = await users_collection.find_one({'username': username})
    return document


@movies_router.post('/')
async def admin_add_movie(data: MovieSchema, user=Depends(manager)):
    await add_data(data, user)
    return {
        "status": "success",
        "description": "data movies add to db",
        "data": data
    }


@movies_router.put('/{id}')
async def admin_update_movie(id: str, data: MovieSchema, user=Depends(manager)):
    data = await update_data(id, data, user)
    return{
        "status": "success",
        "description": "data updated !",
        "data": data
    }


@movies_router.post('/{id}')
async def customer_rating_review(id: str, data: RateSchema, user=Depends(manager)):
    await rate_revew_data(id, data, user)
    return {
        "status": "success",
        "description": "Movie has be reviews dan rate !",

    }


@movies_router.delete('/{id}')
async def admin_remove_review(id: str, user=Depends(manager)):
    await remove_review(id, user)
    return {
        "status": "success",
        "description": "reviews dan been removed !",

    }
