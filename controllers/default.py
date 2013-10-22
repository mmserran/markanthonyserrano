# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

#### FRONTEND UI BEGIN #############################################################################
def index():
    """
    homepage of markanthonyserrano.com
    """
    return dict()

def portfolio():
    return dict()

def view():
    record = db(db.post.source.filename==request.args(0)).select().first()
    db.post[record.id] = dict(counter=(int(record.counter) + 1))
    
    return dict(record=record)
#### FRONTEND UI END ###############################################################################

#### MANAGEMENT INTERFACE BEGIN ####################################################################
@auth.requires_login()
def manage():
    q = db.post
    if len(db(q).select()) == 0:
        return dict(grid=None)
    else:
        grid = SQLFORM.grid(q,
            searchable=True,
            fields=[db.post.source, db.post.description, db.post.tag],
            csv=False, create=False, details=False, editable=True, deletable=True,
            links=[
                dict(header=T('Public Link'),
                    body = lambda r: A('Public Link', _class='btn', _href=URL('default', 'view', args=[r.id]))),
                dict(header=T('Download file'),
                    body = lambda r: A('Download', _class='btn', _href=URL('default', 'download', args=[r.source.file])) )
                ]
            )

        return dict(grid=grid)

@auth.requires_login()
def upload():
    fields = ['filename', 'file', 'thumbnail'];
    form = SQLFORM(db.project, fields=fields, submit_button = 'Upload')
    if request.vars.file!=None:
            form.vars.filename = request.vars.file.filename
    if form.process().accepted:
        # Successful upload! Redirect the user to the upload page
        response.flash = 'Success! Uploaded'
        redirect(URL('upload'))
    elif form.errors:
        # There was an error let's let the user know
        response.flash = 'Error'
    
    q = db.project
    if len(db(q).select()) == 0:
        return dict(grid=None, form=form)
    else:
        grid = SQLFORM.grid(q,
            searchable=True,
            fields=[db.project.filename, db.project.file],
            csv=False, create=False, details=False, editable=True, deletable=True,
            links=[
                dict(header=T('Download file'),
                    body = lambda r: A('Download', _class='btn', _href=URL('default', 'download', args=[r.file])) )
                ]
            )
        return dict(grid=grid, form=form)

def post():
    fields = ['source', 'description', 'tag'];
    form = SQLFORM(db.post, fields=fields, submit_button = 'Post')
    if form.process().accepted:
        # Successful upload! Redirect the user to the manage page
        response.flash = 'Success! Posted.'
        redirect(URL('manage'))
    elif form.errors:
        # There was an error let's let the user know
        response.flash = 'Error'
    return dict(form=form)
#### MANAGEMENT INTERFACE END ######################################################################

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
