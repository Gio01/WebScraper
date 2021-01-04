import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Creating the connection to firebase through the AdminSDK

cred = credentials.Certificate("thirtyspider-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

"""
We can now use the db obj to add and query data
"""
