from config.database import connect
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

users_collection = connect('users')


async def register(user):
    data = dict(user, **{"role": "customer"})
    document = await users_collection.find_one({"username": data["username"]})

    if document:
        raise HTTPException(status_code=409, detail='user already registered')
    await users_collection.insert_one(data)


async def register_admin(data, user):
    if user['role'] == 'admin':
        data = dict(data, **{"role": "admin"})
        document = await users_collection.find_one({"username": data["username"]})

        if document:
            raise HTTPException(
                status_code=409, detail='user already registered')
        await users_collection.insert_one(data)
    else:
        raise HTTPException(status_code=403, detail='access denied')


async def update_data_customer(id, data):
    data = dict(data)
    try:
        document = await users_collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id not correct")
    if not document:
        raise HTTPException(status_code=404, detail="Item not found")

    await users_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    data = await users_collection.find_one({"_id": ObjectId(id)})
    data['id'] = str(data['_id'])
    del[data['_id']]

    return data


async def ban(id, status, user):
    user_data = await users_collection.find_one({"_id": ObjectId(id)})
    print(f"=== USER : {user}")
    print(f"=== USER_DATA : {user_data['role']}")
    if user['role'] == 'admin':
        if user_data['role'] == 'customer':
            update = await users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
        else:
            raise HTTPException(status_code=403, detail='Not allowed ')
    else:
        raise HTTPException(
            status_code=403, detail='not allowed you not admin')


async def delete_data(id, user):
    if user['role'] == 'admin':
        try:
            item = await users_collection.find_one({"_id": ObjectId(id)})
        except InvalidId:
            raise HTTPException(status_code=422, detail='id not correct')
        if not item:
            raise HTTPException(status_code=404, detail='item not found')

        await users_collection.find_one_and_delete({"_id": ObjectId(id)})

    else:
        raise HTTPException(
            status_code=403, detail='not allowed delete data !')
