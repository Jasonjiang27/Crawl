import mongoengine

mongoengine.connect('project1', host = "127.0.0.1", port = 27017)
'''建模，指出数据库的字段类型
'''
class CarPrice(mongoengine.Document):
    url = mongoengine.StringField(max_length=64, primary_key=True)
    brand = mongoengine.StringField(max_length=64)
    name = mongoengine.StringField(max_length=64)
    price = mongoengine.StringField(max_length=64)