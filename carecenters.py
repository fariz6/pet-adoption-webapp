#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Uid = form.getvalue("id")

# HTML Header (similar to your existing one)
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Care Centers | PetMatch</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Chewy&display=swap" rel="stylesheet">
    <style>
        /* Your existing CSS styles here */
        :root {
            --primary-color: #6C63FF;
            --secondary-color: #FF6584;
            --accent-color: #4FD1C5;
            --dark-color: #2D3748;
            --light-color: #F8F9FA;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--light-color);
            color: var(--dark-color);
        }

        .navbar {
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .navbar-brand {
            font-family: 'Chewy', cursive;
            font-size: 1.8rem;
            color: var(--primary-color) !important;
        }

        .resource-card {
            border: none;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            margin-bottom: 2rem;
            height: 100%;
        }

        .resource-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }

        .resource-img {
            height: 200px;
            object-fit: cover;
            width: 100%;
        }

        .badge-category {
            background-color: var(--accent-color);
            color: white;
        }

        .section-title {
            position: relative;
            padding-bottom: 0.75rem;
            margin-bottom: 2rem;
        }

        .section-title:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 60px;
            height: 4px;
            background-color: var(--primary-color);
            border-radius: 2px;
        }
    </style>
</head>
<body>
    <!-- Navigation Bar (same as your existing one) -->
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="fas fa-home me-1"></i> Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="fas fa-paw me-1"></i> Pets</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="#"><i class="fas fa-heart me-1"></i> Care Resources</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="fas fa-question-circle me-1"></i> Help Center</a>
                    </li>
                </ul>
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user-circle me-1"></i> My Account
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="#"><i class="fas fa-tachometer-alt me-2"></i> Dashboard</a></li>
                            <li><a class="dropdown-item" href="#"><i class="fas fa-bookmark me-2"></i> Saved Items</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="#"><i class="fas fa-sign-out-alt me-2"></i> Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container py-5">
        <h1 class="section-title">All Care Centers</h1>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
""")

# Fetch all care centers from the database
cur.execute("SELECT * FROM careresource_info")
centers = cur.fetchall()

if centers:
    for center in centers:
        print(f"""
            <div class="col">
                <div class="resource-card">
                    <img src="./images/{center[10]}" class="resource-img" alt="{center[1]}">
                    <div class="card-body">
                        <span class="badge badge-category mb-2">{center[2]}</span>
                        <h3 class="h5">{center[1]}</h3>
                        <p class="text-muted"><i class="fas fa-map-marker-alt me-1"></i>{center[4]}</p>
                        <p class="card-text">{center[9][:100]}{'...' if len(center[9]) > 100 else ''}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star-half-alt text-warning"></i>
                                <span class="ms-1">4.5</span>
                            </div>
                            <a href="center_details.py?id={center[0]}&userid={Uid}" class="btn btn-sm btn-outline-primary">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
        """)
else:
    print("""
        <div class="col-12">
            <div class="alert alert-info">
                No care centers found in our database.
            </div>
        </div>
    """)

print("""
        </div>
    </div>

    <!-- Footer (same as your existing one) -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 mb-5 mb-lg-0">
                    <div class="footer-links">
                        <h5><i class="fas fa-paw me-2"></i>PetMatch</h5>
                        <p class="mt-3">Connecting loving homes with animals in need and providing resources for pet care and wellness.</p>
                        <div class="social-icons mt-4">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-twitter"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                            <a href="#"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 mb-4 mb-md-0">
                    <div class="footer-links">
                        <h5>Quick Links</h5>
                        <ul>
                            <li><a href="#">Home</a></li>
                            <li><a href="#">About Us</a></li>
                            <li><a href="#">Adoptable Pets</a></li>
                            <li><a href="#">Care Resources</a></li>
                            <li><a href="#">Success Stories</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 mb-4 mb-md-0">
                    <div class="footer-links">
                        <h5>Resources</h5>
                        <ul>
                            <li><a href="#">Veterinary Care</a></li>
                            <li><a href="#">Training Guides</a></li>
                            <li><a href="#">Pet Nutrition</a></li>
                            <li><a href="#">Behavior Tips</a></li>
                            <li><a href="#">Emergency Care</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-4 col-md-4">
                    <div class="footer-links">
                        <h5>Contact Us</h5>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-map-marker-alt me-2"></i> 123 Pet Street, Animal City, AC 12345</li>
                            <li><i class="fas fa-phone me-2"></i> (555) 123-4567</li>
                            <li><i class="fas fa-envelope me-2"></i> info@petmatch.com</li>
                            <li><i class="fas fa-clock me-2"></i> Mon-Fri: 9AM-6PM</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="copyright text-center">
                <p class="mb-0">&copy; 2023 PetMatch. All rights reserved. | <a href="#" class="text-white">Privacy Policy</a> | <a href="#" class="text-white">Terms of Service</a></p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()