import pymysql
db=pymysql.connect(user="root",password="",host="localhost",database="mobiles")
def insert(data):
    cu=db.cursor()
    cu.execute(data)
    db.commit() 

def selectone(data):
    cu=db.cursor()
    cu.execute(data)
    d=cu.fetchone()
    return d
def selectall(data):
    cu=db.cursor()
    cu.execute(data)
    data=cu.fetchall()
    return data
def update(data):
    cu=db.cursor()
    cu.execute(data)
    db.commit()


    
