# -*- coding: utf-8 -*-
import utils

def index(): return dict(message="hello from opforms.py")



# Smart Grid for operattions documents/forms

# @auth.requires_membership('admin')
@auth.requires_login()
def grid():

    # import json

    branch_ids = []
    row = db(db.org_access.auth_user_id == auth.user_id ).select().first()
    if row:
        if row['pos_id'] is not None: db.point_of_sale._common_filter = lambda q: db.point_of_sale.id == row['pos_id']
        else: 
            if row['branch_id'] > -1: db.point_of_sale._common_filter = lambda q: db.point_of_sale.branch_id == row['branch_id']
            else: 
                if row['region_id'] > -1: 
                    for i in db(db.branch.region_id == r['region_id']):
                        branch_ids.append(i) 
                    db.point_of_sale._common_filter = lambda q: db.point_of_sale.branch_id in branch_ids
    last_nos = {}
    for r in db(db.point_of_sale).select():
        last_nos[r.id] = db(db.AAP.pos_id == r.id).select(db.AAP.doc_number.max().with_alias('max_no')).first()['max_no']
        last_nos[r.id] = utils.NextSequence(last_nos[r.id])

    title = request.vars['title']
    action = ''

    if any(x in request.args for x in ['new', 'edit']):
        response.view = 'opforms/edit_AAP.html'
        action = request.args(1)

    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], deletable=False, editable=True, searchable=dict(parent=True, child=True))
    return dict(grid=grid, title=title, action=action, last_nos=last_nos)
