from collections import namedtuple
import sqlite3

Link=namedtuple('List',['id','name','age','school_name','marks'])

list=[
    Link(1,'gurjot',23,'ster',98),
    Link(2,'jot',3,'sero',78),
    Link(3,'gu',2,'ste',90)
    ]

#creating databse connection
db=sqlite3.connect(':memory:')
#creating table in named gurjot
db.execute('create table gurjot '+'(id integer,name text,age integer,school_name text,marks integer)')
#inserting values from a list into a database table
for j in list:
    db.execute('insert into gurjot values(?,?,?,?,?)',j)


#executing select query on table named gurjot
c=db.execute('select * from gurjot')
#c is a cursor that points to the rows entry of gurjot table 
for k in c:
    #we are creating a object of type Link and then using dot operator we are accessing various attributes
    link=Link(*k)
    print link.name+' has obtained '+str(link.marks)+' and his school is '+link.school_name+'\n'
    

    
