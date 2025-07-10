#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Get centreid from URL parameter
centreid = form.getvalue('careid')

# Get bookings data with center and user info using JOIN
query = """
SELECT 
    cb.carebookingid, 
    cb.centerid, 
    cb.userid, 
    cb.species, 
    cb.breed,
    cb.date,
    cb.status,
    cb.caretype,
    ci.centername,
    ci.centertype,
    ci.address,
    ci.city,
    ci.state,
    ci.mob,
    ci.mail,
    ci.description,
    ci.image,
    ur.email AS user_email,
    ur.name,
    ur.city,
    ur.mob,
    cr.careresourcername,
    cr.careresourcetype
FROM 
    carebookings cb
INNER JOIN 
    careresource_info ci ON cb.centerid = ci.careid
INNER JOIN 
    care_reg cr ON ci.careid = cr.centreid
LEFT JOIN 
    usereg ur ON cb.userid = ur.id
WHERE 
    cb.status = 'approved' AND cr.centreid = %s
ORDER BY 
    cb.carebookingid
"""

cur.execute(query, (centreid,))
bookings = cur.fetchall()

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animal Shelter Management</title>
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
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
        }

        .navbar {
            background-color:lightpink;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .main-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            margin: 2rem auto;
            flex: 1;
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

        .table {
            width: 100%%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }

        .table thead {
            background: linear-gradient(135deg, #6C63FF 0%%, #FF6584 100%%);
            color: white;
        }

        .table th {
            padding: 1rem;
            text-align: left;
        }

        .table td {
            padding: 1rem;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
        }

        .table tbody tr:last-child td {
            border-bottom: none;
        }

        .table tbody tr:hover {
            background-color: rgba(108, 99, 255, 0.05);
        }

        .badge-service {
            font-size: 0.85rem;
            padding: 0.5em 1em;
            border-radius: 20px;
        }

        .modal-content {
            border: none;
            border-radius: 1rem;
        }

        .modal-header {
            background: linear-gradient(135deg, #6C63FF 0%%, #FF6584 100%%);
            color: white;
            border-radius: 1rem 1rem 0 0;
        }

        .modal-body img {
            max-width: 100%%;
            height: auto;
            max-height: 200px;
            object-fit: cover;
            border-radius: 6px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 3rem 0;
            margin-top: auto;
        }

        .footer-links h5 {
            margin-bottom: 1.5rem;
            position: relative;
        }

        .footer-links h5:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -10px;
            width: 40px;
            height: 2px;
            background-color: var(--primary-color);
        }

        .footer-links ul {
            list-style: none;
            padding-left: 0;
        }

        .footer-links li {
            margin-bottom: 0.5rem;
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
            padding-top: 1.5rem;
            margin-top: 2rem;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg  sticky-top">
        <div class="container">
            <a class="navbar-brand text-primary" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                <li> <a class="nav-link" href="get_services.py?careid=%s">Home</a></li>
                    <li class="nav-item dropdown">
                      <a class="nav-link dropdown-toggle" href="#" id="trainingDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-graduation-cap me-1"></i>Bookings
                        </a>
                        <ul class="dropdown-menu">
                            <li> <a class="nav-link" href="carevetreq.py?careid=%s">Service Requests</a></li>
                            <li><a class="nav-link" href="caremodcomplete.py?careid=%s">Approved</a>
</li>
                            
</li>
                            <li><a class="nav-link" href="caremodrejected.py?careid=%s">Rejected</a>
</li>
                             
                        </ul> 
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <section id="shelter-management" class="py-5">
        <div class="container main-container">
            <h2 class="section-title">Bookings Approved</h2>


            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>S.No.</th>
                            <th>Center Info</th>
                            <th>Service Type</th>
                            <th>Care Type</th>
                            <th>Species</th>
                            <th>Breeds</th>
                            <th>Location</th>
                            <th>User Info</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
"""  %(centreid,centreid,centreid,centreid))

# Display all bookings
sno = 1
for booking in bookings:
    booking_id = booking[0]
    center_id = booking[1]
    user_id = booking[2]
    species = booking[3]
    breed = booking[4]
    date = booking[5]
    status = booking[6]
    caretype = booking[7]
    center_name = booking[8]
    center_type = booking[9]
    address = booking[10]
    city = booking[11]
    state = booking[12]
    phone = booking[13]
    email = booking[14]
    description = booking[15]
    image = booking[16]
    user_email = booking[17]
    username = booking[18]
    location = booking[19]

    care_resource_name = booking[21]
    care_resource_type = booking[22]

    # Determine service type badge class
    service_class = "info"
    if center_type == "Training":
        service_class = "warning"
    elif center_type == "Pet Spa":
        service_class = "success"
    elif center_type == "Veterinary" or center_type == "Veterinary Clinic":
        service_class = "primary"

    print(f"""
                                <tr>
                                    <td>{sno}</td>
                                    <td><button class="btn btn-sm btn-outline-primary center-info" data-bs-toggle="modal" data-bs-target="#centerModal{booking_id}">View Center</button></td>
                                    <td><span class="badge bg-{service_class} {'text-dark' if service_class in ['info', 'warning'] else ''} badge-service">{center_type}</span></td>
                                    <td>{caretype}</td>
                                    <td>{species}</td>
                                    <td>{breed}</td>
                                    <td>{city}, {state}</td>
                                    <td><button class="btn btn-sm btn-outline-secondary user-info" data-bs-toggle="modal" data-bs-target="#userModal{booking_id}">View User</button></td>
                                    <td><span class="badge bg-success">Approved</span></td>
                                </tr>
    """)
    sno += 1

print("""
                    </tbody>
                </table>
            </div>
        </div>
    </section>
""")

# Generate center modals
for booking in bookings:
    booking_id = booking[0]
    center_name = booking[8]
    center_type = booking[9]
    address = booking[10]
    city = booking[11]
    state = booking[12]
    email = booking[14]
    description = booking[15]
    image = booking[16] if booking[16] else "default.jpg"

    print(f"""
    <!-- Center Info Modal -->
    <div class="modal fade" id="centerModal{booking_id}" tabindex="-1" aria-labelledby="centerModalLabel{booking_id}" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="centerModalLabel{booking_id}">Center Information</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="text-center mb-3">
                        <img src="./images/{image}" alt="Center Picture" class="img-fluid mb-3" onerror="this.src='./images/default.jpg';">
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Name:</strong> {center_name}</p>
                            <p><strong>Center Type:</strong> {center_type}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Location:</strong> {city}, {state}</p>
                            <p><strong>Email:</strong> {email}</p>
                        </div>
                    </div>
                    <div class="mt-3">
                        <p><strong>Address:</strong> {address}</p>
                        <p><strong>Description:</strong> {description}</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    """)

# Generate user modals
for booking in bookings:
    booking_id = booking[0]
    user_id = booking[2]
    user_email = booking[17]
    username = booking[18]
    location = booking[19]
    phone = booking[20]
    date = booking[5]

    print(f"""
    <!-- User Info Modal -->
    <div class="modal fade" id="userModal{booking_id}" tabindex="-1" aria-labelledby="userModalLabel{booking_id}" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="userModalLabel{booking_id}">User Information</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-12">
                            <p><strong>User ID:</strong> {user_id}</p>
                            <p><strong>Username:</strong> {username}</p>
                            <p><strong>Email:</strong> {user_email}</p>
                            <p><strong>Location:</strong> {location}</p>
                            <p><strong>Phone:</strong> {phone}</p>
                            <p><strong>Booking Date:</strong> {date}</p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    """)

print("""
    <!-- Footer -->
    

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
con.close()