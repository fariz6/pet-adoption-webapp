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
    "SELECT careresourcertype, careresourcername, careresourcetype, carecentrename, email, password, mobile, street, pincode, state, city, profile, idproof, registeredtime FROM care_reg WHERE status='approved'")
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
        <h2 class="section-title">Care Resource Management</h2>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Registered Date</th>
                        <th>Profile</th>
                        <th>Resource Type</th>
                        <th>Resource Name</th>
                        <th>Center Name</th>
                        <th>Contact</th>
                        <th>Location</th>
                        <th>Status</th>
                        <th>Care centers</th>
                    </tr>
                </thead>
                <tbody>
""")

# Display care resource data
for index, care in enumerate(care_data):
    # Handle cases where profile might be NULL
    profile_img = care[11] if care[11] and care[11] != "NULL" else "default_profile.jpg"
    
    # Format the registered date
    registered_date = care[13].strftime('%d-%m-%y') if care[13] else 'N/A'

    # Format for displaying data
    print(f"""
                    <tr>
                        <td>{index + 1}</td>
                        <td>{registered_date}</td>
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
                        <td>Active</td>
                        <td>
                            <button type="button" class="btn btn-view" data-bs-toggle="modal" data-bs-target="#careModal{index}">
                                <i class="fas fa-eye"></i> Center info
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

    # Get the centreid for this care resource (need to fetch it, so update the select query to include centreid)
    # We'll assume the centreid is the primary key and is available as the first column if you update the select query
    # For now, let's fetch it using the email (unique) as a workaround
    cur2 = con.cursor()
    cur2.execute("SELECT centreid FROM care_reg WHERE email=%s", (care[4],))
    centreid_row = cur2.fetchone()
    centreid = centreid_row[0] if centreid_row else None

    # Fetch all centers for this owner from careresource_info
    centers = []
    center_count = 0
    if centreid:
        cur2.execute("SELECT centername, centertype, address, city, state, pin, mob, mail, description, Image FROM careresource_info WHERE centerid=%s", (centreid,))
        centers = cur2.fetchall()
        center_count = len(centers)

    print(f"""
    <div class=\"modal fade\" id=\"careModal{index}\" tabindex=\"-1\">
        <div class=\"modal-dialog modal-lg\">
            <div class=\"modal-content\">
                <div class=\"modal-header\">
                    <h5 class=\"modal-title\">Care Resource Details</h5>
                    <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\"></button>
                </div>
                <div class=\"modal-body\">
                    <img src=\"./images/{profile_img}\" class=\"care-modal-profile\" alt=\"Profile\">
                    <div class=\"row mt-3\">
                        <div class=\"col-md-6\">
                            <p><span class=\"care-info-label\">Resource Type:</span> {care[0]}</p>
                            <p><span class=\"care-info-label\">Resource Name:</span> {care[1]}</p>
                            <p><span class=\"care-info-label\">Center Name:</span> {care[3]}</p>
                            <p><span class=\"care-info-label\">Mobile:</span> {care[6] if care[6] and care[6] != '0' else 'N/A'}</p>
                            <p><span class=\"care-info-label\">Email:</span> {care[4]}</p>
                        </div>
                        <div class=\"col-md-6\">
                            <p><span class=\"care-info-label\">Street:</span> {care[7]}</p>
                            <p><span class=\"care-info-label\">City:</span> {care[10]}</p>
                            <p><span class=\"care-info-label\">PIN:</span> {care[8]}</p>
                            <p><span class=\"care-info-label\">State:</span> {care[9]}</p>
                        </div>
                    </div>
                    <div class=\"mt-3\">
                        <p class=\"care-info-label\">ID Proof Document:</p>
                        <img src=\"./images/{id_proof_img}\" class=\"care-proof-img\" alt=\"Proof Document\">
                    </div>
                    <div class=\"mt-4\">
                        <h5 class=\"care-info-label\">Centers Owned: {center_count}</h5>
                        <div class=\"row\">
    """)
    for center in centers:
        center_img = center[9] if center[9] else "default_profile.jpg"
        print(f"""
                            <div class=\"col-md-6 mb-3\">
                                <div class=\"card\">
                                    <img src=\"./images/{center_img}\" class=\"card-img-top\" alt=\"{center[0]}\" style=\"height: 120px; object-fit: cover;\">
                                    <div class=\"card-body\">
                                        <h6 class=\"card-title\">{center[0]}</h6>
                                        <p class=\"card-text\">
                                            Type: {center[1]}<br>
                                            Address: {center[2]}, {center[3]}, {center[4]}, {center[5]}<br>
                                            Phone: {center[6]}<br>
                                            Email: {center[7]}<br>
                                            Description: {center[8][:60]}{'...' if len(center[8]) > 60 else ''}
                                        </p>
                                    </div>
                                </div>
                            </div>
        """)
    print("""
                        </div>
                    </div>
                </div>
                <div class=\"modal-footer\">
                    <button type=\"button\" class=\"btn btn-secondary\" data-bs-dismiss=\"modal\">Close</button>
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