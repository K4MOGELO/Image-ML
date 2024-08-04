import pyodbc

conn = pyodbc.connect('DRIVER={SQL SERVER};'
                       'SERVER=DESKTOP-S1F7VIB;'
                       'DATABASE=SyruProjects;'
                      )

cursor = conn.cursor()


sql_insert = "INSERT INTO Person (email,name,last_name,password, role) VALUES (?,?,?,?,?)"


def insert(email, firstName, lastName, password, role):
    data = (email,firstName,lastName,password, role)
    
    try:
        cursor.execute(sql_insert, data)
        conn.commit()
        print("Data inserted successfully")
        
    except Exception as e:
        conn.rollback()
        print("Error inserting data: ", e)
        
    cursor.close()
    conn.close()