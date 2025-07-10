#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Uid = form.getvalue("id")

# Fetch recent orders where status is 'adopted'
sql = """
    SELECT 
        b.*, 
        p.Petname as petname, 
        p.Animalimg as pet_image,
        p.species,
        p.breed,
        s.sheltername,
        s.street,
        s.city,
        s.state,
        s.pin,
        s.mob as shelter_phone,
        s.email as shelter_email,
        s.profile_pic as shelter_image,
        s.ownername as shelter_owner,
        DATE_FORMAT(b.day, '%%Y-%%m-%%d') as booking_date
    FROM bookings b 
    JOIN product_info p ON b.product_id = p.product_id 
    JOIN shelter_info s ON p.shelter_id = s.shelter_id
    WHERE b.id = %s AND b.status = 'rejected' 
    ORDER BY b.bookingid DESC
"""
cur.execute(sql, (Uid,))
recent_orders = cur.fetchall()

# HTML Form
print("""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - Recent Orders</title>
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

        /* Custom table styles */
        .pets-table {
            width: 100%%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }

        .pets-table thead {
            background: linear-gradient(135deg, #6C63FF 0%%, #FF6584 100%%);
            color: white;
        }

        .pets-table th {
            padding: 1rem;
            text-align: left;
        }

        .pets-table td {
            padding: 1rem;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
        }

        .pets-table tbody tr:last-child td {
            border-bottom: none;
        }

        .pets-table tbody tr:hover {
            background-color: rgba(108, 99, 255, 0.05);
        }

        .pet-image {
            width: 60px;
            height: 60px;
            object-fit: cover;
            border-radius: 50%%;
            margin-right: 1rem;
        }

        .pet-info {
            display: flex;
            align-items: center;
        }

        .badge-available {
            background-color: #28a745;
        }
        .badge-adopted{
            background-color:red;}
        
        

        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 0rem 0;
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

        /* Nested table styles */
        .nested-table {
            width: 100%%;
            border-collapse: collapse;
        }

        .nested-table th, .nested-table td {
            padding: 0.75rem;
            border: 1px solid #dee2e6;
        }

        .nested-table thead {
            background-color: #f8f9fa;
        }

        .nested-table tbody tr:nth-child(even) {
            background-color: rgba(0, 0, 0, 0.02);
        }

.modal-content {
  border: none;
  border-radius: 1rem;
}

.details p {
  margin: 0.2rem 0;
  font-size: 1rem;
}

.shelter-image {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 50%%;
    border: 3px solid var(--primary-color);
    margin: 0 auto;
    display: block;
}

.shelter-details {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-top: 1rem;
}

.shelter-details .details {
    margin-top: 1rem;
}

.shelter-details p {
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.shelter-details strong {
    color: var(--primary-color);
    min-width: 120px;
    display: inline-block;
}

.shelter-details h6 {
    color: var(--primary-color);
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
        <div class="container">
            <a class="navbar-brand text-primary" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <a class="dropdown-item" href="browsepet.py?id=%s">Home</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="myOrdersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> My Orders
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="userrecent.py?id=%s">Recent</a></li>
                            <li><a class="dropdown-item" href="usercomplete.py?id=%s">Aproved</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container main-container">
        <h2 class="section-title">Rejected Orders</h2>

        <div class="table-responsive">
            <table class="table pets-table">
                <thead>
                    <tr>
                        <th>Pet Details</th>
                        <th>Booking Date</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
""" %(Uid,Uid,Uid))
n = 1
# Display recent orders
if recent_orders:
    for i in recent_orders:
        # Pet information from product_info table
        petname = i[7]  # p.Petname
        pet_image = i[10]  # p.Animalimg
        species = i[8]  # p.species
        breed = i[9]  # p.breed
        bookingid = i[0]  # b.bookingid
        id = i[1]  # b.id

        # Debug print statements
        print(f"<!-- Debug: Pet Image Path = /images/{pet_image} -->")

        # Shelter information from shelter_info table
        shelter_name = i[18]  # s.sheltername
        street = i[19]  # s.street
        city = i[20]  # s.city
        state = i[21]  # s.state
        pin = i[22]  # s.pin
        shelter_phone = i[23]  # s.mob
        shelter_email = i[24]  # s.email
        shelter_image = i[25]  # s.profile_pic
        shelter_owner = i[19]  # s.ownername

        # Debug print statements
        print(f"<!-- Debug: Shelter Image Path = /images/{shelter_image} -->")

        print(f"""
                    <tr>
                        <td>
                            <div class="pet-info">
                                <img src="./images/{pet_image}" alt="{petname}" class="pet-image">
                                <div>
                                    <h6 class="mb-0">{petname}</h6>
                                    <small class="text-muted">{species} - {breed}</small>
                                </div>
                            </div>
                        </td>
                        <td>{i[27]}</td>
                        <td><span class="badge badge-adopted">Rejected</span></td>
                        <td>
                            <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#detailsModal{id}">
                                <i class="fas fa-eye"></i> View Details
                            </button>
                        </td>
                    </tr>

                    <!-- Details Modal -->
                    <div class="modal fade" id="detailsModal{id}" tabindex="-1" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Pet and Shelter Details</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="pet-details mb-4">
                                        <h6 class="fw-bold">Pet Information</h6>
                                        <div class="details">
                                            <p><strong>Name:</strong> {petname}</p>
                                            <p><strong>Species:</strong> {species}</p>
                                            <p><strong>Breed:</strong> {breed}</p>
                                            <p><strong>Booking ID:</strong> {bookingid}</p>
                                        </div>
                                    </div>
                                    <div class="shelter-details">
                                        <h6 class="fw-bold">Shelter Information</h6>
                                        <img src="./images/{shelter_image}" alt="{shelter_name}" class="shelter-image mb-3">
                                        <div class="details">
                                            <p><strong>Shelter Name:</strong> {shelter_name}</p>

                                            <p><strong>Address:</strong> {street}, {city}, {state} - {pin}</p>
                                            <p><strong>Phone:</strong> {shelter_phone}</p>
                                            <p><strong>Email:</strong> {shelter_email}</p>
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
        n += 1
else:
    print("""
                    <tr>
                        <td colspan="4" class="text-center">No rejected orders found</td>
                    </tr>
    """)

print("""
                </tbody>
            </table>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">

            <div class="copyright text-center">
                <p>&copy; 2023 PetMatch. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()