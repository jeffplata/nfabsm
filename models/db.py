# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

db.define_table('region',
    Field('region_name', 'string', length=80, unique=True),
    Field('alternate_name', 'string', length=80, unique=True),
    format='%(region_name)s')

db.region.region_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.region.region_name)]
db.region.alternate_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.region.alternate_name)]

db.define_table('branch',
    Field('branch_name', 'string', length=80, unique=True),
    Field('region_id', db.region, label='Region'),
    format='%(branch_name)s')

db.branch.branch_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.branch.branch_name)]


db.define_table('warehouse',
    Field('warehouse_name', 'string', length=80, unique=True),
    Field('warehouse_code', 'string', length=20, unique=True),
    Field('branch_id', db.branch, label='Branch'),
    format='%(warehouse_name)s')

db.warehouse.warehouse_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.warehouse.warehouse_name)]
db.warehouse.warehouse_code.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.warehouse.warehouse_code)]

db.define_table('container',
    Field('container_name', 'string', length=20, unique=True),
    Field('container_shortname', 'string', length=20, unique=True),
    Field('weight', 'decimal(8,2)'),
    format='%(container_name)s')

db.container.container_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.container.container_name)]
db.container.container_shortname.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.container.container_shortname)]


db.define_table('commodity',
    Field('commodity_name', 'string', length=80, unique=True),
    Field('is_cereal', 'boolean', default=True),
    format='%(commodity_name)s')

db.commodity.commodity_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.commodity.commodity_name)]
db.commodity.is_cereal.default = True

db.define_table('variety',
    Field('variety_name', 'string', length=20, unique=True),
    Field('commodity_id', db.commodity, label='Commodity'),
    format='%(variety_name)s')


db.variety.variety_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.variety.variety_name)]

db.define_table('item',
    Field('item_name', 'string', length=80, unique=True),
    Field('variety_id', db.variety, label='Variety'),
    Field('container_id', db.container, label='Container'),
    Field('selling_price', 'decimal(15,2)'),
    format='%(item_name)s')

db.item.item_name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.item.item_name)]

doc_stamp = db.Table(db, 'doc_stamp',
    Field('doc_date', 'date', default=request.now, requires=IS_DATE(format='%m/%d/%Y') ),
    Field('doc_number', 'string', length=40, unique=True))

db.define_table('AAP', 
    doc_stamp,
    Field('customer', 'string', length=80),
    # Field('item_id', db.item, label='Item'),
    Field('variety_id', db.variety, label='Variety'),
    Field('container_id', db.container, label='Container'),
    Field('bags', 'integer'),
    Field('net_kg_qty', 'decimal(15,2)', label='Net Kg or Quantity'),
    Field('selling_price', 'decimal(15,2)'),
    Field('amount', 'decimal(15,2)'),
    Field('check_no', 'string', length=40),
    Field('warehouse_id', db.warehouse, label='Warehouse'),
    Field('prepared_by', 'string', length=80),
    Field('approved_by', 'string', length=80),
    auth.signature, 
    singular='AAP', plural='AAPs')
 