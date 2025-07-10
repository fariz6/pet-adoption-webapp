#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os
import smtplib
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cgitb.enable()

def safe_write_file(file_path, content):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {str(e)}")
        return False

try:
    con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
    cur = con.cursor()
except Exception as e:
    print(f"<script>alert('Database connection failed: {str(e)}');</script>")
    sys.exit(1)

form = cgi.FieldStorage()
Cid = form.getvalue("centreid")
s = """select * from care_reg where centreid="%s" """ % (Cid)
cur.execute(s)
res = cur.fetchall()
# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - Care & Resources</title>
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
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .container {
            flex: 1;
        }

        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
        }

        .navbar {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .dashboard-header {
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

        .resource-card img {
            height: 180px;
            object-fit: cover;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }

        .article-card img {
            height: 200px;
            object-fit: cover;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
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

        footer {
            margin-top: auto;
            background-color: var(--dark-color);
            color: white;
            padding: 2rem 0;
        }

        .footer-links h5 {
            margin-bottom: 1rem;
            position: relative;
        }

        .footer-links h5:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -8px;
            width: 40px;
            height: 2px;
            background-color: var(--primary-color);
        }

        .footer-links ul {
            list-style: none;
            padding-left: 0;
        }

        .footer-links li {
            margin-bottom: 0.3rem;
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
            border-radius: 50%%;
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
            padding-top: 1rem;
            margin-top: 1.5rem;
        }

        .hidden {
            display: none;
        }

        /* Profile Picture Styles */
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

.resource-card {
    background: #fff;
    border-radius: 15px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(0,0,0,0.1);
    width: 100%%;
    min-height: 500px;
    display: flex;
    flex-direction: column;
    margin-bottom: 2rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.resource-card .card-body {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    padding: 1.25rem;
}

.resource-card .card-img-top {
    height: 200px;
    object-fit: cover;
    width: 100%%;
}

.resource-card .card-title {
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
    font-weight: 600;
    line-height: 1.4;
}

.resource-card .card-text {
    flex: 1;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    margin-bottom: 1rem;
    color: #6c757d;
    font-size: 0.9rem;
    line-height: 1.5;
}

.resource-card .badge {
    align-self: flex-start;
    margin-bottom: 0.75rem;
    padding: 0.5em 0.75em;
    font-size: 0.75rem;
}

.resource-card .d-flex.justify-content-between {
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid rgba(0,0,0,0.1);
}

.resource-card .btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
}

.resource-card .btn-outline-primary:hover,
.resource-card .btn-outline-danger:hover {
    transform: translateY(-2px);
    transition: transform 0.2s ease;
}

/* No centers message */
.no-centers {
    text-align: center;
    padding: 3rem;
    background: #f8f9fa;
    border-radius: 10px;
    margin: 2rem 0;
}

.no-centers i {
    font-size: 3rem;
    color: #6c757d;
    margin-bottom: 1rem;
}
    </style>
</head>
<body>
    <!-- Navbar -->
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
                        <a class="nav-link dropdown-toggle" href="#" id="trainingDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-graduation-cap me-1"></i>Bookings
                        </a>
                        <ul class="dropdown-menu">
                            <li> <a class="nav-link" href="carevetreq.py?centreid=%s">Service Requests</a></li>
                            <li><a class="nav-link" href="caremodcomplete.py?centreid=%s">Approved</a>
</li>
                            <li><a class="nav-link" href="caremodpaid.py?centreid=%s">Paid</a>
</li>
                            <li><a class="nav-link" href="caremodrejected.py?centreid=%s">Rejected</a>
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

    <!-- Dashboard Header -->
    <header class="dashboard-header">
        <div class="container text-center">
            <h1>Care & Resource Center</h1>
            <p class="lead">Manage pet care services, training requests, and educational resources</p>
        </div>
    </header>""" %(Cid,Cid,Cid,Cid))
m = """ select * from care_reg where centreid="%s" """ % (Cid)
cur.execute(m)
result = cur.fetchall()

for i in result:
    Centerid=i[0]
    Ownername = i[3]

    Address = i[9]
    City = i[12]
    State = i[11]
    Pin = i[10]
    Phone = i[8]
    Email = i[6]
    Image = i[14]

    print("""    <div class="container">
        <!-- Add Resource Center Form -->
        <section id="resourceCentersSection">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="section-title">Resource Centers</h2>
                <button class="btn btn-primary" id="toggleResourceForm">
                    <i class="fas fa-plus me-2"></i>Add Resource Center
                </button>
            </div>

            <div id="resourceFormContainer" class="form-container hidden">
                <h4>Add New Resource Center</h4>
                <form id="resourceCenterForm" method="post" enctype="multipart/form-data">
                    <div class="row g-3">
                        <input type="hidden" class="form-control" name="Centerid" id="centerName" value="%s"    required>
                        <div class="col-md-6">
                            <label for="centerName" class="form-label">Center Name</label>
                            <input type="text" class="form-control" name="Center" id="centerName"    required>
                        </div>
                        
                        <div class="col-md-6">
                            <label for="centerType" class="form-label">Center Type</label>
                            <select class="form-select" id="centerType" name="Service" required>
                                <option value="">Select type</option>
                                <option>Veterinary Clinic</option>
                                
                                <option>Training Center</option>
                                <option>Pet Spa</option>
                                <option>Other</option>
                            </select>
                            
                        </div>
                        <div class="col-12">
                            <label for="centerAddress" class="form-label">Address</label>
                            <input type="text" class="form-control" id="centerAddress" name="address"  required>
                        </div>
                        <div class="col-md-4">
                            <label for="centerCity" class="form-label">City</label>
                            <input type="text" class="form-control" id="centerCity" name="city"  required>
                        </div>
                        <div class="col-md-4">
                            <label for="centerState" class="form-label">State</label>
                            <input type="text" class="form-control" id="centerState" name="state" required>
                        </div>
                        <div class="col-md-4">
                            <label for="centerZip" class="form-label">Zip Code</label>
                            <input type="text" class="form-control" id="centerZip" name="pin"  required>
                        </div>
                        <div class="col-md-6">
                            <label for="centerPhone" class="form-label">Phone Number</label>
                            <input type="tel" class="form-control" id="centerPhone" name="phone" value=%s required>
                        </div>
                        <div class="col-md-6">
                            <label for="centerEmail" class="form-label">Email</label>
                            <input type="email" class="form-control" id="centerEmail" name="email" value=%s>
                        </div>
                        <div class="col-12">
                            <label for="centerDescription" class="form-label">Description</label>
                            <textarea class="form-control" id="centerDescription" name="description" rows="3"></textarea>
                        </div>
                        <div class="col-12">
                            <label for="centerImage" class="form-label">Upload Image</label>
                            <input class="form-control" type="file" id="centerImage" name="image" >
                        </div>
                        <div class="col-12 mt-3">
                            <input type="submit" value="Save center" name="add" class="btn btn-primary me-2">
                            <button type="button" class="btn btn-outline-secondary" id="cancelResourceForm">Cancel</button>
                        </div>
                    </div>
                </form>
            </div>""" % (Centerid,Phone, Email))

    cur.execute("SELECT * FROM Careresource_info WHERE centerid=%s", (Cid))
    care_centers = cur.fetchall()

    print("""
                <!-- Resource Centers List -->
                <div class="row" id="resourceCentersList">""")

    if not care_centers:
        print("""
                    <div class="col-12">
                        <div class="no-centers">
                            <i class="fas fa-building"></i>
                            <h3>No Care Centers Added Yet</h3>
                            <p class="text-muted">Click the "Add Resource Center" button above to add your first care center.</p>
                        </div>
                    </div>""")
    else:
        for center in care_centers:

            # Unpack the center data (adjust based on your actual table structure)
            careid = center[0]  # Assuming first column is ID
            center_name = center[2]  # centername
            center_type = center[3]  # centertype
            address = center[4]  # address
            city = center[5]  # city
            state = center[6]  # state
            description = center[10]  # description
            image_path = center[11]  # image

            # Use a default image if none is provided

            print(f"""
                        <!-- Center Card -->
                        <div class="col-md-6 col-lg-4">
                            <div class="card resource-card">
                                <img src="./images/{image_path}" class="card-img-top" alt="{center_type}">
                                <div class="card-body d-flex flex-column">
                                    <span class="badge badge-category text-white mb-2">{center_type}</span>
                                    <h5 class="card-title">{center_name}</h5>
                                    <p class="card-text text-muted"><i class="fas fa-map-marker-alt me-1"></i>{address}, {city}, {state}</p>
                                    <p class="card-text">{description}</p>
                                    <div class="d-flex justify-content-between mt-auto">
                                        <a href="get_services.py?careid={careid}" class="btn btn-sm btn-outline-primary">View Details</a>
                                        <div>
                                            <button class="btn btn-sm btn-outline-danger" onclick="deleteCenter({careid})">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>""")

    print("""
                </div>
            </section>""")

print("""        <!-- Articles Section (Initially Hidden) -->
        <section id="articlesSection" class="hidden">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="section-title">Articles</h2>
                <button class="btn btn-primary" id="toggleArticleForm">
                    <i class="fas fa-plus me-2"></i>Post Article
                </button>
            </div>

            <!-- Post Article Form -->
            <div id="articleFormContainer" class="form-container hidden">
                <h4>Create New Article</h4>
                <form id="articleForm">
                    <div class="row g-3">
                        <div class="col-12">
                            <label for="articleTitle" class="form-label">Title</label>
                            <input type="text" name="tittle" class="form-control" id="articleTitle" required>
                        </div>
                        <div class="col-md-6">
                            <label for="articleCategory" class="form-label">Category</label>
                            <select class="form-select" name="category" id="articleCategory" required>
                                <option value="">Select category</option>
                                <option>Pet Care</option>
                                <option>Training</option>
                                <option>Health</option>
                                <option>Nutrition</option>
                                <option>Behavior</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label for="articleAuthor" class="form-label">Author</label>
                            <input type="text" name="author" class="form-control" id="articleAuthor" required>
                        </div>
                        <div class="col-12">
                            <label for="articleContent" class="form-label">Content</label>
                            <textarea class="form-control" name="content" id="articleContent" rows="6" required></textarea>
                        </div>
                        <div class="col-12">
                            <label for="articleImage" class="form-label">Featured Image</label>
                            <input class="form-control" name="images" type="file" id="articleImage">
                        </div>
                        <div class="col-12 mt-3">
                            <input type="submit" name="publish" value="Publish Article" class="btn btn-primary me-2">
                            <button type="button" class="btn btn-outline-secondary" id="cancelArticleForm">Cancel</button>
                        </div>
                    </div>
                </form>
            </div>

            <!-- Articles List -->
            <div class="row" id="articlesList">
                <!-- Article 1 -->
                <div class="col-md-6 col-lg-4">
                    <div class="card article-card">
                        <img src="https://images.unsplash.com/photo-1544568100-847a948585b9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1548&q=80" class="card-img-top" alt="Dog Training">
                        <div class="card-body">
                            <span class="badge badge-category text-white mb-2">Training</span>
                            <h5 class="card-title">Basic Obedience Training for Dogs</h5>
                            <p class="card-text text-muted"><i class="fas fa-user me-1"></i>By Dr. Sarah Johnson</p>
                            <p class="card-text">Learn the essential commands every dog should know and how to teach them effectively.</p>
                            <div class="d-flex justify-content-between">
                                <a href="#" class="btn btn-sm btn-outline-primary">Read More</a>
                                <div>
                                    <button class="btn btn-sm btn-outline-secondary me-1"><i class="fas fa-edit"></i></button>
                                    <button class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Article 2 -->
                <div class="col-md-6 col-lg-4">
                    <div class="card article-card">
                        <img src="https://images.unsplash.com/photo-1519052537078-e6302a4968d4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80" class="card-img-top" alt="Cat Health">
                        <div class="card-body">
                            <span class="badge badge-category text-white mb-2">Health</span>
                            <h5 class="card-title">Common Feline Health Issues</h5>
                            <p class="card-text text-muted"><i class="fas fa-user me-1"></i>By Dr. Michael Chen</p>
                            <p class="card-text">A guide to recognizing and preventing the most common health problems in cats.</p>
                            <div class="d-flex justify-content-between">
                                <a href="#" class="btn btn-sm btn-outline-primary">Read More</a>
                                <div>
                                    <button class="btn btn-sm btn-outline-secondary me-1"><i class="fas fa-edit"></i></button>
                                    <button class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- Footer -->
    <footer>
        
            
                
            <div class="copyright text-center">
                <p class="mb-0">&copy; 2023 PetMatch Care Resources. All rights reserved.</p>
            </div>
        </div>
    </footer>""")
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
    """ % (i[13], i[3], i[8], i[6], i[11]))
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
    """ % (i[13], i[3]))

    for i in res:
        Oldpass = i[7]
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
print("""    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Custom JS -->
    <script>
        // Toggle resource center form
        document.getElementById('toggleResourceForm').addEventListener('click', function() {
            document.getElementById('resourceFormContainer').classList.toggle('hidden');
        });

        document.getElementById('cancelResourceForm').addEventListener('click', function() {
            document.getElementById('resourceFormContainer').classList.add('hidden');
        });

        // Toggle article form
        document.getElementById('toggleArticleForm').addEventListener('click', function() {
            document.getElementById('articleFormContainer').classList.toggle('hidden');
        });

        document.getElementById('cancelArticleForm').addEventListener('click', function() {
            document.getElementById('articleFormContainer').classList.add('hidden');
        });

        // Switch between resource centers and articles sections
        document.getElementById('postArticleBtn').addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('resourceCentersSection').classList.add('hidden');
            document.getElementById('articlesSection').classList.remove('hidden');
            document.getElementById('articleFormContainer').classList.remove('hidden');
        });

        document.getElementById('viewArticlesBtn').addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('resourceCentersSection').classList.add('hidden');
            document.getElementById('articlesSection').classList.remove('hidden');
            document.getElementById('articleFormContainer').classList.add('hidden');
        });

        document.getElementById('articleForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Article published successfully!');
            this.reset();
            document.getElementById('articleFormContainer').classList.add('hidden');
            // Here you would add the new article to the DOM
        });

        // Delete center function
        function deleteCenter(careid) {
            if (confirm('Are you sure you want to delete this care center? This action cannot be undone.')) {
                // Create a form to submit the deletion request
                const form = document.createElement('form');
                form.method = 'post';
                form.action = 'delete_care.py';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'careid';
                input.value = careid;
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        }
    </script>
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
                            (uname, fn, Cid))
            else:
                # Update without changing image
                cur.execute("UPDATE careresource_info SET resourcername=%s WHERE careid=%s",
                            (uname, Cid))

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
            cur.execute("UPDATE careresource_info SET pass=%s WHERE careid=%s", (Confirmpassword, Cid))
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
        print("<script>")
        for msg in error_messages:
            print(f'alert("{msg}");')
        print("</script>")

Add = form.getvalue("add")

if Add:
    try:
        # Get form values
        centerid = form.getvalue("Centerid")
        centername = form.getvalue("Center")
        centertype = form.getvalue("Service")
        address = form.getvalue("address")
        city = form.getvalue("city")
        state = form.getvalue("state")
        pin = form.getvalue("pin")
        phone = form.getvalue("phone")
        email = form.getvalue("email")
        description = form.getvalue("description")
        price = form.getvalue("sprice")

        # Handle file upload
        image_path = None
        if "image" in form:
            file_item = form['image']
            if file_item.filename:
                allowed_extensions = {'.jpg', '.jpeg', '.png'}
                file_ext = os.path.splitext(file_item.filename)[1].lower()
                if file_ext not in allowed_extensions:
                    raise ValueError("Invalid file type. Only JPG, JPEG, and PNG files are allowed.")

                file_item.file.seek(0, 2)
                file_size = file_item.file.tell()
                file_item.file.seek(0)
                if file_size > 2 * 1024 * 1024:
                    raise ValueError("File size exceeds 2MB limit")

                upload_dir = "images"
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                filename = f"{centerid}_{file_item.filename}"
                file_path = os.path.join(upload_dir, filename)
                if safe_write_file(file_path, file_item.file.read()):
                    image_path = filename

        # Insert into database
        sql = """INSERT INTO careresource_info 
                 (centerid, centername, centertype, address, city, state, pin, mob, mail, description, Image) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cur.execute(sql, (
            centerid, centername, centertype, address, city, state, 
            pin, phone, email, description, image_path
        ))
        con.commit()

        print("""
            <script>
                alert('Care center added successfully!');
                    </script>
            """)
    except Exception as e:
        print(f"""
            <script>
                alert('Error adding care center: {str(e)}');
                console.error('Error details: {str(e)}');
            </script>
            """)
        con.rollback()