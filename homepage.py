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
print("""
     <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - Find Your Perfect Pet Companion</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="styles.css">
</head>
<style>
    :root {
    --bs-primary: #4e73df;
    --bs-purple: #6f42c1;
    --bs-brown: #795548;
    --bs-light: #f8f9fa;
}

.bg-purple {
    background-color: var(--bs-purple) !important;
}

.bg-brown {
    background-color: var(--bs-brown) !important;
}

.text-purple {
    color: var(--bs-purple) !important;
}

/* Hero Section */
.hero-section {
    position: relative;
    padding: 150px 0;
    background-color:black;
    min-height: 8a0vh;
    width: 100%;
    color: white;
    display: flex;
    align-items: center;
    margin: 0;
    padding: 0;
}

.hero-content {
    position: relative;
    z-index: 2;
    width: 100%;
    padding: 0 15px;
}

.hero-section h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.hero-section p {
    font-size: 1.25rem;
    margin-bottom: 2rem;
}

.hero-buttons .btn {
    padding: 0.75rem 1.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    margin-right: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color: white;
    border-color: white;
    color: var(--bs-purple);
}

.btn-primary:hover {
    background-color: rgba(255, 255, 255, 0.9);
    border-color: rgba(255, 255, 255, 0.9);
    transform: translateY(-2px);
}

.btn-outline-light {
    border-width: 2px;
    color: white;
    border-color: white;
}

.btn-outline-light:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

/* Responsive adjustments */
@media (max-width: 992px) {
    .hero-section {
        padding: 100px 0;
        text-align: center;
    }
    
    .hero-section h1 {
        font-size: 2.5rem;
    }
    
    .hero-buttons {
        justify-content: center;
    }
}

@media (max-width: 768px) {
    .hero-section {
        padding: 80px 0;
    }
    
    .hero-section h1 {
        font-size: 2rem;
    }
    
    .hero-section p {
        font-size: 1rem;
    }
    
    .hero-buttons .btn {
        display: block;
        width: 100%;
        margin-right: 0;
        margin-bottom: 1rem;
    }
}
/* Pet Cards */
.pet-card {
    border: none;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.pet-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.pet-image-placeholder {
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

.pet-image-placeholder i {
    font-size: 5rem;
}

/* How It Works */
.how-it-works-card {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    height: 100%;
    transition: transform 0.3s ease;
}

.how-it-works-card:hover {
    transform: translateY(-5px);
}

.step-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
    margin: 0 auto 15px;
}

/* Testimonials */
.testimonial-card {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.testimonial-icon {
    color: var(--bs-primary);
}

.testimonial-author-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

/* Custom Button */
.btn-primary {
    background-color: var(--bs-primary);
    border-color: var(--bs-primary);
}

.btn-primary:hover {
    background-color: #3a5ccc;
    border-color: #3a5ccc;
}

.btn-outline-primary {
    color: var(--bs-primary);
    border-color: var(--bs-primary);
}

.btn-outline-primary:hover {
    background-color: var(--bs-primary);
    border-color: var(--bs-primary);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .hero-section {
        padding: 60px 0;
        text-align: center;
    }
    
    .hero-section .d-flex {
        justify-content: center;
    }
}
/* Login Modal Styles */
.login-option-card {
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid transparent;
}

.login-option-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.1);
}

.login-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  font-size: 24px;
  color: white;
}

/* Background colors for each login option */
.bg-light-blue {
  background-color: #f0f5ff;
}
.bg-light-blue .login-icon {
  background-color: var(--bs-primary);
}

.bg-light-purple {
  background-color: #f8f0ff;
}
.bg-light-purple .login-icon {
  background-color: var(--bs-purple);
}

.bg-light-green {
  background-color: #f0fff4;
}
.bg-light-green .login-icon {
  background-color: #28a745;
}

.bg-light-orange {
  background-color: #fff8f0;
}
.bg-light-orange .login-icon {
  background-color: #fd7e14;
}

/* Modal customizations */
.modal-content {
  border-radius: 15px;
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.modal-header .btn-close {
  font-size: 0.8rem;
  padding: 0.5rem;
  margin: -0.5rem -0.5rem -0.5rem auto;
}
/* ======================
   LOGIN MODAL STYLES 
   ====================== */

/* Base Modal Styling */
/* Admin Login Modal Specific Styles */
#adminLoginModal .modal-content {
  border-radius: 12px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

#adminLoginModal .modal-header {
  border-bottom: none;
  padding: 1.5rem 1.5rem 0;
  position: relative;
}

#adminLoginModal .modal-title {
  font-weight: 700;
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 0;
}

#adminLoginModal .modal-body {
  padding: 1.5rem;
}

#adminLoginModal .form-label {
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.5rem;
  display: block;
}

#adminLoginModal .form-control {
  height: 48px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  margin-bottom: 1.25rem;
  transition: all 0.2s;
}

#adminLoginModal .form-control:focus {
  border-color: #4e73df;
  box-shadow: 0 0 0 3px rgba(78, 115, 223, 0.1);
}

#adminLoginModal .form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

#adminLoginModal .form-check {
  display: flex;
  align-items: center;
}

#adminLoginModal .form-check-input {
  width: 1.1em;
  height: 1.1em;
  margin-top: 0;
  margin-right: 0.5rem;
  border: 1px solid #cbd5e0;
}

#adminLoginModal .form-check-label {
  color: #4a5568;
  font-size: 0.9rem;
}

#adminLoginModal .forgot-password {
  color: #4e73df;
  font-size: 0.9rem;
  text-decoration: none;
}

#adminLoginModal .forgot-password:hover {
  text-decoration: underline;
}

#adminLoginModal .login-btn {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  background-color: #4e73df;
  border: none;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
}

#adminLoginModal .login-btn:hover {
  background-color: #3a5ccc;
  transform: translateY(-1px);
}

#adminLoginModal .signup-link {
  text-align: center;
  color: #718096;
  font-size: 0.9rem;
}

#adminLoginModal .signup-link a {
  color: #4e73df;
  font-weight: 600;
  text-decoration: none;
}

#adminLoginModal .signup-link a:hover {
  text-decoration: underline;
}

/* Decorative elements */
#adminLoginModal .modal-header::after {
  content: "";
  display: block;
  width: 50px;
  height: 3px;
  background-color: #4e73df;
  margin-top: 1rem;
  border-radius: 3px;
}

#adminLoginModal .admin-icon {
  position: absolute;
  right: 1.5rem;
  top: 1.5rem;
  color: #4e73df;
  opacity: 0.1;
  font-size: 3rem;
}
#userLoginModal {
  --primary-color: #4e73df;
  --primary-dark: #3a5ccc;
}

#userLoginModal .modal-icon {
  color: #4e73df;
}





/* Animation for modal entry */
@keyframes modalEntry {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-login.fade .modal-dialog {
  animation: modalEntry 0.3s ease-out;
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .modal-login .modal-header {
    padding: 1.25rem 1.25rem 0.5rem;
  }
  
  .modal-login .modal-body {
    padding: 0 1.25rem 1.25rem;
  }
  
  .modal-login .modal-icon {
    font-size: 2.5rem;
    right: 1.25rem;
    top: 1.25rem;
  }
}
/* Shelter Login Modal Specific Styles */
.shelter-modal {
  border-radius: 12px;
  border: none;
  box-shadow: 0 5px 20px rgba(78, 115, 223, 0.2);
}

.shelter-modal-header {
  background-color: #4e73df;
  color: white;
  border-radius: 10px 10px 0 0 !important;
  border-bottom: none;
  padding: 1.5rem;
  position: relative;
}

.shelter-modal-header .modal-title {
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0;
}

.shelter-modal-header .modal-icon {
  position: absolute;
  right: 1.5rem;
  top: 1.5rem;
  font-size: 3rem;
  opacity: 0.1;
}

.shelter-login-btn {
  background-color: #4e73df;
  border: none;
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  transition: all 0.2s;
}

.shelter-login-btn:hover {
  background-color: #3a5ccc;
  transform: translateY(-1px);
}

.shelter-modal .forgot-password {
  color: #4e73df;
  font-size: 0.9rem;
  text-decoration: none;
}

.shelter-modal .forgot-password:hover {
  text-decoration: underline;
}
/* Care Resource Login Modal Specific Styles */
.care-modal {
  border-radius: 12px;
  border: none;
  box-shadow: 0 5px 20px rgba(28, 200, 138, 0.2);
}

.care-modal-header {
  background-color: #1cc88a;
  color: white;
  border-radius: 10px 10px 0 0 !important;
  border-bottom: none;
  padding: 1.5rem;
  position: relative;
}

.care-modal-header .modal-title {
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0;
}

.care-modal-header .modal-icon {
  position: absolute;
  right: 1.5rem;
  top: 1.5rem;
  font-size: 3rem;
  opacity: 0.1;
}

.care-login-btn {
  background-color: #1cc88a;
  border: none;
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  transition: all 0.2s;
}

.care-login-btn:hover {
  background-color: #17a673;
  transform: translateY(-1px);
}

.care-modal .forgot-password {
  color: #1cc88a;
  font-size: 0.9rem;
  text-decoration: none;
}

.care-modal .forgot-password:hover {
  text-decoration: underline;
}
/* User Login Modal Specific Styles */
#userLoginModal .modal-content {
  border-radius: 18px;
  border: none;
  box-shadow: 0 8px 32px rgba(78, 115, 223, 0.18);
  background: linear-gradient(135deg, #f0f4ff 0%, #e6eaff 100%);
}

#userLoginModal .modal-header {
  background: linear-gradient(90deg, #4e73df 60%, #6f42c1 100%);
  color: #fff;
  border-radius: 18px 18px 0 0 !important;
  border-bottom: none;
}

#userLoginModal .modal-title {
  font-weight: 700;
  font-size: 1.6rem;
  letter-spacing: 0.5px;
}

#userLoginModal .form-control {
  border-radius: 10px;
  border: 1px solid #d1d9f0;
  background: #f8faff;
}

#userLoginModal .form-control:focus {
  border-color: #4e73df;
  box-shadow: 0 0 0 2px #4e73df33;
}

#userLoginModal .form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

#userLoginModal .form-check {
  display: flex;
  align-items: center;
}

#userLoginModal .form-check-input {
  width: 1.1em;
  height: 1.1em;
  margin-top: 0;
  margin-right: 0.5rem;
  border: 1px solid #cbd5e0;
}

#userLoginModal .form-check-label {
  color: #4a5568;
  font-size: 0.9rem;
}

#userLoginModal .forgot-password {
  color: #4e73df;
  font-size: 0.9rem;
  text-decoration: none;
}

#userLoginModal .forgot-password:hover {
  text-decoration: underline;
}

#userLoginModal .login-btn {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  background: linear-gradient(90deg, #4e73df 60%, #6f42c1 100%);
  border: none;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
}

#userLoginModal .login-btn:hover {
  background: #3a5ccc;
}

#userLoginModal .signup-link {
  text-align: center;
  color: #718096;
  font-size: 0.9rem;
}

#userLoginModal .signup-link a {
  color: #4e73df;
  font-weight: 600;
  text-decoration: none;
}

#userLoginModal .signup-link a:hover {
  text-decoration: underline;
}

/* Decorative elements */
#userLoginModal .modal-header::after {
  content: "";
  display: block;
  width: 50px;
  height: 3px;
  background-color: white;
  margin-top: 1rem;
  border-radius: 3px;
}

#userLoginModal .user-icon {
  position: absolute;
  right: 1.5rem;
  top: 1.5rem;
  color: white;
  opacity: 0.1;
  font-size: 3rem;
}
/* Why Adopt Section */
.benefit-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 12px;
}

.benefit-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.benefit-icon {
    width: 70px;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.benefit-card:hover .benefit-icon {
    transform: scale(1.1);
}

/* Stats Counter */
.display-5 {
    font-size: 2.5rem;
}

@media (max-width: 768px) {
    .display-5 {
        font-size: 2rem;
    }
}

/* LOGIN MODALS ENHANCED STYLES */
#userLoginModal .modal-content {
  border-radius: 18px;
  border: none;
  box-shadow: 0 8px 32px rgba(78, 115, 223, 0.18);
  background: linear-gradient(135deg, #f0f4ff 0%, #e6eaff 100%);
}
#userLoginModal .modal-header {
  background: linear-gradient(90deg, #4e73df 60%, #6f42c1 100%);
  color: #fff;
  border-radius: 18px 18px 0 0 !important;
  border-bottom: none;
}
#userLoginModal .btn-primary {
  background: linear-gradient(90deg, #4e73df 60%, #6f42c1 100%);
  border: none;
}
#userLoginModal .btn-primary:hover {
  background: #3a5ccc;
}
#userLoginModal .modal-title {
  font-weight: 700;
  font-size: 1.6rem;
  letter-spacing: 0.5px;
}
#userLoginModal .form-control {
  border-radius: 10px;
  border: 1px solid #d1d9f0;
  background: #f8faff;
}
#userLoginModal .form-control:focus {
  border-color: #4e73df;
  box-shadow: 0 0 0 2px #4e73df33;
}
#userLoginModal .signup-link a {
  color: #4e73df;
}

#shelterLoginModal .modal-content {
  border-radius: 18px;
  border: none;
  box-shadow: 0 8px 32px rgba(111, 66, 193, 0.18);
  background: linear-gradient(135deg, #f8f0ff 0%, #ede7f6 100%);
}
#shelterLoginModal .modal-header {
  background: linear-gradient(90deg, #6f42c1 60%, #4e73df 100%);
  color: #fff;
  border-radius: 18px 18px 0 0 !important;
  border-bottom: none;
}
#shelterLoginModal .login-btn {
  background: linear-gradient(90deg, #6f42c1 60%, #4e73df 100%);
  border: none;
}
#shelterLoginModal .login-btn:hover {
  background: #4e73df;
}
#shelterLoginModal .modal-title {
  font-weight: 700;
  font-size: 1.6rem;
  letter-spacing: 0.5px;
}
#shelterLoginModal .form-control {
  border-radius: 10px;
  border: 1px solid #d1d9f0;
  background: #f8faff;
}
#shelterLoginModal .form-control:focus {
  border-color: #6f42c1;
  box-shadow: 0 0 0 2px #6f42c133;
}
#shelterLoginModal .signup-link a {
  color: #6f42c1;
}

#careLoginModal .modal-content {
  border-radius: 18px;
  border: none;
  box-shadow: 0 8px 32px rgba(40, 167, 69, 0.18);
  background: linear-gradient(135deg, #f0fff4 0%, #e6fff7 100%);
}
#careLoginModal .modal-header {
  background: linear-gradient(90deg, #28a745 60%, #4e73df 100%);
  color: #fff;
  border-radius: 18px 18px 0 0 !important;
  border-bottom: none;
}
#careLoginModal .login-btn {
  background: linear-gradient(90deg, #28a745 60%, #4e73df 100%);
  border: none;
}
#careLoginModal .login-btn:hover {
  background: #218838;
}
#careLoginModal .modal-title {
  font-weight: 700;
  font-size: 1.6rem;
  letter-spacing: 0.5px;
}
#careLoginModal .form-control {
  border-radius: 10px;
  border: 1px solid #b2f2dd;
  background: #f8faff;
}
#careLoginModal .form-control:focus {
  border-color: #28a745;
  box-shadow: 0 0 0 2px #28a74533;
}
#careLoginModal .signup-link a {
  color: #28a745;
}

#adminLoginModal .modal-content {
  border-radius: 18px;
  border: none;
  box-shadow: 0 8px 32px rgba(253, 126, 20, 0.18);
  background: linear-gradient(135deg, #fff8f0 0%, #fff3e6 100%);
}
#adminLoginModal .modal-header {
  background: linear-gradient(90deg, #fd7e14 60%, #4e73df 100%);
  color: #fff;
  border-radius: 18px 18px 0 0 !important;
  border-bottom: none;
}
#adminLoginModal .login-btn {
  background: linear-gradient(90deg, #fd7e14 60%, #4e73df 100%);
  border: none;
}
#adminLoginModal .login-btn:hover {
  background: #e8590c;
}
#adminLoginModal .modal-title {
  font-weight: 700;
  font-size: 1.6rem;
  letter-spacing: 0.5px;
}
#adminLoginModal .form-control {
  border-radius: 10px;
  border: 1px solid #ffe5d0;
  background: #f8faff;
}
#adminLoginModal .form-control:focus {
  border-color: #fd7e14;
  box-shadow: 0 0 0 2px #fd7e1433;
}
#adminLoginModal .signup-link a {
  color: #fd7e14;
}
/* User Login Modal */
#userLoginModal .forgot-password,
#userLoginModal .signup-link a {
  text-decoration: none !important;
}

/* Shelter Login Modal */
#shelterLoginModal .forgot-password,
#shelterLoginModal .signup-link a {
  text-decoration: none !important;
}

/* Care Resource Login Modal */
#careLoginModal .forgot-password,
#careLoginModal .signup-link a {
  text-decoration: none !important;
}

/* Admin Login Modal */
#adminLoginModal .forgot-password,
#adminLoginModal .signup-link a {
  text-decoration: none !important;
}
/* Remove the bar from User Login Modal */
#userLoginModal .modal-header::after {
  display: none !important;
}

/* Remove the bar from Care Resource Login Modal */
#careLoginModal .modal-header::after {
  display: none !important;
}
/* Remove the bar from Care Resource Login Modal */
#adminLoginModal .modal-header::after {
  display: none !important;
}
</style>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
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
                        <a class="nav-link" href="#how-it-works">Adoption Process</a>
                    </li>
                   
                   
                </ul>
                <button class="btn btn-outline-light ms-lg-3" data-bs-toggle="modal" data-bs-target="#loginModal">Login/Signup</button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section" id="hero">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="hero-content">
                        <h1>Find Your Perfect Pet Companion</h1>
                        <p class="lead">PetMatch connects loving homes with animals in need. Browse our pets waiting for their forever homes.</p>
                        <div class="d-flex flex-wrap hero-buttons">
                            <a href="#" class="btn btn-primary btn-lg" data-bs-toggle="modal" data-bs-target="#userLoginModal">Browse Pets</a>
                            <a href="#how-it-works" class="btn btn-outline-light btn-lg">How It Works</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

   <!-- Why Adopt? Section -->
<section class="py-5 bg-light" id="browse-pets">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="fw-bold">Why Adopt a Pet?</h2>
            <p class="text-muted">Discover the joys and benefits of pet adoption</p>
        </div>
        <div class="row g-4">
            <!-- Benefit 1 -->
            <div class="col-md-6 col-lg-3">
                <div class="card benefit-card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="benefit-icon bg-primary bg-opacity-10 text-primary rounded-circle mx-auto mb-4">
                            <i class="fas fa-heart fa-2x"></i>
                        </div>
                        <h5 class="card-title">Save a Life</h5>
                        <p class="card-text">You give an animal a second chance at life and free up space for shelters to help more pets.</p>
                    </div>
                </div>
            </div>
            
            <!-- Benefit 2 -->
            <div class="col-md-6 col-lg-3">
                <div class="card benefit-card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="benefit-icon bg-success bg-opacity-10 text-success rounded-circle mx-auto mb-4">
                            <i class="fas fa-dollar-sign fa-2x"></i>
                        </div>
                        <h5 class="card-title">Cost Effective</h5>
                        <p class="card-text">Adoption fees are typically much lower than buying from breeders or pet stores.</p>
                    </div>
                </div>
            </div>
            
            <!-- Benefit 3 -->
            <div class="col-md-6 col-lg-3">
                <div class="card benefit-card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="benefit-icon bg-warning bg-opacity-10 text-warning rounded-circle mx-auto mb-4">
                            <i class="fas fa-stethoscope fa-2x"></i>
                        </div>
                        <h5 class="card-title">Health Benefits</h5>
                        <p class="card-text">Pets reduce stress, lower blood pressure, and provide companionship.</p>
                    </div>
                </div>
            </div>
            
            <!-- Benefit 4 -->
            <div class="col-md-6 col-lg-3">
                <div class="card benefit-card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="benefit-icon bg-info bg-opacity-10 text-info rounded-circle mx-auto mb-4">
                            <i class="fas fa-home fa-2x"></i>
                        </div>
                        <h5 class="card-title">Ready for Home</h5>
                        <p class="card-text">Most shelter pets are already house-trained and socialized.</p>
                    </div>
                </div>
            </div>
        </div>
        
       
</section>

    <!-- How It Works -->
    <section class="py-5" id="how-it-works">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="fw-bold">How PetMatch Works</h2>
                <p class="text-muted">Our simple 4-step adoption process</p>
            </div>
            <div class="row g-4">
                <div class="col-md-6 col-lg-3">
                    <div class="how-it-works-card text-center p-4">
                        <div class="step-number bg-primary">1</div>
                        <i class="fas fa-search fa-3x text-primary mb-3"></i>
                        <h4>Browse Pets</h4>
                        <p>Search our database of adorable pets waiting for their forever homes.</p>
                    </div>
                </div>
                <div class="col-md-6 col-lg-3">
                    <div class="how-it-works-card text-center p-4">
                        <div class="step-number bg-primary">2</div>
                        <i class="fas fa-heart fa-3x text-primary mb-3"></i>
                        <h4>Apply to Adopt</h4>
                        <p>Fill out our simple adoption application for the pet you love.</p>
                    </div>
                </div>
                <div class="col-md-6 col-lg-3">
                    <div class="how-it-works-card text-center p-4">
                        <div class="step-number bg-primary">3</div>
                        <i class="fas fa-handshake fa-3x text-primary mb-3"></i>
                        <h4>Meet & Greet</h4>
                        <p>Meet your potential new pet to ensure it's the perfect match.</p>
                    </div>
                </div>
                <div class="col-md-6 col-lg-3">
                    <div class="how-it-works-card text-center p-4">
                        <div class="step-number bg-primary">4</div>
                        <i class="fas fa-home fa-3x text-primary mb-3"></i>
                        <h4>Welcome Home</h4>
                        <p>Complete the adoption and bring your new family member home!</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

   

  

    <!-- Footer -->
    <footer class="bg-dark text-white py-4">
        <div class="container">
            <div class="row">
                <div class="col-12 text-center">
                    <h5 class="mb-3"><i class="fas fa-paw me-2"></i>PetMatch</h5>
                    <p class="mb-0">Connecting loving homes with animals in need</p>
                    <p class="mt-3 mb-0">&copy; 2023 PetMatch. All rights reserved.</p>
                </div>
            </div>
        </div>
    </footer>
    <!-- Login/Signup Modal -->
<div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header border-0 pb-0">
          <h5 class="modal-title fw-bold" id="loginModalLabel">Welcome to PetMatch</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body pt-0">
          <p class="text-muted mb-4">Select your account type to continue</p>
          
          <div class="row g-3">
            <!-- User Login -->
            <div class="col-md-6">
              <div class="login-option-card bg-light-blue" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#userLoginModal">
                <div class="login-icon">
                  <i class="fas fa-user"></i>
                </div>
                <h6>User Login</h6>
                <p class="small text-muted">For pet adopters</p>
              </div>
            </div>
            
            <!-- Shelter Login -->
            <div class="col-md-6">
              <div class="login-option-card bg-light-purple" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#shelterLoginModal">
                <div class="login-icon">
                  <i class="fas fa-home"></i>
                </div>
                <h6>Shelter Login</h6>
                <p class="small text-muted">For animal shelters</p>
              </div>
            </div>
            
            <!-- Care Resource Login -->
            <div class="col-md-6">
              <div class="login-option-card bg-light-green" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#careLoginModal">
                <div class="login-icon">
                  <i class="fas fa-heart"></i>
                </div>
                <h6>Care Resource</h6>
                <p class="small text-muted">Vets & caregivers</p>
              </div>
            </div>
            
            <!-- Admin Login -->
            <div class="col-md-6">
              <div class="login-option-card bg-light-orange" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#adminLoginModal">
                <div class="login-icon">
                  <i class="fas fa-lock"></i>
                </div>
                <h6>Admin Login</h6>
                <p class="small text-muted">System administrators</p>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>

  <!-- User Login Modal -->
  <div class="modal fade" id="userLoginModal" tabindex="-1" aria-labelledby="userLoginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="userLoginModalLabel">User Login</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="userEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="userEmail" name="email" placeholder="name@example.com" required>
            </div>
            <div class="mb-3">
              <label for="userPassword" class="form-label">Password</label>
              <input type="password" class="form-control" id="userPassword" name="pass" required>
            </div>
            <div class="form-options">
              <a href="#userForgotPassword" class="forgot-password" data-bs-toggle="modal">Forgot password?</a>
            </div>
            <input type="submit" name="register" value="Login" class="btn btn-primary w-100 py-2 mb-3">
            <div class="signup-link">
              Don't have an account? <a href="useregistration.py">Sign up</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- User Forgot Password Modal -->
  <div class="modal fade" id="userForgotPassword" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Reset Password</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="userResetEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="userResetEmail" name="Email" placeholder="name@example.com" required>
            </div>
            <input type="submit" name="send" value="Send" class="btn btn-primary w-100 py-2">
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Shelter Login Modal -->
  <div class="modal fade" id="shelterLoginModal" tabindex="-1" aria-labelledby="shelterLoginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="shelterLoginModalLabel">Shelter Login</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="shelterEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="shelterEmail" name="email2" placeholder="name@example.com" required>
            </div>
            <div class="mb-3">
              <label for="shelterPassword" class="form-label">Password</label>
              <input type="password" class="form-control" id="shelterPassword" name="pass2"  required>
            </div>
            <div class="form-options">
              <a href="#shelterForgotPassword" class="forgot-password" data-bs-toggle="modal">Forgot password?</a>
            </div>
            <input type="submit" name="register2" value="Login" class="login-btn shelter-login-btn">
            <div class="signup-link">
              Don't have an account? <a href="sheltereg.py">Sign up</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Shelter Forgot Password Modal -->
  <div class="modal fade" id="shelterForgotPassword" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content shelter-modal">
        <div class="modal-header shelter-modal-header">
          <h5 class="modal-title">Reset Password</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="shelterResetEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="shelterResetEmail" name="Email2" placeholder="name@example.com" required>
            </div>
            <input type="submit" name="send2" value="Send" class="login-btn shelter-login-btn">
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Care Resource Login Modal -->
  <div class="modal fade" id="careLoginModal" tabindex="-1" aria-labelledby="careLoginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="careLoginModalLabel">Care Resource Login</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="careEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="careEmail" name="email3" placeholder="name@example.com" required>
            </div>
            <div class="mb-3">
              <label for="carePassword" class="form-label">Password</label>
              <input type="password" class="form-control" id="carePassword" name="pass3" required>
            </div>
            <div class="form-options">
              <a href="#careForgotPassword" class="forgot-password" data-bs-toggle="modal">Forgot password?</a>
            </div>
            <input type="submit" name="register3" value="Login" class="login-btn care-login-btn">
            <div class="signup-link">
              Don't have an account? <a href="carereg.py">Sign up</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Care Resource Forgot Password Modal -->
  <div class="modal fade" id="careForgotPassword" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content care-modal">
        <div class="modal-header care-modal-header">
          <h5 class="modal-title">Reset Password</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="careResetEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="careResetEmail" name="Email3" placeholder="name@example.com" required>
            </div>
            <input type="submit" name="send3" value="Send" class="login-btn care-login-btn">
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Admin Login Modal -->
  <div class="modal fade" id="adminLoginModal" tabindex="-1" aria-labelledby="adminLoginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="adminLoginModalLabel">Admin Login</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="adminEmail" class="form-label">Admin Id</label>
              <input type="text"  name="email4" class="form-control" id="adminEmail" placeholder="example123">
            </div>
            <div class="mb-3">
              <label for="adminPassword" class="form-label">Password</label>
              <input type="password" name="pass4" class="form-control" id="adminPassword">
            </div>
            
            <input type="submit" value="Login"name="save4" class="login-btn">
            
          </form>
        </div>
      </div>
    </div>
  </div>
   <div class="modal fade" id="Password" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content care-modal">
        <div class="modal-header care-modal-header">
          <h5 class="modal-title">Reset Password</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form method="post">
            <div class="mb-3">
              <label for="careResetEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="careResetEmail" name="Email4" placeholder="name@example.com" required>
            </div>
            <input type="submit" name="send4" value="Send" class="login-btn care-login-btn">
          </form>
        </div>
      </div>
    </div>
  </div>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JS -->
    <script src="script.js">
        document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.how-it-works-card, .pet-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Set initial state for animation
    const animatedElements = document.querySelectorAll('.how-it-works-card, .pet-card');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });

    // Run animation on load and scroll
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);

    // Pet type filter functionality (example)
    document.querySelectorAll('.pet-filter-btn').forEach(button => {
        button.addEventListener('click', function() {
            // This would be expanded to actually filter pets in a real implementation
            document.querySelectorAll('.pet-filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
});
// Update the existing event listener for the login button
document.querySelector('.navbar .btn-outline-light').addEventListener('click', function(e) {
  e.preventDefault();
  var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
  loginModal.show();
});

// You can add similar event listeners for the other modals if needed
// For example:
document.querySelectorAll('.login-option-card').forEach(card => {
  card.addEventListener('click', function() {
    // Animation when a login option is selected
    this.style.transform = 'scale(0.95)';
    setTimeout(() => {
      this.style.transform = 'scale(1)';
    }, 200);
  });
});
    </script>
</body>
</html>
    """)
form=cgi.FieldStorage()
Email1 = form.getvalue("email")  # Email
Password1 = form.getvalue("pass")  # Password
Submit1 = form.getvalue("register")
if Submit1 != None:
    q = """select id from usereg where email="%s" and pass="%s" """ % (Email1, Password1)
    cur.execute(q)
    res = cur.fetchone()
    if res != None:
        print(""" 
        <script>
        alert("logined successfully")
        location.href="newuserdash.py?id=%s"
        </script>
        """ % (res[0]))
    else:
        print("""
        <script>
        alert("incorrect email or passwprd")
        </script>
        """)

Emails1 = form.getvalue("Email")
Send1 = form.getvalue("send")
if Send1 != None:
    d = """SELECT * FROM usereg WHERE email='%s'""" % (Emails1)
    cur.execute(d)
    user_data = cur.fetchone()

    if user_data:  # If email exists in database
        Password = user_data[4]
        name = user_data[1]

        fromadd = 'farizfreakin@gmail.com'
        ppassword = 'trih xamr rooy pbnr'
        toadd = Emails1
        Subject = "Your Password"
        body = """Hello %s, your password is %s""" % (name, Password)
        msg = """Subject: %s \n\n%s""" % (Subject, body)

        try:
            server = smtplib.SMTP("smtp.gmail.com:587")
            server.ehlo()
            server.starttls()
            server.login(fromadd, ppassword)
            server.sendmail(fromadd, toadd, msg)
            server.quit()
            print("""
                <script>
                alert("Password has been sent to your email.");
                </script>
            """)
        except Exception as e:
            print("""
                <script>
                alert("Failed to send email. Please try again later.");
                console.error('Email error: %s');
                </script>
            """ % str(e))
    else:  # If email doesn't exist
        print("""
            <script>
            alert("Email not found in our records. Please check the email address and try again.");
            </script>
        """)
    con.close()

Email2 = form.getvalue("email2")  # Email
Password2 = form.getvalue("pass2")  # Password
Submit2 = form.getvalue("register2")
if Submit2 != None:
    print(Email2)
    print(Password2)
    b = """select shelter_id from shelter_info where email="%s" and pass="%s" """ % (Email2, Password2)
    cur.execute(b)
    result2 = cur.fetchone()
    print(result2)
    if result2 != None:
        print(""" 
        <script>
        alert("logined successfully")
        location.href="newshelterdash.py?shelter_id=%s"
        </script>
        """ % (result2[0]))
    else:
        print("""
        <script>
        alert("incorrect email or passwprd")
        </script>
        """)
        con.close()

Emails2 = form.getvalue("Email2")
Send2 = form.getvalue("send2")
if Send2 != None:
    # First get the shelter_id from shelter_info table
    m = """SELECT shelter_id FROM shelter_info WHERE email='%s'""" % (Emails2)
    cur.execute(m)
    shelter_result = cur.fetchone()
    
    if shelter_result:
        shelter_id = shelter_result[0]
        # Insert into pass table
        insert_pass = """INSERT INTO pass (shelter_id, email, status) VALUES ('%s', '%s', 'pending')""" % (shelter_id, Emails2)
        cur.execute(insert_pass)
        con.commit()
        
        print("""
        <script>
        alert("Password reset request submitted successfully. Please wait for admin approval.");
        </script>
        """)
    else:
        print("""
        <script>
        alert("Email not found in our records");
        </script>
        """)
    con.close()



Email3 = form.getvalue("email3")  # Email
Password3 = form.getvalue("pass3")  # Password
Submit3 = form.getvalue("register3")
if Submit3 != None:
    q = """select careid from careresource_info where mail="%s" and pass="%s" """ % (Email3, Password3)
    cur.execute(q)
    res = cur.fetchone()
    if res != None:
        print(""" 
        <script>
        alert("logined successfully")
        location.href="get_services.py?careid=%s"
        </script>
        """ % (res[0]))
    else:
        print("""
        <script>
        alert("incorrect email or passwprd")
        </script>
        """)
Email3 = form.getvalue("Email3")  # Email
Send3 = form.getvalue("send3")
if Send3 != None:
    # First get the careid from careresource_info table
    k = """SELECT careid FROM careresource_info WHERE mail='%s'""" % (Email3)
    cur.execute(k)
    care_result = cur.fetchone()
    
    if care_result:
        careid = care_result[0]
        # Insert into cpass table
        insert_cpass = """INSERT INTO cpass (careid, email, status) VALUES ('%s', '%s', 'pending')""" % (careid, Email3)
        cur.execute(insert_cpass)
        con.commit()
        
        print("""
        <script>
        alert("Password reset request submitted successfully. Please wait for admin approval.");
        </script>
        """)
    else:
        print("""
        <script>
        alert("Email not found in our records");
        </script>
        """)
    con.close()

Emails3 = form.getvalue("Email3")
Send3 = form.getvalue("send3")
if Send3 != None:
    # First get the careid from careresource_info table
    k = """SELECT careid FROM careresource_info WHERE mail='%s'""" % (Emails3)
    cur.execute(k)
    care_result = cur.fetchone()
    
    if care_result:
        careid = care_result[0]
        # Insert into cpass table
        insert_cpass = """INSERT INTO cpass (careid, email, status) VALUES ('%s', '%s', 'pending')""" % (careid, Emails3)
        cur.execute(insert_cpass)
        con.commit()
        
        print("""
        <script>
        alert("Password reset request submitted successfully. Please wait for admin approval.");
        </script>
        """)
    else:
        print("""
        <script>
        alert("Email not found in our records");
        </script>
        """)
    con.close()

Email4 = form.getvalue("email4")  # Email
Password4 = form.getvalue("pass4")  # Password
Submit4 = form.getvalue("save4")
if Submit4 != None:
    print(Email4)
    print(Password4)
    b = """select admin_id from admin_info where email="%s" and pass="%s" """ % (Email4, Password4)
    cur.execute(b)
    result4 = cur.fetchone()

    if result4 != None:
        print(""" 
        <script>
        alert("logined successfully")
        location.href="admin.py"
        </script>
        """)
    else:
        print("""
        <script>
        alert("incorrect email or passwprd")
        </script>
        """)
        con.close()

Emails4 = form.getvalue("Email4")
Send4 = form.getvalue("send4")
if Send4 != None:
    e=""" select * from admin_info where email='%s' """%(Emails4)
    cur.execute(e)
    hello=cur.fetchall()
    for j in hello:
        Password=j[2]
        sheltername=j[1]


        fromadd = 'farizfreakin@gmail.com'
        ppassword= 'trih xamr rooy pbnr'
        toadd=Emails4
        Subject=" your Password"
        body="""hello admin your email and password is %s and  %s""" %(sheltername,Password)
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
        con.close()
