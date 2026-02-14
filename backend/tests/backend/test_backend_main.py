import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from bson import ObjectId

from backend.main import main


class TestBackendMain:
    """Test cases for backend main.py functionality."""

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_successful_execution(self):
        """Test successful execution of backend.main function."""
        # Mock the config and dependencies
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            # Setup config mocks
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            # Mock the MongoDB handler and context manager
            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler

            # Mock the async context manager
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)

            # Mock insert_documents result
            mock_result = MagicMock()
            mock_result.inserted_id = ObjectId()
            mock_handler.insert_documents = AsyncMock(return_value=mock_result)

            # Capture print output
            with patch("builtins.print") as mock_print:
                await main()

                # Verify configuration was created correctly
                mock_config_class.assert_called_once_with(
                    mock_config.DB_USER,
                    mock_config.DB_PASS,
                    mock_config.DB_HOST,
                    appName="Cluster0",
                    tls="true",
                    tlsAllowInvalidCertificates="true",
                    retryWrites="true",
                    w="majority",
                )

                # Verify context manager was used
                mock_handler.__aenter__.assert_called_once()
                mock_handler.__aexit__.assert_called_once()

                # Verify insert_documents was called
                mock_handler.insert_documents.assert_called_once_with(
                    "sample_mflix",
                    "users",
                    {"name": "Roshan", "password": "12345", "email": "r@r.com"},
                )

                # Verify print was called with the result
                mock_print.assert_called_once_with(mock_result)

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_with_config_values(self):
        """Test backend.main function uses correct config values."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            # Setup specific config values
            mock_config.DB_USER = "prod_user"
            mock_config.DB_PASS = "prod_secret"
            mock_config.DB_HOST = "prod-cluster.mongodb.net"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)
            mock_handler.insert_documents = AsyncMock(
                return_value=MagicMock(inserted_id=ObjectId())
            )

            with patch("builtins.print"):
                await main()

                # Verify the correct config values were used
                mock_config_class.assert_called_once_with(
                    "prod_user",
                    "prod_secret",
                    "prod-cluster.mongodb.net",
                    appName="Cluster0",
                    tls="true",
                    tlsAllowInvalidCertificates="true",
                    retryWrites="true",
                    w="majority",
                )

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_database_insertion_failure(self):
        """Test backend.main function when database insertion fails."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)

            # Mock insertion failure
            mock_handler.insert_documents = AsyncMock(
                side_effect=Exception("Insert failed")
            )

            with (
                patch("builtins.print") as mock_print,
                pytest.raises(Exception, match="Insert failed"),
            ):
                await main()

            # Should still attempt the insertion
            mock_handler.insert_documents.assert_called_once()

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_context_manager_exception(self):
        """Test backend.main function when context manager raises exception."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler

            # Mock context manager exception
            mock_handler.__aenter__ = AsyncMock(
                side_effect=Exception("Connection failed")
            )
            mock_handler.__aexit__ = AsyncMock(return_value=None)

            with (
                patch("builtins.print") as mock_print,
                pytest.raises(Exception, match="Connection failed"),
            ):
                await main()

            # Should still attempt to enter context
            mock_handler.__aenter__.assert_called_once()

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_config_error(self):
        """Test backend.main function when config values are missing."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            # Mock missing config values
            mock_config.DB_USER = None
            mock_config.DB_PASS = None
            mock_config.DB_HOST = None

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)
            mock_handler.insert_documents = AsyncMock(
                return_value=MagicMock(inserted_id=ObjectId())
            )

            with patch("builtins.print"):
                await main()

                # Should still call with None values (up to implementation to handle)
                mock_config_class.assert_called_once()
                args, kwargs = mock_config_class.call_args
                assert args[0] is None  # DB_USER
                assert args[1] is None  # DB_PASS
                assert args[2] is None  # DB_HOST

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_different_document_data(self):
        """Test backend.main function with different document data structures."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)

            mock_result = MagicMock()
            mock_result.inserted_id = ObjectId()
            mock_handler.insert_documents = AsyncMock(return_value=mock_result)

            with patch("builtins.print"):
                await main()

                # Verify the specific document data being inserted
                mock_handler.insert_documents.assert_called_once_with(
                    "sample_mflix",
                    "users",
                    {"name": "Roshan", "password": "12345", "email": "r@r.com"},
                )

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_database_names_used(self):
        """Test backend.main function uses correct database and collection names."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)
            mock_handler.insert_documents = AsyncMock(
                return_value=MagicMock(inserted_id=ObjectId())
            )

            with patch("builtins.print"):
                await main()

                # Capture the actual call arguments
                call_args = mock_handler.insert_documents.call_args
                assert call_args[0][0] == "sample_mflix"  # database_name
                assert call_args[0][1] == "users"  # collection_name

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_config_options(self):
        """Test backend.main function passes correct options to MongoDBConfig."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)
            mock_handler.insert_documents = AsyncMock(
                return_value=MagicMock(inserted_id=ObjectId())
            )

            with patch("builtins.print"):
                await main()

                # Verify all expected options are passed
                args, kwargs = mock_config_class.call_args
                expected_kwargs = {
                    "appName": "Cluster0",
                    "tls": "true",
                    "tlsAllowInvalidCertificates": "true",
                    "retryWrites": "true",
                    "w": "majority",
                }

                for key, value in expected_kwargs.items():
                    assert kwargs[key] == value

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_print_output_format(self):
        """Test backend.main function print output format."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)

            # Create a mock result with inserted_id
            test_id = ObjectId()
            mock_result = MagicMock()
            mock_result.inserted_id = test_id
            mock_handler.insert_documents = AsyncMock(return_value=mock_result)

            with patch("builtins.print") as mock_print:
                await main()

                # Verify print was called with the result object
                mock_print.assert_called_once_with(mock_result)

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_no_result_inserted_id(self):
        """Test backend.main function when insertion returns no inserted_id."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)

            # Mock result without inserted_id
            mock_result = MagicMock()
            del mock_result.inserted_id  # Remove the attribute
            mock_handler.insert_documents = AsyncMock(return_value=mock_result)

            with patch("builtins.print") as mock_print:
                await main()

                # Should still print the result even without inserted_id
                mock_print.assert_called_once_with(mock_result)

    @pytest.mark.backend
    def test_main_function_imports(self):
        """Test that main function imports are working correctly."""
        from backend.main import main

        assert callable(main)
        assert asyncio.iscoroutinefunction(main)

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_connection_cleanup(self):
        """Test backend.main function properly cleans up connections."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)
            mock_handler.insert_documents = AsyncMock(
                return_value=MagicMock(inserted_id=ObjectId())
            )

            with patch("builtins.print"):
                await main()

                # Verify context manager cleanup was called
                mock_handler.__aenter__.assert_called_once()
                mock_handler.__aexit__.assert_called_once()

    @pytest.mark.backend
    @pytest.mark.asyncio
    async def test_main_function_user_data_structure(self):
        """Test backend.main function inserts correct user data structure."""
        with (
            patch("backend.main.config") as mock_config,
            patch("backend.main.MongoDBConfig") as mock_config_class,
            patch("backend.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config.DB_USER = "test_user"
            mock_config.DB_PASS = "test_pass"
            mock_config.DB_HOST = "test.mongodb.com"

            mock_db_config = MagicMock()
            mock_config_class.return_value = mock_db_config

            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            mock_handler.__aenter__ = AsyncMock(return_value=mock_handler)
            mock_handler.__aexit__ = AsyncMock(return_value=None)
            mock_handler.insert_documents = AsyncMock(
                return_value=MagicMock(inserted_id=ObjectId())
            )

            expected_user_data = {
                "name": "Roshan",
                "password": "12345",
                "email": "r@r.com",
            }

            with patch("builtins.print"):
                await main()

                # Verify the exact user data structure
                call_args = mock_handler.insert_documents.call_args
                assert call_args[0][2] == expected_user_data
