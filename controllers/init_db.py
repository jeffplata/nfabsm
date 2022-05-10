# -*- coding: utf-8 -*-
# from gluon import *


# run with cli
# web2py -M -S nfabsm/init_db/init_db
# -M = import models, so no need for db = ...
def init_db(exposed=False):
    # db = DAL('sqlite://storage.sqlite')

    def find_or_create_commodity(commodity_name, is_cereal):
        r = db(db.commodity.commodity_name == commodity_name).select().first()
        if r: return r.id
        temp = db.commodity.validate_and_insert(commodity_name=commodity_name, is_cereal=is_cereal)
        if temp.id: return temp.id
        else: return False

    local_rice = find_or_create_commodity('Local Rice', True)
    local_palay = find_or_create_commodity('Local Palay', True)
    facilities = find_or_create_commodity('Facilities', False)
    miscellaneous = find_or_create_commodity('Miscellaneous', False)

    def find_or_create_container(container_name, container_shortname, weight):
        r = db(db.container.container_name == container_name).select().first()
        if r: return r.id
        temp = db.container.validate_and_insert(container_name=container_name, 
            container_shortname=container_shortname, weight=weight)
        if temp.id: return temp.id
        else: return False

    g50 = find_or_create_container('PPRG50', 'G50', 0.78)
    e50 = find_or_create_container('PPRE50', 'E50', 0.86)

    def find_or_create_variety(variety_name, commodity_id):
        r = db(db.variety.variety_name == variety_name).select().first()
        if r: return r.id
        temp = db.variety.validate_and_insert(variety_name=variety_name, commodity_id=commodity_id)
        if temp.id: return temp.id
        else: return False

    wd1 = find_or_create_variety('WD1', local_rice)
    wd2 = find_or_create_variety('WD2', local_rice)
    pd1 = find_or_create_variety('PD1', local_palay)
    pd3 = find_or_create_variety('PD3', local_palay)
    var_fac = find_or_create_variety('Facilities', facilities)
    var_misc = find_or_create_variety('Miscellaneous', miscellaneous)

    def find_or_create_item(item_name, variety_id, container_id=None, default_price=0.00):
        r = db(db.item.item_name == item_name).select().first()
        if r: return r.id
        temp = db.item.validate_and_insert(item_name=item_name,
            variety_id=variety_id, container_id=container_id, selling_price=default_price)
        if temp.id: return temp.id
        else: return False

    # Item(item_name, variety, container, unit price)
    find_or_create_item('WD1', wd1, g50, 25.00)
    find_or_create_item('WD2', wd2, g50, 23.00)
    find_or_create_item('PD1', pd1, e50)
    find_or_create_item('PD3', pd3, e50)
    find_or_create_item('Tennis Court', var_fac, None, 160.00)
    find_or_create_item('Staffhouse', var_fac)
    find_or_create_item('Educational Loan', miscellaneous, var_misc)
    find_or_create_item('EA Loan', var_misc)

    # user management

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

    print('\n#####')

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

    print('\nCommodities')
    commodity_dict = {}
    for r in db(db.commodity).select():
        commodity_dict[r.id] = r.commodity_name
        print(r.commodity_name)

    print('\nContainers')
    container_dict = {}
    for r in db(db.container).select():
        container_dict[r.id] = r.container_name
        print(r.container_name)

    print('\nVarieties')
    variety_dict = {}
    for r in db(db.variety).select():
        variety_dict[r.id] = r.variety_name
        print(r.variety_name, commodity_dict[r.commodity_id])

    print('\nItems')
    for r in db(db.item).select():
        print(r.item_name, variety_dict[r.variety_id], 
            container_dict[r.container_id] if r.container_id else None, r.selling_price or '')

    print('\n#####')
    print('** end **')
