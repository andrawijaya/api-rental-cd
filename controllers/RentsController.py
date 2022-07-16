
from config.database import connect
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

movies_collection = connect('movies')
rents_collection = connect('rents')


async def rent_movie(id, data, user):
    data = dict(data)
    if user['role'] == 'customer':
        movie = await movies_collection.find_one({"_id": ObjectId(id)})
        new_data = {
            'title': movie['title'],
            'release': movie['release'],
            'gendre': movie['gendre'],
            'quantity': 1,
            'movie_id': ObjectId(id),
            'user_id': user['_id']
        }

        if movie['stock'] > 0:
            new_stock = movie['stock'] - 1
            order = await rents_collection.insert_one(new_data)
            await movies_collection.update_one({"_id": ObjectId(id)}, {'$set': {'stock': new_stock}})

            return order
        else:
            raise HTTPException(
                status_code=409, detail='cant order stock habis')
    else:
        raise HTTPException(status_code=403, detail='access denied !')


async def get_rent_history(id, user):
    items = []
    if user['role'] == 'customer':
        datas = rents_collection.find({'user_id': {"$eq": ObjectId(id)}})

        async for data in datas:
            data['user_id'] = str(data['user_id'])
            data['movie_id'] = str(data['movie_id'])
            data['_id'] = str(data['_id'])
            items.append(data)

    else:
        raise HTTPException(status_code=403, detail='access denied!')

    return items
