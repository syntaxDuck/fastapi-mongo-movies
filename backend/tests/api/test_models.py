from datetime import datetime

from api.models import Comment, CommentQuery, Movie, MovieQuery, User, UserQuery
from bson import ObjectId


class TestMovieModel:
    """Test cases for Movie model."""

    def test_movie_from_mongo_valid(self):
        """Test creating Movie from MongoDB document."""
        mongo_data = {
            "_id": ObjectId(),
            "title": "Test Movie",
            "plot": "Test plot",
            "genres": ["Drama"],
            "runtime": 120,
            "cast": ["Actor 1", "Actor 2"],
            "countries": ["USA"],
            "released": datetime.now(),
            "directors": ["Director 1"],
            "awards": {"nominations": 0, "text": "N/A", "wins": 0},
            "lastupdated": datetime.now(),
            "year": 2023,
            "type": "movie",
            "imdb": {"rating": 8.0, "votes": 1000},
            "tomatoes": {"viewer": {"rating": 4.0, "numReviews": 100}},
        }

        movie = Movie.from_mongo(mongo_data)
        assert movie.title == "Test Movie"
        assert isinstance(movie.id, str)
        assert movie.plot == "Test plot"

    def test_movie_validate_id_objectid(self):
        """Test Movie.validate_id with ObjectId."""
        obj_id = ObjectId()
        result = Movie.validate_id(obj_id)
        assert isinstance(result, str)

    def test_movie_validate_id_string(self):
        """Test Movie.validate_id with string."""
        test_str = "test_string"
        result = Movie.validate_id(test_str)
        assert result == test_str


class TestUserModel:
    """Test cases for User model."""

    def test_user_from_mongo_valid(self):
        """Test creating User from MongoDB document."""
        mongo_data = {
            "_id": ObjectId(),
            "name": "Test User",
            "password": "hashed_password",
            "email": "test@example.com",
        }

        user = User.from_mongo(mongo_data)
        assert user.name == "Test User"
        assert isinstance(user.id, str)
        assert user.email == "test@example.com"

    def test_user_from_mongo_no_email(self):
        """Test creating User from MongoDB document without email."""
        mongo_data = {
            "_id": ObjectId(),
            "name": "Test User",
            "password": "hashed_password",
        }

        user = User.from_mongo(mongo_data)
        assert user.name == "Test User"
        assert isinstance(user.id, str)
        assert user.email is None


class TestCommentModel:
    """Test cases for Comment model."""

    def test_comment_from_mongo_valid(self):
        """Test creating Comment from MongoDB document."""
        movie_id = ObjectId()
        mongo_data = {
            "_id": ObjectId(),
            "name": "Test User",
            "email": "test@example.com",
            "movie_id": movie_id,
            "text": "Great movie!",
            "date": datetime.now(),
        }

        comment = Comment.from_mongo(mongo_data)
        assert comment.name == "Test User"
        assert isinstance(comment.id, str)
        assert comment.movie_id == str(movie_id)
        assert comment.text == "Great movie!"

    def test_comment_validate_id_objectid(self):
        """Test Comment.validate_id with ObjectId."""
        obj_id = ObjectId()
        result = Comment.validate_id(obj_id)
        assert isinstance(result, str)

    def test_comment_validate_id_string(self):
        """Test Comment.validate_id with string."""
        test_str = "test_string"
        result = Comment.validate_id(test_str)
        assert result == test_str


class TestQueryModels:
    """Test cases for query model classes."""

    def test_movie_query_defaults(self):
        """Test MovieQuery default values."""
        query = MovieQuery()
        assert query.id is None
        assert query.title is None
        assert query.type is None
        assert query.limit == 10  # Changed from None to 10
        assert query.skip == 0  # Changed from None to 0
        assert query.genres is None
        assert query.runtime is None

    def test_user_query_defaults(self):
        """Test UserQuery default values."""
        query = UserQuery()
        assert query.id is None
        assert query.name is None
        assert query.password is None
        assert query.email is None
        assert query.limit == 10
        assert query.skip == 0

    def test_comment_query_defaults(self):
        """Test CommentQuery default values."""
        query = CommentQuery()
        assert query.id is None
        assert query.name is None
        assert query.email is None
        assert query.movie_id is None
        assert query.limit == 10  # Changed from None to 10
        assert query.skip == 0  # Changed from None to 0


def test_movie_query_with_values():
    """Test MovieQuery with provided values."""
    query = MovieQuery(title="Test Movie", type="movie", limit=5, skip=10)
    assert query.title == "Test Movie"
    assert query.type == "movie"
    assert query.limit == 5
    assert query.skip == 10
