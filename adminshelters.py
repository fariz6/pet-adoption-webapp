#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Select data from product_info table
cur.execute("""
    SELECT Sheltername, Email, Petname, Species, Breed, gender, location, Age, Animalimg
    FROM product_info
    ORDER BY Sheltername 
""")
pet_data = cur.fetchall()

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pet Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    /* General Body Styling */
    body {
        font-family: 'Roboto', Arial, sans-serif;
        background-color: #f4f7f6;
        margin: 0;
        padding: 0;
        color: #333;
        padding-bottom: 60px;
    }

    /* Navbar */
    .navbar {
        background-color: #333;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .navbar-brand {
        font-size: 1.8rem;
        font-weight: bold;
        color: #FFD54F !important;
        transition: color 0.3s ease-in-out;
    }

    .navbar-brand:hover {
        color: #FFF176 !important;
    }

    .navbar-nav .nav-link {
        font-size: 1.1rem;
        margin-right: 15px;
        transition: transform 0.3s, color 0.3s ease;
    }

    .navbar-nav .nav-link:hover {
        color: #FFD54F !important;
        transform: scale(1.1);
    }

    /* Section Title Styles */
    .section-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;
        position: relative;
    }

    .section-title::after {
        content: '';
        display: block;
        width: 70px;
        height: 4px;
        background: linear-gradient(to right, #FFD54F, #4CAF50);
        margin: 10px auto;
        border-radius: 2px;
    }

    /* Table Styling */
    .table {
        border-radius: 10px;
        overflow: hidden;
        background-color: white;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #dee2e6;
    }

    .table th, .table td {
        border: 1px solid #dee2e6;
        padding: 12px;
    }

    .table th {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }

    .table-hover tbody tr:hover {
        background-color: #f1f1f1;
        transition: background-color 0.3s ease-in-out;
    }

    .table td, .table th {
        text-align: center;
        vertical-align: middle;
    }

    /* Pet Image */
    .pet-image {
        width: 100px;
        height: 100px;
        border-radius: 10px;
        object-fit: cover;
        border: 2px solid #4CAF50;
        margin: 0 auto;
        display: block;
    }

    /* Footer */
    footer {
        background-color: #333;
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 0.9rem;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    </style>
</head>
<body>
    <!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
    <div class="container-fluid">
        <a class="navbar-brand" href="#"><i class="fas fa-user-shield"></i> Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link active" href="admin.py"><i class="fas fa-home"></i> Home</a></li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="shelterDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-home"></i> Shelters
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="shelterDropdown">
                        <li><a class="dropdown-item" href="adminshelternew.py?shelter_status=new">New Requests</a></li>
                        <li><a class="dropdown-item" href="adminmanager.py?shelter_status=active">Active Shelters</a></li>
                        <li><a class="dropdown-item" href="adminmanagerrej.py?shelter_status=rejected">Rejected Shelters</a></li>
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="careDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-hospital"></i> Care Centers
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="careDropdown">
                        <li><a class="dropdown-item" href="carenew.py?care_status=new">New Requests</a></li>
                        <li><a class="dropdown-item" href="caremanager.py?care_status=active">Active Centers</a></li>
                        <li><a class="dropdown-item" href="caremanagerrejected.py?care_status=rejected">Rejected Centers</a></li>
                    </ul>
                </li>
                <li class="nav-item"><a class="nav-link" href="adminuser.py"><i class="fas fa-users"></i> Users</a></li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="careDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-key"></i> Passwords Requests
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="careDropdown">
                        <li><a class="dropdown-item" href="password_requests.py?care_status=new">shelter</a></li>
                        <li><a class="dropdown-item" href="password_request.py?care_status=active">Care center</a></li>
                     
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
    <!-- Main Content -->
    <div class="container mt-5">
        <h2 class="section-title">Pet Information</h2>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Shelter Name</th>
                        <th>Email</th>
                        <th>Pet Name</th>
                        <th>Species</th>
                        <th>Breed</th>
                        <th>Gender</th>
                        <th>Location</th>
                        <th>Age</th>
                        <th>Pet Image</th>
                    </tr>
                </thead>
                <tbody>
""")

# Display pet data
sno = 1
for row in pet_data:
    print(f"""
                    <tr>
                        <td>{sno}</td>
                        <td>{row[0]}</td>
                        <td>{row[1]}</td>
                        <td>{row[2]}</td>
                        <td>{row[3]}</td>
                        <td>{row[4]}</td>
                        <td>{row[5]}</td>
                        <td>{row[6]}</td>
                        <td>{row[7]}</td>
                        <td><img src="images/{row[8]}" class="pet-image" alt="Pet Image"></td>
                    </tr>
    """)
    sno += 1

print("""
                </tbody>
            </table>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 PetMatch. All rights reserved.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()