#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Select data from careresource_info table
cur.execute("""
    SELECT centername, centertype, address, city, state, pin, mob, mail, description, Image
    FROM careresource_info
    ORDER BY centername
""")
centers_data = cur.fetchall()

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Center Management</title>
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

    /* Center Image */
    .center-image {
        width: 60px;
        height: 60px;
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

    .center-modal-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #4CAF50;
        margin: 0 auto 20px;
        display: block;
    }

    .center-info-label {
        font-weight: bold;
        color: #4CAF50;
    }

    .center-description {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
        margin-top: 15px;
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
        <h2 class="section-title">Center Management</h2>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Center Image</th>
                        <th>Center Name</th>
                        <th>Center Type</th>
                        <th>Address</th>
                        <th>City</th>
                        <th>State</th>
                        <th>PIN</th>
                        <th>Mobile</th>
                        <th>Email</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
""")

# Display center data
for index, center in enumerate(centers_data, 1):
    centername = center[0]
    centertype = center[1]
    address = center[2]
    city = center[3]
    state = center[4]
    pin = center[5]
    mob = center[6]
    mail = center[7]
    description = center[8]
    IImage = center[9]

    print(f"""
                    <tr>
                        <td>{index}</td>
                        <td><img src="./images/{IImage}" class="center-image" alt="Center Image"></td>
                        <td>{centername}</td>
                        <td>{centertype}</td>
                        <td>{address}</td>
                        <td>{city}</td>
                        <td>{state}</td>
                        <td>{pin}</td>
                        <td>{mob}</td>
                        <td>{mail}</td>
                        <td>{description}</td>
                        <td>
                            <button type="button" class="btn btn-view" data-bs-toggle="modal" data-bs-target="#viewModal{index}">
                                <i class="fas fa-eye"></i> View
                            </button>
                        </td>
                    </tr>

                    <!-- View Modal -->
                    <div class="modal fade" id="viewModal{index}" tabindex="-1">
                        <div class="modal-dialog modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Center Details</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <img src="./images/{IImage}" class="center-modal-image" alt="Center Image">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><span class="center-info-label">Center Name:</span> {centername}</p>
                                            <p><span class="center-info-label">Center Type:</span> {centertype}</p>
                                            <p><span class="center-info-label">Address:</span> {address}</p>
                                            <p><span class="center-info-label">City:</span> {city}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><span class="center-info-label">State:</span> {state}</p>
                                            <p><span class="center-info-label">PIN:</span> {pin}</p>
                                            <p><span class="center-info-label">Mobile:</span> {mob}</p>
                                            <p><span class="center-info-label">Email:</span> {mail}</p>
                                        </div>
                                    </div>
                                    <div class="center-description">
                                        <p><span class="center-info-label">Description:</span><br>{description}</p>
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