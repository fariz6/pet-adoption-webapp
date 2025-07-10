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


# Process form submissions
if form.getvalue("care_reject"):
    center_id = form.getvalue("center_id")
    c = """UPDATE careresource_info SET status='rejected' WHERE careid=%s"""
    cur.execute(c, (center_id,))
    con.commit()

    cur.execute("SELECT resourcername, mail FROM careresource_info WHERE careid=%s", (center_id,))
    manager = cur.fetchone()
    if manager:
        resourcer_name, email = manager

        # Send rejection email
        fromadd = 'farizfreakin@gmail.com'
        ppassword = 'trih xamr rooy pbnr'
        toadd = email
        subject = "Care Center Registration Status"
        body = f"""
Dear {resourcer_name},

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
        alert('Rejection email sent successfully');
        location.href = "carenew.py";
        </script>
        """)
        exit()

elif form.getvalue("care_approve"):
    center_id = form.getvalue("center_id")
    password = generate_random_password()

    b = """UPDATE careresource_info SET pass=%s, status='approved' WHERE careid=%s"""
    cur.execute(b, (password, center_id))
    con.commit()

    cur.execute("SELECT resourcername, mail FROM careresource_info WHERE careid=%s", (center_id,))
    manager = cur.fetchone()
    if manager:
        resourcer_name, email = manager

        # Send approval email with credentials
        fromadd = 'farizfreakin@gmail.com'
        ppassword = 'trih xamr rooy pbnr'
        toadd = email
        subject = "Your Care Center Account Has Been Approved"
        body = f"""
Dear {resourcer_name},

Your care center account has been approved. Here are your login credentials:

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
        location.href =" carenew.py";
        </script>
        """)
        exit()

# Process password request form submission
if form.getvalue("send_password"):
    shelter_id = form.getvalue("shelter_id")
    password = generate_random_password()
    
    # Update shelter_info table with new password
    update_shelter = """UPDATE shelter_info SET pass=%s WHERE shelter_id=%s"""
    cur.execute(update_shelter, (password, shelter_id))
    
    # Update pass table status
    update_pass = """UPDATE pass SET status='sended' WHERE shelter_id=%s"""
    cur.execute(update_pass, (shelter_id,))
    con.commit()
    
    # Get shelter email
    cur.execute("SELECT email FROM shelter_info WHERE shelter_id=%s", (shelter_id,))
    shelter_email = cur.fetchone()[0]
    
    # Send email with new password
    fromadd = 'farizfreakin@gmail.com'
    ppassword = 'trih xamr rooy pbnr'
    toadd = shelter_email
    subject = "Your New Password"
    body = f"""
Dear Shelter Manager,

Your new password has been generated. Here are your login credentials:

Email: {shelter_email}
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
    alert('Password sent successfully');
    location.href = "password_requests.py";
    </script>
    """)
    exit()

# Get pending password requests with shelter info
pass_query = """
SELECT p.*, s.sheltername, s.email, s.mob, s.street, s.city, s.state, s.pin 
FROM pass p 
JOIN shelter_info s ON p.shelter_id = s.shelter_id 
WHERE p.status='pending'
"""
cur.execute(pass_query)
pass_res = cur.fetchall()

# Get pending care resources
care_query = """SELECT * FROM careresource_info WHERE status='pending'"""
cur.execute(care_query)
care_res = cur.fetchall()

# HTML output starts here
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Requests Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
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

/* Cover Image Styles */
.cover-image {
    width: 100%;
    height: 400px;
    object-fit: cover;
    position: relative;
}

.cover-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
}

.cover-content {
    z-index: 1;
}

.cover-content h1 {
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.cover-content p {
    font-size: 1.2rem;
    max-width: 600px;
    margin: 0 auto;
}

/* Table Styling */
.table {
    border-radius: 10px;
    overflow: hidden;
    background-color: white;
    width: 100%;
}

.table th {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    white-space: nowrap;
}

.table-hover tbody tr:hover {
    background-color: #f1f1f1;
    transition: background-color 0.3s ease-in-out;
}

.table td, .table th {
    text-align: center;
    vertical-align: middle;
    word-break: break-word;
}

/* Responsive Table Container */
.table-responsive {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin-bottom: 1rem;
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

/* Dropdown Menu Styles */
.dropdown-menu {
    background-color: #333;
    border: none;
}

.dropdown-item {
    color: white;
}

.dropdown-item:hover {
    background-color: #4CAF50;
    color: white;
}

html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}
body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}
.wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
}
/* Add this to your existing styles */
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}

body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
}

/* Keep your existing footer styles but add margin-top: auto */
footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 15px;
    font-size: 0.9rem;
    margin-top: auto;
}
</style>
</head>
<body>
<div class="wrapper">
<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
    <div class="container-fluid">
        <a class="navbar-brand" href="#"><i class="fas fa-user-shield"></i> Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link active" href="admin.py"><i class="fas fa-home"></i> Home</a></li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="shelterDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-home"></i> Shelters
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="shelterDropdown">
                        <li><a class="dropdown-item" href="adminshelternew.py?shelter_status=new">New Requests</a></li>
                        <li><a class="dropdown-item" href="adminmanager.py?shelter_status=active">Active Shelters</a></li>
                        <li><a class="dropdown-item" href="adminmanagerrej.py?shelter_status=rejected">Rejected Shelters</a></li>
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="careDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-hospital"></i> Care Centers
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="careDropdown">
                        <li><a class="dropdown-item" href="carenew.py?care_status=new">New Requests</a></li>
                        <li><a class="dropdown-item" href="caremanager.py?care_status=active">Active Centers</a></li>
                        <li><a class="dropdown-item" href="caremanagerrejected.py?care_status=rejected">Rejected Centers</a></li>
                    </ul>
                </li>
                <li class="nav-item"><a class="nav-link" href="adminuser.py"><i class="fas fa-users"></i> Users</a></li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="careDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-key"></i> Passwords Requests
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="careDropdown">
                        <li><a class="dropdown-item" href="password_requests.py?care_status=new">shelter</a></li>
                        <li><a class="dropdown-item" href="password_request.py?care_status=active">Care center</a></li>
                     
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!-- Password Requests Section -->
<section id="password-requests" class="py-5 bg-light">
    <div class="container">
        <h2 class="section-title text-center">Shelter Forgot Password Requests</h2>
        <p class="text-center mb-4">Review and manage pending password reset requests.</p>
        <div class="table-responsive">
            <table class="table table-hover table-bordered">
                <thead class="table-primary">
                    <tr>
                        <th>Sno.</th>
                        <th>Request Date</th>
                        <th>Shelter Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Address</th>
                        <th>City</th>
                        <th>State</th>
                        <th>Pincode</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>""")

# Display all pending password requests
m = 1
for i in pass_res:
    request_id = i[0]
    shelter_id = i[1]
    request_date = i[3]
    status = i[3]
    sheltername = i[5]
    email = i[6]
    phone = i[7]
    address = i[8]
    city = i[9]
    state = i[10]
    pincode = i[11]
    
    # Format the date
    try:
        req_date = request_date.strftime('%d-%m-%y')
    except:
        req_date = request_date
        
    print(f"""
                    <tr>
                        <td>{m}</td>
                        <td>{req_date}</td>
                        <td>{sheltername}</td>
                        <td>{email}</td>
                        <td>{phone}</td>
                        <td>{address}</td>
                        <td>{city}</td>
                        <td>{state}</td>
                        <td>{pincode}</td>
                        <td>
                            <form method="post" onsubmit="return confirm('Are you sure you want to send a new password to this shelter?')">
                                <input type="hidden" name="shelter_id" value="{shelter_id}">
                                <input type="submit" name="send_password" class="btn btn-sm btn-primary" value="Send Password">
                            </form>
                        </td>
                    </tr>""")
    m += 1

print("""                </tbody>
            </table>
        </div>
    </div>
</section>


<!-- Footer -->
<div class="wrapper">
    <!-- All your content (navbar, sections, etc.) goes here -->
    
    <!-- Footer at the bottom -->
    <footer class="bg-dark text-white text-center py-3">
        <p>&copy; 2025 Admin Dashboard. All Rights Reserved.</p>
    </footer>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
<script>
function openDocumentsModal(profile, license, title) {
    const modal = new bootstrap.Modal(document.getElementById('documentsModal'));
    document.getElementById('modalProfile').src = './images/' + profile;
    document.getElementById('modalLicense').src = './images/' + license;
    document.getElementById('documentsModalLabel').textContent = title;
    modal.show();
}
</script>
</body>
</html>""")

# Close database connection
cur.close()
con.close()