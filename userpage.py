#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

# HTML Form

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://unpkg.com/ionicons@5.5.2/dist/css/ionicons.min.css"> <!-- Include Ionicons CSS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<style>




  /* Search Form Styles */
  .form-inline .form-control {
            width: auto;
        }

        .form-inline .btn {
            margin-left: 10px;
        }
.btn{
    width: 100px;
    height: 40px;
    background: black;
    border: 2px solid  black;
    margin-top: 13px;
    color: #fff;
    font-size: 15px;
    border-bottom-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
.btn:focus{
    outline: none;
}
.srch:focus{
    outline: none;
         .footer {
    background-color: #343a40;
    color: #fff;
    padding: 20px 0;
    text-align: center;
}}

.footer {
    background-color:#818C78; 
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

         /* Search Form Styles */
         .form-inline .form-control {
            width: auto;
        }

        .form-inline .btn {
            margin-left: 10px;
        }

        /* Ensure Search Form is Visible on Small Screens */
        @media (max-width: 992px) {
            .form-inline {
                width: 100%;
                display: flex !important;
                justify-content: center;
            }

            .form-inline .form-control {
                width: 70%; /* Adjust the width as needed */
                margin: 5px 0;
            }

            .form-inline .btn {
                width: 30%; /* Adjust the width as needed */
                margin: 5px 0;
            }
        }

        /* Menu Styles */
        .navbar-nav .nav-link {
            color:  white!important;
            transition: color 0.3s ease;
        }

        .navbar-nav .nav-link:hover {
            color: red !important;
        }
        .navbar-brand {
            color:black !important;
            font-size: 20px;
            font-family: Arial;
            padding-left: 36px;
            background-image: linear-gradient(to left, rgb(214, 202, 225), rgb(96, 197, 223));
            background-clip: text;
            color: transparent;
        }
        .text-center{
            margin-top: 80px;

        }
        body {
    font-family: Arial, sans-serif;
}
nav {
    background-color: #818C78;
}
.container {
    padding: 50px 0;
}

h1 {
    font-size: 3rem;
    color: #fff;
}

.course-description {
    font-size: 1.2rem;
    color: #ddd;
}

/* Button Styles */
.btn-danger {

    border: none;

    font-size: 1.1rem;
}

         ul li::after{
            content:'';
            height:2px;
            width:0%;
            background:black;
            display:block;
            margin:auto;
            transition:0.5s;
        }
        ul li:hover::after{
            width:100%;
        }




h2 {
    margin-bottom: -15px;
    color:#343a40;
}

label {
    font-weight: bold;
}

button {
    width: 100%;
    background-color: #4CAF50;
    border: none;
    padding: 10px;
    color: #fff;
    font-size: 1.1rem;
    border-radius: 5px;
}

.hollo {
    max-width: 500px;
    margin: 0 auto;
    background-color:#818C78;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.hh
{
    text-decoration: none;
}
.main {
            width: 100%;
            background:url(./pexels-mahmoud-yahyaoui-30002756.jpg);
            background-position: center;
            background-size: cover;
            min-height: 100vh;
        }


</style>
<body>
    <div class="main">
    <nav class="navbar navbar-expand-lg navbar-light ">
        <a class="navbar-brand" href="#">PetAdoption.in</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <form class="form-inline mx-auto d-none d-lg-flex">
                <input class="form-control mr-sm-2" type="search" placeholder="Type to search" aria-label="Search">
                <button class="btn btn-outline-danger my-2 my-sm-0" type="submit">Search</button>
            </form>

                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#">Adopt</a></li>
                    <li class="nav-item"><a class="nav-link" href="#">Care</a></li>
                    <li class="nav-item"><a class="nav-link" href="#">Stories</a></li>
                    <li class="nav-item"><a class="nav-link" href="#">Contact</a></li>
            </ul>
        </div>
    </nav>
    <div class="container mt-5 hollo">
        <div class="logo-container text-center">
            <i class="fas fa-user-circle form-logo"></i>
        </div>
        <h2 class="text-center">User Login</h2>
        <form>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="text" class="form-control" id="eamil" placeholder="Enter your user ID" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" placeholder="Enter your password" required>
            </div>
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="rememberMe">
                <label class="form-check-label" for="rememberMe">Remember Me</label>
            </div>
            <input type="submit" value="Login" class="btn btn-danger w-100">
        </form>
        <div class="mt-3 text-center hh">
            <a href="#">Forgot Password?</a>
        </div>
        <div class="mt-3 text-center hh">
           Don't have an account? <a href="./uderregistration.html">Register here</a>
        </div>
    </div>
    <header class="hero bg-light text-center py-5">
        <div class="container">
            <h1 style="color:#4CAF50;">Contact us</h1>
            <p style="color:#333;">Have questions or need assistance? Reach out to us through our contact page or follow us on social media for the latest updates and events.</p>
            <a href="#" class="btn btn-danger">Contact us</a>
        </div>
    </header>

</section>
    <footer class="footer  text-white py-4">
        <div class="container ">
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
                        <button type="submit" class="btn btn-danger btn-block">Subscribe</button>
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
</div>


    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
</body>
</html>
""")