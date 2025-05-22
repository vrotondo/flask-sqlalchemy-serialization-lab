#!/usr/bin/env python3

from app import app
from models import db, Customer, Review, Item

with app.app_context():
    # Clear existing data
    Review.query.delete()
    Customer.query.delete()
    Item.query.delete()
    db.session.commit()

    # Create customers
    customer1 = Customer(name='Tal Yuri')
    customer2 = Customer(name='Raha Rosario')
    customer3 = Customer(name='Luca Mahan')
    db.session.add_all([customer1, customer2, customer3])
    db.session.commit()

    # Create items
    item1 = Item(name='Laptop Backpack', price=49.99)
    item2 = Item(name='Insulated Coffee Mug', price=9.99)
    item3 = Item(name='6 Foot HDMI Cable', price=12.99)
    db.session.add_all([item1, item2, item3])
    db.session.commit()

    # Create reviews
    review1 = Review(comment="zipper broke the first week", customer=customer1, item=item1)
    review2 = Review(comment="love this backpack!", customer=customer2, item=item1)
    review3 = Review(comment="coffee stays hot for hours!", customer=customer1, item=item2)
    review4 = Review(comment="best coffee mug ever!", customer=customer3, item=item2)
    review5 = Review(comment="cable too short", customer=customer3, item=item3)
    
    db.session.add_all([review1, review2, review3, review4, review5])
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Created {Customer.query.count()} customers")
    print(f"Created {Item.query.count()} items") 
    print(f"Created {Review.query.count()} reviews")