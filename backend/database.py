from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin


cred = credentials.Certificate('fuber-f554e-firebase-adminsdk-aeco8-e67ff51ec2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()    
    



