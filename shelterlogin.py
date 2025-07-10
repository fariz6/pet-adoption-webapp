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

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shelter Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #6c63ff;
            --secondary-color: #f8f9fa;
            --dark-color: #343a40;
            --light-color: #ffffff;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding-top: 70px;
        }

        /* Navbar Styles */
        .navbar {
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }

        .navbar-brand {
            font-weight: 600;
            color: var(--primary-color) !important;
            font-size: 1.5rem;
        }

        .navbar-brand i {
            margin-right: 8px;
        }

        .nav-link {
            color: var(--dark-color) !important;
            font-weight: 500;
            padding: 8px 15px;
            margin: 0 2px;
            border-radius: 5px;
            transition: all 0.3s;
        }

        .nav-link:hover, .nav-link.active {
            background-color: var(--primary-color);
            color: white !important;
        }

        /* Login Container */
        .login-container {
            max-width: 500px;
            margin: 50px auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .login-header {
            background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }

        .login-header i {
            font-size: 3rem;
            margin-bottom: 15px;
        }

        .login-body {
            padding: 30px;
        }

        .form-control {
            border-radius: 8px;
            padding: 12px 15px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s;
        }

        .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.25rem rgba(108, 99, 255, 0.25);
        }

        .btn-login {
            background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%);
            border: none;
            padding: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s;
        }

        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3);
        }

        .login-links a {
            color: var(--primary-color);
            text-decoration: none;
            transition: all 0.3s;
        }

        .login-links a:hover {
            text-decoration: underline;
        }

        /* Footer Styles */
        .footer {
            background-color: var(--dark-color);
            color: white;
            padding: 40px 0;
        }

        .footer-logo {
            font-weight: 600;
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }

        .footer-links h5 {
            color: white;
            margin-bottom: 20px;
            font-size: 1.2rem;
        }

        .footer-links ul {
            list-style: none;
            padding: 0;
        }

        .footer-links li {
            margin-bottom: 10px;
        }

        .footer-links a {
            color: #adb5bd;
            text-decoration: none;
            transition: all 0.3s;
        }

        .footer-links a:hover {
            color: white;
            padding-left: 5px;
        }

        .copyright {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 20px;
            margin-top: 30px;
            color: #adb5bd;
            font-size: 0.9rem;
        }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .login-container {
                margin: 30px auto;
                border-radius: 10px;
            }

            .login-body {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw"></i> PetAdoption
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Adopt</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Care</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Stories</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Contact</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Shelter Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="sheltereg.py">Shelter Register</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Login Form -->
    <div class="login-container">
        <div class="login-header">
            <i class="fas fa-home"></i>
            <h2>Shelter Login</h2>
            <p>Welcome back to PetAdoption Shelter Portal</p>
        </div>

        <div class="login-body">
            <form method="post">
                <div class="mb-4">
                    <label for="email" class="form-label">Email Address</label>
                    <input type="email" class="form-control" id="email" name="email" placeholder="your@email.com" required>
                </div>

                <div class="mb-4">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="pass" placeholder="••••••••" required>
                </div>

                <div class="mb-4 form-check">
                    <input type="checkbox" class="form-check-input" id="rememberMe">
                    <label class="form-check-label" for="rememberMe">Remember me</label>
                </div>

                <input type="submit" name="register" value="Login" class="btn btn-login w-100">
            </form>

            <div class="mt-4 text-center login-links">
                <a href="#" data-bs-toggle="modal" data-bs-target="#forgotPasswordModal">Forgot Password?</a>
                <span class="mx-2">|</span>
                <a href="./sheltereg.py">Create Shelter Account</a>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 mb-4">
                    <a href="#" class="footer-logo"><i class="fas fa-paw me-2"></i>PetAdoption</a>
                    <p>Helping pets find loving homes since 2010. Our mission is to connect animals in need with caring families.</p>
                    <div class="social-icons mt-3">
                        <a href="#"><i class="fab fa-facebook-f"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
                <div class="col-lg-2 col-md-6 mb-4">
                    <div class="footer-links">
                        <h5>Quick Links</h5>
                        <ul>
                            <li><a href="#">Home</a></li>
                            <li><a href="#">Adopt</a></li>
                            <li><a href="#">Care</a></li>
                            <li><a href="#">Stories</a></li>
                            <li><a href="#">Contact</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="footer-links">
                        <h5>Resources</h5>
                        <ul>
                            <li><a href="#">Pet Care</a></li>
                            <li><a href="#">Training Tips</a></li>
                            <li><a href="#">Pet Health</a></li>
                            <li><a href="#">FAQ</a></li>
                            <li><a href="#">Blog</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="footer-links">
                        <h5>Contact Us</h5>
                        <ul>
                            <li><i class="fas fa-map-marker-alt me-2"></i> 123 Pet Street, Pet City, PC 12345</li>
                            <li><i class="fas fa-phone me-2"></i> +1 (555) 123-4567</li>
                            <li><i class="fas fa-envelope me-2"></i> info@petadoption.com</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="copyright text-center">
                <p>&copy; 2023 PetAdoption. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Forgot Password Modal -->
    <div class="modal fade" id="forgotPasswordModal" tabindex="-1" aria-labelledby="forgotPasswordModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header" style="background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%); color: white;">
                    <h5 class="modal-title" id="forgotPasswordModalLabel"><i class="fas fa-key me-2"></i>Reset Password</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Enter your email address and we'll send you a link to reset your password.</p>
                    <form method="post">
                        <div class="mb-3">
                            <label for="forgotEmail" class="form-label">Email address</label>
                            <input type="email" class="form-control" id="forgotEmail" name="email" required>
                        </div>
                        <div class="d-grid gap-2">
                            <input type="submit" name="send" class="btn btn-primary" style="background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%); border: none;">Send Reset Link</button>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

form = cgi.FieldStorage()
Email = form.getvalue("email")  # Email
Password = form.getvalue("pass")  # Password
Submit = form.getvalue("register")
if Submit != None:
    q = """select shelter_id from shelter_info where email="%s" and pass="%s" """ % (Email, Password)
    cur.execute(q)
    res = cur.fetchone()
    if res != None:
        print(""" 
        <script>
        alert("Logged in successfully")
        location.href="newshelterdash.py?shelter_id=%s"
        </script>
        """ % (res[0]))
    else:
        print("""
        <script>
        alert("Incorrect email or password")
        location.href="shelterlogin.py"
        </script>
        """)

Emails = form.getvalue("email")
Send = form.getvalue("send")
if Send != None:
    d = """ select * from shelter_info where email='%s' """ % (Emails)
    cur.execute(d)
    hello = cur.fetchall()
    for j in hello:
        Password = j[10]
        Fname = j[2]

        fromadd = 'farizfreakin@gmail.com'
        ppassword = 'wmmb jmwm uury cnwc'
        toadd = Emails
        Subject = "Your Password"
        body = """Hello %s, your password is %s""" % (Fname, Password)
        msg = """Subject: {} \n\n{}""".format(Subject, body)
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(fromadd, ppassword)
        server.sendmail(fromadd, toadd, msg)
        server.quit()
        print("""
             <script>
             alert("Mail sent Successfully");
             </script>
               """)