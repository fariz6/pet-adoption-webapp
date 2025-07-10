#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Get form data for status update at the beginning
action = form.getvalue("action")
booking_id = form.getvalue("booking_id")
shelter_id = form.getvalue("shelter_id")

# Handle the accept/reject action FIRST before generating HTML
if action and booking_id:
    try:
        # Update the status in the bookings table
        new_status = "accepted" if action == "accept" else "rejected"
        update_query = """UPDATE bookings SET status = %s WHERE bookingid = %s"""
        cur.execute(update_query, (new_status, booking_id))
        con.commit()

        # Fetch user's email and name using booking_id
        user_query = """SELECT u.email, u.name FROM usereg u JOIN bookings b ON u.id = b.id WHERE b.bookingid = %s"""
        cur.execute(user_query, (booking_id,))
        user_result = cur.fetchone()

        if user_result:
            recipient_email = user_result[0]
            recipient_name = user_result[1]

            # Email content
            subject = "Pet Adoption Status Update"
            status_text = "accepted" if action == "accept" else "rejected"
            body = f"""
            Hi {recipient_name},

            Your pet adoption request has been {status_text}.

            {f"Congratulations! Your adoption request has been approved. Please wait for further communication from the shelter." if action == "accept" else "We regret to inform you that your adoption request has been declined. We appreciate your interest in pet adoption and encourage you to consider other pets available for adoption."}

            Thank you for choosing PetMatch!

            Best regards,
            PetMatch Team
            """

            # Email configuration
            sender_email = "farizfreakin@gmail.com"
            sender_password = "trih xamr rooy pbnr"
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Connect to SMTP server
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.ehlo()
                server.starttls()
                server.ehlo()

                # Login and send email
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()

                # Show success message
                print(f"""
                <script>
                    alert("Booking {status_text} and email sent successfully!");
                    window.location.href = window.location.href.split('?')[0];
                </script>
                """)
            except smtplib.SMTPAuthenticationError:
                print("""
                <script>
                    alert("Failed to send email: Authentication error. Please check email credentials.");
                    window.location.href = window.location.href.split('?')[0];
                </script>
                """)
            except smtplib.SMTPException as e:
                print(f"""
                <script>
                    alert("Failed to send email: {str(e)}");
                    window.location.href = window.location.href.split('?')[0];
                </script>
                """)
            except Exception as e:
                print(f"""
                <script>
                    alert("An unexpected error occurred: {str(e)}");
                    window.location.href = window.location.href.split('?')[0];
                </script>
                """)
        else:
            print("""
            <script>
                alert("No user found for this booking.");
                window.location.href = window.location.href.split('?')[0];
            </script>
            """)
    except Exception as e:
        print(f"""
        <script>
            alert("An error occurred: {str(e)}");
            window.location.href = window.location.href.split('?')[0];
        </script>
        """)

# HTML Form
print("""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recent Adoptions - PetMatch</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
        }
        .navbar {
            background-color: #6C63FF;
        }
        .navbar-brand {
            color: white !important;
            font-weight: bold;
        }
        .table {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }
        .table thead {
            background-color: #6C63FF;
            color: white;
        }
        .pet-image {
            width: 50px;
            height: 50px;
            object-fit: cover;
            border-radius: 50%%;
        }
        .status-badge {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9rem;
        }
        .status-adopted {
            background-color: red;
            color: white;
        }
        .btn-accept {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            margin-right: 5px;
        }
        .btn-reject {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .btn-accept:hover, .btn-reject:hover {
            opacity: 0.8;
        }
        .btn-user-info {
            background-color: #6C63FF;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .btn-user-info:hover {
            opacity: 0.8;
        }
        .modal-content {
            border-radius: 15px;
        }
        .modal-header {
            background-color: #6C63FF;
            color: white;
            border-radius: 15px 15px 0 0;
        }
        .user-detail-row {
            margin-bottom: 10px;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .user-detail-label {
            font-weight: bold;
            color: #6C63FF;
        }
        /* Remove bullet points from dropdown menu */
.navbar .dropdown-menu {
    list-style: none;
    padding-left: 0;
    margin-left: 0;
}

/* Style dropdown items */
.navbar .dropdown-menu li {
    padding: 0;
    margin: 0;
}

.navbar .dropdown-menu a {
    padding: 8px 16px;
    display: block;
    color: #333;
    text-decoration: none;
    transition: all 0.3s ease;
}

.navbar .dropdown-menu a:hover {
    background-color: #f8f9fa;
}

/* Align dropdown menu properly */
.nav-item.dropdown {
    position: relative;
    list-style: none;
}

/* Remove default list styling */
.navbar-nav {
    list-style: none;
    padding-left: 0;
}
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <a class="dropdown-item" href="newshelterdash.py?shelter_id=%s">Home</a>
            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="ordersDropdown" role="button" data-bs-toggle="dropdown">
                                    <i class="fas fa-shopping-cart"></i> Order Requests
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="ordersDropdown">
                                    <li><a class="dropdown-item" href="shelterrecent.py?shelter_id=%s"><i class="fas fa-clock"></i> Recent</a></li>
                                   
                                    
                                    <li><a class="dropdown-item" href="usercompleted.py?shelter_id=%s"><i class="fas fa-check-circle"></i>Aproved</a></li>
                                </ul>
                            </li>
        </div>
    </nav>

    <!-- User Details Modal -->
    <div class="modal fade" id="userDetailsModal" tabindex="-1" aria-labelledby="userDetailsModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="userDetailsModalLabel">User Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="userDetailsContent">
                    <!-- User details will be loaded here -->
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="container mt-4">
        <h2 class="mb-4">Recent Adoptions</h2>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>SNO</th>
                        <th>Pet Name</th>
                        <th>Species</th>
                        <th>Breed</th>
                        <th>Adoption Date</th>
                        <th>Date of Booking</th>
                        <th>Status</th>
                        <th>User Info</th>
                       
                    </tr>
                </thead>
                <tbody>
""" %(shelter_id,shelter_id,shelter_id))

# Query to get recent adopted bookings for the specific shelter
query = """
SELECT 
    b.bookingid,
    p.Petname,
    p.Species,
    p.Breed,
    b.day,
    b.bookingdate,
    u.name as adopter_name,
    b.status,
    u.id as user_id,
    u.profile_pic,
    u.proof_attachment,
    u.email,
    u.mob,
    u.street,
    u.city,
    u.state,
    u.pin
FROM 
    bookings b
JOIN 
    product_info p ON b.product_id = p.product_id
JOIN 
    shelter_info s ON p.shelter_id = s.shelter_id
LEFT JOIN 
    usereg u ON b.id = u.id
WHERE 
    s.shelter_id = %s
AND 
    b.status = 'rejected'
ORDER BY 
    b.bookingid DESC
"""

cur.execute(query, (shelter_id,))
results = cur.fetchall()

if results:
    sno = 1
    for row in results:
        booking_id, pet_name, species, breed, booking_date, bookingdate, adopter_name, status, user_id, profile_pic, proof_attachment, email, mob, address, city, state, pincode = row
        # Format dates to DD-MM-YY, handling datetime strings that include time
        formatted_booking_date = datetime.strptime(str(booking_date).split()[0], '%Y-%m-%d').strftime('%d-%m-%y')
        formatted_bookingdate = datetime.strptime(str(bookingdate).split()[0], '%Y-%m-%d').strftime('%d-%m-%y')
        print(f"""
                    <tr>
                        <td>{sno}</td>
                        <td>{pet_name}</td>
                        <td>{species}</td>
                        <td>{breed}</td>
                        <td>{formatted_booking_date}</td>
                        <td>{formatted_bookingdate}</td>
                        <td><span class="status-badge status-adopted">Rejected</span></td>
                        <td>
                            <button class="btn btn-user-info" onclick="showUserDetails({{
                                'name': '{adopter_name}',
                                'email': '{email}',
                                'mobile': '{mob}',
                                'address': '{address}',
                                'city': '{city}',
                                'state': '{state}',
                                'pincode': '{pincode}',
                                'profile_pic': '{profile_pic}',
                                'proof_attachment': '{proof_attachment}'
                            }})">
                                <i class="fas fa-user-circle"></i> View Details
                            </button>
                        </td>

                    </tr>
""")
        sno += 1
else:
    print("""
                    <tr>
                        <td colspan="7" class="text-center">No recent adoptions found.</td>
                    </tr>
    """)

print("""
                </tbody>
            </table>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showUserDetails(userData) {
            const modalContent = document.getElementById('userDetailsContent');
            modalContent.innerHTML = `
                <div class="user-detail-row">
                    <div class="user-detail-label">Profile Picture:</div>
                    <div><img src="./images/${userData.profile_pic}" alt="Profile Picture" style="max-width: 200px; max-height: 200px; border-radius: 10px;"></div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">Proof Document:</div>
                    <div><img src="./images/${userData.proof_attachment}" alt="Proof Document" style="max-width: 200px; max-height: 200px; border-radius: 10px;"></div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">Name:</div>
                    <div>${userData.name}</div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">Email:</div>
                    <div>${userData.email}</div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">Mobile:</div>
                    <div>${userData.mobile}</div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">Address:</div>
                    <div>${userData.address}</div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">City:</div>
                    <div>${userData.city}</div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">State:</div>
                    <div>${userData.state}</div>
                </div>
                <div class="user-detail-row">
                    <div class="user-detail-label">Pincode:</div>
                    <div>${userData.pincode}</div>
                </div>
            `;

            const modal = new bootstrap.Modal(document.getElementById('userDetailsModal'));
            modal.show();
        }
    </script>
</body>
</html>
""")

# Close database connection
con.close()


