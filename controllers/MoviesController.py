from config.database import connect
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

movies_collection = connect('movies')


async def add_data(data, user):
    if user['role'] == 'admin':
        document = dict(data)
        await movies_collection.insert_one(document)
    else:
        raise HTTPException(status_code=403, detail='not allowed to add data')


async def update_data(id, data, user):
    new_data = dict(data)
    if user['role'] == 'admin':
        try:
            document = await movies_collection.find_one({"_id": ObjectId(id)})
        except InvalidId:
            raise HTTPException(status_code=422, detail='Id not correct')
        if not document:
            raise HTTPException(status_code=404, detail='item not found')

        await movies_collection.update_one({"_id": ObjectId(id)}, {"$set": new_data})

        data = await movies_collection.find_one({"_id": ObjectId(id)})
        data['id'] = str(data['_id'])
        del[data['_id']]

        return data

    else:
        raise HTTPException(
            status_code=403, detail='not allowed update data !')


async def rate_revew_data(id, data, user):
    data = dict(data)
    if user['role'] == 'customer':
        await movies_collection.update_one(
            {"_id": ObjectId(id)},
            {'$set': {
                'ratings': [
                    {'_id': ObjectId(),
                        'user_id': user['_id'], 'rate': data['rating']}
                ],
                'reviews': [
                    {'_id': ObjectId(), 'user_id': user['_id'],
                     'review': data['review']}
                ]
            }})
    else:
        raise HTTPException(status_code=403, detail='not allowed !')


async def remove_review(id, user):
    if user['role'] == 'admin':
        data = await movies_collection.update_many(
            {},
            {
                "$pull": {
                    "reviews": {
                        "_id": ObjectId(id)
                    }
                }
            }

        )
    else:
        raise HTTPException(status_code=403, detail='access denied!')
