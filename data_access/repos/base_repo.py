from firebase_admin import firestore, storage

class BaseRepo():
    def __init__(self):
        self.db = firestore.client()
        self.bucket = storage.bucket('rvawol.appspot.com')