from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from api.models.database import Database


# Replace the placeholder with your Atlas connection string
URI = "mongodb+srv://andrewmayes14:BrjQVlo77dvaPioq@cluster0.ucap6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "Netflix"

# Set the Stable API version when creating a new client
client = AsyncIOMotorClient(URI, server_api=ServerApi("1"))
# client_sync =
database = client["test"]

router = APIRouter()


async def try_connection():
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


@router.post("/create_database", status_code=status.HTTP_201_CREATED)
async def create_database(db_name: Database):
    try:
        # Attempt to connect to MongoDB to ensure it's reachable
        await client.admin.command("ping")
        database = client[db_name.name]
        collection = database["test_collection"]

        # Insert a dummy document to ensure the database is registered
        await collection.insert_one({"initial": "data"})

        return {
            "message": f"Database '{db_name.name}' and test collection created successfully with initial data."
        }

    except ConnectionFailure as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to MongoDB: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


@router.delete("/delete_database", status_code=status.HTTP_204_NO_CONTENT)
async def delete_database(db_name: Database):
    try:
        # Attempt to connect to MongoDB to ensure it's reachable
        await client.admin.command("ping")
        await client.drop_database(db_name.name)
        return {"message": f"Database '{db_name.name}' deleted successfully."}

    except ConnectionFailure as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to MongoDB: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


@router.get("/list_databases", response_model=list, status_code=status.HTTP_200_OK)
async def list_databases():
    try:
        # Attempt to connect to MongoDB to ensure it's reachable
        await client.admin.command("ping")
        # Retrieve the list of database names
        database_names = await client.list_database_names()
        return database_names

    except ConnectionFailure as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to MongoDB: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )
