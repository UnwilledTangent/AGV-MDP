import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate('C:\\Users\\EEE\\Desktop\\jsonKeyFileFirebase.json')
firebase_admin.initialize_app(cred)

dataBase = firestore.client()

doc_ref = dataBase.collection(u'players').document(u'megaman')
doc_ref.set({
    u'first': u'Mega',
    u'last': u'Man',
    u'born': 1987
})
