# -*- coding: utf-8 -*-
# from gluon import *


# run with cli
# web2py -M -S nfabsm/init_db/init_db
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


    def find_or_create_region(region_name, alternate_name):
        r = db(db.region.region_name == region_name).select().first()
        if r: return r.id
        temp = db.region.validate_and_insert(region_name=region_name, alternate_name=alternate_name)
        if temp.id: return temp.id
        else: return False

    # region: region_name, alternate_name
    find_or_create_region('Region 1', 'Ilocos Region')
    find_or_create_region('Region 2', 'Cagayan Valley Region')
    find_or_create_region('Region 3', 'Central Luzon Region')
    find_or_create_region('Region 4', 'Southern Tagalog Region')
    find_or_create_region('Region 5', 'Bicol Region')
    find_or_create_region('Region 6', 'Central Visayas Region')
    find_or_create_region('Region 7', 'Western Visayas Region')
    region8_id = find_or_create_region('Region 8', 'Eastern Visayas Region')
    find_or_create_region('Region 9', 'Zamboanga Peninsula')
    find_or_create_region('Region 10', 'Northern Mindanao Region')
    find_or_create_region('Region 11', 'Davao Region')
    find_or_create_region('Region 12', 'Soccsksargen')
    find_or_create_region('Region 13', 'National Capital Region')
    find_or_create_region('Region 14', 'BARMM')
    find_or_create_region('Region 15', 'CARAGA')
    find_or_create_region('CO', 'Central Office')


    def find_or_create_branch(branch_name, region):
        r = db(db.branch.branch_name == branch_name).select().first()
        if r: return r.id
        temp = db.branch.validate_and_insert(branch_name=branch_name, region_id=region)
        if temp.id: return temp.id
        else: return False

    # branch: branch_name, region
    leyte_br_id = find_or_create_branch('Leyte Branch', region8_id)
    find_or_create_branch('Samar Branch', region8_id)
    

    def find_or_create_warehouse(warehouse_name, warehouse_code, branch_id):
        r = db(db.warehouse.warehouse_name == warehouse_name).select().first()
        if r: return r.id
        temp = db.warehouse.validate_and_insert(warehouse_name=warehouse_name, warehouse_code=warehouse_code, branch_id=branch_id)
        if temp.id: return temp.id
        else: return False

    # warehouse: name, code, branch
    find_or_create_warehouse('Port Area GID', '123456', leyte_br_id)
    find_or_create_warehouse('Alang-alang GID 1', '223456', leyte_br_id)
    find_or_create_warehouse('Alang-alang GID 2', '323456', leyte_br_id)
    find_or_create_warehouse('San Pablo GID', '423456', leyte_br_id)
    find_or_create_warehouse('Cogon GID', '523456', leyte_br_id)
    find_or_create_warehouse('Maasin GID', '623456', leyte_br_id)
    find_or_create_warehouse('Hilongos JICA', '723456', leyte_br_id)
    find_or_create_warehouse('Hinunangan MLGC', '823456', leyte_br_id)
    find_or_create_warehouse('St. Bernard FLGC', '923456', leyte_br_id)
    find_or_create_warehouse('Biliran GID', '023456', leyte_br_id)


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

    print('\nRegions')
    for r in db(db.region).select():
        print(r.region_name, r.alternate_name)

    print('\nBranches')
    for r in db(db.branch).select():
        print(r.branch_name)

    print('\nWarehouses')
    for r in db(db.warehouse).select():
        print(r.warehouse_name)



    print('\n#####')   
    print('** end **')
