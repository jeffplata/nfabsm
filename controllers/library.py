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


@auth.requires_membership('admin')
def sgrid():
    response.view = 'library/edit_record.html'
    title = request.vars['title']
    tablename = request.args(0)
    action = ''

    if tablename == 'org_access':
        if any(x in request.args for x in ['new', 'edit']):
            response.view = 'library/edit_org_access.html'
            action = 'new' if 'new' in request.args else 'edit'

    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=True, editable=True, ondelete=m_ondelete, maxtextlength=40)
    return dict(grid=grid, title=title, action=action)

@auth.requires_membership('admin')
def grid():
    response.view = 'library/edit_record.html'
    title = request.vars['title']
    tablename = request.args(0)
    action = ''

    if tablename == 'org_access':
        if any(x in request.args for x in ['new', 'edit']):
            response.view = 'library/edit_org_access.html'
            action = 'new' if 'new' in request.args else 'edit'

    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], deletable=True, editable=True, ondelete=m_ondelete, maxtextlength=40)
    return dict(grid=grid, title=title, action=action)
