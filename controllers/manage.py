# -*- coding: utf-8 -*-

#### MANAGEMENT INTERFACE BEGIN ####################################################################
@auth.requires_login()
def index():
    return dict()

def uploads():
    q = db.project
    if len(db(q).select()) == 0:
        grid=None
    else:
        grid = SQLFORM.grid(q,
            searchable=True,
            fields=[db.project.filename, db.project.file, db.project.thumbnail],
            csv=False, create=False, details=False, editable=True, deletable=True,
            links=[
                dict(header=T('Download file'),
                     body = lambda r: A('Download', _class='btn', _href=URL('default', 'download', args=[r.file])) ),
                dict(header=T('Thumbnail'),
                     body = lambda r: A(IMG(_src=URL('default', 'download', args=[r.thumbnail]))) )
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
    return dict(form=form)

def posts():
    q = db.post
    if len(db(q).select()) == 0:
        grid=None
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