import os

REDDIT_CONF = {
    "user_agent" : "Reply rock and stone bot test. (By u/KaeWye)",
    "client_id" : os.environ.get("CLIENT_ID","<your client id>"),
    "client_secret" : os.environ.get("CLIENT_SECRET","<your_client_secret>"),
    "username": os.environ.get("USERNAME","<your_username>"),
    "password": os.environ.get("PASSWORD","<your_password>")
}

IGNORED_USERS = {"kaewye", "WanderingDwarfMiner"}
REPLIES = [
    "Rock and Stone!",
    "Rock and Stone, Brother!",
    "Rock and Stone everyone!",
    "Rock and Stone forever!",
    "Rock and roll and stone!",
    "Rock and Stone to the Bone!",
    "Rock and Stone in the Heart!",
    "For Rock and Stone!",
    "If you don't Rock and Stone, you ain't comin' home!",
    "Did I hear a Rock and Stone?",
    "To Rock and Stone!",
    "That's it lads! Rock and Stone!",
    "We fight for Rock and Stone!",
    "For Karl!"
    ]