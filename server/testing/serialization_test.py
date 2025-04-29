from app import app
from models import *


def test_customer_is_serializable(test_client):
    '''customer is serializable'''
    c = Customer(name='Phil')
    db.session.add(c)
    db.session.commit()
    r = Review(comment='great!', customer=c)
    db.session.add(r)
    db.session.commit()
    customer_dict = CustomerSchema().dump(c)

    assert customer_dict['id']
    assert customer_dict['name'] == 'Phil'
    assert customer_dict['reviews']
    assert 'customer' not in customer_dict['reviews']

def test_item_is_serializable(test_client):
    '''item is serializable'''
    i = Item(name='Insulated Mug', price=9.99)
    db.session.add(i)
    db.session.commit()
    r = Review(comment='great!', item=i)
    db.session.add(r)
    db.session.commit()

    item_dict = ItemSchema().dump(i)
    assert item_dict['id']
    assert item_dict['name'] == 'Insulated Mug'
    assert item_dict['price'] == 9.99
    assert item_dict['reviews']
    assert 'item' not in item_dict['reviews']

def test_review_is_serializable(test_client):
    '''review is serializable'''
    c = Customer()
    i = Item()
    db.session.add_all([c, i])
    db.session.commit()

    r = Review(comment='great!', customer=c, item=i)
    db.session.add(r)
    db.session.commit()

    review_dict = ReviewSchema().dump(r)
    assert review_dict['id']
    assert review_dict['customer']
    assert review_dict['item']
    assert review_dict['comment'] == 'great!'
    assert 'reviews' not in review_dict['customer']
    assert 'reviews' not in review_dict['item']
