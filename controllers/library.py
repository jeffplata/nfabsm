# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from library.py")

# @auth.requires_membership('admin')
# def regions():
#     tablename = request.args(0)
#     grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
#     return locals()

@auth.requires_membership('admin')
def grid():
    tablename = request.args(0)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return locals()