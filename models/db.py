# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite')
## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.actions_disabled.append('register')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## tables
import datetime

db.define_table('project',
    Field('filename'),
    Field('file', 'upload'),
    Field('thumbnail', 'upload'),
    format = '%(filename)s')

db.define_table('post',
    Field('source', 'reference project', unique=True),
    Field('description', 'text'),
    Field('tag', 'list:string'),
    Field('date', 'datetime', default=datetime.datetime.utcnow()),
    Field('counter', 'integer', default=0))

db.project.filename.writable = False
db.post.date.writable    = db.post.date.readable    = False
db.post.counter.writable = db.post.counter.readable = False
## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
