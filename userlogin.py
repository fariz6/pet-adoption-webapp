#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import smtplib


cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

# HTML Form

print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetAdoption - Login</title>
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
            color: #333;
            padding-top: 70px; /* For fixed navbar */
        }
        
        /* Navbar - Matching Registration Page */
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
        
        .navbar-toggler {
            border: none;
        }
        
        .search-box {
            margin-left: auto;
            margin-right: 20px;
        }
        
        .search-box .form-control {
            border-radius: 8px;
            padding: 8px 15px;
            border: 1px solid #e0e0e0;
        }
        
        .search-box .btn {
            background-color: var(--primary-color);
            color: white;
            border-radius: 8px;
            padding: 8px 15px;
            transition: all 0.3s;
        }
        
        .search-box .btn:hover {
            background-color: #5a52d5;
        }

        /* Login Form */
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            padding: 30px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .login-header i {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 10px;
        }
        
        .login-header h2 {
            font-size: 1.5rem;
            color: var(--dark-color);
            margin-bottom: 5px;
        }
        
        .login-header p {
            color: #6c757d;
            font-size: 0.9rem;
        }
        
        .form-control {
            height: 45px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(108, 99, 255, 0.15);
        }
        
        .btn-login {
            background-color: var(--primary-color);
            border: none;
            padding: 10px;
            font-weight: 500;
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .btn-login:hover {
            background-color: #5a52d5;
            transform: translateY(-2px);
        }
        
        .login-links {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9rem;
        }
        
        .login-links a {
            color: var(--primary-color);
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .login-links a:hover {
            text-decoration: underline;
        }
        
        .separator {
            color: #dee2e6;
            margin: 0 10px;
        }
        
        /* Footer */
        .footer {
            background-color: var(--dark-color);
            color: white;
            padding: 40px 0 20px;
        }
        
        .footer-logo {
            font-weight: 600;
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }
        
        .footer h5 {
            font-size: 1.1rem;
            margin-bottom: 15px;
        }
        
        .footer ul {
            list-style: none;
            padding: 0;
        }
        
        .footer ul li {
            margin-bottom: 8px;
        }
        
        .footer a {
            color: #adb5bd;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .footer a:hover {
            color: white;
            padding-left: 5px;
        }
        
        .newsletter-form .form-control {
            height: 40px;
            margin-bottom: 10px;
        }
        
        .newsletter-form .btn {
            background-color: var(--primary-color);
            border: none;
        }
        
        .copyright {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 20px;
            margin-top: 30px;
            font-size: 0.85rem;
            color: #adb5bd;
        }
        
        @media (max-width: 768px) {
            .login-container {
                margin: 30px auto;
                padding: 25px;
            }
            
            .footer .col-md-4 {
                margin-bottom: 30px;
            }
            
            .search-box {
                margin: 10px 0;
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- Navbar Matching Registration Page -->
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw"></i> PetAdoption
            </a>
            
            <div class="search-box d-flex">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn" type="submit">
                    <i class="fas fa-search"></i>
                </button>
            </div>
            
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
                        <a class="nav-link active" href="#">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="useregistration.py">Register</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Login Form -->
    <div class="container">
        <div class="login-container">
            <div class="login-header">
                <i class="fas fa-user-circle"></i>
                <h2>Welcome back to PetAdoption</h2>
            </div>
            
            <form method="post">
                <div class="mb-3">
                    <label for="email" class="form-label">Email Address</label>
                    <input type="email" class="form-control" id="email" name="email" placeholder="your@email.com" required>
                </div>
                
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="pass" placeholder="••••••••" required>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="rememberMe">
                    <label class="form-check-label" for="rememberMe">Remember me</label>
                </div>
                
                <input type="submit" value="Login" name="register" class="btn btn-login w-100">
            </form>
            
            <div class="login-links">
                <a href="#" data-bs-toggle="modal" data-bs-target="#forgotPasswordModal">Forgot Password?</a>
                <span class="separator">|</span>
                <a href="./useregistration.py">Create Account</a>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="footer-logo"><i class="fas fa-paw"></i> PetAdoption</div>
                    <p>Helping pets find loving homes since 2010. Our mission is to connect animals in need with caring families.</p>
                </div>
                <div class="col-md-2 mb-4">
                    <h5>Quick Links</h5>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Adopt</a></li>
                        <li><a href="#">Care</a></li>
                        <li><a href="#">Stories</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div class="col-md-3 mb-4">
                    <h5>Recent Blog Posts</h5>
                    <ul>
                        <li><a href="#">Browse our adoption gallery</a></li>
                        <li><a href="#">Fill out an adoption application</a></li>
                        <li><a href="#">Meet-and-greet process</a></li>
                        <li><a href="#">Adoption success stories</a></li>
                    </ul>
                </div>
                <div class="col-md-3 mb-4">
                    <h5>Newsletter</h5>
                    <p>Subscribe for updates on new pets and events.</p>
                    <form class="newsletter-form">
                        <input type="email" class="form-control" placeholder="Your email">
                        <button type="submit" class="btn btn-primary w-100 mt-2">Subscribe</button>
                    </form>
                </div>
            </div>
            <div class="copyright text-center">
                <p>&copy; 2023 PetAdoption. All rights reserved.</p>
            </div>
        </div>
    </footer>
    <div class="modal fade" id="forgotPasswordModal" tabindex="-1" aria-labelledby="forgotPasswordModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header" style="background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%); color: white; border-top-left-radius: 10px; border-top-right-radius: 10px;">
                <h5 class="modal-title" id="forgotPasswordModalLabel"><i class="fas fa-key me-2"></i>Reset Password</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body p-4">
                <p class="mb-4">Enter your email address and we'll send you a link to reset your password.</p>
                <form method="post">
                    <div class="mb-3">
                        <label for="forgotEmail" class="form-label">Email Address</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                            <input type="email" class="form-control" id="forgotEmail" name="Email" placeholder="your@email.com" required>
                        </div>
                    </div>
                    <div class="d-grid gap-2">
                        <input type="submit" name="send" class="btn btn-primary" style="background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%); border: none; padding: 10px; border-radius: 8px;">
                            
                        
                    </div>
                </form>
            </div>
            <div class="modal-footer" style="border-top: none; justify-content: center; padding-bottom: 20px;">
                <p class="text-muted small mb-0">Didn't receive an email? <a href="#" style="color: #6c63ff;">Resend</a></p>
            </div>
        </div>
    </div>
</div>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")
form=cgi.FieldStorage()
Email = form.getvalue("email")  # Email
Password = form.getvalue("pass")  # Password
Submit = form.getvalue("register")
if Submit != None:
    q = """select id from usereg where email="%s" and pass="%s" """ % (Email, Password)
    cur.execute(q)
    res = cur.fetchone()
    if res != None:
        print(""" 
        <script>
        alert("logined successfully")
        location.href="deepseeek.py?id=%s"
        </script>
        """ % (res[0]))
    else:
        print("""
        <script>
        alert("incorrect email or passwprd")
        location.href="userlogin.py"
        </script>
        """)

Emails = form.getvalue("Email")
Send = form.getvalue("send")
if Send != None:
    d=""" select * from usereg where email='%s' """%(Emails)
    cur.execute(d)
    hello=cur.fetchall()
    for j in hello:
        Password=j[4]
        Fname=j[1]


        fromadd = 'farizfreakin@gmail.com'
        ppassword= 'wmmb jmwm uury cnwc'
        toadd=Emails
        Subject=" your Password"
        body="""hello %s your password is %s""" %(Fname,Password)
        msg="""Subject: {} \n\n{}""".format(Subject,body)
        server=smtplib.SMTP("smtp.gmail.com:587")
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