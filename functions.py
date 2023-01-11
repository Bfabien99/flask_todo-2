import pymysql

def Connect():
    conn = None
    try:
        conn = pymysql.connect(host="sql11.freemysqlhosting.net", port=3306, user="sql11589853", passwd="BUtDMeHHSx", database="sql11589853", cursorclass=pymysql.cursors.DictCursor)
    except pymysql.Error as e:
        print(e)
    return conn


def findAll():
    conn = Connect()
    cursor = conn.cursor()
    
    sql = f"SELECT * FROM todosapi"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if result:
        return result
    return False


def findCompleted():
    conn = Connect()
    cursor = conn.cursor()
    
    sql = f"SELECT * FROM todosapi WHERE completed = 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if result:
        return result
    return False


def findIncompleted():
    conn = Connect()
    cursor = conn.cursor()
    
    sql = f"SELECT * FROM todosapi WHERE completed = 0"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if result:
        return result
    return False


def findOne(table, champ, valeur):
    conn = Connect()
    cursor = conn.cursor()
    
    sql = f"SELECT * FROM {table} WHERE {champ} = '{valeur}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result:
        return result
    return False