# -*- coding: utf-8 -*-

#### FRONTEND UI BEGIN #############################################################################
def home():
    """
    homepage of markanthonyserrano.com
    """
    return dict()

def main():
    return dict()

def contactme():
    form = SQLFORM.factory(
        Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()], default="youremail@domain.com"),
        Field('subject', requires=IS_NOT_EMPTY()),
        Field('message', 'text', default="Sorry, this form is not working just yet. Please instead compose your email in some other functional mail application"))
    if form.process().accepted:
        session.flash = 'mail sent!'
        mail.send(to=['mmserran@me.com'],
          subject=form.vars.subject,
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to=form.vars.email,
          message=form.vars.message)
    elif form.errors:
        session.flash = 'form has errors'
    return dict(form=form)

def createQuery():  
    session.reset = True
    ''' BEGIN GENERATE AVAILABLE TAGS '''''''''''''''
    tags_available = []
    
    # Selector Data
    category = request.vars.values()[0]
    session.category = category
    
    if category == 'All':
        # Get all tags
        group = db(db.post).select()
    else:
        # Get set of all tags in category
        group = db(db.post.category == category).select()
       
    # Convert to list of unique tags 
    for row in group:
        tags_available += row.tag
    tags_available = list(set(tags_available))
    
    # Convert to dict with selected status at default on
    tags_selected = dict(zip(tags_available, (True for num in tags_available)))
    
    if '' in tags_selected:
        del tags_selected['']
    
    ''' END GENERATE AVAILABLE TAGS '''''''''''''''
    
    ''' BEGIN CREATE/OVERWRITE tags_selected COOKIE '''''''''''''''
    # Create/Overwrite JSON formatted cookie
    session.tags_selected = tags_selected
    ''' END CREATE/OVERWRITE tags_selected COOKIE '''''''''''''''
    
    return dict(tagList_selected=tags_selected, 
                order=list(sorted(session.tags_selected)))

def modifyQuery():
    tagtoToggle = request.vars.values()[0]
    
    ''' BEGIN TOGGLE STR tagtoToggle in DICT tags_selected '''''''''''''''
    # Modify tags_selected to user input
    session.tags_selected[tagtoToggle] = not session.tags_selected[tagtoToggle]
    ''' END TOGGLE STR tagtoToggle in DICT tags_selected '''''''''''''''
    
    if session.reset:
        for tag in session.tags_selected.keys():
            session.tags_selected[tag] = False
        session.tags_selected[tagtoToggle] = True
    
    session.reset = False
    return dict(tagList_selected=session.tags_selected, 
                order=sorted(session.tags_selected))

def loading():
    
    # Grid Data
    results = db(db.post.title==None).select()
    for tag, selected in session.tags_selected.items():
        if selected:
            q1 = db.post.tag.contains(tag)
            if session.category!='All':
                q2 = db.post.category==session.category
                results = results | db(q1)(q2).select()
            else:
                results = results | db(q1).select()
    
    
    return dict(numPosts=len(results))

def updateGrid():
        # Grid Data
    results = db(db.post.title==None).select()
    for tag, selected in session.tags_selected.items():
        if selected:
            q1 = db.post.tag.contains(tag)
            if session.category!='All':
                q2 = db.post.category==session.category
                results = results | db(q1)(q2).select()
            else:
                results = results | db(q1).select()
    
    return dict(results=results)

def post():
    
    title = request.vars.values()[0]
    
    q = db.post.title==title
    record = db(q).select().first()
    
    
    if not owner():
        # only increment if a visitor visits
        count=-1
        record.update_record(counter=(int(record.counter) + 1))
    else:
        # only the owner may see the page counter
        count=record.counter
    
    return dict(post=record, count=count)
#### FRONTEND UI END ###############################################################################



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
