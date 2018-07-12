import mongoengine

mongoengine.connect('project1', host = "127.0.0.1", port = 27017)

class CarPrice(mongoengine.Document):
    url = mongoengine.StringField(max_length=64, primary_key=True)
    brand = mongoengine.StringField(max_length=64)
    name = mongoengine.StringField(max_length=64)
    price = mongoengine.StringField(max_length=64)