from unittest.mock import AsyncMock, patch

import pytest
from bson import ObjectId
from pymongo.errors import PyMongoError

from backend.database import MongoDBClientHandler, MongoDBConfig


class TestMongoDBConfig:
    """Test cases for MongoDBConfig class."""

    @pytest.mark.database
    def test_mongodb_config_initialization(self):
        """Test MongoDBConfig initialization."""
        config = MongoDBConfig(
            username="test_user",
            password="test_password",
            host="test.mongodb.com",
            tls="true",
        )

        assert config._username == "test_user"
        assert config._password == "test_password"
        assert config._host == "test.mongodb.com"
        assert config._options["tls"] == "true"

    @pytest.mark.database
    def test_get_db_uri_without_options(self):
        """Test get_db_uri method without options."""
        config = MongoDBConfig(
            username="test_user", password="test_password", host="test.mongodb.com"
        )

        uri = config.get_db_uri()
        expected = "mongodb+srv://test_user:test_password@test.mongodb.com/"
        assert uri == expected

    @pytest.mark.database
    def test_get_db_uri_with_options(self):
        """Test get_db_uri method with options."""
        config = MongoDBConfig(
            username="test_user",
            password="test_password",
            host="test.mongodb.com",
            tls="true",
            tlsAllowInvalidCertificates="true",
        )

        uri = config.get_db_uri()
        assert "mongodb+srv://test_user:test_password@test.mongodb.com/" in uri
        assert "tls=true" in uri
        assert "tlsAllowInvalidCertificates=true" in uri

    @pytest.mark.database
    def test_get_db_uri_with_special_characters(self):
        """Test get_db_uri method with special characters in credentials."""
        config = MongoDBConfig(
            username="test@user", password="pass/word", host="test.mongodb.com"
        )

        uri = config.get_db_uri()
        assert "test%40user" in uri  # @ should be URL encoded
        assert "pass%2Fword" in uri  # / should be URL encoded


class TestMongoDBClientHandler:
    """Test cases for MongoDBClientHandler class."""

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_client_handler_initialization(self, mock_db_config):
        """Test MongoDBClientHandler initialization."""
        handler = MongoDBClientHandler(mock_db_config)
        assert handler._config == mock_db_config
        assert handler._client is None
        assert handler._databases is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_get_mongo_connection_success(self, mock_db_config):
        """Test successful MongoDB connection."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            client = await handler.client

            assert client == mock_client
            mock_client_class.assert_called_once_with(mock_db_config.get_db_uri())
            mock_client.admin.command.assert_called_once_with("ping")

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_get_mongo_connection_failure(self, mock_db_config):
        """Test MongoDB connection failure."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.side_effect = PyMongoError("Connection failed")
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            client = await handler.client

            assert client is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_ping_server_success(self, mock_db_config):
        """Test successful server ping."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            await handler.client  # Initialize client

            # Should not raise exception
            await handler.ping_server()
            mock_client.admin.command.assert_called_with("ping")

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_ping_server_failure(self, mock_db_config):
        """Test server ping failure."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.side_effect = PyMongoError("Ping failed")
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            await handler.client  # Initialize client

            # Should not raise exception, just print error
            await handler.ping_server()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_list_databases_success(self, mock_db_config):
        """Test successful database listing."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.list_database_names.return_value = ["db1", "db2", "db3"]
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            databases = await handler.databases

            assert databases == ["db1", "db2", "db3"]
            mock_client.list_database_names.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_list_databases_failure(self, mock_db_config):
        """Test database listing failure."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.list_database_names.side_effect = PyMongoError("List failed")
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            databases = await handler.databases

            assert databases == []

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_fetch_documents_success(self, mock_db_config, sample_movie_data):
        """Test successful document fetching."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            # Mock collection and cursor
            mock_collection = AsyncMock()
            mock_cursor = AsyncMock()
            mock_cursor.to_list.return_value = [sample_movie_data]
            mock_collection.find.return_value.skip.return_value.limit.return_value = (
                mock_cursor
            )
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            documents = await handler.fetch_documents(
                database_name="test_db",
                collection_name="test_collection",
                filter_query={"title": "Test Movie"},
                limit=10,
                skip=0,
            )

            assert documents == [sample_movie_data]
            mock_collection.find.assert_called_once_with({"title": "Test Movie"})
            mock_cursor.skip.assert_called_once_with(0)
            mock_cursor.limit.assert_called_once_with(10)

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_fetch_documents_failure(self, mock_db_config):
        """Test document fetching failure."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.__getitem__.side_effect = PyMongoError("Fetch failed")
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            documents = await handler.fetch_documents(
                database_name="test_db", collection_name="test_collection"
            )

            assert documents == []

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_insert_documents_success(self, mock_db_config, sample_user_data):
        """Test successful document insertion."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            # Mock collection and result
            mock_collection = AsyncMock()
            mock_result = AsyncMock()
            mock_result.inserted_id = ObjectId()
            mock_collection.insert_one.return_value = mock_result
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            result = await handler.insert_documents(
                database_name="test_db",
                collection_name="test_collection",
                documents=sample_user_data,
            )

            assert result == mock_result
            mock_collection.insert_one.assert_called_once_with(sample_user_data)

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_insert_documents_failure(self, mock_db_config, sample_user_data):
        """Test document insertion failure."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.__getitem__.side_effect = PyMongoError("Insert failed")
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            result = await handler.insert_documents(
                database_name="test_db",
                collection_name="test_collection",
                documents=sample_user_data,
            )

            assert result is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_update_documents_success(self, mock_db_config):
        """Test successful document update."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            # Mock collection and result
            mock_collection = AsyncMock()
            mock_result = AsyncMock()
            mock_result.matched_count = 1
            mock_result.modified_count = 1
            mock_collection.update_many.return_value = mock_result
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            result = await handler.update_documents(
                database_name="test_db",
                collection_name="test_collection",
                filter_query={"_id": ObjectId()},
                update_query={"$set": {"name": "Updated Name"}},
            )

            assert result == mock_result
            mock_collection.update_many.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_delete_documents_success(self, mock_db_config):
        """Test successful document deletion."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            # Mock collection and result
            mock_collection = AsyncMock()
            mock_result = AsyncMock()
            mock_result.deleted_count = 1
            mock_collection.delete_many.return_value = mock_result
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            result = await handler.delete_documents(
                database_name="test_db",
                collection_name="test_collection",
                filter_query={"_id": ObjectId()},
            )

            assert result == mock_result
            mock_collection.delete_many.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_db_config):
        """Test async context manager functionality."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client_class.return_value = mock_client

            async with MongoDBClientHandler(mock_db_config) as handler:
                assert handler._client == mock_client

            mock_client.close.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_close_connection(self, mock_db_config):
        """Test closing database connection."""
        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.close.return_value = None
            mock_client_class.return_value = mock_client

            handler = MongoDBClientHandler(mock_db_config)
            await handler.client  # Initialize client
            await handler.close()

            mock_client.close.assert_called_once()
