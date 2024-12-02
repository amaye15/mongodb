import asyncio
import importlib
import os
import sys
import configparser
from motor.motor_asyncio import AsyncIOMotorClient


class AsyncMongoMigrator:
    def __init__(
        self, db, migrations_path="migrations", metastore="migrations", dry_run=False
    ):
        self.db = db
        self.migrations_path = migrations_path
        self.migrations_collection = db[metastore]
        self.dry_run = dry_run

    async def get_applied_migrations(self):
        applied_migrations = await self.migrations_collection.find().to_list(
            length=None
        )
        return set(m["name"] for m in applied_migrations)

    def get_migration_modules(self):
        migration_files = [
            f[:-3]
            for f in os.listdir(self.migrations_path)
            if f.endswith(".py") and not f.startswith("__")
        ]
        migration_modules = []
        for filename in sorted(migration_files):
            # Adjust for nested directories
            module_name = os.path.splitext(
                os.path.relpath(os.path.join(self.migrations_path, filename), start=".")
            )[0]
            module_name = module_name.replace(os.sep, ".")
            module = importlib.import_module(module_name)
            migration_modules.append((filename, module))
        return migration_modules

    async def apply_migrations(self):
        applied_migrations = await self.get_applied_migrations()
        migration_modules = self.get_migration_modules()

        for migration_name, module in migration_modules:
            if migration_name in applied_migrations:
                print(f"Migration {migration_name} already applied, skipping.")
                continue
            else:
                print(f"Applying migration {migration_name}...")
                migration_class = getattr(module, "Migration", None)
                if migration_class is None:
                    print(f"No 'Migration' class found in {migration_name}, skipping.")
                    continue

                migration_instance = migration_class(self.db)
                if self.dry_run:
                    print(f"[Dry Run] Would apply migration {migration_name}")
                else:
                    await migration_instance.upgrade()
                    await self.migrations_collection.insert_one(
                        {"name": migration_name}
                    )
                    print(f"Migration {migration_name} applied.")

    async def rollback_migrations(self, steps=1):
        applied_migrations = await self.get_applied_migrations()
        migration_modules = self.get_migration_modules()

        applied_migration_modules = [
            (name, module)
            for name, module in migration_modules
            if name in applied_migrations
        ]

        migrations_to_rollback = applied_migration_modules[-steps:]

        for migration_name, module in reversed(migrations_to_rollback):
            print(f"Rolling back migration {migration_name}...")
            migration_class = getattr(module, "Migration", None)
            if migration_class is None:
                print(f"No 'Migration' class found in {migration_name}, skipping.")
                continue

            migration_instance = migration_class(self.db)
            if self.dry_run:
                print(f"[Dry Run] Would rollback migration {migration_name}")
            else:
                await migration_instance.downgrade()
                await self.migrations_collection.delete_one({"name": migration_name})
                print(f"Migration {migration_name} rolled back.")


async def main():
    # Read configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    mongo_config = config["mongo"]
    host = mongo_config.get("host", "mongodb://localhost:27017")
    port = mongo_config.getint("port", 27017)
    database_name = mongo_config.get("database", "test")
    migrations_path = mongo_config.get("migrations", "migrations")
    metastore = mongo_config.get("metastore", "migrations")
    dry_run = mongo_config.getboolean("dry_run", False)

    # Adjust the Python path if necessary
    sys.path.append(os.getcwd())

    # Connect to MongoDB
    client = AsyncIOMotorClient(host)
    db = client[database_name]

    migrator = AsyncMongoMigrator(db, migrations_path, metastore, dry_run)
    await migrator.apply_migrations()
    # Uncomment the line below to rollback migrations
    # await migrator.rollback_migrations(steps=1)


if __name__ == "__main__":
    asyncio.run(main())
