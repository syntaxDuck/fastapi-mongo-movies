import asyncio
from config import config
from database import MongoDBConfig, MongoDBClientHandler


async def main():
    """
    Asynchronously establishes a connection to a MongoDB server and pings the server to confirm a successful connection.

    This function does the following:
    - Creates a MongoDB configuration object using the `MongoDBConfig` class.
    - Creates a MongoDB connection object using the `MongoDBConnection` class.
    - Awaits the `client` property to establish the connection.
    - Optionally, calls the `query_server` function to ping the server.

    Parameters:
    - None

    Returns:
    - None
    """
    # Assuming settings is already defined with USER, PASS, and HOST
    db_config = MongoDBConfig(
        config.DB_USER,
        config.DB_PASS,
        config.DB_HOST,
        appName="Cluster0",
        tls="true",
        tlsAllowInvalidCertificates="true",
        retryWrites="true",
        w="majority",
    )
    # mongo_connection = MongoDBConnection(config)
    # await mongo_connection.client

    db_name = "sample_mflix"
    collection_name = "users"

    # Define different queries
    queries = [
        {"name": {"$regex": "^M"}},  # Users older than 30
        {"name": {"$regex": "^J"}},  # Users younger than 20
        {"name": {"$regex": "^A"}},  # Users whose names start with 'A'
    ]

    # Start fetching data concurrently
    async with MongoDBClientHandler(config) as mongo_connection:
        # tasks = [mongo_connection.fetch_documents(db_name, collection_name, query) for query in queries]
        # Wait for all tasks to complete
        # results = await asyncio.gather(*tasks)
        results = await mongo_connection.insert_documents(
            db_name,
            collection_name,
            {"name": "Roshan", "password": "12345", "email": "r@r.com"},
        )

    # Print results
    # for i, result in enumerate(results):
    #     print(f"Results for query {i+1}:")
    #     for doc in result:
    #         print(doc)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
