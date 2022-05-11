# -*- coding: utf-8 -*-
def index(): return dict(message="hello from opforms.py")


# Smart Grid for operattions documents/forms
@auth.requires_membership('admin')
def grid():
    tablename = request.args(0)
    title = request.vars['title']
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid, title=title)
