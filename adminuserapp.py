#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Select data from shelter_info table
cur.execute("SELECT ownername, street, city, pin, state, mob, email, profile_pic, proof_attachment FROM shelter_info where status='pending' ")
shelter_data = cur.fetchall()

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shelter Management</title>
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

    /* View Button */
    .btn-view {
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 20px;
        transition: all 0.3s ease;
    }

    .btn-view:hover {
        background-color: #0d8bf2;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: white;
    }

    /* Shelter Profile Image */
    .shelter-profile {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #4CAF50;
    }

    /* Modal Styling */
    .modal-header {
        background-color: #4CAF50;
        color: white;
    }

    .modal-footer {
        background-color: #f8f9fa;
    }

    .shelter-modal-profile {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #4CAF50;
        margin: 0 auto 20px;
        display: block;
    }

    .shelter-info-label {
        font-weight: bold;
        color: #4CAF50;
    }

    .shelter-proof-img {
        width: 100%;
        max-height: 200px;
        object-fit: contain;
        margin-top: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
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
        <h2 class="section-title">Shelter Management</h2>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Profile</th>
                        <th>Owner Name</th>
                        <th>Contact</th>
                        <th>Location</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
""")

# Display shelter data
for index, shelter in enumerate(shelter_data):
    print(f"""
                    <tr>
                        <td><img src="./images/{shelter[7]}" class="shelter-profile" alt="Profile"></td>
                        <td>{shelter[0]}</td>
                        <td>
                            <i class="fas fa-phone"></i> {shelter[5]}<br>
                            <i class="fas fa-envelope"></i> {shelter[6]}
                        </td>
                        <td>
                            {shelter[1]}, {shelter[2]}<br>
                            {shelter[3]}, {shelter[4]}
                        </td>
                        <td>Pending</td>
                        <td>
                            <button type="button" class="btn btn-view" data-bs-toggle="modal" data-bs-target="#shelterModal{index}">
                                <i class="fas fa-eye"></i> View Details
                            </button>
                        </td>
                    </tr>
    """)

print("""
                </tbody>
            </table>
        </div>
    </div>

    <!-- Shelter Detail Modals -->
""")

# Create modals for each shelter
for index, shelter in enumerate(shelter_data):
    print(f"""
    <div class="modal fade" id="shelterModal{index}" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Shelter Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <img src="./images/{shelter[7]}" class="shelter-modal-profile" alt="Profile">
                    <div class="row mt-3">
                        <div class="col-md-6">
                            <p><span class="shelter-info-label">Owner Name:</span> {shelter[0]}</p>
                            <p><span class="shelter-info-label">Mobile:</span> {shelter[5]}</p>
                            <p><span class="shelter-info-label">Email:</span> {shelter[6]}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="shelter-info-label">Address:</span> {shelter[1]}</p>
                            <p><span class="shelter-info-label">City:</span> {shelter[2]}</p>
                            <p><span class="shelter-info-label">PIN:</span> {shelter[3]}</p>
                            <p><span class="shelter-info-label">State:</span> {shelter[4]}</p>
                        </div>
                    </div>
                    <div class="mt-3">
                        <p class="shelter-info-label">Proof Document:</p>
                        <img src="./images/{shelter[8]}" class="shelter-proof-img" alt="Proof Document">
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
    <!-- Footer -->
    <footer>
        <p>&copy; 2024 PetMatch. All rights reserved.</p>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
con.close()