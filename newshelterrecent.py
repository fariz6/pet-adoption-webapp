#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
from flask import Flask, render_template
import mysql.connector
from datetime import datetime

cgitb.enable()

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'petcare'
}

@app.route('/shelter_adoptions')
def show_shelter_adoptions():
    try:
        # Establish database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to get adoption information
        query = """
        SELECT 
            b.booking_id,
            b.adopted_status,
            p.product_id,
            p.Petname,
            p.Species,
            p.Breed,
            p.Age,
            p.Gender,
            p.Image,
            s.Sheltername,
            s.Email as shelter_email,
            s.Address,
            s.City,
            s.State,
            s.Phone,
            b.booking_date,
            u.username as adopter_name,
            u.email as adopter_email
        FROM bookings b
        JOIN product_info p ON b.product_id = p.product_id
        JOIN shelter_info s ON p.shelter_id = s.shelter_id
        LEFT JOIN users u ON b.user_id = u.user_id
        WHERE b.adopted_status = 'Adopted'
        ORDER BY b.booking_date DESC
        """

        cursor.execute(query)
        adoptions = cursor.fetchall()

        return render_template('shelter_adoptions.html', adoptions=adoptions)

    except mysql.connector.Error as err:
        return f"Database Error: {err}"
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

# Get shelter_id from form
form = cgi.FieldStorage()
shelter_id = form.getvalue("shelter_id")

# SQL query to join the tables and filter by shelter_id and adopted status
query = """
SELECT DISTINCT p.*, b.booking_id, b.booking_date, b.status, b.ownername
FROM product_info p
INNER JOIN bookings b ON p.product_id = b.product_id
INNER JOIN shelter_info s ON p.shelter_id = s.shelter_id
WHERE p.shelter_id = %s AND b.status = 'adopted'
ORDER BY b.booking_date DESC
"""

# Execute query with shelter_id parameter
cur.execute(query, (shelter_id,))
results = cur.fetchall()

def get_status_color(status):
    status_colors = {
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'completed': 'info'
    }
    return status_colors.get(status.lower(), 'secondary')

# HTML output
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recent Bookings</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            padding: 20px;
        }
        .table-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .table th {
            background-color: #6C63FF;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container table-container">
        <h2 class="mb-4">Recent Bookings</h2>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Booking ID</th>
                        <th>Pet Name</th>
                        <th>Owner Name</th>
                        <th>Booking Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
""")

# Display results in table
for row in results:
    print(f"""
    <tr>
        <td>{row[0]}</td>
        <td>{row['petname']}</td>
        <td>{row['ownername']}</td>
        <td>{row['booking_date']}</td>
        <td><span class="badge bg-{get_status_color(row['status'])}">{row['status']}</span></td>
    </tr>
    """)

print("""
                </tbody>
            </table>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()

if __name__ == '__main__':
    app.run(debug=True) 