# -- Requirements --
# * pydantic

import pydantic
from safedb import SDB

class User(pydantic.BaseModel):  # Basic User class
    id: int
    username: str
    email: str
    password: str

    @pydantic.validator('username')
    def username_validator(cls, username):
        # Enforce a set of rules for usernames
        if len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if ' ' in username:
            raise ValueError('Username cannot contain spaces')
        if len(username) > 10:
            raise ValueError('Username cannot be longer than 10 characters')
        
        # Verify the username is not already in use
        with db:
            if db.get_index_from_index('users', 'username', username):
                raise ValueError('Username already exists')

        return username

    @pydantic.validator('email')
    def email_validator(cls, email):
        # Enforce a set of rules for emails
        if len(email) < 3:
            raise ValueError('Email must be at least 3 characters long')
        if ' ' in email or '@' not in email or '.' not in email:
            raise ValueError('Invalid email')
        
        # Verify the email is not already in use
        with db:
            if db.get_index_from_index('users', 'email', email):
                raise ValueError('email already exists')

        return email

    @pydantic.validator('id')
    def id_validator(cls, id):
        # Verify the id is not already in use
        with db:
            if db.get_index_from_index('users', 'id', id):
                raise ValueError('id already exists')

        return id

db = SDB('data')

db.start_exchange()

if not 'users' in db.tables:
    db.add_table('users')

db.add_index('users', 'id')           # Create an index to quickly find users based on ID's
db.add_index('users', 'username')     # Create an index to quickly find users based on usernames
db.add_index('users', 'email')        # Create an index to quickly find users based on emails

user = User(id=1, username='test', email='example@gmail.com', password='test')
db.add_content('users', user)

db.commit()

print(db.in_exchange)

print(db.get_data_from_index('users', db.get_index_from_index('users', 'email', 'example@gmail.com')).username)

db.save()   # Save the database to disk
db.close()  # Close the database, deleting temporary files

# Output: 'test'
