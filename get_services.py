#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb,os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Get the careid from either form submission or URL parameter
careid = form.getvalue("careid")
print("<!-- Debug careid initial:", careid, "-->")

if isinstance(careid, list):
    careid = careid[1]  # Take the second value which should be '1'
    print("<!-- Debug careid after list check:", careid, "-->")

if not careid:
    print("<script>alert('No care center ID provided!');</script>")
    exit()

# First fetch the care center details
s = "select * from careresource_info where careid = %s"
cur.execute(s, (careid,))
res = cur.fetchall()
print("<!-- Debug query result:", res, "-->")

if not res:
    print("<script>alert('Care center not found!');</script>")
    exit()

Addservice = form.getvalue("addservice")
# Handle form submission for adding service
if Addservice != None:
    try:
        servicetype = form.getvalue("servicetype")
        serviceprice = form.getvalue("serviceprice")
        print("<!-- Debug service values - type:", servicetype, "price:", serviceprice, "-->")
        
        if not all([servicetype, serviceprice]):
            print("<script>alert('Please fill in all required fields!');</script>")
        else:
            # Insert into serviceprice table
            sql = "INSERT INTO serviceprice (careid, servicetype, serviceprice) VALUES (%s, %s, %s)"
            cur.execute(sql, (careid, servicetype, serviceprice))
            con.commit()

            if cur.rowcount > 0:
                print("<script>alert('Service added successfully!');</script>")
            else:
                print("<script>alert('Failed to add service!');</script>")

    except Exception as e:
        print(f"<script>alert('Database Error: {str(e)}');</script>")
        con.rollback()

# Now fetch all services for this care center
services_sql = """SELECT * FROM serviceprice WHERE careid=%s"""
cur.execute(services_sql, (careid,))
services = cur.fetchall()

# Start HTML output
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - Care Center Details</title>
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
        }

        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
        }

        .navbar {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
            /* Add to your existing CSS */
.navbar {
    background-color: #F8F9FA !important;
}

.navbar-brand {
    color: #6C63FF !important;
}

.nav-link {
    color: #2c3e50 !important;
}

.dropdown-menu {
    background-color: #F8F9FA !important;
    border: 1px solid #e9ecef !important;
}

.dropdown-item {
    color: #6C63FF !important;
}
        .center-header {
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('https://images.unsplash.com/photo-1450778869180-41d0601e046e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%%3D%%3D&auto=format&fit=crop&w=1586&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 5rem 0;
            margin-bottom: 2rem;
        }

        .card {
            border: none;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
            margin-bottom: 20px;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .center-image {
            height: 300px;
            object-fit: cover;
            border-radius: 10px;
        }

        .badge-category {
            background-color: var(--primary-color);
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

        .form-container {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 3rem;
        }

        .service-card {
            border-left: 4px solid var(--primary-color);
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }

        .service-card:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
        }

        .center-info-item {
            margin-bottom: 15px;
        }

        .center-info-item i {
            width: 25px;
            color: var(--primary-color);
        }

        .info-icon-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%%;
            background-color: rgba(108, 99, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
        }

        .info-icon-circle i {
            color: var(--primary-color);
            font-size: 20px;
        }

       /* Update footer styles */
/* Full-width footer styling */
footer {
    background-color:  #F8F9FA; /* Same as navbar */
    color: var(--primary-color);
     text-align: center;
    padding: 2rem 0;
    width: 100%%;
    margin-top: auto; /* Pushes footer to bottom */
}

/* Make navbar and footer colors match */

footer {
    background-color:  #F8F9FA!important;
}
        .btn-outline-primary {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        .btn-outline-primary:hover {
            background-color: var(--primary-color);
            color: white;
        }

        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }

        .btn-primary:hover {
            background-color: #5a52d5;
            border-color: #5a52d5;
        }
        .profile-pic-container {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 0 auto;
    border-radius: 50%%;
    overflow: hidden;
    border: 5px solid #f8f9fa;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.profile-pic {
    width: 100%%;
    height: 100%%;
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
    border-radius: 50%%;
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

        /* Profile Modal Styles */
        .modal-content {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .modal-header {
            background: linear-gradient(135deg, var(--primary-color), #8B85FF);
            color: white;
            border-radius: 15px 15px 0 0;
            padding: 1.5rem;
            border: none;
        }

        .modal-header .btn-close {
            color: white;
            filter: brightness(0) invert(1);
        }

        .modal-body {
            padding: 2rem;
        }

        .modal-footer {
            border-top: 1px solid #eee;
            padding: 1.5rem;
        }

        /* Profile Form Styles */
        .profile-form .form-group {
            margin-bottom: 1.5rem;
        }

        .profile-form label {
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 0.5rem;
        }

        .profile-form .form-control {
            border: 2px solid #eee;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            transition: all 0.3s ease;
        }

        .profile-form .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(108, 99, 255, 0.15);
        }

        /* Profile Image Styles */
        .profile-image-container {
            text-align: center;
            margin-bottom: 2rem;
        }

        .profile-image {
            width: 150px;
            height: 150px;
            border-radius: 50%%;
            object-fit: cover;
            border: 4px solid var(--primary-color);
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.2);
        }

        .profile-image-upload {
            margin-top: 1rem;
        }

        /* Button Styles */
        .modal .btn-primary {
            background: var(--primary-color);
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .modal .btn-primary:hover {
            background: #5a52d5;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3);
        }

        .modal .btn-secondary {
            background: #f8f9fa;
            border: 2px solid #eee;
            color: var(--dark-color);
            padding: 0.75rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .modal .btn-secondary:hover {
            background: #e9ecef;
            border-color: #dee2e6;
        }

        /* Change Password Form Specific Styles */
        .password-form .form-group {
            position: relative;
        }

        .password-form .form-control {
            padding-right: 2.5rem;
        }

        .password-toggle {
            position: absolute;
            right: 1rem;
            top: 50%%;
            transform: translateY(-50%%);
            cursor: pointer;
            color: #6c757d;
            transition: color 0.3s ease;
        }

        .password-toggle:hover {
            color: var(--primary-color);
        }

        /* Success Message Styles */
        .alert-success {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        }

        /* Error Message Styles */
        .alert-danger {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        }
body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    
     padding: 0;
    margin: 0;
}

/* Main content wrapper pushes footer down */
.wrapper {
    flex: 1;
}
.nav-link {
      color: black;
      text-decoration: none; /* optional: removes underline */
    }
    .dropdown-item {
      color:var(--primary-color)!important ;
      text-decoration: none; /* optional: removes underline */
    }
    #color{
    background-color:pink;
    }
    </style>
</head>
<body>
    
    <!-- Navbar -->
    <nav id="color" class="navbar navbar-expand-lg navbar-light sticky-top" style="background-color: #F8F9FA;">
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
                        <a class="nav-link dropdown-toggle" href="#" id="trainingDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-graduation-cap me-1"></i>Bookings
                        </a>
                        <ul class="dropdown-menu">
                            <li> <a class="nav-link" href="carevetreq.py?careid=%s">Service Requests</a></li>
                            <li><a class="nav-link" href="caremodcomplete.py?careid=%s">Approved</a>
</li>
                            <li><a class="nav-link" href="caremodpaid.py?careid=%s">Paid</a>
</li>
                            <li><a class="nav-link" href="caremodrejected.py?careid=%s">Rejected</a>
</li>
                             
                        </ul>
                    </li>
                    
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="settingsDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-cog me-1"></i> Settings
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#profileModal">Profile</a></li>
                            <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change Password</a></li>
                            <li><hr class="dropdown-divider"></li>
                            
                        </ul>
                    </li>
                </ul>
            </div>
            
        </div>
    </nav>

    <!-- Center Header -->
    <header class="center-header">
        <div class="container text-center">
            <h1>Care Center Details</h1>
            <p class="lead">View and manage services offered by this center</p>
        </div>
    </header>"""  %(careid,careid,careid,careid))
for i in res:
    img=i[14]
    type=i[3]
    Center=i[2]
    street=i[5]
    city=i[6]
    state=i[7]
    phone=i[9]
    email=i[10]
    description=i[12]

    print(f"""<!-- Main Content -->
     <div class="wrapper">
    <div class="container">
        <div class="row">
            <!-- Center Details -->
            <div class="col-lg-8">
                <div class="card mb-4">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <img src="./images/{img}" alt="Center Image" class="img-fluid center-image mb-3 mb-md-0">
                            </div>
                            <div class="col-md-6">
                                <span class="badge badge-category text-white mb-2">{type}</span>
                                <h2>{Center}</h2>
                                
                                <div class="center-info-item">
                                    <i class="fas fa-map-marker-alt me-2"></i>
                                    <span>{street},{city},{state}</span>
                                </div>
                                
                                <div class="center-info-item">
                                    <i class="fas fa-phone me-2"></i>
                                    <span>{phone}</span>
                                </div>
                                
                                <div class="center-info-item">
                                    <i class="fas fa-envelope me-2"></i>
                                    <span>{email}</span>
                                </div>
                                
                                <hr>
                                
                                <h5>About This Center</h5>
                                <p>{description}</p>
                            </div>
                        </div>
                    </div>
                </div>""")
print("""
                <!-- Services Section -->
                <h3 class="section-title">Services Offered</h3>
                
                <div class="services-list">""")

# Display actual services from database
if services:
    for service in services:
        print(f"""
                    <div class="service-card">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h5 class="mb-1">{service[3]}</h5>
                            </div>
                            <span class="badge bg-primary">${service[4]}</span>
                        </div>
                    </div>""")
else:
    print("""
                    <div class="alert alert-info">
                        No services have been added yet.
                    </div>""")

print("""
                </div>
                
                
            </div>""")

# Add Service Form
print(f"""            <!-- Add Service Form -->
            <div class="col-lg-4">
                <div class="form-container">
                    <h4>Add New Service</h4>
                    <form method="post" action="">
                        <input type="hidden" name="careid" value="%s">
                        
                        <div class="mb-3">
                            <label for="serviceType" class="form-label">Service Type</label>
                            <select class="form-select" id="serviceType" name="servicetype" required>
                                <option value="">Select service type</option>
                                <option value="Veterinary Check-up">Veterinary Check-up</option>
                                <option value="Vaccination">Vaccination</option>
                                <option value="Pet Grooming">Pet Grooming</option>
                                <option value="Dental Care">Dental Care</option>
                                <option value="Surgery">Surgery</option>
                                <option value="Boarding">Boarding</option>
                                <option value="Training">Training</option>
                                <option value="Basic Commands Training">Basic Commands Training</option>
                                <option value="Socialization Session">Socialization Session</option>
                                <option value="Pet Spa">Pet Spa</option>
                                <option value="Behavior Consultation">Behavior Consultation</option>
                                <option value="Bathing">Bathing</option>
                                <option value="Breed styling">Breed Specific Stylinh</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label for="servicePrice" class="form-label">Price ($)</label>
                            <div class="input-group">
                                <span class="input-group-text">$</span>
                                <input type="number" class="form-control" id="servicePrice" name="serviceprice" step="0.01" min="0" required>
                            </div>
                        </div>
                        
                        <input type="submit" name="addservice" value="Add Service" class="btn btn-primary w-100">
                    </form>
                </div>
                </div>""")

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
    """ % (i[13], i[4], i[6], i[9], i[10]))
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
    """ % (i[13], i[4]))

    for i in res:
        Oldpass = i[11]
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
            </div>
            </div>""" % (Oldpass))

print("""              

    <footer  text-white py-4 mt-auto">
    <div class="container-fluid px-4">  <!-- container-fluid for full width -->
        <div class="row">
            <div class="col-md-12">
                <h5>About PetMatch</h5>
                <p>Connecting pet owners with the best care services in their area.</p>
            </div>
        </div>
    </div>
</footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
      """)
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
                open('images/' + fn, 'wb').write(fileitem.file.read())
                # Update database with new image
                cur.execute("UPDATE careresource_info SET resourcername=%s, Image=%s WHERE careid=%s",
                            (uname, fn, careid))
            else:
                # Update without changing image
                cur.execute("UPDATE careresource_info SET resourcername=%s WHERE careid=%s",
                            (uname, careid))

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
        error_messages.append("Current password is incorrect")

    # 2. Validate new password requirements
    if Newpassword:
        if len(Newpassword) < 8:
            error_messages.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in Newpassword):
            error_messages.append("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in Newpassword):
            error_messages.append("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in Newpassword):
            error_messages.append("Password must contain at least one number")
        if not any(c in '!@#$%^&*' for c in Newpassword):
            error_messages.append("Password must contain at least one special character (!@#$%^&*)")
        if Newpassword == Oldpassword:
            error_messages.append("New password cannot be same as old password")
    else:
        error_messages.append("New password cannot be empty")

    # 3. Validate password confirmation
    if Newpassword != Confirmpassword:
        error_messages.append("New password and confirmation do not match")

    # Only proceed if no validation errors
    if not error_messages:
        try:
            # Update database
            cur.execute("UPDATE careresource_info SET pass=%s WHERE careid=%s", (Confirmpassword, careid))
            con.commit()
            print("""
            <script>
                alert("Password changed successfully!");
                window.location.href = window.location.href;
            </script>
            """)
        except Exception as e:
            error_messages.append(f"Error saving changes: {str(e)}")

    # Show errors if any
    if error_messages:
        combined_errors = "\\n".join(error_messages)  # Join errors with newlines
        print(f"""
           <script>
               alert("Please fix the following errors:\\n\\n{combined_errors}");
           </script>
           """)

