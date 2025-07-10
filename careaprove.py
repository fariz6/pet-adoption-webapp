#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
import sys
import codecs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print("Content-type: text/html; charset=utf-8\n\n")
import pymysql, cgi, cgitb

cgitb.enable()

def send_payment_confirmation_email(user_email, center_name, booking_date, amount, payment_method, transaction_id):
    # Email configuration
    sender_email = "farizfreakin@gmail.com"  # Replace with your email
    sender_password = "trih xamr rooy pbnr"  # Replace with your app password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create message for user
    user_message = MIMEMultipart()
    user_message["From"] = sender_email
    user_message["To"] = user_email
    user_message["Subject"] = "Payment Confirmation - PetMatch Care Services"

    # Email body for user
    user_body = f"""
    <html>
        <body>
            <h2>Payment Confirmation</h2>
            <p>Dear PetMatch User,</p>
            <p>Your payment for the following service has been successfully processed:</p>
            <ul>
                <li>Service Center: {center_name}</li>
                <li>Booking Date: {booking_date}</li>
                <li>Amount Paid: ₹{amount:.2f}</li>
                <li>Payment Method: {payment_method}</li>
                <li>Transaction ID: {transaction_id}</li>
            </ul>
            <p>Thank you for choosing PetMatch Care Services. You can visit the center on your scheduled date.</p>
            <p>Best regards,<br>PetMatch Team</p>
        </body>
    </html>
    """

    user_message.attach(MIMEText(user_body, "html"))

    # Create message for sender
    sender_message = MIMEMultipart()
    sender_message["From"] = sender_email
    sender_message["To"] = sender_email
    sender_message["Subject"] = "New Payment Received - PetMatch Care Services"

    # Email body for sender
    sender_body = f"""
    <html>
        <body>
            <h2>New Payment Notification</h2>
            <p>Dear PetMatch Admin,</p>
            <p>A new payment has been received for the following service:</p>
            <ul>
                <li>Service Center: {center_name}</li>
                <li>Booking Date: {booking_date}</li>
                <li>Amount Received: ₹{amount:.2f}</li>
                <li>Customer Email: {user_email}</li>
            </ul>
            <p>Please ensure the service is prepared for the scheduled date.</p>
            <p>Best regards,<br>PetMatch System</p>
        </body>
    </html>
    """

    sender_message.attach(MIMEText(sender_body, "html"))

    # Send emails
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send user email
        server.send_message(user_message)

        # Send sender notification
        server.send_message(sender_message)

        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Database connection and existing logic remains the same...
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
user_id = form.getvalue('id')

# Handle payment action
if form.getvalue('pay') and form.getvalue('booking_id'):
    booking_id = form.getvalue('booking_id')
    payment_option = form.getvalue('payment_option')

    # Get user email and booking details
    cur.execute("""
        SELECT u.email, cb.centerid, cb.date, ci.centername, cb.caretype, cb.userid
        FROM carebookings cb
        JOIN usereg u ON cb.userid = u.id
        JOIN careresource_info ci ON cb.centerid = ci.careid
        WHERE cb.carebookingid = %s
    """, (booking_id,))
    booking_details = cur.fetchone()

    if booking_details:
        user_email, center_id, booking_date, center_name, care_type, user_id = booking_details

        # Get service price from the form
        service_price = form.getvalue('service_price')
        if not service_price:
            print("""
            <script>
                window.onload = function() {
                    alert("Error: Service price not found. Please try again.");
                    window.location.href = "careaprove.py?id=""" + str(user_id) + """";
                }
            </script>
            """)
            exit()

        # Update booking status
        cur.execute("UPDATE carebookings SET status = 'paid' WHERE carebookingid = %s",
                    (booking_id,))
        con.commit()

        # Insert into payment table using form data
        upi_id = form.getvalue('upi_id') if payment_option == 'upi' else None
        
        # Generate a transaction ID based on payment method
        if payment_option == 'upi':
            transaction_id = upi_id
        elif payment_option == 'card':
            transaction_id = f"CARD_{booking_id}_{int(time.time())}"
        else:  # cash
            transaction_id = f"CASH_{booking_id}_{int(time.time())}"
        
        cur.execute("""
            INSERT INTO payment (service, serviceprice, serviceid, careid, userid, paymethod, transid) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (care_type, service_price, booking_id, center_id, user_id, payment_option, transaction_id))
        con.commit()

        # Send confirmation email
        if send_payment_confirmation_email(user_email, center_name, booking_date, float(service_price), payment_option, transaction_id):
            print("""
            <script>
                window.onload = function() {
                    alert("Payment successful and pet service in this center is booked. A confirmation email has been sent to your registered email address.");
                    window.location.href = "careaprove.py?id=""" + str(user_id) + """";
                }
            </script>
            """)
        else:
            print("""
            <script>
                window.onload = function() {
                    alert("Payment successful and pet service in this center is booked. However, we couldn't send the confirmation email.");
                    window.location.href = "careaprove.py?id=""" + str(user_id) + """";
                }
            </script>
            """)
    else:
        print("""
        <script>
            window.onload = function() {
                alert("Error processing payment. Please try again.");
                window.location.href = "careaprove.py?id=""" + str(user_id) + """";
            }
        </script>
        """)

# Fetch bookings
query = """
SELECT 
    cb.carebookingid, cb.centerid, cb.species, cb.breed, cb.date, cb.status,
    ci.centername, cb.caretype, ci.city, ci.state,
    COALESCE(p.serviceprice, 0) as amount_paid,
    p.paymethod, cb.bookingdate
FROM 
    carebookings cb
LEFT JOIN 
    careresource_info ci ON cb.centerid = ci.careid
LEFT JOIN
    payment p ON cb.carebookingid = p.serviceid
WHERE 
    cb.userid = %s
ORDER BY 
    cb.carebookingid DESC
"""
cur.execute(query, (user_id,))
bookings = cur.fetchall()

# HTML with enhanced navbar and footer
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Care Service Bookings</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        body {
            background-color: #f0f2ff;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .navbar{
           background-color:  #4e73df !important;
        }
        .navbar-brand {
            font-weight: 600;
        }
        .nav-link.active {
            font-weight: 500;
            color: black !important;
        }
        .main-content {
            flex: 1;
        }
        footer {
            background-color: beige;
            padding: 1.5rem 0;
            margin-top: 2rem;
        }
        .status-badge {
            font-size: 0.85rem;
            padding: 0.35em 0.65em;
        }
        .table-responsive {
            overflow-x: auto;
        }
        @media (max-width: 768px) {
            .navbar-collapse {
                padding-top: 1rem;
            }
        }
        /* Colorful Navbar Styles */
        
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg  shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="bi bi-heart-pulse me-2"></i>PetMatch Care
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="usercare.py?id=""" + str(user_id) + """"><i class="bi bi-house-door me-1"></i> Home</a>
                    </li>
                   
                    
                </ul>
                
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">
        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><i class="bi bi-calendar3 me-2"></i>My Care Service Bookings</h2>
                
            </div>

            <div class="table-responsive">
                <table class="table table-bordered align-middle">
                    <thead class="table-primary">
                        <tr>
                            <th>S.No.</th>
                            <th>Center Info</th>
                            <th>Care Type</th>
                            <th>Species</th>
                            <th>Breeds</th>
                            <th>Location</th>
                            <th>Appointment Date</th>
                            <th>Status</th>
                            <th>Action</th>
                            <th>Amount Paid</th>
                            <th>Payment Method</th>
                            <th>Date of Booking</th>
                        </tr>
                    </thead>
                    <tbody>
""")

sno = 1
for booking in bookings:
    booking_id, center_id, species, breed, date, status, center_name, care_type, city, state, amount_paid, paymethod, bookingdate = booking
    status_badge = {
        "requested": '<span class="badge bg-warning text-dark status-badge">Requested</span>',
        "approved": '<span class="badge bg-success status-badge">Approved</span>',
        "completed": '<span class="badge bg-primary status-badge">Completed</span>',
        "rejected": '<span class="badge bg-danger status-badge">Rejected</span>',
        "paid": '<span class="badge bg-info text-dark status-badge">Paid</span>'
    }.get(status.lower(), status)

    action_html = ""
    if status.lower() == "requested":
        action_html = '<span class="text-muted">Waiting for approval</span>'
    elif status.lower() == "approved":
        action_html = f'''
            <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#payModal{booking_id}">
                <i class="bi bi-credit-card me-1"></i> Pay Now
            </button>
        '''
    elif status.lower() == "completed":
        action_html = '<span class="text-success"><i class="bi bi-check2-all me-1"></i>Completed</span>'
    elif status.lower() == "paid":
        action_html = '<span class="text-info"><i class="bi bi-check-circle me-1"></i>Paid</span>'
    else:
        action_html = '-'

    print(f"""
        <tr>
            <td>{sno}</td>
            <td>{center_name}</td>
            <td>{care_type}</td>
            <td>{species}</td>
            <td>{breed}</td>
            <td>{city}, {state}</td>
            <td>{date.strftime('%d-%m-%y') if date else '-'}</td>
            <td>{status_badge}</td>
            <td>{action_html}</td>
            <td>₹{float(amount_paid):.2f}</td>
            <td>{paymethod if paymethod else '-'}</td>
            <td>{bookingdate.strftime('%d-%m-%y') if bookingdate else '-'}</td>
        </tr>
    """)
    sno += 1

print("""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Pay Modals for approved bookings -->
""")

cur2 = con.cursor()
for booking in bookings:
    booking_id, center_id, species, breed, date, status, center_name, care_type, city, state, amount_paid, paymethod, bookingdate = booking
    if status.lower() == "approved":
        cur2.execute("""
            SELECT servicetype, serviceprice 
            FROM serviceprice 
            WHERE careid = %s AND servicetype = %s
        """, (center_id, care_type))
        service = cur2.fetchone()

        services_html = ""
        total = 0
        if service:
            service_type, service_price = service
            services_html = f"<tr><td>{service_type}</td><td>₹{float(service_price):.2f}</td></tr>"
            total = float(service_price)
        else:
            services_html = "<tr><td colspan='2'>Service details not found</td></tr>"

        print(f"""
        <div class="modal fade" id="payModal{booking_id}" tabindex="-1" aria-labelledby="payModalLabel{booking_id}" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <form method="post">
                <div class="modal-header">
                  <h5 class="modal-title" id="payModalLabel{booking_id}">Pay for Services at {center_name}</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="mb-3">
                    <h6>Booking Details:</h6>
                    <p class="mb-1"><strong>Pet Species:</strong> {species}</p>
                    <p class="mb-1"><strong>Pet Breed:</strong> {breed}</p>
                    <p class="mb-1"><strong>Appointment Date:</strong> {date.strftime('%d-%m-%y') if date else '-'}</p>
                  </div>
                  <div class="mb-3">
                    <h6>Service & Pricing:</h6>
                    <table class="table table-bordered">
                      <thead class="table-light">
                        <tr><th>Service</th><th>Price</th></tr>
                      </thead>
                      <tbody>
                        {services_html}
                      </tbody>
                      <tfoot class="table-light">
                        <tr><th>Total</th><th>₹{total:.2f}</th></tr>
                      </tfoot>
                    </table>
                  </div>
                  <div class="mb-3">
                    <label for="paymentOption{booking_id}" class="form-label">Payment Option</label>
                    <select class="form-select" id="paymentOption{booking_id}" name="payment_option" required onchange="toggleUpiField(this)">
                      <option value="">Select</option>
                      <option value="upi">UPI</option>
                      <option value="card">Credit/Debit Card</option>
                      <option value="cash">Cash at Center</option>
                    </select>
                  </div>
                  <div class="mb-3 upi-field" style="display: none;">
                    <label for="upiId{booking_id}" class="form-label">UPI ID</label>
                    <input type="text" class="form-control" id="upiId{booking_id}" name="upi_id" placeholder="Enter your UPI ID">
                  </div>
                  <input type="hidden" name="pay" value="1">
                  <input type="hidden" name="booking_id" value="{booking_id}">
                  <input type="hidden" name="id" value="{user_id}">
                  <input type="hidden" name="service_price" value="{total}">
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                  <button type="submit" class="btn btn-success">
                    <i class="bi bi-credit-card me-1"></i> Pay ₹{total:.2f}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        """)

print("""
   

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleUpiField(selectElement) {
            const upiField = selectElement.closest('.modal-body').querySelector('.upi-field');
            if (selectElement.value === 'upi') {
                upiField.style.display = 'block';
                upiField.querySelector('input').required = true;
            } else {
                upiField.style.display = 'none';
                upiField.querySelector('input').required = false;
            }
        }
    </script>
</body>
</html>
""")

# Close database connection
cur.close()
cur2.close()
con.close()