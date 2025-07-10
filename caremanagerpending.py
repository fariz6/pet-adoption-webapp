#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Select data from care_reg table
cur.execute(
    "SELECT careresourcertype, careresourcername, careresourcetype, carecentrename, email, password, mobile, street, pincode, state, city, profile, idproof FROM care_reg WHERE status='pending'")
care_data = cur.fetchall()

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

    /* Profile Image */
    .care-profile {
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

    .care-modal-profile {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #4CAF50;
        margin: 0 auto 20px;
        display: block;
    }

    .care-info-label {
        font-weight: bold;
        color: #4CAF50;
    }

    .care-proof-img {
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
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#">PetMatch</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-5">
        <h2 class="section-title">Care Resource Management</h2>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Profile</th>
                        <th>Resource Type</th>
                        <th>Resource Name</th>
                        <th>Center Name</th>
                        <th>Contact</th>
                        <th>Location</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
""")

# Display care resource data
for index, care in enumerate(care_data):
    # Handle cases where profile might be NULL
    profile_img = care[11] if care[11] and care[11] != "NULL" else "default_profile.jpg"

    # Format for displaying data
    print(f"""
                    <tr>
                        <td><img src="./images/{profile_img}" class="care-profile" alt="Profile"></td>
                        <td>{care[0]}</td>
                        <td>{care[1]}</td>
                        <td>{care[3]}</td>
                        <td>
                            <i class="fas fa-phone"></i> {care[6] if care[6] and care[6] != '0' else 'N/A'}<br>
                            <i class="fas fa-envelope"></i> {care[4]}
                        </td>
                        <td>
                            {care[7]}, {care[10]}<br>
                            {care[9]}, {care[8]}
                        </td>
                        <td>Pending</td>
                        <td>
                            <button type="button" class="btn btn-view" data-bs-toggle="modal" data-bs-target="#careModal{index}">
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

    <!-- Care Resource Detail Modals -->
""")

# Create modals for each care resource
for index, care in enumerate(care_data):
    # Handle cases where profile and idproof might be NULL
    profile_img = care[11] if care[11] and care[11] != "NULL" else "default_profile.jpg"
    id_proof_img = care[12] if care[12] and care[12] != "NULL" else "default_proof.jpg"

    print(f"""
    <div class="modal fade" id="careModal{index}" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Care Resource Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <img src="./images/{profile_img}" class="care-modal-profile" alt="Profile">
                    <div class="row mt-3">
                        <div class="col-md-6">
                            <p><span class="care-info-label">Resource Type:</span> {care[0]}</p>
                            <p><span class="care-info-label">Resource Name:</span> {care[1]}</p>
                            <p><span class="care-info-label">Center Name:</span> {care[3]}</p>
                            <p><span class="care-info-label">Mobile:</span> {care[6] if care[6] and care[6] != '0' else 'N/A'}</p>
                            <p><span class="care-info-label">Email:</span> {care[4]}</p>
                        </div>
                        <div class="col-md-6">
                            <p><span class="care-info-label">Street:</span> {care[7]}</p>
                            <p><span class="care-info-label">City:</span> {care[10]}</p>
                            <p><span class="care-info-label">PIN:</span> {care[8]}</p>
                            <p><span class="care-info-label">State:</span> {care[9]}</p>
                        </div>
                    </div>
                    <div class="mt-3">
                        <p class="care-info-label">ID Proof Document:</p>
                        <img src="./images/{id_proof_img}" class="care-proof-img" alt="Proof Document">
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