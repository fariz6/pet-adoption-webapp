#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cgitb.enable()

def safe_write_file(filepath, content):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"<script>alert('Error saving file: {str(e)}');</script>")
        return False

form = cgi.FieldStorage()

# Get form data
sheltername = form.getvalue("sheltername")
email = form.getvalue("email")
phone = form.getvalue("phone")
address = form.getvalue("address")
centreid = form.getvalue("centreid")

# Handle profile picture upload
profile_pic = None
if "profile_pic" in form:
    fileitem = form["profile_pic"]
    if fileitem.filename:
        # Get the file extension
        fn = os.path.basename(fileitem.filename)
        ext = os.path.splitext(fn)[1]
        # Create new filename
        new_filename = f"profile_{centreid}{ext}"
        filepath = os.path.join("profile_pics", new_filename)
        
        if safe_write_file(filepath, fileitem.file.read()):
            profile_pic = new_filename

try:
    con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
    cur = con.cursor()
    
    # Update query
    if profile_pic:
        update_query = """UPDATE care_reg 
                         SET sheltername=%s, email=%s, mob=%s, street=%s, profile_pic=%s 
                         WHERE centreid=%s"""
        cur.execute(update_query, (sheltername, email, phone, address, profile_pic, centreid))
    else:
        update_query = """UPDATE care_reg 
                         SET sheltername=%s, email=%s, mob=%s, street=%s 
                         WHERE centreid=%s"""
        cur.execute(update_query, (sheltername, email, phone, address, centreid))
    
    con.commit()
    print("<script>alert('Profile updated successfully!'); window.location='care.py?centreid=" + centreid + "';</script>")

except Exception as e:
    print(f"<script>alert('Error updating profile: {str(e)}'); window.history.back();</script>")
finally:
    if 'con' in locals():
        con.close() 