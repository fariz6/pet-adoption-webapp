#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")

import pymysql

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

try:
    # Get table structure
    cur.execute("DESCRIBE serviceprice")
    columns = cur.fetchall()
    
    print("<h2>Serviceprice Table Structure</h2>")
    print("<table border='1'>")
    print("<tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th><th>Extra</th></tr>")
    for col in columns:
        print(f"<tr><td>{col[0]}</td><td>{col[1]}</td><td>{col[2]}</td><td>{col[3]}</td><td>{col[4]}</td><td>{col[5]}</td></tr>")
    print("</table>")
    
    # Get sample data
    cur.execute("SELECT * FROM serviceprice LIMIT 5")
    rows = cur.fetchall()
    
    print("<h2>Sample Data</h2>")
    print("<table border='1'>")
    print("<tr><th>ID</th><th>CenterID</th><th>ServiceType</th><th>ServicePrice</th></tr>")
    for row in rows:
        print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>")
    print("</table>")
    
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    con.close() 