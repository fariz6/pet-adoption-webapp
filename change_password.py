#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cgitb.enable()

form = cgi.FieldStorage()

# Get form data
current_password = form.getvalue("current_password")
new_password = form.getvalue("new_password")
confirm_password = form.getvalue("confirm_password")
centreid = form.getvalue("centreid")

# Validate passwords
if new_password != confirm_password:
    print("<script>alert('New password and confirm password do not match!'); window.history.back();</script>")
    sys.exit()

try:
    con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
    cur = con.cursor()
    
    # First verify current password
    verify_query = "SELECT pass FROM care_reg WHERE centreid=%s"
    cur.execute(verify_query, (centreid,))
    result = cur.fetchone()
    
    if result and result[0] == current_password:
        # Update password
        update_query = "UPDATE care_reg SET pass=%s WHERE centreid=%s"
        cur.execute(update_query, (new_password, centreid))
        con.commit()
        print("<script>alert('Password updated successfully!'); window.location='care.py?centreid=" + centreid + "';</script>")
    else:
        print("<script>alert('Current password is incorrect!'); window.history.back();</script>")

except Exception as e:
    print(f"<script>alert('Error changing password: {str(e)}'); window.history.back();</script>")
finally:
    if 'con' in locals():
        con.close() 