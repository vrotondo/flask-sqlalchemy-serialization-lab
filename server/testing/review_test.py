from app import app
from models import *

def test_can_be_instantiated(test_client):
    '''can be invoked to create a Python object.'''
    r = Review()
    assert r
    assert isinstance(r, Review)

def test_has_comment(test_client):
    '''can be instantiated with a comment attribute.'''
    r = Review(comment='great product!')
    assert r.comment == 'great product!'

def test_can_be_saved_to_database(test_client):
    '''can be added to a transaction and committed to review table with comment column.'''
    assert 'comment' in Review.__table__.columns
    r = Review(comment='great!')
    db.session.add(r)
    db.session.commit()
    assert hasattr(r, 'id')
    assert db.session.query(Review).filter_by(id=r.id).first()

def test_is_related_to_customer_and_item(test_client):
    '''has foreign keys and relationships'''
    assert 'customer_id' in Review.__table__.columns
    assert 'item_id' in Review.__table__.columns

    c = Customer()
    i = Item()
    db.session.add_all([c, i])
    db.session.commit()

    r = Review(comment='great!', customer=c, item=i)
    db.session.add(r)
    db.session.commit()

    # check foreign keys
    assert r.customer_id == c.id
    assert r.item_id == i.id
    # check relationships
    assert r.customer == c
    assert r.item == i
    assert r in c.reviews
    assert r in i.reviews
