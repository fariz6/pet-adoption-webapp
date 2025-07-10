#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os
import smtplib

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
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
    <title>Care Resource Centers | PetMatch</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Chewy&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4e73df;
            --secondary-color: #1cc88a;
            --dark-color: #2d3748;
            --light-color: #f8f9fa;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--light-color);
            color: var(--dark-color);
        }
        
        .navbar {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .navbar-brand {
            font-family: 'Chewy', cursive;
            font-size: 1.8rem;
            color: var(--primary-color) !important;
        }
        
        .page-header {
            background: linear-gradient(rgba(78, 115, 223, 0.1), rgba(78, 115, 223, 0.05));
            padding: 4rem 0;
            margin-bottom: 3rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        .page-title {
            font-family: 'Chewy', cursive;
            color: var(--primary-color);
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .resource-card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            margin-bottom: 2rem;
            overflow: hidden;
        }
        
        .resource-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .resource-img {
            height: 250px;
            object-fit: cover;
            width: 100%;
        }
        
        .card-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: var(--secondary-color);
            color: white;
            padding: 5px 15px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .resource-details {
            padding: 1.5rem;
        }
        
        .resource-title {
            color: var(--primary-color);
            margin-bottom: 0.75rem;
        }
        
        .resource-meta {
            color: #6c757d;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .resource-meta i {
            margin-right: 5px;
        }
        
        .btn-details {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 50px;
            transition: all 0.3s ease;
        }
        
        .btn-details:hover {
            background-color: #3a5bc7;
            color: white;
            transform: translateY(-2px);
        }
        
        .filter-section {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            margin-bottom: 2rem;
        }
        
        .filter-title {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 3rem 0;
            margin-top: 4rem;
        }
        
        .social-icon {
            color: white;
            font-size: 1.25rem;
            margin: 0 10px;
            transition: all 0.3s ease;
        }
        
        .social-icon:hover {
            color: var(--secondary-color);
            transform: translateY(-3px);
        }
        
        @media (max-width: 768px) {
            .page-header {
                padding: 2.5rem 0;
            }
            
            .resource-img {
                height: 200px;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Pets</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Care Resources</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Adoption</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">About</a>
                    </li>
                </ul>
                <button class="btn btn-outline-primary ms-lg-3">Login</button>
            </div>
        </div>
    </nav>

    <!-- Page Header -->
    <section class="page-header">
        <div class="container text-center">
            <h1 class="page-title">Care Resource Centers</h1>
            <p class="lead">Find veterinary clinics, shelters, and pet care services near you</p>
        </div>
    </section>

    <!-- Main Content -->
    <div class="container">
        <!-- Filter Section -->
        <div class="filter-section">
            <div class="row">
                <div class="col-md-6">
                    <h5 class="filter-title"><i class="fas fa-filter me-2"></i>Filter Centers</h5>
                </div>
                <div class="col-md-6">
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" placeholder="Search by name or location...">
                        <button class="btn btn-primary" type="button">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-3 mb-3">
                    <label class="form-label">Center Type</label>
                    <select class="form-select">
                        <option selected>All Types</option>
                        <option>Veterinary Clinic</option>
                        <option>Animal Shelter</option>
                        <option>Pet Grooming</option>
                        <option>Training Center</option>
                        <option>Emergency Care</option>
                    </select>
                </div>
                <div class="col-md-3 mb-3">
                    <label class="form-label">Location</label>
                    <select class="form-select">
                        <option selected>All Areas</option>
                        <option>Downtown</option>
                        <option>Northside</option>
                        <option>Southside</option>
                        <option>East End</option>
                        <option>West District</option>
                    </select>
                </div>
                <div class="col-md-3 mb-3">
                    <label class="form-label">Services</label>
                    <select class="form-select">
                        <option selected>All Services</option>
                        <option>Vaccinations</option>
                        <option>Spay/Neuter</option>
                        <option>Emergency Care</option>
                        <option>Dental Care</option>
                        <option>Behavioral Training</option>
                    </select>
                </div>
                <div class="col-md-3 mb-3">
                    <label class="form-label">Rating</label>
                    <select class="form-select">
                        <option selected>Any Rating</option>
                        <option>4+ Stars</option>
                        <option>3+ Stars</option>
                    </select>
                </div>
            </div>
        </div>
        
        <!-- Resource Centers Listing -->
        <div class="row">
            <!-- Center 1 -->
            <div class="col-lg-4 col-md-6">
                <div class="resource-card">
                    <div class="position-relative">
                        <img src="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80" class="resource-img" alt="Veterinary Clinic">
                        <span class="card-badge">Veterinary</span>
                    </div>
                    <div class="resource-details">
                        <h3 class="resource-title">Happy Paws Veterinary Clinic</h3>
                        <div class="resource-meta">
                            <span><i class="fas fa-map-marker-alt"></i> 123 Pet Care Ave, Downtown</span><br>
                            <span><i class="fas fa-phone"></i> (555) 123-4567</span>
                        </div>
                        <p>Full-service veterinary clinic offering wellness exams, surgeries, and emergency care with compassionate service.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star-half-alt text-warning"></i>
                                <span class="ms-1">4.5</span>
                            </div>
                            <a href="#" class="btn btn-details">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Center 2 -->
            <div class="col-lg-4 col-md-6">
                <div class="resource-card">
                    <div class="position-relative">
                        <img src="https://images.unsplash.com/photo-1450778869180-41d0601e046e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1586&q=80" class="resource-img" alt="Animal Shelter">
                        <span class="card-badge">Shelter</span>
                    </div>
                    <div class="resource-details">
                        <h3 class="resource-title">Safe Haven Animal Shelter</h3>
                        <div class="resource-meta">
                            <span><i class="fas fa-map-marker-alt"></i> 456 Rescue Lane, Northside</span><br>
                            <span><i class="fas fa-phone"></i> (555) 987-6543</span>
                        </div>
                        <p>Non-profit shelter dedicated to rescuing and rehoming abandoned pets with a no-kill policy and volunteer programs.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <span class="ms-1">5.0</span>
                            </div>
                            <a href="#" class="btn btn-details">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Center 3 -->
            <div class="col-lg-4 col-md-6">
                <div class="resource-card">
                    <div class="position-relative">
                        <img src="https://images.unsplash.com/photo-1591769225440-811ad7d6eab2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1587&q=80" class="resource-img" alt="Pet Grooming">
                        <span class="card-badge">Grooming</span>
                    </div>
                    <div class="resource-details">
                        <h3 class="resource-title">Pampered Pets Spa</h3>
                        <div class="resource-meta">
                            <span><i class="fas fa-map-marker-alt"></i> 789 Luxury St, West District</span><br>
                            <span><i class="fas fa-phone"></i> (555) 456-7890</span>
                        </div>
                        <p>Premium pet grooming services including baths, haircuts, nail trims, and specialty treatments in a relaxing environment.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="far fa-star text-warning"></i>
                                <span class="ms-1">4.0</span>
                            </div>
                            <a href="#" class="btn btn-details">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Center 4 -->
            <div class="col-lg-4 col-md-6">
                <div class="resource-card">
                    <div class="position-relative">
                        <img src="https://images.unsplash.com/photo-1544568100-847a948585b9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1588&q=80" class="resource-img" alt="Training Center">
                        <span class="card-badge">Training</span>
                    </div>
                    <div class="resource-details">
                        <h3 class="resource-title">Well-Behaved Canines</h3>
                        <div class="resource-meta">
                            <span><i class="fas fa-map-marker-alt"></i> 321 Obedience Rd, Southside</span><br>
                            <span><i class="fas fa-phone"></i> (555) 789-0123</span>
                        </div>
                        <p>Professional dog training center offering group classes, private lessons, and behavior modification programs.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star-half-alt text-warning"></i>
                                <span class="ms-1">4.5</span>
                            </div>
                            <a href="#" class="btn btn-details">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Center 5 -->
            <div class="col-lg-4 col-md-6">
                <div class="resource-card">
                    <div class="position-relative">
                        <img src="https://images.unsplash.com/photo-1583339793403-3ad9f42da536?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1588&q=80" class="resource-img" alt="Emergency Care">
                        <span class="card-badge">Emergency</span>
                    </div>
                    <div class="resource-details">
                        <h3 class="resource-title">Pet Emergency Center</h3>
                        <div class="resource-meta">
                            <span><i class="fas fa-map-marker-alt"></i> 911 Emergency Way, East End</span><br>
                            <span><i class="fas fa-phone"></i> (555) 911-9111</span>
                        </div>
                        <p>24/7 emergency veterinary hospital with ICU, surgery suite, and critical care specialists for urgent pet needs.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <span class="ms-1">5.0</span>
                            </div>
                            <a href="#" class="btn btn-details">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Center 6 -->
            <div class="col-lg-4 col-md-6">
                <div class="resource-card">
                    <div class="position-relative">
                        <img src="https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1471&q=80" class="resource-img" alt="Pet Boarding">
                        <span class="card-badge">Boarding</span>
                    </div>
                    <div class="resource-details">
                        <h3 class="resource-title">Home Away From Home</h3>
                        <div class="resource-meta">
                            <span><i class="fas fa-map-marker-alt"></i> 101 Vacation Dr, West District</span><br>
                            <span><i class="fas fa-phone"></i> (555) 101-0101</span>
                        </div>
                        <p>Luxury pet boarding facility with private suites, play areas, and webcam access so you can check on your pet.</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="fas fa-star text-warning"></i>
                                <i class="far fa-star text-warning"></i>
                                <span class="ms-1">4.0</span>
                            </div>
                            <a href="#" class="btn btn-details">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Pagination -->
        <nav aria-label="Page navigation" class="mt-4">
            <ul class="pagination justify-content-center">
                <li class="page-item disabled">
                    <a class="page-link" href="#" tabindex="-1">Previous</a>
                </li>
                <li class="page-item active"><a class="page-link" href="#">1</a></li>
                <li class="page-item"><a class="page-link" href="#">2</a></li>
                <li class="page-item"><a class="page-link" href="#">3</a></li>
                <li class="page-item">
                    <a class="page-link" href="#">Next</a>
                </li>
            </ul>
        </nav>
    </div>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-lg-4 mb-4">
                    <h5><i class="fas fa-paw me-2"></i>PetMatch</h5>
                    <p>Connecting pet owners with quality care resources to ensure happy, healthy lives for all animals.</p>
                    <div class="mt-3">
                        <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 mb-4">
                    <h5>Resources</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="text-white">Veterinary Care</a></li>
                        <li><a href="#" class="text-white">Training</a></li>
                        <li><a href="#" class="text-white">Grooming</a></li>
                        <li><a href="#" class="text-white">Boarding</a></li>
                        <li><a href="#" class="text-white">Emergency</a></li>
                    </ul>
                </div>
                <div class="col-lg-2 col-md-4 mb-4">
                    <h5>Company</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="text-white">About Us</a></li>
                        <li><a href="#" class="text-white">Our Team</a></li>
                        <li><a href="#" class="text-white">Careers</a></li>
                        <li><a href="#" class="text-white">Blog</a></li>
                        <li><a href="#" class="text-white">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 mb-4">
                    <h5>Newsletter</h5>
                    <p>Subscribe to get updates on new care resources and pet health tips.</p>
                    <div class="input-group mb-3">
                        <input type="email" class="form-control" placeholder="Your email">
                        <button class="btn btn-primary" type="button">Subscribe</button>
                    </div>
                </div>
            </div>
            <hr class="my-4 bg-light">
            <div class="text-center">
                <p class="mb-0">&copy; 2023 PetMatch Care Resources. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
      """)