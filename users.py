from models import User

# normally this would come from models/db data
users = [User(1, "Jose", "1234"), User(2, "Mimi", "1234")]
username_dict = {u.username: u for u in users}
userid_dict = {u.id: u for u in users}


def authenticate(username, password):
    user = username_dict.get(username, None)
    if user and password == user.password:
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_dict.get(user_id, None)
