# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from library.py")

# @auth.requires_membership('admin')
# def regions():
#     tablename = request.args(0)
#     grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
#     return locals()

def m_ondelete(table, id):
    if table == db.region:
        branches = db(db.branch.region_id==id).select().first()
        org_accesses = db(db.org_access.region_id==id).select().first()
        if branches or org_accesses:
            response.flash = 'Cannot delete this record'
            raise HTTP(403)
    if table == db.branch:
        warehouses = db(db.warehouse.branch_id==id).select().first()
        points_of_sales = db(db.point_of_sale.branch_id==id).select().first()
        org_accesses = db(db.org_access.branch_id==id).select().first()
        if warehouses or points_of_sales or org_accesses:
            response.flash = 'Cannot delete this record'
            raise HTTP(403)
    if table == db.point_of_sale:
        org_accesses = db(db.org_access.pos_id==id).select().first()
        if org_accesses:
            response.flash = 'Cannot delete this record'
            raise HTTP(403)

# Regions, Organizational Access
# @auth.requires_membership(role=='admin' or role=='branch_admin')
@auth.requires(auth.has_membership(role='admin') or auth.has_membership(role='branch_admin'))
def sgrid():
    response.view = 'library/edit_record.html'
    title = request.vars['title']
    tablename = request.args(0)
    action = ''

    if tablename == 'org_access':
        if any(x in request.args for x in ['new', 'edit']):
            response.view = 'library/edit_org_access.html'
            action = 'new' if 'new' in request.args else 'edit'

    if 'warehouse.branch_id' in request.args:
        title = 'Warehouses'
    else:
        if 'branch.region_id' in request.args:
            title = 'Branches'
        else:
            if 'region' in request.args:
                title = 'Regions'

    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=True, editable=True, ondelete=m_ondelete, maxtextlength=40)
    return dict(grid=grid, title=title, action=action)

# def m_oncreate(form):
#     if request.vars._formname == 'auth_user_form':
#         form.vars.password = 'Password1'

# Users
@auth.requires_membership('admin')
def manage_users():
    response.view = 'library/edit_record.html'
    title = request.vars['title']
    tablename = request.args(0)
    action = ''

    if tablename == 'org_access':
        if any(x in request.args for x in ['new', 'edit']):
            response.view = 'library/edit_org_access.html'
            action = 'new' if 'new' in request.args else 'edit'

    editing_user = False
    if tablename == 'auth_user':
        if any(x in request.args for x in ['new', 'edit']):
            response.view = 'library/edit_user.html'
            action = 'new' if 'new' in request.args else 'edit'
            if 'new' in request.args:
                db.auth_user.password.default = db.auth_user.password.requires[0]('Password1')[0]
                db.auth_user.password.writable = False
                db.auth_user.password.readable = False

    #         crypt_validator = db.auth_user.password.requires[0] # The validator is in a list.
    #         hash_password = lambda password: crypt_validator(password)[0]
    #         db.auth_user.password.default = hash_password('Password1')
            # db.auth_user.password.default = db.auth_user.password.requires[0]('Password1')[0]

    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], ondelete=m_ondelete,
        formname=tablename+'_form', maxtextlength=40,
        links = [lambda row: A(SPAN(XML("&nbsp"), _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
            'View (1)', _href=URL('library', 'manage_users', args=['auth_user', 'view', 'auth_user', row.id], 
            vars=dict(title='Users'), user_signature=True, hash_vars=False), 
            _class='button btn btn-secondary'),
        lambda row: A(SPAN(XML("&nbsp"), _class="icon pen icon-pencil glyphicon glyphicon-pencil"),
            'Edit (1)', _href=URL('library', 'manage_users', args=['auth_user', 'edit', 'auth_user', row.id], 
            vars=dict(title='Users'), user_signature=True, hash_vars=False), 
            _class='button btn btn-secondary'),
            ]
        )
    return dict(grid=grid, title=title, action=action)
