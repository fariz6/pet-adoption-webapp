#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
import sys
import json
import pymysql
import cgi
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print("Content-type: application/json; charset=utf-8\n\n")

form = cgi.FieldStorage()
booking_id = form.getvalue('booking_id')

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

# Fetch booking details
cur.execute("""
    SELECT 
        cb.carebookingid, cb.centerid, cb.date, cb.caretype,
        ci.centername, sp.serviceprice
    FROM 
        carebookings cb
    JOIN 
        careresource_info ci ON cb.centerid = ci.careid
    JOIN 
        serviceprice sp ON cb.centerid = sp.careid AND cb.caretype = sp.servicetype
    WHERE 
        cb.carebookingid = %s
""", (booking_id,))

booking = cur.fetchone()

if booking:
    response = {
        'success': True,
        'bookingId': booking[0],
        'centerId': booking[1],
        'bookingDate': booking[2].strftime('%Y-%m-%d'),
        'careType': booking[3],
        'centerName': booking[4],
        'amount': float(booking[5])
    }
else:
    response = {
        'success': False,
        'message': 'Booking not found'
    }

print(json.dumps(response)) 