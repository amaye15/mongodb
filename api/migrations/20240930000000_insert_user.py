from api.database.queries import add_document
from api.models.user import User


class Migration:
    def __init__(self, db):
        self.db = db

    async def upgrade(self):
        user_test = User(
            id=0,
            first_name="Bob",
            last_name="Marley",
            age=50,
            sex="Male",
            email="bobmarley1890@hotmail.com",
            favourite_movies=[]
        )

        result = await add_document(user_test.model_dump(), collection_name="user")
        print(f"Inserted user: {result}")

    async def downgrade(self):
        # Implement the logic to reverse the migration
        result = await self.db["user"].delete_one({"id": 0})
        print(f"Deleted user: {result.deleted_count}")
