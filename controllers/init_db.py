# -*- coding: utf-8 -*-
# from gluon import *

def init_db(exposed=False):
    # db = DAL('sqlite://storage.sqlite')
    
    db.auth_user.validate_and_insert(first_name='admin_fn', last_name='admin_ln', email='admin@email.com', password='Password1')
    id = db.auth_user.validate_and_insert(first_name='user2', last_name='user2', email='user2@email.com', password='Password1')
    db.auth_group.validate_and_insert(role='admin', decription='admin users')
    db.auth_group.validate_and_insert(role='dev', decription='dev users')

    # db.auth_membership
    # user_id
    # group_id
    db.commit()
    
    print('#####')   
    print(id)
    print('** end **')
