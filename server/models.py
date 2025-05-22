from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # One-to-many relationship: Customer has many Reviews
    reviews = db.relationship('Review', back_populates='customer')
    
    # Association proxy: Customer has many Items through Reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # One-to-many relationship: Item has many Reviews
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Many-to-one relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

# Marshmallow Schemas for Serialization

class ReviewSchema(Schema):
    id = fields.Integer()
    comment = fields.String()
    
    # Nested relationships - exclude recursive fields to prevent circular references
    customer = fields.Nested('CustomerSchema', exclude=('reviews',))
    item = fields.Nested('ItemSchema', exclude=('reviews',))

class CustomerSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    
    # Nested relationships - exclude recursive fields to prevent circular references
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('customer', 'item'))

class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Float()
    
    # Nested relationships - exclude recursive fields to prevent circular references
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('customer', 'item'))