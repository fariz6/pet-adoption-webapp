#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
# Add debug output to see what's happening
import os
import sys
import traceback

# Make errors visible in the browser
print("Content-type: text/html\n\n")
print("<html><head><title>Pet Deletion</title></head><body>")
print("<h2>Processing Pet Deletion</h2>")

try:
    import pymysql
    import cgi
    import cgitb

    # Enable detailed error reporting
    cgitb.enable(display=1)

    # Get form data
    form = cgi.FieldStorage()
    pet_id = form.getvalue("pet_id")
    shelter_id = form.getvalue("shelter_id")

    print(f"<p>Attempting to delete pet ID: {pet_id}</p>")
    print(f"<p>Shelter ID: {shelter_id}</p>")

    if not pet_id or not shelter_id:
        print("<p style='color:red'>Error: Missing pet_id or shelter_id parameter</p>")
        print("<p><a href='javascript:history.back()'>Go Back</a></p>")
    else:
        # Create database connection
        con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
        cur = con.cursor()

        print("<p>Database connection established</p>")

        # Delete pet from product_info table
        delete_query = """DELETE FROM product_info WHERE product_id = %s"""
        cur.execute(delete_query, (pet_id,))
        rows_affected = cur.rowcount
        con.commit()
        con.close()

        print(f"<p>Query executed. Rows affected: {rows_affected}</p>")

        if rows_affected > 0:
            print("<p style='color:green'>Pet deleted successfully!</p>")
        else:
            print("<p style='color:orange'>No pet found with that ID or already deleted.</p>")

        # JavaScript redirect
        print(f"""
        <script>
            alert("Pet removed successfully!");
            window.location.href = "newshelterdash.py?shelter_id={shelter_id}";
        </script>
        """)

except Exception as e:
    print("<p style='color:red'>An error occurred:</p>")
    print(f"<pre>{traceback.format_exc()}</pre>")
    print("<p><a href='javascript:history.back()'>Go Back</a></p>")

print("</body></html>")