from pymongo.errors import PyMongoError
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
)
from urllib.parse import quote, urlencode


class MongoDBConfig:
    """
    A MongoDB configuration object.

    Attributes:
        username (str): The username for the MongoDB connection.
        password (str): The password for the MongoDB connection.
        host (str): The host for the MongoDB connection.
        options (dict): Additional keyword arguments for the MongoDB connection.
    """

    def __init__(self, username: str, password: str, host: str, **kwargs) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._options = kwargs

    def get_db_uri(self) -> str:
        """
        Builds a MongoDB Atlas URI based on the provided configuration.

        Returns:
            str: The MongoDB Atlas URI.
        """
        encoded_username = quote(self._username)
        encoded_password = quote(self._password)

        base_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{self._host}/"

        if self._options:
            query_params = urlencode(self._options)
            base_uri += "?" + query_params

        return base_uri


class MongoDBClientHandler:
    def __init__(self, config: MongoDBConfig) -> None:
        """
        Initializes a MongoDB connection object.

        Args:
            config (MongoDBConfig): The MongoDB configuration object.
        """
        self._config: MongoDBConfig = config
        from typing import Optional
        self._client: Optional[AsyncIOMotorClient] = None
        self._databases: Optional[list[str]] = None

    @property
    async def client(self) -> AsyncIOMotorClient:
        """
        A property that asynchronously establishes a connection to a MongoDB server.

        Returns:
            AsyncIOMotorClient: The established MongoDB client connection.
        """
        if self._client is None:
            await self._initialize_client()
        return self._client
    @client.setter
    async def client(self, config: MongoDBConfig) -> None:
        """
        Asynchronously sets the client configuration and resets the connection.

        Args:
            config (MongoDBConfig): The MongoDB configuration object.
        """
        self._config = config
        if self._client:
            self._client.close()
        self._client = None
        self._client = None

    @property
    async def databases(self) -> list[str]:
        """
        A property that returns a list of all databases in the MongoDB server.

        Returns:
            list: A list of all database names in the server.
        """
        if self._databases is None:
            await self._initialize_client()
            self._databases = await self.list_databases()
        return self._databases

    async def _initialize_client(self) -> None:
        if self._client is None:
            await self._get_db_connection()

    async def _get_db_connection(self) -> None:
        """
        Asynchronously establishes a connection to a MongoDB server.
        """
        uri = self._config.get_db_uri()
        self._client = AsyncIOMotorClient(uri)

        try:
            await self.ping_server()
        except PyMongoError as e:
            print(f"Failed to connect to MongoDB at host '{self._config._host}': {e}")
            self._client = None

    async def ping_server(self) -> None:
        """
        Asynchronously pings a MongoDB server to confirm a successful connection.
        """
        if self._client is None:
            await self._initialize_client()

        try:
            await self._client.admin.command("ping")
            # print("Ping successful...")
        except PyMongoError as e:
            print(f"Ping failed for server {self._config.get_db_uri()}: {e}")

    async def list_databases(self) -> list[str]:
        """
        Asynchronously lists all databases in the MongoDB server.

        Returns:
            list: A list of database names.
        """
        if self._client is None:
            await self._initialize_client()

        try:
            return await self._client.list_database_names()
        except PyMongoError as e:
            print(f"Error listing databases on host '{self._config._host}': {e}")
            return []

    async def fetch_documents(
        self,
        database_name: str,
        collection_name: str,
        filter_query: dict = None,
        limit: int = 10,
        skip: int = 0,
    ) -> list[dict]:
        """
        Asynchronously queries the specified collection and returns the documents.

        Args:
            database_name (str): The database name.
            collection_name (str): The collection name.
            filter_query (dict, optional): The query filter.

        Returns:
            list: A list of documents matching the filter.
        """
        if self._client is None:
            await self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][
                collection_name
            ]
            cursor: AsyncIOMotorCursor = (
                collection.find(filter_query).skip(skip).limit(limit)
            )
            return await cursor.to_list(length=None)
        except PyMongoError as e:
            print(f"Error fetching documents from database '{database_name}', collection '{collection_name}': {e}")
            return []

    async def insert_documents(
        self, database_name: str, collection_name: str, documents: list[dict] | dict
    ):
        if self._client is None:
            await self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][
                collection_name
            ]
            # if isinstance(documents, list):
            #     result = await collection.insert_many(documents)
            # else:
            result = await collection.insert_one(documents)
        except PyMongoError as e:
            print(f"Error inserting documents into database '{database_name}', collection '{collection_name}': {e}")
        finally:
            return result

    async def update_documents(
        self,
        database_name: str,
        collection_name: str,
        filter_query: dict,
        update_query: dict,
    ):
        if self._client is None:
            await self._initialize_client()

        result = None
        try:
            collection: AsyncIOMotorCollection = self._client[database_name][
                collection_name
            ]
            result = await collection.update_many(filter_query, update_query)
        except PyMongoError as e:
            print(f"Error updating document in database '{database_name}', collection '{collection_name}': {e}")
        finally:
            return result
    async def delete_documents(
        self,
        database_name: str,
        collection_name: str,
        filter_query: dict,
    ):
        result = None  # Initialize result to None

        if self._client is None:
            await self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][
                collection_name
            ]
            result = await collection.delete_many(filter_query)
        except PyMongoError as e:
            print(f"Error deleting documents from database '{database_name}', collection '{collection_name}': {e}")
        finally:
            return result
            return result

    async def __aenter__(self):
        await self._initialize_client()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._client:
            self._client.close()

    async def close(self):
        """
        Asynchronously closes the MongoDB client connection if the event loop is running.
        """
        if self._client:
            try:
                await self._client.close()
            except RuntimeError as e:
                print(f"Error closing MongoDB client: {e}")
