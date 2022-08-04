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

    # editing_user = False
    if tablename == 'auth_user':
        if any(x in request.args for x in ['new', 'edit']):
            response.view = 'library/edit_user.html'
            action = 'new' if 'new' in request.args else 'edit'
            if 'new' in request.args:
                # db.auth_user.password.default = db.auth_user.password.requires[0]('Password1')[0]
                # db.auth_user.password.writable = False
                # db.auth_user.password.readable = False
                redirect(URL('edit_user', vars=dict(title="Add User")))
            else:
                if request.env.http_referer:
                    session.back_url = request.env.http_referer
                else:
                    session.back_url = URL('library', 'manage_users', args='auth_user', vars=dict(title='Users'), user_signature=True )
                session.back_url = None
                # session.back_url = URL(args=request.args, vars=request.get_vars, host=True)
                # print('session.back_url = ', session.back_url)
                redirect(URL('edit_user', args=request.args[3], vars=dict(title="Edit User")))

    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], ondelete=m_ondelete,
        formname=tablename+'_form', maxtextlength=40,
        links = [
            lambda row: A(SPAN(XML("&nbsp"), _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
            'EDIT', _href=URL('library', 'edit_user', args=['auth_user', 'view', 'auth_user', row.id], 
            vars=dict(title='Users'), user_signature=True, hash_vars=False), 
            _class='button btn btn-secondary'),
            lambda row: A(SPAN(XML("&nbsp"), _class="icon pen icon-pencil glyphicon glyphicon-pencil"),
            'Edit (1)', _href=URL('library', 'manage_users', args=['auth_user', 'edit', 'auth_user', row.id], 
            vars=dict(title='Users'), user_signature=True, hash_vars=False), 
            _class='button btn btn-secondary'),
            ]
        )
    # grid.links = [lambda row: A('Test', _href="#")]
    return dict(grid=grid, title=title, action=action)

def editUserAnchor():
    anchor = A(SPAN(XML("&nbsp"), _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
            'EDIT', _href=URL('library', 'edit_user', args=['auth_user', 'view', 'auth_user', row.id], 
            vars=dict(title='Users'), user_signature=True, hash_vars=False), _class='button btn btn-secondary')
    return anchor

@auth.requires_login()
def add_user():
    return

@auth.requires_login()
def edit_user():
    # if request.args: there is always request.args(0)
    user = db.auth_user(request.args(0))
    user_loc = db.user_location(auth_user_id=user.id)
    fields = []
    for f in user: fields.append(f)
    for f in user_loc: fields.append(f)
    
    # print('////////////\n')
    # for f in fields: print(f)
    
    # else:
        # id not passed, new record
        # db.auth_user.password.default = db.auth_user.password.requires[0]('Password1')[0]

    db.auth_user.password.writable = False
    db.auth_user.password.readable = False
    db.user_location.auth_user_id.writable = False
    db.user_location.auth_user_id.readable = False

    emails = db(db.auth_user.email != user.email)
    db.auth_user.email.requires = IS_NOT_IN_DB(emails, 'auth_user.email')

    grid = SQLFORM.factory(db.auth_user, db.user_location, _class="web2py_grid")
    # if request.args:
    for f in db.auth_user:
        grid.vars[f.name] = user[f.name]
    for f in db.user_location:
        grid.vars[f.name] = user_loc[f.name]

    grid.element('#no_table_email')['_readonly'] = 'readonly'

    # if grid.process().accepted:
        # if grid.vars.id is None:
        #     print('id is none', grid.vars.id)
        #     # new record
        #     id = db.auth_user.insert(**db.auth_user._filter_fields(grid.vars))
        #     grid.vars.auth_user_id = id
        #     id = db.user_location.insert(**db.user_location._filter_fields(grid.vars))
        #     response.flash = 'New user added succesully.'
        # else:

    # if request.env.http_referer:
    #     back_url = request.env.http_referer
    # else:
    #     back_url = URL('library', 'manage_users', args='auth_user', vars=dict(title='Users'), user_signature=True )
                
    # print('(2) session.back_url = ', session.back_url)

    back_url = session.back_url or URL('library', 'manage_users', args='auth_user', vars=dict(title='Users'), user_signature=True )
    
    if grid.validate():
        # db.auth_user.update_record(**db.auth_user._filter_fields(grid.vars))
        # db.user_location.update_record(**db.user_location._filter_fields(grid.vars))
        user.update_record(**db.auth_user._filter_fields(grid.vars))
        user_loc.update_record(**db.user_location._filter_fields(grid.vars))
        response.flash = 'User record updated successfully.'
        print('(3) session.back_url = ', session.back_url)
        redirect( session.back_url )

    my_extra_element = DIV(
                            A(SPAN(XML("&nbsp"), _class="icon arrowleft icon-arrow-left glyphicon glyphicon-arrow-left"), 
                                SPAN('Back', _class="buttontext button", _title="Back"), 
                                _href=back_url, 
                                _class="button btn btn-default btn-secondary"),
                            # A(SPAN(XML("&nbsp"), _class="icon pen icon-pencil glyphicon glyphicon-pencil"), 
                            #     SPAN('Edit', _class="buttontext button"), _href=URL(), _class="button btn btn-secondary"),
                       _class="form_header row_buttons")
    grid[0].insert(0, my_extra_element)
    return dict(grid=grid, title=request.vars['title'])
