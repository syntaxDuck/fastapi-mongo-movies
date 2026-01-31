import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from pymongo.errors import PyMongoError, ConnectionFailure, ServerSelectionTimeoutError
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

from backend.database import MongoDBConfig, MongoDBClientHandler


class TestMongoDBConfigExtended:
    """Extended test cases for MongoDBConfig class covering edge cases."""

    @pytest.mark.database
    def test_config_with_complex_options(self):
        """Test configuration with complex connection options."""
        config = MongoDBConfig(
            username="user@domain.com",
            password="p@ssw0rd!#",
            host="cluster.mongodb.net",
            tls="true",
            tlsAllowInvalidCertificates="true",
            retryWrites="true",
            w="majority",
            readPreference="secondaryPreferred",
            appName="MyApp",
            connectTimeoutMS="30000",
            socketTimeoutMS="45000",
        )

        uri = config.get_db_uri()
        assert (
            "mongodb+srv://user%40domain.com:p%40ssw0rd%21%23@cluster.mongodb.net/"
            in uri
        )
        assert "tls=true" in uri
        assert "retryWrites=true" in uri
        assert "w=majority" in uri
        assert "readPreference=secondaryPreferred" in uri

    @pytest.mark.database
    def test_config_unicode_credentials(self):
        """Test configuration with unicode characters in credentials."""
        config = MongoDBConfig(
            username="üñîçødë_usér",
            password="pässwörd_ñümérîc_123",
            host="test.mongodb.com",
        )

        uri = config.get_db_uri()
        assert (
            "%C3%BC%C3%B1%C3%AE%C3%A7%C3%B8d%C3%AB_us%C3%A9r" in uri
        )  # URL encoded unicode

    @pytest.mark.database
    def test_config_empty_options(self):
        """Test configuration with empty options dictionary."""
        config = MongoDBConfig(
            username="test_user",
            password="test_password",
            host="test.mongodb.com",
            **{},
        )

        uri = config.get_db_uri()
        expected = "mongodb+srv://test_user:test_password@test.mongodb.com/"
        assert uri == expected

    @pytest.mark.database
    def test_config_boolean_options(self):
        """Test configuration with boolean options."""
        config = MongoDBConfig(
            username="test_user",
            password="test_password",
            host="test.mongodb.com",
            ssl=True,
            retryWrites=False,
        )

        uri = config.get_db_uri()
        assert "ssl=True" in uri
        assert "retryWrites=False" in uri


class TestMongoDBClientHandlerExtended:
    """Extended test cases for MongoDBClientHandler covering error scenarios."""

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_client_setter_with_new_config(self):
        """Test client setter with new configuration."""
        old_config = MongoDBConfig("old_user", "old_pass", "old_host.com")
        new_config = MongoDBConfig("new_user", "new_pass", "new_host.com")

        handler = MongoDBClientHandler(old_config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client

            # Set initial client
            await handler.client

            # Set new config
            handler._config = new_config

            assert handler._config == new_config
            mock_client.close.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_connection_with_invalid_credentials(self):
        """Test connection failure due to invalid credentials."""
        config = MongoDBConfig("invalid_user", "invalid_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.side_effect = ConnectionFailure(
                "Authentication failed"
            )
            mock_client_class.return_value = mock_client

            client = await handler.client
            assert client is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_server_timeout_error(self):
        """Test server timeout during connection."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.side_effect = ServerSelectionTimeoutError(
                "Server timeout"
            )
            mock_client_class.return_value = mock_client

            client = await handler.client
            assert client is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_ping_server_without_client(self):
        """Test ping server when client is not initialized."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)
        handler._client = None

        with patch.object(handler, "_initialize_client") as mock_init:
            await handler.ping_server()
            mock_init.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_list_databases_without_client(self):
        """Test list databases when client is not initialized."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)
        handler._client = None

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.list_database_names.return_value = ["db1", "db2"]
            mock_client_class.return_value = mock_client

            databases = await handler.list_databases()
            assert databases == ["db1", "db2"]

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_fetch_documents_with_complex_filter(self):
        """Test fetching documents with complex filter query."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            mock_collection = AsyncMock()
            mock_cursor = AsyncMock()
            mock_cursor.to_list.return_value = [
                {"_id": ObjectId(), "title": "Test Movie"}
            ]
            mock_collection.find.return_value.skip.return_value.limit.return_value = (
                mock_cursor
            )
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            # Complex filter query
            filter_query = {
                "year": {"$gte": 2020, "$lte": 2023},
                "genres": {"$in": ["Drama", "Action"]},
                "imdb.rating": {"$gte": 8.0},
                "$or": [{"type": "movie"}, {"type": "series"}],
            }

            documents = await handler.fetch_documents(
                database_name="test_db",
                collection_name="movies",
                filter_query=filter_query,
                limit=20,
                skip=10,
            )

            assert len(documents) == 1
            mock_collection.find.assert_called_once_with(filter_query)

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_insert_documents_with_list_input(self):
        """Test inserting multiple documents as a list."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            mock_collection = AsyncMock()
            mock_result = AsyncMock()
            mock_result.inserted_ids = [ObjectId(), ObjectId()]
            mock_collection.insert_one.return_value = mock_result
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            documents = [
                {"name": "User 1", "email": "user1@example.com"},
                {"name": "User 2", "email": "user2@example.com"},
            ]

            result = await handler.insert_documents(
                database_name="test_db", collection_name="users", documents=documents
            )

            assert result == mock_result
            # Should call insert_one with the first document (based on current implementation)

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_insert_documents_connection_failure(self):
        """Test document insertion when connection fails."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.__getitem__.side_effect = PyMongoError("Connection lost")
            mock_client_class.return_value = mock_client

            result = await handler.insert_documents(
                database_name="test_db",
                collection_name="users",
                documents={"name": "Test User"},
            )

            assert result is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_update_documents_no_matches(self):
        """Test document update with no matching documents."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            mock_collection = AsyncMock()
            mock_result = AsyncMock()
            mock_result.matched_count = 0
            mock_result.modified_count = 0
            mock_collection.update_many.return_value = mock_result
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            result = await handler.update_documents(
                database_name="test_db",
                collection_name="users",
                filter_query={"email": "nonexistent@example.com"},
                update_query={"$set": {"name": "Updated"}},
            )

            assert result == mock_result
            assert result.matched_count == 0

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_update_documents_database_error(self):
        """Test document update with database error."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.__getitem__.side_effect = PyMongoError("Update failed")
            mock_client_class.return_value = mock_client

            result = await handler.update_documents(
                database_name="test_db",
                collection_name="users",
                filter_query={"_id": ObjectId()},
                update_query={"$set": {"name": "Updated"}},
            )

            assert result is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_delete_documents_no_matches(self):
        """Test document deletion with no matching documents."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            mock_collection = AsyncMock()
            mock_result = AsyncMock()
            mock_result.deleted_count = 0
            mock_collection.delete_many.return_value = mock_result
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            result = await handler.delete_documents(
                database_name="test_db",
                collection_name="users",
                filter_query={"email": "nonexistent@example.com"},
            )

            assert result == mock_result
            assert result.deleted_count == 0

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_delete_documents_database_error(self):
        """Test document deletion with database error."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.__getitem__.side_effect = PyMongoError("Delete failed")
            mock_client_class.return_value = mock_client

            result = await handler.delete_documents(
                database_name="test_db",
                collection_name="users",
                filter_query={"_id": ObjectId()},
            )

            assert result is None

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_context_manager_with_exception(self):
        """Test async context manager with exception during operations."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client_class.return_value = mock_client

            try:
                async with MongoDBClientHandler(config) as handler:
                    assert handler._client == mock_client
                    raise ValueError("Test exception")
            except ValueError:
                pass  # Expected exception

            mock_client.close.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_close_connection_runtime_error(self):
        """Test closing connection when event loop is not running."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.close.side_effect = RuntimeError("Event loop is closed")
            mock_client_class.return_value = mock_client

            await handler.client  # Initialize client
            await handler.close()  # Should not raise exception

            mock_client.close.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_multiple_concurrent_operations(self):
        """Test multiple concurrent database operations."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None

            mock_collection = AsyncMock()
            mock_cursor = AsyncMock()
            mock_cursor.to_list.return_value = [{"_id": ObjectId(), "title": "Movie 1"}]
            mock_collection.find.return_value.skip.return_value.limit.return_value = (
                mock_cursor
            )
            mock_client.__getitem__.return_value.__getitem__.return_value = (
                mock_collection
            )

            mock_client_class.return_value = mock_client

            # Create multiple concurrent operations
            tasks = [
                handler.fetch_documents("test_db", "test_collection", limit=5),
                handler.fetch_documents("test_db", "test_collection", skip=10),
                handler.fetch_documents(
                    "test_db", "test_collection", filter_query={"test": "value"}
                ),
            ]

            results = await asyncio.gather(*tasks)

            assert len(results) == 3
            assert all(len(result) == 1 for result in results)

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_databases_property_caching(self):
        """Test that databases property caches results properly."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.admin.command.return_value = None
            mock_client.list_database_names.return_value = ["db1", "db2", "db3"]
            mock_client_class.return_value = mock_client

            # First call should populate cache
            databases1 = await handler.databases
            assert databases1 == ["db1", "db2", "db3"]

            # Second call should use cache (not call list_database_names again)
            databases2 = await handler.databases
            assert databases2 == ["db1", "db2", "db3"]

            # Should only call list_database_names once
            mock_client.list_database_names.assert_called_once()

    @pytest.mark.database
    @pytest.mark.asyncio
    async def test_client_property_reinitialization(self):
        """Test that client property reinitializes when client is None."""
        config = MongoDBConfig("test_user", "test_pass", "test.mongodb.com")
        handler = MongoDBClientHandler(config)

        with patch("backend.database.AsyncIOMotorClient") as mock_client_class:
            mock_client1 = AsyncMock()
            mock_client1.admin.command.return_value = None
            mock_client2 = AsyncMock()
            mock_client2.admin.command.return_value = None

            # Return different clients on subsequent calls
            mock_client_class.side_effect = [mock_client1, mock_client2]

            # First client initialization
            client1 = await handler.client
            assert client1 == mock_client1

            # Simulate client becoming None and reinitialize
            handler._client = None
            client2 = await handler.client
            assert client2 == mock_client2

            assert mock_client_class.call_count == 2
