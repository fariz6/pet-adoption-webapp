#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os

cgitb.enable()

try:
    con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
    cur = con.cursor()
except Exception as e:
    print(f"<script>alert('Database connection failed: {str(e)}');</script>")
    sys.exit(1)

form = cgi.FieldStorage()
careid = form.getvalue("careid")

if careid:
    try:
        # First, get the image path to delete the file
        cur.execute("SELECT Image FROM careresource_info WHERE centerid = %s", (careid,))
        result = cur.fetchone()
        
        if result and result[0]:
            image_path = os.path.join("images", result[0])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete the record from the database
        cur.execute("DELETE FROM careresource_info WHERE centerid = %s", (careid,))
        con.commit()
        
        print("""
        <script>
            alert('Care center deleted successfully!');
            window.location.href = 'care.py';
        </script>
        """)
    except Exception as e:
        print(f"""
        <script>
            alert('Error deleting care center: {str(e)}');
            window.location.href = 'care.py';
        </script>
        """)
        con.rollback()
else:
    print("""
    <script>
        alert('Invalid request');
        window.location.href = 'care.py';
    </script>
    """) 