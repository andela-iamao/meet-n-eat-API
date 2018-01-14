from app import db
from utilities.common import utc_now_ts as now


class User(db.Document):
    username = db.StringField(db_field="u", required=True, unique=True)
    password = db.StringField(db_field="p", required=True)
    email = db.EmailField(db_field="e", required=True, unique=True)
    first_name = db.StringField(db_field="fn", max_length=50, required=True)
    last_name = db.StringField(db_field="ln", max_length=50, required=True)
    bio = db.StringField(db_field="b", max_length=128)
    created = db.IntField(db_field="c", default=now())

    meta = {
        "indexes": ["username", "email", "-created"]
    }

    @property
    def serialize(self):
        return {
            "bio": self.bio,
            "id": str(self.id),
            "email": self.email,
            "created": self.created,
            "username": self.username,
            "last_name": self.last_name,
            "first_name": self.first_name,
        }
