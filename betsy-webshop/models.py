# Models go here

from unicodedata import name
from peewee import*
from pyparsing import Char

db = SqliteDatabase("Betsy.db")

class BaseModel(Model):
    class Meta:
        database = db 

class Users(BaseModel):
    user_id = AutoField()
    naam = CharField()
    adres = CharField()
    info = CharField()

# class Labels(BaseModel):
#     id_pk = AutoField()
#     tag = CharField()

class Products(BaseModel):
    products_id = AutoField()
    productnaam = CharField()
    owner = ForeignKeyField(Users)
    price_pu = DecimalField(auto_round=2)
    quantity = IntegerField()
    description = CharField()

class Labels(BaseModel):
    id_pd = AutoField()
    name = CharField()

class Productlabels(BaseModel):
    product = ForeignKeyField(Products)
    tag = ForeignKeyField(Labels)

class Transaction(BaseModel):
    transaction_id = AutoField()
    product = ForeignKeyField(Products)
    by_user = ForeignKeyField(Users)
    price = DecimalField(auto_round=2)
    quantity = IntegerField()

# Maak de tabellen 

def populate_test_data():
    db.connect()

    db.create_tables([Users, Labels, Productlabels, Products, Transaction])

populate_test_data()

# Gebruik sqlite3, sqlite .database om te controleren wat de ID's zijn, .exit als je weer Peewee gebruikt. 
Siam = Users(naam = "Siam", adres = "Rotterdam 7", info = 12345)
Siam.save()
Kaya = Users(naam = "Kaya", adres = "Bergen NH 29", info = 20210)
Kaya.save()
Babs = Users(naam = "Babs", adres = "Nijmegen 26", info = 13219)
Babs.save()
kleurig = Labels(name= "Kleurrijk")
kleurig.save()
natuurlijk = Labels(name= "natuurlijk")
natuurlijk.save()

Ketting = Products(productnaam = "Ketting", owner = 1, price_pu = 9.00, quantity = 2, description = "Vrolijke ketting van houten kralen")
Ketting.save()
Vaas = Products(productnaam = "Handgemaakt aardewerk", owner = 2, price_pu = 39.00, quantity = 1, description = "Fraai geglazuurd aardewerk van klei")
Vaas.save()

Kettinglabel1 = Productlabels(product = Ketting, tag = kleurig)
Kettinglabel1.save()
Kettinglabel2 = Productlabels(product = Ketting, tag = natuurlijk)
Kettinglabel2.save()
Vaaslabel = Productlabels(product= Vaas, tag = natuurlijk)
Vaaslabel.save()


