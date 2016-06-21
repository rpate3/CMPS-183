# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """

    Allows a person to register in the system, if they are not registered already.
    """
    boardList = db(db.b_board).select()
    return dict(boardList=boardList)


def show_posts():
    board_id = request.args(0)
    post_list = db(db.p_post.board_id == board_id).select(db.p_post.ALL,orderby=~db.p_post.post_time)
    return dict(post_list=post_list, board_id=board_id)


def add_board():
    """Lets user add board"""
    form = SQLFORM(db.b_board)
    if form.process().accepted:
        session.flash = T('The data inserted')
        redirect(URL('default', 'index'))
    return dict(form=form)

def view():
    """View a post."""
    p = db.p_post(request.args(0)) or redirect(URL('default', 'index'))
    form = SQLFORM(db.p_post, record=p, readonly=True)
    return dict(form=form)

def add_post():
    form = SQLFORM(db.p_post)
    board_id= request.args(0)
    db.p_post.board_id.default = board_id
    if form.process().accepted:
        session.flash = T('The data inserted')
        redirect(URL('default', 'show_posts', args=[board_id]))
    return dict(form=form)



@auth.requires_login()
def edit_post():
    x = db.p_post(request.args(0))
    form = SQLFORM(db.p_post, record=x)
    if form.process().accepted:
        session.flash = T('Updated')
        redirect(URL('default', 'view', args=[x]))
    return dict(form=form)
#def view
#@auth.requires_login()
#def edit_post():
 #   """View a post."""
  #  # p = db(db.bboard.id == request.args(0)).select().first()
  #  p = db.pst(request.args(0)) or redirect(URL('default', 'show_posts'))
  #  if p.user_id != auth.user_id:
  #      session.flash = T('Not authorized.')
  #      redirect(URL('default', 'index'))
  #  form = SQLFORM(db.pst, record=p)
  #  if form.process().accepted:
  #      session.flash = T('Updated')
  #      redirect(URL('default', 'show_posts', args=[p.id]))
    # p.name would contain the name of the poster.
  #  return dict(form=form)

#@auth.requires_login()
#def post_edit():
#    post = db.post(request.args(0))
 #   if post is None:
 #       session.flash = T('No such store')
 #       redirect(URL('default', 'show_posts'))
 #   form = SQLFORM(db.post, record=post)
 #   if form.process().accepted:
 #       session.flash = T('The data was edited')
 #       redirect(URL('default', 'board_details', args=[post.id]))
 #   edit_button = A('View', _class='btn btn-warning',
 #                   _href=URL('default', 'show_posts', args=[post.id]))
 #   return dict(form=form, edit_button=edit_button)


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
    http://..../[app]/default/user/bulk_register
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
