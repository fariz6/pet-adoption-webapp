#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb
import sys
import os

cgitb.enable()

form = cgi.FieldStorage()
booking_id = form.getvalue("bookingid")
user_id = form.getvalue("id")

# Initialize connection variable
con = None

try:
    con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
    cur = con.cursor()

    # Update the status to 'cancelled'
    sql = "UPDATE bookings SET status = 'cancelled' WHERE bookingid = %s AND id = %s"
    cur.execute(sql, (booking_id, user_id))
    con.commit()

    # Redirect back to the orders page
    print(f"""
    <script>
        alert("Order has been cancelled successfully!");
        window.location.href = "userrecent.py?id={user_id}";
    </script>
    """)

except Exception as e:
    print(f"""
    <script>
        alert("Error cancelling order: {str(e)}");
        window.location.href = "userrecent.py?id={user_id}";
    </script>
    """)
finally:
    # Only try to close if connection was established
    if con is not None:
        con.close()