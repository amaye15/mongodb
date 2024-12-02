from api.database.queries import add_document, update_document
from api.models.user import User
from api.models.movies import Movie

from typing import List
from pydantic import BaseModel

# Sample movie data
movies = [
    Movie(
        id="1",
        name="Inception",
        description="A skilled thief is given a chance at redemption if he can successfully perform inception, planting an idea into someone's subconscious.",
        genre=["Sci-Fi", "Action", "Thriller"],
        rating=8.8,
    ),
    Movie(
        id="2",
        name="The Shawshank Redemption",
        description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        genre=["Drama", "Crime"],
        rating=9.3,
    ),
    Movie(
        id="3",
        name="The Godfather",
        description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        genre=["Crime", "Drama"],
        rating=9.2,
    ),
    Movie(
        id="4",
        name="The Dark Knight",
        description="Batman raises the stakes in his war on crime, facing the Joker, a criminal mastermind with a warped sense of humor.",
        genre=["Action", "Crime", "Drama"],
        rating=9.0,
    ),
    Movie(
        id="5",
        name="Pulp Fiction",
        description="The lives of two mob hitmen, a boxer, a gangster, and his wife intertwine in four tales of violence and redemption.",
        genre=["Crime", "Drama"],
        rating=8.9,
    ),
]

# updated_user = await update_document(
#     filter_criteria={"email": user_email},
#     update_data={"favourite_movies": updated_movies},
#     collection_name=collection_name
# )


class Migration:
    def __init__(self, db):
        self.db = db

    async def upgrade(self):

        for movie in movies:
            # print(movie)
            result = await add_document(movie.model_dump(), collection_name="movie")
            print(f"Inserted movie: {result}")
        # Update
        updated_user = await update_document(
            filter_criteria={"id": 0},
            update_data={"favourite_movies": [movies[0].id]},
            collection_name="user",
        )

    async def downgrade(self):
        # Implement the logic to reverse the migration
        for movie in movies:
            result = await self.db["movie"].delete_one({"id": movie.id})
            print(f"Deleted user: {result.deleted_count}")
