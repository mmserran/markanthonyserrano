# -*- coding: utf-8 -*-

#### MANAGEMENT INTERFACE BEGIN ####################################################################
@is_owner
def home():
    return dict()

@is_owner
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
                     body = lambda r: A('Download', _class='btn', _href=URL('viewer', 'download', args=[r.file])) ),
                dict(header=T('Thumbnail'),
                     body = lambda r: A(IMG(_src=URL('viewer', 'download', args=[r.thumbnail]))) ),
                dict(header=T('Delete file'),
                     body = lambda r: A('Delete', _class='btn', _href=URL('manage', 'delete', args=[r.id, '0'])) )
                ]
            )
    return dict(grid=grid)

@is_owner
def delete():
    if request.args(1)=='0':
        upload = request.args(0)
        db(db.project.id==upload).delete()
        redirect(URL('manage', 'uploads'))
    else:
        upload = request.args(0)
        db(db.post.id==upload).delete()
        redirect(URL('manage', 'posts'))
        
    return dict()

@is_owner
def upload():
    fields = ['file', 'thumbnail'];
    form = SQLFORM(db.project, fields=fields, submit_button = 'Upload')
    
        
    if request.vars.file!=None:
        try:
            form.vars.filename = request.vars.file.filename
        except:
            pass
    else:
            form.vars.filename = ''
    if form.process().accepted:
        # Successful upload! Redirect the user to the upload page
        response.flash = 'Success! Uploaded'
        redirect(URL('manage', 'uploads'))
    elif form.errors:
        # There was an error let's let the user know
        response.flash = 'Error'
    return dict(form=form)

@is_owner
def posts():
    q = db.post
    if len(db(q).select()) == 0:
        grid=None
    else:
        grid = SQLFORM.grid(q,
            searchable=True,
            fields=[db.post.source, db.post.title, db.post.description, db.post.category, db.post.tag, db.post.other],
            csv=False, create=False, details=False, editable=True, deletable=True,
            links=[
                dict(header=T('Public Link'),
                    body = lambda r: A('Public Link', _class='btn', _href=URL('viewer', 'view', args=[r.title.replace(' ', '_')]))),
                dict(header=T('Download file'),
                    body = lambda r: A('Download', _class='btn', _href=URL('viewer', 'download', args=[r.source.file])) ),
                dict(header=T('Delete file'),
                     body = lambda r: A('Delete', _class='btn', _href=URL('manage', 'delete', args=[r.id, '1'])) )
                ]
            )
    return dict(grid=grid)

@is_owner
def post():
    fields = ['source', 'title', 'description', 'category', 'tag', 'other'];
    form = SQLFORM(db.post, fields=fields, submit_button = 'Post')
    if form.process().accepted:
        # Successful upload! Redirect the user to the manage page
        response.flash = 'Success! Posted.'
        redirect(URL('manage', 'posts'))
    elif form.errors:
        # There was an error let's let the user know
        response.flash = 'Error'
    return dict(form=form)
#### MANAGEMENT INTERFACE END ######################################################################