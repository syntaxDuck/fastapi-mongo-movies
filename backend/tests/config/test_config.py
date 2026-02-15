import os
from unittest.mock import patch

from config.Config import Config, config


class TestConfig:
    """Test cases for Config class."""

    def test_config_initialization_defaults(self):
        """Test Config initialization with default values."""
        with patch.dict(os.environ, {}, clear=True):
            # Reload config to test with empty environment
            from importlib import reload

            import config.Config

            reload(config.Config)

            test_config = Config()
            assert test_config.DB_HOST is None
            assert test_config.DB_USER is None
            assert test_config.DB_PASS is None
            assert test_config.API_URL is None
            assert test_config.MOVIE_LIST_PAGE_SIZE == 10
            assert test_config.COMMENT_PAGE_SIZE == 10

    def test_config_initialization_with_env_vars(self):
        """Test Config initialization with environment variables."""
        env_vars = {
            "DB_HOST": "test.mongodb.com",
            "DB_USER": "test_user",
            "DB_PASS": "test_password",
            "API_URL": "http://localhost:8000",
        }

        # Create a new config instance with mocked environment
        from unittest.mock import patch

        with patch.dict(os.environ, env_vars, clear=True):
            test_config = Config()
            assert test_config.DB_HOST == "test.mongodb.com"
            assert test_config.DB_USER == "test_user"
            assert test_config.DB_PASS == "test_password"
            assert test_config.API_URL == "http://localhost:8000"
            assert test_config.MOVIE_LIST_PAGE_SIZE == 10
            assert test_config.COMMENT_PAGE_SIZE == 10

    def test_config_dataclass_decorator(self):
        """Test that Config is properly decorated as dataclass."""
        assert hasattr(Config, "__dataclass_fields__")
        assert hasattr(Config, "__annotations__")

    def test_config_instance_creation(self):
        """Test creating a config instance."""
        test_config = Config(
            DB_HOST="test.mongodb.com",
            DB_USER="test_user",
            DB_PASS="test_password",
            API_URL="http://localhost:8000",
        )

        assert test_config.DB_HOST == "test.mongodb.com"
        assert test_config.DB_USER == "test_user"
        assert test_config.DB_PASS == "test_password"
        assert test_config.API_URL == "http://localhost:8000"
        assert test_config.MOVIE_LIST_PAGE_SIZE == 10
        assert test_config.COMMENT_PAGE_SIZE == 10


class TestGlobalConfig:
    """Test cases for global config instance."""

    @patch.dict(
        os.environ,
        {
            "DB_HOST": "global.mongodb.com",
            "DB_USER": "global_user",
            "DB_PASS": "global_password",
            "API_URL": "http://api.example.com",
        },
    )
    def test_global_config_instance(self):
        """Test the global config instance."""
        # Note: This test depends on the actual environment variables
        # when the module was first loaded
        assert hasattr(config, "DB_HOST")
        assert hasattr(config, "DB_USER")
        assert hasattr(config, "DB_PASS")
        assert hasattr(config, "API_URL")
        assert hasattr(config, "MOVIE_LIST_PAGE_SIZE")
        assert hasattr(config, "COMMENT_PAGE_SIZE")
        assert config.MOVIE_LIST_PAGE_SIZE == 10
        assert config.COMMENT_PAGE_SIZE == 10
