# SafeDB
## What is SafeDB?
SafeDB is a simple and secure database framework for Python. Its purpose is to provide a simple yet fast way to store data while also allowing for more flexibility than SQL.
## How is it more flexible than SQL?
Well, unlike SQL, SafeDB uses lists and dictionaries to store data. This means you can store any type of data (including custom objects).
## Can I use threading and multiprocessing?
SafeDB is perfectly thread-safe (with or without GIL), but isn't made to be used with multiprocessing.
# Installation
To install SafeDB, run the following command:
```bash
pip install -U safedb
```
To upgrade SafeDB, run the following command:
```bash
pip install --upgrade safedb
```
# Documentation

## Basic Usage

### Creating a Database
To create a new database or open an existing one:

```python
from safedb.database import SDB

# Create or open a database
db = SDB("my_database")
```

### Working with Tables

```python
# Create a new table
db.add_table("users")

# List all tables
print(db.tables)

# Remove a table
db.remove_table("users")
```

### Adding and Retrieving Data

```python
# Add data to a table
user = {"id": 1, "username": "john_doe", "email": "john@example.com"}
db.add_content("users", user)

# Get all data from a table
all_users = db.get_table("users")

# Get data by index position
user = db.get_data_from_index("users", 0)  # Get the first user
```

### Working with Indexes
Indexes improve query performance by creating lookup dictionaries for specific fields:

```python
# Create an index on the "username" field
db.add_index("users", "username")

# Retrieve data using an index
user_index = db.get_index_from_index("users", "username", "john_doe")
user = db.get_data_from_index("users", user_index)
```

## Transaction System
SafeDB uses an exchange system (similar to transactions) to ensure data integrity:

```python
# Method 1: Using context manager (recommended)
with SDB("my_database") as db:
    db.add_table("products")
    db.add_content("products", {"id": 1, "name": "Laptop"})
    # Changes are automatically committed if no exceptions occur
    # and rolled back if an exception is raised

# Method 2: Manual transaction management
db = SDB("my_database")
db.start_exchange()  # Begin transaction
try:
    db.add_table("categories")
    db.add_content("categories", {"id": 1, "name": "Electronics"})
    db.commit()  # Commit changes
except Exception as e:
    db.rollback()  # Rollback on error
finally:
    db.save()  # Save changes to disk
```

## Data Persistence

```python
# Save database to disk
db.save()

# Load database from disk
db.load()

# Close the database (removes temporary files)
db.close()

# Delete the database (removes all database files)
db.delete()
```

## Best Practices

1. **Use the context manager** when possible to ensure proper transaction handling.
2. **Create indexes** for fields you frequently search on to improve performance.
3. **Use consistent data types** within a table to avoid issues with indexing.
4. **Save regularly** to ensure data persistence.

## Data Structure Compatibility
SafeDB can store various Python data types:

- Dictionaries (recommended)
- Custom objects with attributes
- Lists (with numeric indexes)
- Basic data types (strings, numbers, booleans)
- Nested data structure

For best performance, use dictionaries with consistent keys across all records in a table.
# Internal Workings
SafeDB uses an ordinary list to store data. Although, to fix the speed issue, there are multiple "indexes". Each index is a dictionary, where a key is a value of a column and a value is the index of a certain row in a list.

Please note that a "row" is an item in the table's list, and a "column" is a property/attribute of a row.

Storing multiple data types in a table is not recommended, and doing so will force you to make indexes based on common attributes.

SafeDB also has an implementation of the saving algorithm that includes durability and atomicity for the primary file.
# Notes
## Warnings
1. Make sure to define any custom classes before you define the database object
2. Don't forget to call `SDB.close()` to delete the temporary files
3. Make sure all index-keys are valid attributes of every row in the table and are hash-able.
## Notes
1. If you need to store dictionaries in a table, you can create indexes with the index-keys being keys from your dictionaries (just make sure all dictionaries have the keys you use for indexes)
