#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
import sys
import codecs
import pymysql
import cgi
import json

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print("Content-type: application/json; charset=utf-8\n\n")

form = cgi.FieldStorage()
center_id = form.getvalue('center_id')

if not center_id:
    print(json.dumps({"error": "Center ID is required"}))
    sys.exit()

try:
    con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
    cur = con.cursor()
    
    cur.execute("""
        SELECT careid, centername, ownername, contact, email, address, city, state, pincode, 
               description, facilities, opening_hours, rating, image
        FROM careresource_info 
        WHERE careid = %s
    """, (center_id,))
    
    center = cur.fetchone()
    
    if center:
        center_data = {
            "careid": center[0],
            "centername": center[1],
            "ownername": center[2],
            "contact": center[3],
            "email": center[4],
            "address": center[5],
            "city": center[6],
            "state": center[7],
            "pincode": center[8],
            "description": center[9],
            "facilities": center[10],
            "opening_hours": center[11],
            "rating": center[12],
            "image": center[13]
        }
        print(json.dumps(center_data))
    else:
        print(json.dumps({"error": "Center not found"}))
    
    cur.close()
    con.close()
    
except Exception as e:
    print(json.dumps({"error": str(e)})) 