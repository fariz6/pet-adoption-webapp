#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()


# HTML Form

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<style>
    /* Navbar Styles */
.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
    color: #f6c364 !important;
}

/* Hero Section */
.hero {
    background: linear-gradient(90deg, #4CAF50 30%, #f6c364);
    color: #fff;
}

.hero h1 {
    font-size: 3rem;
    font-weight: bold;
}

.hero .btn-primary {
    background-color:  rgb(246, 162, 5);
    border: none;
    font-size: 1.2rem;
}

.hero .btn-primary:hover {
    background-color: rgb(246, 195, 100);
}

/* Card Styles */
.card-title {
    font-size: 1.4rem;
    font-weight: bold;
    color: #333;
}

.hover-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.card .btn-outline-primary {
    border-color: #4CAF50;
    color: #4CAF50;
}

.card .btn-outline-primary:hover {
    background-color: #4CAF50;
    color: #fff;
}

/* Footer Styles */
footer {
    background-color: #333;
    color: #fff;
}

footer .social-icons a {
    font-size: 1.5rem;
    transition: color 0.3s ease;
}

footer .social-icons a:hover {
    color: #f6c364;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5rem;
    }
}
.navbar-nav .nav-link {
            color:  rgb(246, 195, 100)!important;
            transition: color 0.3s ease;
        }
        
        .navbar-nav .nav-link:hover {
            color: white !important;
        }

         ul li::after{
            content:'';
            height:2px;
            width:0%;
            background:rgb(246, 195, 100);
            display:block;
            margin:auto;
            transition:0.5s;
        }
        ul li:hover::after{
            width:100%;
        }
        
        .footer {
    background-color:#333; 
    color: #fff;
    padding: 20px 0;
    text-align: center;
}
        .footer-logo {
    font-size: 24px;
    font-family: Arial;
    margin-bottom: 10px;
    background-image: linear-gradient(to left, rgb(214, 202, 225), rgba(244, 169, 19, 0.134));
    color: transparent;
    background-clip: text;
}

.footer p {
    font-family: Arial;
    font-size: 14px;
    line-height: 1.6;
}

.footer h5 {
    font-size: 18px;
    margin-bottom: 15px;
}

.footer ul {
    list-style: none;
    padding: 0;
}

.footer ul li {
    margin-bottom: 10px;
}

.footer ul li a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer ul li a:hover {
    color:black;
}

.social-icons a {
    font-size: 20px;
    transition: color 0.3s ease;
}

.social-icons a:hover {
    color: rgb(96, 197, 223);
}
 .pet-card {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            width: 100%;
            max-width: 350px;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .pet-card:hover {
            transform: translateY(-5px);
        }
        
        .pet-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
        
        .pet-info {
            padding: 20px;
        }
        
        .pet-name {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        
        .pet-location {
            display: flex;
            align-items: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .pet-location svg {
            width: 14px;
            height: 14px;
            margin-right: 5px;
            fill: #666;
        }
        
        .pet-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .detail-item {
            display: flex;
            flex-direction: column;
        }
        
        .detail-label {
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            margin-bottom: 3px;
        }
        
        .detail-value {
            font-size: 16px;
            font-weight: 600;
            color: #444;
        }
        
        .buy-button {
            width: 100%;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .buy-button:hover {
            background-color: #45a049;
        }

</style>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">User Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#profile">Profile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#search">Search Pets</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#applications">Applications</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-danger text-white ms-lg-2" href="#">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero bg-light text-center py-5">
        <div class="container">
            <h1 class="display-4">Welcome to Your Pet Dashboard</h1>
            <p class="lead">Connect with your perfect furry companion and manage your adoption journey all in one place!</p>
            <button class="btn btn-primary btn-lg mt-3">Get Started</button>
        </div>
    </section>

    <!-- Dashboard Content -->
    <div class="container mt-5">
        <div class="row text-center">
            <div class="col-md-4">
                <div class="card border-0 shadow mb-4 hover-card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-user-circle"></i> Profile Management</h5>
                        <p class="card-text">Update your profile, preferences, and contact details with ease.</p>
                        <a href="#profile" class="btn btn-outline-warning">Manage Profile</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card border-0 shadow mb-4 hover-card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-search"></i> Search Pets</h5>
                        <p class="card-text">Find your ideal pet using advanced filters like age, breed, and location.</p>
                        <a href="#search" class="btn btn-outline-warning">Search Pets</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card border-0 shadow mb-4 hover-card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-paw"></i> Adoption Applications</h5>
                        <p class="card-text">Submit, track, and manage your adoption applications effortlessly.</p>
                        <a href="#applications" class="btn btn-outline-warning">Manage Applications</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <section id="profile" class="py-5 bg-light">
        <div class="container">
            <h3 class="section-title">Profile Management</h3>
            <form>
                <div class="mb-3">
                    <label for="userName" class="form-label">Name</label>
                    <input type="text" class="form-control" id="userName" placeholder="Enter your name">
                </div>
                <div class="mb-3">
                    <label for="userEmail" class="form-label">Email</label>
                    <input type="email" class="form-control" id="userEmail" placeholder="Enter your email">
                </div>
                <div class="mb-3">
                    <label for="preferences" class="form-label">Preferences</label>
                    <input type="text" class="form-control" id="preferences" placeholder="Preferred pet types">
                </div>
                <button type="submit" class="btn btn-warning">Save Changes</button>
            </form>
        </div>
    </section>

    <!-- Search Pets Section -->
    <section id="search" class="py-5">
        <div class="container">
            <h3 class="section-title">Search Pets</h3>
            <form class="row g-3">
                <div class="col-md-3">
                    <label for="species" class="form-label">Species</label>
                    <select class="form-select" id="species" name="species">
                        <option selected>Choose...</option>
                        <option value="Dog">Dog</option>
                        <option value="Cat">Cat</option>
                        <option value="Bird">Bird</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="breed" class="form-label">Breed</label>
                    <input type="text" value="" class="form-control" id="breed" name="breed" placeholder="Enter breed">
                </div>
                <div class="col-md-3">
                    <label for="age" class="form-label">Age</label>
                    <input type="number" value="" class="form-control" id="age" name="age" placeholder="Enter age">
                </div>
                <div class="col-md-3">
                    <label for="location" class="form-label">Location</label>
                    <input type="text" value="" class="form-control" id="location" name="location" placeholder="Enter location">
                </div>
                <div class="col-md-12 text-center mt-3">
                    <input type="submit" value="Search" name="search" class="btn btn-warning">
                </div>
            </form>
        </div>
    </section>""")
Stype=form.getvalue("species")
Sbreed=form.getvalue("breed")
Sage=form.getvalue("age")
Slocation=form.getvalue("location")
Search=form.getvalue("search")

if Search != None:
    a = f"""select * from product_info where Species='{Stype}' and location='{Slocation}' """
    cur.execute(a)
    result = cur.fetchall()
    print("""
    <script>
    location.href="#card"
    </script>
    """)


    for i in result:
            Animalimg=i[9]
            Name=i[4]
            Location=i[7]
            Age=i[8]
            Species=i[5]
            Breed=i[6]

            print("""<div class="pet-card" id="card">
                   <img src="./images/%s" class="card-img-top" >
                    <div class="pet-info">
                        <h2 class="pet-name">%s</h2>
                        <div class="pet-location">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                            </svg>
                            <span>%s</span>
                        </div>
                        <div class="pet-details">
                            <div class="detail-item">
                                <span class="detail-label">Age</span>
                                <span class="detail-value">%s years</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Species</span>
                                <span class="detail-value">%s</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Breed</span>
                                <span class="detail-value">%s</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Gender</span>
                                <span class="detail-value">Male</span>
                            </div>
                        </div>
                        <input type="submit" name="adopt" value="Adopt now" class="buy-button">
                    </div>
            </div>""" %(Animalimg,Name,Location,Age,Species,Breed))

print(""" <!-- Adoption Applications Section -->
    <section id="applications" class="py-5 bg-light">
        <div class="container">
   
   
            <h3 class="section-title">Adoption Applications</h3>
            <p class="section-description">Manage your applications for adopting pets. Track status or withdraw applications.</p>
            <button class="btn btn-warning">View Submitted Applications</button>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer  text-white py-4">
        <div class="container">
            <div class="row">
                <div class="col-lg-3 col-md-6">
                    <h4 class="footer-logo">PetAdoption.in</h4>
                    <p>Your go-to platform for mastering web design and development.</p>
                    <p>Address: 1234 sai baba colony, Tech City, IN 56789</p>
                    <p>Email: support@abdcourse.co</p>
                    <p>Phone: +91 12345 67890</p>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="text-white">Home</a></li>
                        <li><a href="#" class="text-white">Adopt</a></li>
                        <li><a href="#" class="text-white">Care</a></li>
                        <li><a href="#" class="text-white">stories</a></li>
                        <li><a href="#" class="text-white">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5>Recent Blog Posts</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="text-white">Browse our adoption gallery and select a pet.</a></li>
                        <li><a href="#" class="text-white">Fill out an adoption application online.</a></li>
                        <li><a href="#" class="text-white">Arrange a meet-and-greet to ensure a good match.</a></li>
                        <li><a href="#" class="text-white">Complete the adoption process and bring your new friend home.</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5>Newsletter</h5>
                    <p>Subscribe to our newsletter for the latest updates and tutorials.</p>
                    <form action="#" method="post">
                        <input type="email" name="email" class="form-control mb-2" placeholder="Enter your email">
                        <button type="submit" class="btn btn-warning btn-block">Subscribe</button>
                    </form>
                    <h5 class="mt-4">Follow Us</h5>
                    <div class="social-icons">
                        <a href="#" class="text-white mr-2"><ion-icon name="logo-facebook"></ion-icon></a>
                        <a href="#" class="text-white mr-2"><ion-icon name="logo-instagram"></ion-icon></a>
                        <a href="#" class="text-white mr-2"><ion-icon name="logo-twitter"></ion-icon></a>
                        <a href="#" class="text-white mr-2"><ion-icon name="logo-google"></ion-icon></a>
                        <a href="#" class="text-white"><ion-icon name="logo-skype"></ion-icon></a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
   
    
<script src="https://unpkg.com/ionicons@5.4.0/dist/ionicons.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>




    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
</body>
</html>


""")