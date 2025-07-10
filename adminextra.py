#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os
import smtplib
import random
import string

cgitb.enable()
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()


# Function to generate random password
def generate_random_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(8))
    return password


shelter = """SELECT * FROM shelter_info WHERE Status='pending'"""
# Get all shelters from database
cur.execute(shelter)
res = cur.fetchall()
# Process form submissions
if form.getvalue("reject"):
    # Reject action
    shelter_id = form.getvalue("shelter_id")
    c = """UPDATE shelter_info SET status='rejected' WHERE shelter_id=%s"""
    cur.execute(c, (shelter_id))
    con.commit()

    # Get manager details for email
    cur.execute("SELECT ownername, email FROM shelter_info WHERE shelter_id=%s", (shelter_id))
    manager = cur.fetchone()
    if manager:
        ownername, email = manager

        # Send rejection email
        fromadd = 'farizfreakin@gmail.com'
        ppassword = 'trih xamr rooy pbnr'
        toadd = email
        subject = "Account Registration Status"
        body = f"""
Dear {ownername},

After reviewing your application, we regret to inform you that your request for registration has not been approved at this time. 

If you believe this decision was made in error, please contact our support team.

Best regards,  
Admin Team
"""

        message = f"Subject:{subject}\n\n{body}"
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(fromadd, ppassword)
        server.sendmail(fromadd, toadd, message)
        server.quit()
        print("""
           <script>
           window.location.href = window.location.href;
           </script>
           """)
        exit()
elif form.getvalue("approve"):
    # Approve action
    shelter_id = form.getvalue("shelter_id")
    password = generate_random_password()

    # Update database with new password and status
    b = """UPDATE shelter_info SET pass=%s, status='approved' WHERE shelter_id=%s"""
    cur.execute(b, (password, shelter_id))
    con.commit()

    # Get manager details for email
    cur.execute("SELECT ownername, email FROM shelter_info WHERE shelter_id=%s", (shelter_id))
    manager = cur.fetchone()
    if manager:
        ownername, email = manager

        # Send approval email with credentials
        fromadd = 'farizfreakin@gmail.com'
        ppassword = 'trih xamr rooy pbnr'
        toadd = email
        subject = "Your Account Has Been Approved"
        body = f"""
Dear {ownername},

Your account has been approved. Here are your login credentials:

Email: {email}
Password: {password}

Please change your password after your first login for security reasons.

Best regards,  
Admin Team
"""

        message = f"Subject:{subject}\n\n{body}"
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(fromadd, ppassword)
        server.sendmail(fromadd, toadd, message)
        server.quit()
        print("""
        <script>
        alert('Approval email with credentials sent successfully');
        window.location.href = window.location.href;
        </script>
        """)

        exit()

# HTML output starts here
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Module</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<style>
    /* General Body Styling */
body {
    font-family: 'Roboto', Arial, sans-serif;
    background-color: #f4f7f6;
    margin: 0;
    padding: 0;
    color: #333;
}

/* Navbar */
.navbar {
    background-color: #333;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
    font-size: 1.8rem;
    font-weight: bold;
    color: #FFD54F !important;
    transition: color 0.3s ease-in-out;
}

.navbar-brand:hover {
    color: #FFF176 !important;
}

.navbar-nav .nav-link {
    font-size: 1.1rem;
    margin-right: 15px;
    transition: transform 0.3s, color 0.3s ease;
}

.navbar-nav .nav-link:hover {
    color: #FFD54F !important;
    transform: scale(1.1);
}

/* Gradient Background for Hero Section */
.bg-gradient {
    background: linear-gradient(45deg, #2196F3, #4CAF50);
    text-align: center;
    padding: 60px 20px;
    color: white;
    border-radius: 0 0 15px 15px;
}

.bg-gradient h1 {
    font-size: 3rem;
    font-weight: bold;
}

.bg-gradient p {
    font-size: 1.2rem;
}

.bg-gradient .btn {
    margin-top: 20px;
    padding: 12px 30px;
    border-radius: 25px;
    font-size: 1rem;
    background-color: #FFD54F;
    color: #333;
    border: none;
    transition: all 0.3s ease;
}

.bg-gradient .btn:hover {
    background-color: #FFC107;
    transform: translateY(-3px);
    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
}

/* Section Title Styles */
.section-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
    margin-bottom: 20px;
    text-transform: uppercase;
    position: relative;
}

.section-title::after {
    content: '';
    display: block;
    width: 70px;
    height: 4px;
    background: linear-gradient(to right, #FFD54F, #4CAF50);
    margin: 10px auto;
    border-radius: 2px;
}

/* Table Styling */
.table {
    border-radius: 10px;
    overflow: hidden;
    background-color: white;
}

.table th {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

.table-hover tbody tr:hover {
    background-color: #f1f1f1;
    transition: background-color 0.3s ease-in-out;
}

.table td, .table th {
    text-align: center;
    vertical-align: middle;
}

.badge {
    padding: 5px 10px;
    font-size: 0.9rem;
    border-radius: 12px;
    font-weight: bold;
}

.badge-success {
    background-color: #4CAF50;
    color: white;
}

.badge-warning {
    background-color: #FFC107;
    color: black;
}

.badge-secondary {
    background-color: #9E9E9E;
    color: white;
}

/* Cards */
.card {
    border-radius: 10px;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    background: linear-gradient(135deg, #ffffff, #f7f7f7);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15);
}

.card h5 {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 15px;
}

.card h3 {
    font-size: 2.5rem;
    font-weight: bold;
}

.card small {
    font-size: 0.9rem;
    color: #757575;
}

/* Buttons in Cards */
.card .btn {
    font-size: 0.9rem;
    padding: 10px 20px;
    border-radius: 25px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.card .btn-primary {
    background-color: #4CAF50;
    border: none;
    color: white;
}

.card .btn-primary:hover {
    background-color: #45a049;
    transform: scale(1.05);
}

.card .btn-warning {
    background-color: #FFC107;
    color: black;
    border: none;
}

.card .btn-warning:hover {
    background-color: #FFB300;
    transform: scale(1.05);
}

/* List Group Items (Platform Settings) */
.list-group-item {
    font-size: 1.1rem;
    padding: 15px 20px;
    border-left: 5px solid #4CAF50;
    border-radius: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.list-group-item:hover {
    background-color: #e8f5e9;
    border-left: 5px solid #FFD54F;
}

/* Footer */
footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 15px;
    font-size: 0.9rem;
}

footer p {
    margin: 0;
}

footer a {
    color: #FFD54F;
    text-decoration: none;
    transition: color 0.3s ease;
}

footer a:hover {
    color: #FFF176;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .navbar-brand {
        font-size: 1.5rem;
    }

    .section-title {
        font-size: 2rem;
    }

    .bg-gradient h1 {
        font-size: 2.5rem;
    }

    .bg-gradient p {
        font-size: 1rem;
    }
}
#overview h1,p{
    color:#FFC107;
}
</style>
<body>
<!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
        <div class="container-fluid">
            <a class="navbar-brand" href="#"><i class="fas fa-user-shield"></i> Admin Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link active" href="#overview">Overview</a></li>
                    <li class="nav-item"><a class="nav-link" href="#user-management">Users & Shelters</a></li>
                    <li class="nav-item"><a class="nav-link" href="#content-moderation">Moderation</a></li>
                    <li class="nav-item"><a class="nav-link" href="#adoption-reports">Statistics</a></li>
                    <li class="nav-item"><a class="nav-link" href="#platform-settings">Settings</a></li>
                    <li class="nav-item"><a class="nav-link btn btn-danger text-white ms-lg-3" href="#">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Dashboard Overview -->
    <section id="overview" class="bg-gradient text-white text-center py-5">
        <div class="container">
            <h1>Welcome, Admin</h1>
            <p class="lead">Manage users, shelters, content, and platform operations efficiently.</p>
            <button class="btn btn-warning btn-lg"><i class="fas fa-tools"></i> Go to Admin Tools</button>
        </div>
    </section>
     <section id="user-management" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">User and Shelter Management</h2>
            <p class="text-center mb-4">Administer user accounts and shelter registrations for compliance and security.</p>
            <div class="table-responsive">
                <table class="table table-hover table-bordered">
                    <thead class="table-success">
                        <tr>
                            <th>ID</th>
                            <th>Profile</th>
                            <th>Shelter Name</th>
                            <th>Owner Name</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>""")

# Display all shelters
for i in res:
    shelter_id = i[0]
    profile = i[10]
    shelter_name = i[1]
    owner_name = i[2]
    email = i[8]
    print(f"""
                        <tr>
                            <td>{shelter_id}</td>
                            <td><img src="./images/{profile}" alt="Profile" class="img-thumbnail" style="width: 60px; height: 60px;"></td>
                            <td>{shelter_name}</td>
                            <td>{owner_name}</td>
                            <td>{email}</td>
                            <td>
                                <form method="post" onsubmit="return confirm('Are you sure you want to approve this shelter?')">
                                    <input type="hidden" name="shelter_id" value="{shelter_id}">
                                    <input type="hidden" name="email" value="{email}">
                                    <input type="submit" name="approve" class="btn btn-sm btn-success me-2" value="Approve">
                                     <input type="submit" name="reject" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this shelter?')">


                                </form>

                            </td>
                        </tr>""")

print("""                    </tbody>
                </table>
            </div>
        </div>
    </section>""")
print(""" <section id="user-management" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center"> Care Resource Management</h2>
            <p class="text-center mb-4">Administer user accounts and shelter registrations for compliance and security.</p>
            <div class="table-responsive">
                <table class="table table-hover table-bordered">
                    <thead class="table-success">
                        <tr>
                            <th>ID</th>
                            <th>Profile</th>
                            <th>Shelter Name</th>
                            <th>Owner Name</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>""")

# Display all careResource
care = """SELECT * FROM care_reg WHERE Status='pending'"""
# Get all shelters from database
cur.execute(care)
res = cur.fetchall()
for i in res:
    Center_id = i[0]
    profile = i[13]
    Center_name = i[5]
    Resourcer_name = i[3]
    email = i[6]
    print(f"""
                        <tr>
                            <td>{Center_id}</td>
                            <td><img src="./images/{profile}" alt="Profile" class="img-thumbnail" style="width: 60px; height: 60px;"></td>
                            <td>{Center_name}</td>
                            <td>{Resourcer_name}</td>
                            <td>{email}</td>
                            <td>
                                <form method="post" onsubmit="return confirm('Are you sure you want to approve this shelter?')">
                                    <input type="hidden" name="shelter_id" value="{Center_id}">
                                    <input type="hidden" name="email" value="{email}">
                                    <input type="submit" name="approve" class="btn btn-sm btn-success me-2" value="Approve">
                                </form>
                                <button class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this shelter?')">
                                    <i class="fas fa-trash"></i> Delete
                                </button>
                            </td>
                        </tr>""")

print("""                    </tbody>
                </table>
            </div>
        </div>
    </section>""")
print("""<!-- Content Moderation -->
    <section id="content-moderation" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Content Moderation</h2>
            <p class="text-center mb-4">Review and moderate content for quality assurance and relevance.</p>
            <div class="table-responsive">
                <table class="table table-striped table-bordered">
                    <thead class="table-primary">
                        <tr>
                            <th>Content ID</th>
                            <th>Title</th>
                            <th>Type</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>101</td>
                            <td>Pet Nutrition Tips</td>
                            <td>Article</td>
                            <td><span class="badge bg-warning text-dark">Under Review</span></td>
                            <td>
                                <button class="btn btn-sm btn-success"><i class="fas fa-check"></i> Approve</button>
                                <button class="btn btn-sm btn-danger"><i class="fas fa-trash"></i> Reject</button>
                            </td>
                        </tr>
                        <tr>
                            <td>102</td>
                            <td>Adoption Success Story</td>
                            <td>Post</td>
                            <td><span class="badge bg-success">Approved</span></td>
                            <td>
                                <button class="btn btn-sm btn-danger"><i class="fas fa-trash"></i> Delete</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Adoption Statistics -->
    <section id="adoption-reports" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Adoption Statistics</h2>
            <p class="text-center mb-4">Analyze and assess platform effectiveness through detailed reports.</p>
            <div class="row g-4 text-center">
                <div class="col-md-4">
                    <div class="card shadow-sm border-0">
                        <div class="card-body">
                            <h5>Total Adoptions</h5>
                            <h3 class="text-primary">1,245</h3>
                            <small class="text-muted">+10% compared to last month</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-sm border-0">
                        <div class="card-body">
                            <h5>Pending Applications</h5>
                            <h3 class="text-warning">89</h3>
                            <small class="text-muted">Moderation required</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-sm border-0">
                        <div class="card-body">
                            <h5>Rejected Applications</h5>
                            <h3 class="text-danger">24</h3>
                            <small class="text-muted">Due to policy violations</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Platform Settings -->
    <section id="platform-settings" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Platform Settings</h2>
            <p class="text-center mb-4">Configure and customize platform-wide settings and policies.</p>
            <ul class="list-group">
                <li class="list-group-item"><i class="fas fa-cogs"></i> Configure Content Upload Guidelines</li>
                <li class="list-group-item"><i class="fas fa-user-check"></i> Set User Registration Criteria</li>
                <li class="list-group-item"><i class="fas fa-shield-alt"></i> Update Security Policies</li>
            </ul>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3">
        <p>&copy; 2025 Admin Dashboard. All Rights Reserved.</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
</body>
</html>""")

# Close database connection
cur.close()
con.close()
