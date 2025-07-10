#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: application/json\n\n")

import pymysql
import cgi
import cgitb
import json

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

form = cgi.FieldStorage()
action = form.getvalue("action")
centerid = form.getvalue("centerid")

try:
    if action == "add":
        servicetype = form.getvalue("servicetype")
        serviceprice = form.getvalue("serviceprice")
        
        # Insert new service
        cur.execute("""
            INSERT INTO serviceprice (centerid, servicetype, serviceprice)
            VALUES (%s, %s, %s)
        """, (centerid, servicetype, serviceprice))
        
        con.commit()
        print(json.dumps({"success": True, "message": "Service added successfully"}))
        
    elif action == "delete":
        serviceid = form.getvalue("serviceid")
        cur.execute("DELETE FROM serviceprice WHERE id = %s AND centerid = %s", (serviceid, centerid))
        con.commit()
        print(json.dumps({"success": True, "message": "Service deleted successfully"}))
        
    else:
        print(json.dumps({"success": False, "message": "Invalid action"}))
        
except Exception as e:
    print(json.dumps({"success": False, "message": str(e)}))
finally:
    con.close() 