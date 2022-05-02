# -*- coding: utf-8 -*-
# from gluon import *


# run with cli
# web2py -S -M nfabsm/init_db/initdb
# -M = import models, so no need for db = ...
def init_db(exposed=False):
    # db = DAL('sqlite://storage.sqlite')

    def find_or_create_user(user_name):
        u = db(db.auth_user.email == user_name).select().first()
        if u:
            return u.id
        else:
            temp = db.auth_user.validate_and_insert(email=user_name, password='Password1', first_name=user_name+' fn', last_name=user_name+' ln')
            if temp.id:
                return temp.id
            else:
                return False

    def find_or_create_group(group_name):
        g = db(db.auth_group.role == group_name).select().first ()
        if g:
            return g.id
        else:
            temp = db.auth_group.validate_and_insert(role=group_name, description=group_name + ' users')
            if temp.id:
                return temp.id
            else:
                return False            
            
    def assign_user_to_group(user, group):
        u = db(db.auth_user.email == user).select().first()
        g = db(db.auth_group.role == group).select().first()
        if not db((db.auth_membership.user_id == u.id) & (db.auth_membership.group_id == g.id)).select():
            db.auth_membership.validate_and_insert(user_id=u.id, group_id=g.id)

    find_or_create_user('admin@email.com')
    find_or_create_user('user@email.com')
    find_or_create_group('admin')
    assign_user_to_group('admin@email.com', 'admin')

    db.commit()
    
    print('\nUsers')
    user_dict = {}
    for r in db(db.auth_user).select():
        user_dict[r.id] = r.email
        print(r.email, r.first_name, r.last_name)

    print('\nGroups')
    group_dict = {}
    for r in db(db.auth_group).select():
        group_dict[r.id] = r.role
        print(r.role, r.description)

    print('\nMemberships')
    for r in db(db.auth_membership).select():
        print(user_dict[r.user_id], group_dict[r.group_id])

    print('\n#####')   
    print('** end **')
