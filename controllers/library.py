# -*- coding: utf-8 -*-
def index(): return dict(message="hello from library.py")

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

# Users
@auth.requires_membership('admin')
def manage_users():
    response.view = 'library/edit_user.html'
    title = request.vars['title']
    tablename = request.args(0)    # it should be auth_user
    action = ''
    if not tablename in db.tables: raise HTTP(403)

    # todo: filter users according to admin's level of access
    myrows = None
    if session.user_branch_id:
        myrows = db(db.user_location.branch_id==session.user_branch_id).select(db.user_location.auth_user_id)
    else:
        if session.user_region_id:
            myrows = db(db.user_location.region_id==session.user_region_id).select(db.user_location.auth_user_id)
    if myrows:
        allowed_user_ids = [i['auth_user_id'] for i in myrows]
        db.auth_user._common_filter = lambda q: db.auth_user.id.belongs(allowed_user_ids)

    if tablename == 'auth_user':
        if any(x in request.args for x in ['new', 'edit']):
            action = 'new' if 'new' in request.args else 'edit'

            session.back_url = URL('library', 'manage_users', args='auth_user', vars=request.get_vars, user_signature=True )

            if 'new' in request.args:
                redirect(URL('add_user', vars=dict(title="Add User")))
            else:
                # session.back_url = URL(args=request.args, vars=request.get_vars, host=True)
                redirect(URL('edit_user', args=request.args[3], vars=dict(title="Edit User")))

    grid = SQLFORM.grid(db[tablename], args=[tablename], ondelete=m_ondelete,
        formname=tablename+'_form', maxtextlength=40,
        # links = [
        #     lambda row: A(SPAN(XML("&nbsp"), _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
        #     # 'EDIT', _href=URL('library', 'branches', args=8, 
        #     'EDIT', _href=URL('library', 'edit_user', args=['auth_user', 'view', 'auth_user', row.id], 
        #     vars=dict(title='Users'), user_signature=True, hash_vars=False), 
        #     _class='button btn btn-secondary'),
        #     lambda row: A(SPAN(XML("&nbsp"), _class="icon pen icon-pencil glyphicon glyphicon-pencil"),
        #     'Edit (1)', _href=URL('library', 'manage_users', args=['auth_user', 'edit', 'auth_user', row.id], 
        #     vars=dict(title='Users'), user_signature=True, hash_vars=False), 
        #     _class='button btn btn-secondary'),
        #     ]
        )
    # grid.links = [lambda row: A('Test', _href="#")]
    return dict(grid=grid, title=title, action=action)

def editUserAnchor():
    anchor = A(SPAN(XML("&nbsp"), _class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
            'EDIT', _href=URL('library', 'edit_user', args=['auth_user', 'view', 'auth_user', row.id], 
            vars=dict(title='Users'), user_signature=True, hash_vars=False), _class='button btn btn-secondary')
    return anchor

def form_extra_element(back_url):
    el = DIV(
            A(SPAN(XML("&nbsp"), _class="icon arrowleft icon-arrow-left glyphicon glyphicon-arrow-left"), 
                SPAN('Back', _class="buttontext button", _title="Back"), 
                _href=back_url, 
                _class="button btn btn-default btn-secondary"),
           _class="form_header row_buttons")
    return el

def branches():
    ops = ''
    if request.vars.region_id:
        if session.user_branch_id:
            branches = db(db.branch.id==session.user_branch_id).select(db.branch.ALL)
            ops1 = []
        else:
            branches = db(db.branch.region_id==request.vars.region_id).select(db.branch.ALL)
            ops1 = ['<option value=""></option>']
        [print(i['id'], i['branch_name']) for i in branches]
        ops = ops1 + [f"<option value={i['id']}>{i['branch_name']}</option>" for i in branches]
    return ops

def region_branch_common_filter():
    if session.user_region_id:
        db.region._common_filter = lambda q: db.region.id==session.user_region_id
        db.user_location.region_id.requires = IS_IN_DB(db, db.region.id, "%(region_name)s", zero=None)
        # if session.user_branch_id:
        #     db.branch._common_filter = lambda q: db.branch.id==session.user_branch_id
        #     db.user_location.branch_id.requires = IS_IN_DB(db, db.branch.id, '%(branch_name)s', zero=None)
        # else:
        #     db.branch._common_filter = lambda q: db.branch.region_id==session.user_region_id
        #     db.user_location.branch_id.requires = IS_IN_DB(db, db.branch.id, '%(branch_name)s')
    return None

@auth.requires_login()
def add_user():

    db.auth_user.password.default = db.auth_user.password.requires[0]('Password1')[0]
    db.auth_user.password.writable = False
    db.auth_user.password.readable = False
    db.user_location.auth_user_id.writable = False
    db.user_location.auth_user_id.readable = False

    region_branch_common_filter()

    response.view = 'library/edit_user.html'
    grid = SQLFORM.factory(db.auth_user, db.user_location, _class="web2py_grid")

    back_url = session.back_url or URL('library', 'manage_users', args='auth_user', vars=dict(title='Users'), user_signature=True )
    
    if grid.validate():
        id = db.auth_user.insert(**db.auth_user._filter_fields(grid.vars))
        if grid.vars.region_id:
            grid.vars.auth_user_id = id
            id = db.user_location.insert(**db.user_location._filter_fields(grid.vars))
        response.flash = 'New user added successfully.'
        redirect( back_url )

    my_extra_element = form_extra_element(back_url)
    grid[0].insert(0, my_extra_element)
    return dict(grid=grid, title=request.vars['title'])

@auth.requires_login()
def edit_user():
    user = db.auth_user(request.args(0))
    user_loc = db.user_location(auth_user_id=user.id)

    db.auth_user.password.writable = False
    db.auth_user.password.readable = False
    db.user_location.auth_user_id.writable = False
    db.user_location.auth_user_id.readable = False

    emails = db(db.auth_user.email != user.email)
    db.auth_user.email.requires = IS_NOT_IN_DB(emails, 'auth_user.email')

    region_branch_common_filter()

    grid = SQLFORM.factory(db.auth_user, db.user_location, _class="web2py_grid")
    for f in db.auth_user:
        grid.vars[f.name] = user[f.name]
    if user_loc:
        for f in db.user_location:
            grid.vars[f.name] = user_loc[f.name]

    grid.element('#no_table_email')['_readonly'] = 'readonly'

    back_url = session.back_url or URL('library', 'manage_users', args='auth_user', vars=dict(title='Users'), user_signature=True )
    
    if grid.validate():
        user.update_record(**db.auth_user._filter_fields(grid.vars))
        if user_loc:
            user_loc.update_record(**db.user_location._filter_fields(grid.vars))
        else:
            if grid.vars.region_id:
                grid.vars.auth_user_id = grid.vars.id
                db.user_location.insert(**db.user_location._filter_fields(grid.vars))
        response.flash = 'User record updated successfully.'
        redirect( back_url )

    my_extra_element = form_extra_element(back_url)
    grid[0].insert(0, my_extra_element)
    return dict(grid=grid, title=request.vars['title'])
