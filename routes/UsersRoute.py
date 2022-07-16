from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from models.UsersModel import UserSchema
from controllers.UsersController import register, ban, delete_data, update_data_customer, register_admin
from fastapi_login import LoginManager
from config.database import connect


users_router = APIRouter(prefix="/api/users")

users_collection = connect('users')

SECRET = "super-secret-key"
manager = LoginManager(SECRET, token_url='/api/users/login')


@manager.user_loader()
async def query_user(username):
    document = await users_collection.find_one({'username': username})
    return document


@users_router.post("/register")
async def customer_register(user: UserSchema):
    await register(user)
    return {
        "status": "success",
        "description": "inserted",
        "data": user
    }


@users_router.post("/")
async def admin_add_admin(data: UserSchema, user=Depends(manager)):
    await register_admin(data, user)
    return {
        "status": "success",
        "description": "inserted",
        "data": user
    }

# LOGIN


@users_router.post('/login')
async def login_all(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = await query_user(username)

    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        return {
            "status": "failed",
            "description": "wrong password"
        }

    access_token = manager.create_access_token(data={"sub": username})
    return {
        "status": "success",
        "descriptrion": f"login with {user['role']}",
        "access_token": access_token
    }


@users_router.put('/{id}')
async def customer_update_profile(id: str, data: UserSchema):
    document = await update_data_customer(id, data)
    return {
        "status": "success",
        "descriptrion": "data customer updated !",
        "data": document
    }


@users_router.post("/ban")
async def admin_ban_customer(id: str, status: str, user=Depends(manager)):
    document = await ban(id, status, user)
    return {
        "status": "success",
        "description": f"user with ID:{id} has {status}",
    }


@users_router.delete('/{id}')
async def admin_delete_admin(id: str, user=Depends(manager)):
    await delete_data(id, user)
    return {
        "status": "success",
        "description": f"user with ID:{id} has deleted !",
    }
