import pyrebase


class firebaseAPI:
    def __init__(self, config):
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()

    def register(self, account_info, user_info):
        auth = self.firebase.auth()
        email = account_info["email"]
        passwd = account_info["passwd"]
        try:
            user = auth.create_user_with_email_and_password(email, passwd)
        except:
            print("Failed to verify the email address")
        self.token = user["idToken"]
        self.db.child("users").push(user_info, self.token)
        print("Account created successfully!")

    def auth(self, account_info):
        auth = self.firebase.auth()
        email = account_info["email"]
        passwd = account_info["passwd"]
        try:
            user = auth.sign_in_with_email_and_password(email, passwd)
            self.token = user["idToken"]
            print("Sign in successfully!")
        except:
            print("User not registered")
            name = input("Name: ")
            age = input("Age: ")
            user_info = {
                "name": name,
                "age": age
            }
            self.register(account_info, user_info)

    def store_data(self, col, data, keys=[]):
        if keys == []:
            self.db.child(col).push(data)
        else:
            keystr = ""
            for key in keys:
                keystr += "/" + key
            self.db.child(col).child(keystr).set(data)

    def retrieve_data(self, col, keys=[]):
        if keys == []:
            data = self.db.child(col).get()
        else:
            keystr = ""
            for key in keys:
                keystr += "/" + key
            data = self.db.child(col).child(keystr).get()
        return data

    def delete_data(self, col, keys=[]):
        if keys == []:
            data = self.db.child(col).remove()
        else:
            keystr = ""
            for key in keys:
                keystr += "/" + key
            data = self.db.child(col).child(keystr).remove()
        return data
