#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Fetch all users from usereg table
cur.execute("SELECT name, email, mob, dob, gender, street, city, pin, state, profile_pic, proof_attachment, registeredtime FROM usereg")
users = cur.fetchall()

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management</title>
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

    /* User Profile Image */
    .user-profile {
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

    .user-modal-profile {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #4CAF50;
        margin: 0 auto 20px;
        display: block;
    }

    .user-info-label {
        font-weight: bold;
        color: #4CAF50;
    }

    .user-proof-img {
        width: 100%;
        max-height: 200px;
        object-fit: contain;
        margin-top: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }

    /* Cover Image Styles */
    .cover-image {
        width: 100%;
        height: 300px;
        object-fit: cover;
        position: relative;
    }

    .cover-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white;
    }

    .cover-content {
        z-index: 1;
    }

    .cover-content h1 {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    .cover-content p {
        font-size: 1.2rem;
        max-width: 600px;
        margin: 0 auto;
        color: white;
    }

    /* Dropdown Menu Styles */
    .dropdown-menu {
        background-color: #333;
        border: none;
    }

    .dropdown-item {
        color: white;
    }

    .dropdown-item:hover {
        background-color: #4CAF50;
        color: white;
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

    footer p {
        margin: 0;
        color: white;
    }

    footer a {
        color: #FFD54F;
        text-decoration: none;
        transition: color 0.3s ease;
    }

    footer a:hover {
        color: #FFF176;
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .navbar-brand {
            font-size: 1.5rem;
        }

        .section-title {
            font-size: 2rem;
        }

        .cover-content h1 {
            font-size: 2.5rem;
        }

        .cover-content p {
            font-size: 1rem;
        }
        
        .user-modal-profile {
            width: 100px;
            height: 100px;
        }

        /* Adjust footer padding for mobile */
        body {
            padding-bottom: 50px;
        }
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

   

    <!-- User Management Section -->
    <section id="user-management" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">User Information</h2>
            <p class="text-center mb-4">Manage and view detailed information about registered users.</p>
            
            <!-- Search and Filter Controls -->
           
            
            <!-- Users Table -->
            <div class="table-responsive">
                <table class="table table-hover table-bordered">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>Registered Date</th>
                            <th>Profile</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Mobile</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
""")

# Display user data in the table
for i, user in enumerate(users, 1):
    name, email, mob, dob, gender, street, city, pin, state, profile_pic, proof_attachment, registeredtime = user
    # Format the registered date
    formatted_date = registeredtime.strftime('%d-%m-%y') if registeredtime else ''
    print(f"""
                        <tr>
                            <td>{i}</td>
                            <td>{formatted_date}</td>
                            <td><img src="images/{profile_pic}" class="user-profile" alt="{name}"></td>
                            <td>{name}</td>
                            <td>{email}</td>
                            <td>{mob}</td>
                            <td>
                                <button class="btn btn-sm btn-view" data-bs-toggle="modal" data-bs-target="#userModal{i}">
                                    <i class="fas fa-eye"></i> View
                                </button>
                            </td>
                        </tr>
    """)

print("""
                    </tbody>
                </table>
            </div>
            
            
        </div>
    </section>

    <!-- Generate modals for each user -->
""")

# Generate modals for each user
for i, user in enumerate(users, 1):
    name, email, mob, dob, gender, street, city, pin, state, profile_pic, proof_attachment, registeredtime = user
    print(f"""
    <!-- User Modal {i} -->
    <div class="modal fade" id="userModal{i}" tabindex="-1" aria-labelledby="userModalLabel{i}" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="userModalLabel{i}">User Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="text-center mb-4">
                        <img src="images/{profile_pic}" class="user-modal-profile" alt="{name}">
                        <h4>{name}</h4>
                    </div>
                    
                    <div class="row g-3">
                        <div class="col-md-6">
                            <p><span class="user-info-label">Email:</span> {email}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">Mobile:</span> {mob}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">Date of Birth:</span> {dob}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">Gender:</span> {gender}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">Street:</span> {street}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">City:</span> {city}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">State:</span> {state}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="user-info-label">PIN:</span> {pin}</p>
                        </div>
                        <div class="col-12">
                            <p><span class="user-info-label">ID Proof:</span></p>
                            <img src="images/{proof_attachment}" class="user-proof-img" alt="ID Proof">
                        </div>
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
    <footer class="bg-dark text-white text-center py-3">
        <p class="mb-0">&copy; 2025 Admin Dashboard. All Rights Reserved.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()
