#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

def safe_write_file(filepath, content):
    """Helper function to safely write files with proper encoding"""
    try:
        with open(filepath, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {filepath}: {str(e)}")
        raise

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Uid = form.getvalue("id")
s = """select * from usereg where id="%s" """ % (Uid)
cur.execute(s)
res = cur.fetchall()


# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - User Dashboard</title>
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
        .cover-section {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center;
    color: white;
    padding: 6rem 0;
    text-align: center;
    margin-bottom: -2rem;  # Changed from 0rem to -2rem
}

        
        .cover-section h1 {
            font-size: 3rem;
            margin-bottom: 1.5rem;
        }
        
        .cover-section p {
            font-size: 1.2rem;
            max-width: 700px;
            margin: 0 auto 2rem;
        }
        
        .search-btn {
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .search-form {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-top: -50px;
            margin-bottom: 3rem;
            display: none;
        }
        
        .search-form.show {
            display: block;
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
        
        .pet-card {
            border: none;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
            margin-bottom: 20px;
        }
        
        .pet-card:hover {
            transform: translateY(-5px);
        }
        
        .pet-card img {
            height: 200px;
            object-fit: cover;
        }
        
        .pet-card .card-body {
            padding: 1.5rem;
        }
        
        .pet-card .badge {
            font-size: 0.8rem;
            padding: 0.35rem 0.75rem;
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
        /* Profile Modal Styles */
.modal-content {
    border-radius: 15px;
    border: none;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.modal-header {
    border-bottom: none;
    padding-bottom: 0;
}

.modal-header .btn-close {
    box-shadow: none;
}

.modal-title {
    font-weight: 600;
    color: #2c3e50;
}

/* Profile Picture Styles */
.profile-pic-container {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    border: 5px solid #f8f9fa;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.profile-pic {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-name {
    font-weight: 600;
    color: #2c3e50;
    margin-top: 15px;
}

/* Info Item Styles */
.profile-info {
    background-color: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
}

.info-item {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #e9ecef;
}

.info-item:last-child {
    border-bottom: none;
}

.icon-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #6C63FF;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    flex-shrink: 0;
}

.icon-circle i {
    font-size: 16px;
}

.info-content h6 {
    font-weight: 600;
    margin-bottom: 2px;
    color: #2c3e50;
    font-size: 14px;
}

.info-content p {
    margin: 0;
    color: #6c757d;
    font-size: 15px;
}

/* Edit Profile Modal Specific Styles */
.upload-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 8px;
    text-align: center;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s;
}

.profile-pic-container:hover .upload-overlay {
    opacity: 1;
}

/* Form Styles */
.form-control {
    border-radius: 8px;
    padding: 10px 15px;
    border: 1px solid #e0e0e0;
    transition: all 0.3s;
}

.form-control:focus {
    border-color: #6C63FF;
    box-shadow: 0 0 0 0.25rem rgba(108, 99, 255, 0.25);
}

.form-label {
    font-weight: 500;
    color: #495057;
    margin-bottom: 8px;
}

/* Button Styles */
.btn {
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
    transition: all 0.3s;
}

.btn-primary {
    background-color: #6C63FF;
    border-color: #6C63FF;
}

.btn-primary:hover {
    background-color: #5a52d6;
    border-color: #5a52d6;
}

.btn-outline-secondary {
    border-color: #e0e0e0;
    color: #6c757d;
}

.btn-outline-secondary:hover {
    background-color: #f8f9fa;
    border-color: #e0e0e0;
}

/* Modal Footer */
.modal-footer {
    border-top: none;
    padding-top: 0;
    justify-content: space-between;
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.modal-body {
    animation: fadeIn 0.3s ease-out;
}
 .badge {
            font-size: 0.8rem;
            padding: 0.35rem 0.75rem;
            font-weight: 500;
        }
        .bg-success {
            background-color: #28a745 !important;
        }
        .bg-danger {
            background-color: #dc3545 !important;
        }
        /* Add this to your existing CSS */
:root {
    --cover-height: calc(100vh - 120px); /* Adjust 120px based on your header height */
}

body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin: 0;
}

/* Cover Section - Full Height */
.cover-section {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                url('https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: var(--cover-height);
    padding: 2rem 0;
    position: relative;
}

/* Content Container */
.container.main-content {
    flex: 1;
}

/* Compact Footer */
footer {
    background-color: var(--dark-color);
    color: white;
    padding: 1.5rem 0;
    text-align: center;
}

.copyright {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1rem;
    margin-top: 0rem;
    font-size: 0.9rem;
}
    </style>
</head>
<body>""")
for i in res:

    print(f"""    <!-- Navbar -->
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
                            <i class="fas fa-shopping-cart me-1"></i> Pet Bookings
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="userrecent.py?id={i[0]}">Recent</a></li>
                           
                            <li><a class="dropdown-item" href="userejected.py?id={i[0]}">Rejected</a></li>
                            <li><a class="dropdown-item" href="usercomplete.py?id={i[0]}">Approved</a></li>
                        </ul>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="ordersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> Care Resource Bookings
                        </a>
                        <ul class="dropdown-menu">
                            
                            <li><a class="dropdown-item" href="careaprove.py?id={i[0]}"><i class="fas fa-check-circle me-2"></i>Requests</a></li>
                            
                        </ul>
                    </li>
                   
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="settingsDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-cog me-1"></i> Settings
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#profileModal">Profile</a></li>
                            <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change Password</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>""" )

for u in res:

        print(f"""
    <!-- Cover Section -->
    <section class="cover-section">
        <div class="container">
            <h1>Find Your Perfect Pet Companion</h1>
            <p>Browse through hundreds of pets waiting for their forever homes. Your new best friend is just a click away!</p>
            <div class="d-flex justify-content-center gap-3">
                <a href="browsepet.py?id={u[0]}" class="btn btn-primary btn-lg search-btn" id="searchToggle">
                    <i class="fas fa-search me-2"></i>Browse pets
                </a>
                <a href="usercare.py?id={u[0]}" class="btn btn-secondary btn-lg search-btn">
                    <i class="fas fa-hand-holding-heart me-2"></i>Request Care
                </a>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <div class="container main-content">
        <!-- Your existing content here -->
    </div>
""")

print("""   <!-- Search Form -->
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div id="searchForm" class="search-form">
                    <form method="post" enctype="multipart/form-data">
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label for="petType" class="form-label">Pet Type</label>
                                <select class="form-select" id="petType" name="species">
                                    <option selected>Any</option>
                                    <option>Dog</option>
                                    <option>Cat</option>
                                    <option>Bird</option>
                                    <option>Rabbit</option>
                                    <option>Other</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                        <label for="breed" class="form-label">Breed</label>
                        <input type="text" class="form-control" id="breed" name="breed" placeholder="Any breed">
                    </div>
                    

                           
                            <div class="col-md-4">
                                <label for="gender" class="form-label">Gender</label>
                                <select class="form-select" id="gender" name="gender">
                                    <option selected>Any</option>
                                    <option>Male</option>
                                    <option>Female</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                        <label for="location" class="form-label">Location</label>
                        <input type="text" class="form-control" id="location" name="location" placeholder="Any location">
                    </div>
                            
                            <div class="col-12 text-center mt-3">
                                <input type="submit" name="search" value="Search now" class="btn btn-primary px-4">
                                    
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>""")

Stype = form.getvalue("species")
Sbreed = form.getvalue("breed")
Sgender = form.getvalue("gender")
Slocation = form.getvalue("location")
Search = form.getvalue("search")

if Search != None:
    a = f"""select * from product_info where Species='{Stype}' or location='{Slocation}' or Breed='{Sbreed}' or Gender={Sgender} """
    cur.execute(a)
    result = cur.fetchall()
    print("""
    <script>
    location.href="#card"
    </script>
    """)

    print("""
            <div class="container mt-4" id="card">
                <div class="row">
                    <div class="col-12">
                        <h4 class="mb-4">Search Results</h4>
                    </div>
                </div>
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">""")

    for i in result:
        Animalimg = i[9]
        Name = i[4]
        Location = i[8]
        Gender = i[7]
        Species = i[5]
        Breed = i[6]
        Status= i[10]
        print(f"""

# In the search results section, replace the pet card HTML with this:

            <div class="col">
                        <div class="pet-card h-100">
                            <img src="./images/{Animalimg}" class="card-img-top img-fluid" alt="Pet image">
                            <div class="pet-info p-3">
                                <span class="badge %s mb-2">{Status}</span>
                                <h2 class="pet-name h5">{Name}</h2>
                            </div>
                               
                                    <div class="detail-item d-flex justify-content-between py-1 border-bottom">
                                        <span class="detail-label">Species</span>
                                        <span class="detail-value">{Species}</span>
                                    </div>
                                    <div class="detail-item d-flex justify-content-between py-1 border-bottom">
                                        <span class="detail-label">Breed</span>
                                        <span class="detail-value">{Breed}</span>
                                    </div>
                                    <div class="detail-item d-flex justify-content-between py-1">
                                        <span class="detail-label">Gender</span>
                                        <span class="detail-value">{Gender}</span>
                                    </div>
                                </div>
                                <a href="petdetails.py?product_id=%s" class="btn btn-primary w-100 mt-3">View pet</a>
                            </div>
                        </div>""" )


# HTML for Recent Pets Section


# Fetch recently added pets from database
# Fetch recently added pets from database
try:
    cur.execute("SELECT * FROM product_info ORDER BY product_id DESC LIMIT 3")  # Get 3 most recent pets
    recent_pets = cur.fetchall()
except Exception as e:
    recent_pets = []
    print(f"<!-- Database error: {str(e)} -->")



print("""<!-- Footer -->
    <footer>
        <div class="container">
            <div class="copyright text-center">
                <p class="mb-0">&copy; 2023 PetMatch. All rights reserved.</p>
            </div>
        </div>
    </footer>
""")

for i in res:
    print("""
    <!-- Profile View Modal -->
    <div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="profileModalLabel">My Profile</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="text-center mb-4">
                        <div class="profile-pic-container mb-3">
                            <img src="./images/%s" class="profile-pic" alt="Profile Picture">
                        </div>
                        <h4 class="profile-name">%s</h4>
                        <p class="text-muted">Member since June 2023</p>
                    </div>

                    <div class="profile-info">
                        <div class="info-item mb-3">
                            <div class="icon-circle">
                                <i class="fas fa-phone"></i>
                            </div>
                            <div class="info-content">
                                <h6>Phone Number</h6>
                                <p>%s</p>
                            </div>
                        </div>

                        <div class="info-item mb-3">
                            <div class="icon-circle">
                                <i class="fas fa-envelope"></i>
                            </div>
                            <div class="info-content">
                                <h6>Email Address</h6>
                                <p>%s</p>
                            </div>
                        </div>

                        <div class="info-item">
                            <div class="icon-circle">
                                <i class="fas fa-map-marker-alt"></i>
                            </div>
                            <div class="info-content">
                                <h6>Location</h6>
                                <p>%s</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal">
                        <i class="fas fa-edit me-2"></i>Edit Profile
                    </button>
                </div>
            </div>
        </div>
    </div>
    """ % (i[11], i[1], i[3], i[2], i[8]))

# Edit Profile Modal
for i in res:
    print("""
    <!-- Edit Profile Modal -->
    <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="editProfileModalLabel">Edit Profile</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form method="post" enctype="multipart/form-data">
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <div class="profile-pic-container mb-3">
                                <img src="./images/%s" class="profile-pic" alt="Profile Picture" id="profileImagePreview">
                                <input type="file" id="profileImageUpload" name="Img" accept="image/*" class="d-none">
                                <div class="upload-overlay" onclick="document.getElementById('profileImageUpload').click()">
                                    <i class="fas fa-camera"></i>
                                </div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="editName" class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="editName" name="uname" value="%s">
                        </div>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                        <input type="submit" class="btn btn-primary" name="savechange" value="Save Changes">
                    </div>
                </form>
            </div>
        </div>
    </div>
    """ % (i[11], i[1]))

for i in res:
    Oldpass = i[4]
    print("""
        <!-- Change Password Modal -->
        <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="changePasswordModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="changePasswordModalLabel">Change Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form method="post">
                        <div class="modal-body">
                            <input type="hidden" value="%s" name="old">
                            <div class="mb-3">
                                <label for="currentPassword" class="form-label">Current Password</label>
                                <input type="password" class="form-control" id="currentPassword" name="oldpassword" placeholder="Enter current password">
                            </div>
                            <div class="mb-3">
                                <label for="newPassword" class="form-label">New Password</label>
                                <input type="password" class="form-control" id="newPassword" name="newpassword" placeholder="Enter new password">
                                <div class="form-text">Minimum 8 characters with at least one number and one special character</div>
                            </div>
                            <div class="mb-3">
                                <label for="confirmPassword" class="form-label">Confirm New Password</label>
                                <input type="password" class="form-control" id="confirmPassword" name="confirmpassword" placeholder="Confirm new password">
                                <div class="invalid-feedback" id="passwordMatchError">Passwords do not match</div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                            <input type="submit" class="btn btn-primary" name="savech" value="Save Changes">
                        </div>
                    </form>
                </div>
            </div>
        </div>""" % (Oldpass))

print(""" <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script>
      
        
        // Initialize tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
         // Password validation
            const newPassword = document.getElementById('newPassword');
            const confirmPassword = document.getElementById('confirmPassword');

            if (newPassword && confirmPassword) {
                function validatePassword() {
                    if (newPassword.value !== confirmPassword.value) {
                        confirmPassword.setCustomValidity("Passwords don't match");
                    } else {
                        confirmPassword.setCustomValidity('');
                    }
                }

                newPassword.addEventListener('change', validatePassword);
                confirmPassword.addEventListener('keyup', validatePassword);
            }
        });

    </script>
</body>
</html>
""")
# Edit Profile Form Submission
if form.getvalue("savechange"):
    try:
        # Get form values
        uname = form.getvalue("uname")


        # Handle file upload
        if 'Img' in form:
            fileitem = form['Img']
            if fileitem.filename:
                # Save the uploaded file
                fn = os.path.basename(fileitem.filename)
                safe_write_file('images/' + fn, fileitem.file.read())
                # Update database with new image
                cur.execute("UPDATE usereg SET name=%s, image=%s WHERE id=%s",
                            (uname, fn, Uid))
            else:
                # Update without changing image
                cur.execute("UPDATE usereg SET name=%s WHERE id=%s",
                            (uname,  Uid))

        con.commit()
        print("""
        <script>
            alert("Profile updated successfully!");
            window.location.href = window.location.href;
        </script>
        """)
    except Exception as e:
        print(f"""
        <script>
            alert("Error updating profile: {str(e)}");
        </script>
        """)
if form.getvalue("savech"):
    error_messages = []
    Old = form.getvalue("old")
    Oldpassword = form.getvalue("oldpassword")
    Newpassword = form.getvalue("newpassword")
    Confirmpassword = form.getvalue("confirmpassword")

    # 1. Validate old password first
    if Old != Oldpassword:
        error_messages.append("• Current password is incorrect")

    # 2. Validate new password requirements
    if Newpassword:
        if len(Newpassword) < 8:
            error_messages.append("• Password must be at least 8 characters")
        if not any(c.isupper() for c in Newpassword):
            error_messages.append("• Password must contain at least one uppercase letter")
        if not any(c.islower() for c in Newpassword):
            error_messages.append("• Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in Newpassword):
            error_messages.append("• Password must contain at least one number")
        if not any(c in '!@#$%^&*' for c in Newpassword):
            error_messages.append("• Password must contain at least one special character (!@#$%^&*)")
        if Newpassword == Oldpassword:
            error_messages.append("• New password cannot be same as old password")
    else:
        error_messages.append("• New password cannot be empty")

    # 3. Validate password confirmation
    if Newpassword != Confirmpassword:
        error_messages.append("• New password and confirmation do not match")

    # Only proceed if no validation errors
    if not error_messages:
        try:
            # Update database
            cur.execute("UPDATE usereg SET pass=%s WHERE id=%s", (Confirmpassword, Uid))
            con.commit()
            print("""
            <script>
                alert("Password changed successfully!");
                window.location.href = window.location.href;
            </script>
            """)
        except Exception as e:
            error_messages.append(f"• Error saving changes: {str(e)}")

    # Show errors if any
    if error_messages:
        combined_errors = "Please fix the following issues:\\n\\n" + "\\n".join(error_messages)
        print(f"""
        <script>
            alert(`{combined_errors}`);
        </script>
        """)