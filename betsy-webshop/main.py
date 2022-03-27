__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from fuzzywuzzy import fuzz

# sqlite> .mode column
# sqlite> .header on
# SELECT * FROM products

def search(term): # Naam of description 
    selectie = Products.select(Products.productnaam, Products.products_id)
    lijst = [] 
    for x in selectie:
        # To account for typo's
        typo2 = fuzz.partial_ratio(x.productnaam, term)
        if typo2 > 80:
            lijst.append({x.productnaam : x.products_id})
    return lijst 
        
# print(search("Keting"))

def list_user_products(user_id):
    query = Products.select(Products.productnaam, Users.user_id).join(Users, JOIN.INNER).where(Users.user_id == user_id)
    for thing in query:
        return thing.productnaam

# print(list_user_products(2))

def list_products_per_tag(tag):
    query = Products.select().join(Productlabels, JOIN.INNER).join(Labels, JOIN.INNER).where(Labels.name == tag)
    total = []
    for thing in query:
        total.append(thing.productnaam)
    return total

# print(list_products_per_tag("Kleurrijk"))

def add_product_to_catalog(user_id, product):

    nieuw = Products.insert(productnaam = product[0], owner = user_id, price_pu = product[1], quantity = product[2], description = product[3])
    nieuw.execute()
    check = Products.select(Products.productnaam).where(Products.productnaam == product[0]).dicts()
    for print in check:
        return print, "Is added"
    
# print(add_product_to_catalog(3,["Schilderij", 135.00, 1, "Fraai acrylschilderij"]))

def update_stock(product_id, new_quantity):
    query = Products.update({Products.quantity : new_quantity}).where(Products.products_id == product_id)
    query.execute()
    check = Products.select(Products.productnaam, Products.quantity, Products.products_id).where(Products.products_id == product_id)
    for print in check:
        return print.productnaam, print.quantity 

# print(update_stock(2, 9))

def purchase_product(product_id, buyer_id, hoeveelheid):
    query = Products.select(Products.products_id, Products.productnaam, Products.price_pu, Products.quantity, Users.user_id).join(Users, JOIN.INNER).where(Products.products_id == product_id)
    for thing in query:
        qty = thing.quantity
        if qty < hoeveelheid:
            return "Sorry, products was sold out"
        elif qty == hoeveelheid:
            # Remove instance in products. user.delete_instance(
            row = Products.get(Products.products_id == product_id)
            row.delete_instance()
            for thing in query:
                Transaction.create(product = product_id, by_user = buyer_id, price = thing.price_pu, quantity = hoeveelheid)
                # Check
                return "Product was sold"
        elif qty > hoeveelheid:
            # Update 
            row = Products.get(Products.products_id == product_id)
            row.quantity = (row.quantity - hoeveelheid)
            row.save()
            for thing in query:
                Transaction.create(product = product_id, by_user = buyer_id, price = thing.price_pu, quantity = hoeveelheid)
                # Check
                check = Products.get(Products.products_id == product_id)
                return check.productnaam, check.quantity, "left" 

# print(purchase_product(1,2,1))

def remove_product(product_id):
    try:
        thing = Products.select(Products.productnaam, Products.products_id, Products.owner).where(Products.products_id == product_id)
        for thingey in thing:
            deleted = thingey.productnaam
            user = thingey.owner.naam
        obj = Products.get(Products.products_id == product_id)
        obj.delete_instance()
        return (deleted + " is deleted from " + user)
    except:
        return "Item does not exist"

# print(remove_product(2))