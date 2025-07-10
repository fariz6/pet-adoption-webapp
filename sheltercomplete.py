#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Sid=form.getvalue("shelter_id")
# HTML Form
print("""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - Pets List</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #6C63FF;
            --secondary-color: #FF6584;
            --light-color: #F8F9FA;
            --dark-color: #343A40;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
        }

        .navbar {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .main-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            margin: 2rem auto;
            flex: 1;
        }

        .section-title {
            position: relative;
            margin-bottom: 2rem;
            padding-bottom: 0.5rem;
        }

        .section-title:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 50px;
            height: 3px;
            background-color: var(--primary-color);
        }

        /* Custom table styles */
        .pets-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }

        .pets-table thead {
            background: linear-gradient(135deg, #6C63FF 0%, #FF6584 100%);
            color: white;
        }

        .pets-table th {
            padding: 1rem;
            text-align: left;
        }

        .pets-table td {
            padding: 1rem;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
        }

        .pets-table tbody tr:last-child td {
            border-bottom: none;
        }

        .pets-table tbody tr:hover {
            background-color: rgba(108, 99, 255, 0.05);
        }

        .pet-image {
            width: 60px;
            height: 60px;
            object-fit: cover;
            border-radius: 50%;
            margin-right: 1rem;
        }

        .pet-info {
            display: flex;
            align-items: center;
        }

        .badge-available {
            background-color: #28a745;
        }

        .badge-adopted {
            background-color: var(--secondary-color);
        }

        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 3rem 0;
            margin-top: auto;
        }

        .footer-links h5 {
            margin-bottom: 1.5rem;
            position: relative;
        }

        .footer-links h5:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -10px;
            width: 40px;
            height: 2px;
            background-color: var(--primary-color);
        }

        .footer-links ul {
            list-style: none;
            padding-left: 0;
        }

        .footer-links li {
            margin-bottom: 0.5rem;
        }

        .footer-links a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer-links a:hover {
            color: white;
        }

        .social-icons a {
            display: inline-block;
            width: 40px;
            height: 40px;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            margin-right: 10px;
            transition: all 0.3s;
        }

        .social-icons a:hover {
            background-color: var(--primary-color);
            transform: translateY(-3px);
        }

        .copyright {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 1.5rem;
            margin-top: 2rem;
        }

        /* Nested table styles */
        .nested-table {
            width: 100%;
            border-collapse: collapse;
        }

        .nested-table th, .nested-table td {
            padding: 0.75rem;
            border: 1px solid #dee2e6;
        }

        .nested-table thead {
            background-color: #f8f9fa;
        }

        .nested-table tbody tr:nth-child(even) {
            background-color: rgba(0, 0, 0, 0.02);
        }

.modal-content {
  border: none;
  border-radius: 1rem;
}

.details p {
  margin: 0.2rem 0;
  font-size: 1rem;
}


    </style>
</head>
<body>
    <!-- Navbar (same as your user dashboard) -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
        <div class="container">
            <a class="navbar-brand text-primary" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="myOrdersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> My Orders
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="shelterrecent.py?id=%s">Recent</a></li>
                            <li><a class="dropdown-item" href="sheltercomplete.py?id=%s">Completed</a></li>
                        </ul>
                    </li>

                </ul>
            </div>
        </div>
    </nav>""")

# Fetch completed bookings with product info
s = """
SELECT b.*, p.Sheltername, p.Email as shelter_email
FROM bookings b 
JOIN product_info p ON b.product_id = p.product_id 
WHERE b.status="accepted"
ORDER BY b.bookingid DESC
"""
cur.execute(s)
bookings = cur.fetchall()

print(f"""  <!-- Main Content -->
    <div class="container main-container">
        <h2 class="section-title">Completed Adoptions</h2>
        <div class="table-responsive">
            <table class="table pets-table">
                <thead>
                    <tr>
                        <th>Booking ID</th>
                        <th>Pet Name</th>
                        <th>Species</th>
                        <th>Breed</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>""")

for booking in bookings:
    Bookingid = booking[0]
    Petname = booking[7]
    Species = booking[8]
    Breed = booking[9]
    Status = booking[11]
    Sheltername = booking[-2]  # Second to last column from our SELECT
    ShelterEmail = booking[-1]  # Last column from our SELECT

    print(f"""
        <tr>
            <td>{Bookingid}</td>
            <td>{Petname}</td>
            <td>{Species}</td>
            <td>{Breed}</td>
            <td><span class="badge badge-adopted">{Status}</span></td>
            <td>
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#shelterModal{Bookingid}">
                    View Shelter Info
                </button>
            </td>
        </tr>""")

print("""
                </tbody>
            </table>
        </div>
    </div>
""")

# Add modals for shelter information
for booking in bookings:
    Bookingid = booking[0]
    Sheltername = booking[-2]
    ShelterEmail = booking[-1]

    print(f"""
    <!-- Shelter Information Modal -->
    <div class="modal fade" id="shelterModal{Bookingid}" tabindex="-1" aria-labelledby="shelterModalLabel{Bookingid}" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="shelterModalLabel{Bookingid}">Shelter Information</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="details">
                        <p><strong>Shelter Name:</strong> {Sheltername}</p>
                        <p><strong>Email:</strong> {ShelterEmail}</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    """)

print("""
    <!-- Bootstrap JS and dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
</body>
</html>
""")