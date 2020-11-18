# from .. import db

# class User(db.Document):

#     user_id = db.SequenceField()
#     full_name = db.StringField()
#     username = db.StringField()
#     city = db.StringField(default="")
#     avatar_hash = db.StringField(default="")
#     phone = db.StringField(default="")
#     about_me = db.StringField(default="")


from .. import db
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Document):
    
    user_id = db.SequenceField()
    full_name = db.StringField()
    username = db.StringField()
    password = db.StringField()
    city = db.StringField(default="")
    avatar_hash = db.StringField(default="")
    phone = db.StringField(default="")
    about_me = db.StringField(default="")

class Posts(db.Document):
    
    post_id = db.SequenceField()
    user_id = db.SequenceField()
    text = db.StringField()
    header =  db.StringField()

@login.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()