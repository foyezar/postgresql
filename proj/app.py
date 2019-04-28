from db import Database
from user import User

Database.initialize(database="learning", user="postgres", password="admin", host="localhost")

user = User('farah@email.com', 'Farah', 'Islam', None)
user.save_to_db()
user_from_db = User.load_from_db_by_email('farah@email.com')
print(user_from_db) 