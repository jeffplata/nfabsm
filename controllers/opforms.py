# -*- coding: utf-8 -*-
def index(): return dict(message="hello from opforms.py")


# Smart Grid for operattions documents/forms
@auth.requires_membership('admin')
def grid():
    title = request.vars['title']

    if any(x in request.args for x in ['new', 'edit']):
    # if ('edit' in request.args) or :
        response.view = 'opforms/edit_AAP.html'
        title = request.vars['title'] + ' [' + request.args(1) + ']'

    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], deletable=False, editable=True, searchable=dict(parent=True, child=True))
    return dict(grid=grid, title=title)
