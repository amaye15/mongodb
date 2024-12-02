from typing import Dict, List, Optional
from api.database.database_manager import database
from bson import ObjectId


async def add_document(document: Dict, collection_name: str):
    collection = database[collection_name]

    # Insert a dummy document to ensure the database is registered
    result = await collection.insert_one(document)

    return result


async def update_document(
    filter_criteria: Dict, update_data: Dict, collection_name: str, upsert: bool = False
) -> Optional[Dict]:
    """
    Updates a document in the specified collection based on the filter criteria using motor.

    Parameters:
    - filter_criteria (Dict): The filter to identify the document(s) to update.
    - update_data (Dict): The data to update in the document(s).
    - collection_name (str): The name of the collection.
    - upsert (bool): If True, inserts the document if it does not exist. Default is False.

    Returns:
    - Optional[Dict]: The updated document if found and modified, otherwise None.
    """
    collection = database[collection_name]

    # MongoDB requires that update operations be wrapped in `$set` to update fields
    update_operation = {"$set": update_data}

    # Use `find_one_and_update` to get the updated document after modification
    result = await collection.find_one_and_update(
        filter_criteria,
        update_operation,
        upsert=upsert,
        return_document=True,  # motor uses `True` instead of `ReturnDocument.AFTER`
    )

    return result


async def get_user(
    user_id: str,
    user_collection_name: str = "user",
    movie_collection_name: str = "movie",
):
    """
    Retrieve a user from the MongoDB collection by their ID.

    Args:
        user_id (str): The ID of the user to retrieve.
        collection_name (str): The name of the collection (default is "user").

    Returns:
        dict: The user document if found, or None if no user exists with the given ID.
    """
    user_collection = database[user_collection_name]
    movie_collection = database[movie_collection_name]

    # Fetch the user from the collection
    user = await user_collection.find_one({"id": user_id})

    movie_list = user.favourite_movies

    results = []

    for val in movie_list:

        res = await movie_collection.find_one({"id": val})

        results.append(res)

    return user


# TODO

# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId

# # MongoDB connection setup
# MONGO_URI = "mongodb://localhost:27017"
# client = AsyncIOMotorClient(MONGO_URI)
# database = client["your_database_name"]

# async def get_user_with_favourite_movies(user_id: str):
#     """
#     Fetch user details along with favorite movie details using $lookup.

#     Args:
#         user_id (str): The ID of the user to fetch.

#     Returns:
#         dict: User with favorite movie details.
#     """
#     try:
#         # Convert user_id to ObjectId
#         user_id = ObjectId(user_id)
#     except Exception as e:
#         print(f"Invalid user_id format: {e}")
#         return None

#     pipeline = [
#         {"$match": {"_id": user_id}},  # Match the specific user
#         {
#             "$lookup": {  # Perform the $lookup operation
#                 "from": "movies",  # The collection to join with
#                 "localField": "favourite_movies",  # Field in 'users' containing the movie IDs
#                 "foreignField": "_id",  # Field in 'movies' to match
#                 "as": "movie_details",  # Output array field for the joined data
#             }
#         }
#     ]

#     collection = database["users"]
#     result = await collection.aggregate(pipeline).to_list(length=1)
#     return result[0] if result else None
