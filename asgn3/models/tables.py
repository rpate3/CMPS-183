#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
from datetime import datetime

def getname():
    name = 'Nobody'
    if auth.user:
        name = auth.user.first_name
    return name

db.define_table('b_board',
                Field('name', required=True),
                Field('description', 'text'),
                Field('id')
                )

db.define_table('p_post',
    Field('name'),
    Field('description', 'text'),
    Field('user_id', db.auth_user),
    Field('post_time', 'datetime', default=datetime.utcnow()),
    Field('board_id', db.b_board)
    )

db.p_post.description.label = 'Message'
db.b_board.id.readable = False
db.p_post.id.readable = False


db.p_post.board_id.writable = False
db.p_post.board_id.readable = False

db.p_post.user_id.writable = db.p_post.user_id.readable = False
db.p_post.post_time.writable = False
db.p_post.user_id.default = auth.user_id
