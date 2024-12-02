from pymongo import MongoClient

# Replace with your actual connection string with the new credentials
# connection_string = "mongodb://root:root@amaye15-MongoDB.hf.space"
connection_string = "mongodb://admin:yourpassword@amaye15-mongodb.hf.space:7860"
# connection_string = "mongodb://amaye15-mongodb.hf.space:27017"
# connection_string = "mongodb://admin:yourpassword@localhost:27017"

# Create a MongoDB client
client = MongoClient(connection_string)

try:
    # Test the connection
    print("Connecting to MongoDB with authentication...")
    client.admin.command("ping")
    print("Successfully connected to MongoDB!")
    # print("Databases available:", databases)

except Exception as e:
    print("Failed to connect to MongoDB:", e)
finally:
    # Close the connection
    client.close()
