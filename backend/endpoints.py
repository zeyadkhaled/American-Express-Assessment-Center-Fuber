# server endpoints
import json
import tornado.web
from database import db

# OUR MEMORY DB
users = dict()  # ie: {"uname": {"location": "brighton", "type": "driver"}}
notifs = dict()  # ie: {"driver": {"dest": "brighton", "origin": "london"}}


class LoginHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
    def OPTIONS(self):
        pass

    def get(self):
        self.write({"Hello": "FUBER!"})

    def post(self):
        try:
            body = json.loads(self.request.body)  # Try to load the body as a JSON object
        except:
            pass
        else:
            uname = body["uname"]
            location = body["location"]
            type_ = body["type"]

            doc_ref = db.collection("users").document(uname)

            if doc_ref.get().exists:
                self.set_status(500)
                self.write({"FAIL": "user already in DB", "Status": "500"})
            else:
                # users[uname] = {"location": location, "type": type_}
                isdriver = True
                if type_ == "passenger":
                    isdriver = False
                
                doc_ref.set({
                    u'uname': uname,
                    u'location': location,
                    u'isdriver': isdriver
                })

                self.write({"Success": "User saved to database", "Status": "200"})


class LocateHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        city = self.get_argument('city')
        result = []
        doc_ref = db.collection("users").get()
        for u in doc_ref:
            if u.get("isdriver") and u.get("location") == city:
                result.append(u.get("uname"))


        # for u in users:
        #     if users[u]["type"] == "driver" and users[u]["location"] == city:
        #         result.append(u)

        self.set_header("Content-Type", "text/plain")
        self.finish(json.dumps(result))


class BookHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def post(self):
        try:
            body = json.loads(self.request.body)  # Try to load the body as a JSON object
        except:
            pass
        else:
            driver = body["driver"]
            origin = body["origin"]
            dest = body["dest"]

            notifs[driver] = {"dest": dest, "origin": origin}
            print(notifs)
            self.write({"Success": "Notif written", "Status": "200"})


class NotifHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        driver = self.get_argument('driver')
        result = []
        for n in notifs:
            if n == driver:
                result.append(notifs[n])

        self.set_header("Content-Type", "text/plain")
        self.finish(json.dumps(result))


# class RegisterHandler(tornado.web.RequestHandler):
#     def set_default_headers(self):
#         self.set_header("Access-Control-Allow-Origin", "*")
#         self.set_header("Access-Control-Allow-Headers", "x-requested-with")
#         self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

#     def get(self):
#         self.write({"Hello": "FUBER!"})

#     def post(self):
#         try:
#             body = json.loads(self.request.body)  # Try to load the body as a JSON object
#         except:
#             pass
#         else:
#             uname = body["uname"]
#             location = body["location"]
#             type_ = body["type"]
#             password = body["password"]

#             doc_ref = db.collection("users").document(uname)

#             if doc_ref.get().exists:
#                 self.set_status(500)
#                 self.write({"FAIL": "user already in DB", "Status": "500"})
#             else:
#                 doc_ref.set({
#                     u'uname': uname,
#                     u'location': location,
#                     u'isdriver': isdriver
#                     u'password' : password
#                 })

#                 self.write({"Success": "User saved to database", "Status": "200"})
