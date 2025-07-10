#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

cgitb.enable()

def send_email(to_email, subject, message):
    try:
        # Email configuration
        sender_email = "farizfreakin@gmail.com"  # Replace with your email
        sender_password = "trih xamr rooy pbnr"   # Replace with your app password
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

form = cgi.FieldStorage()
Uid = form.getvalue("id")
if Uid:
    a = "select * from usereg where id=%s"
    cur.execute(a, (Uid,))
    user = cur.fetchall()

# Get careid from URL parameters
careid = form.getvalue("careid")
s = "select * from careresource_info where careid=%s"
cur.execute(s, (careid,))
cares = cur.fetchall()



# Build approve link with ID


# HTML Header (similar to your existing one)
print("""
      <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Care Center | PetMatch</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Chewy&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4e73df;
            --secondary-color: #1cc88a;
            --dark-color: #2d3748;
            --light-color: #f8f9fa;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--light-color);
            color: var(--dark-color);
        }
        
        .navbar {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .navbar-brand {
            font-family: 'Chewy', cursive;
            font-size: 1.8rem;
            color: var(--primary-color) !important;
        }
        
        .center-header {
            background: linear-gradient(rgba(78, 115, 223, 0.1), rgba(78, 115, 223, 0.05));
            padding: 3rem 0;
            margin-bottom: 3rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        .center-title {
            font-family: 'Chewy', cursive;
            color: var(--primary-color);
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .center-image {
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            height: 100%%;
            object-fit: cover;
            max-height: 400px;
        }
        
        .center-details {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }
        
        .detail-item {
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px dashed #eee;
        }
        
        .detail-item:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .btn-apply {
            background-color: var(--secondary-color);
            border: none;
            padding: 12px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(28, 200, 138, 0.3);
        }
        
        .btn-apply:hover {
            background-color: #17a673;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(28, 200, 138, 0.4);
        }
        
        .service-features {
            margin-top: 3rem;
        }
        
        .feature-icon {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
        
        footer {
           
            color:clack;
            padding: 2rem 0;
            margin-top: 4rem;
        }
        
        .social-icon {
            color: white;
            font-size: 1.5rem;
            margin: 0 10px;
            transition: all 0.3s ease;
        }
        
        .social-icon:hover {
            color: var(--secondary-color);
            transform: translateY(-3px);
        }
        
        .application-form {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            margin-top: 3rem;
        }
        
        .form-label {
            font-weight: 600;
            color: var(--dark-color);
        }
        
        @media (max-width: 768px) {
            .center-header {{
                padding: 2rem 0;
            }
            
            .center-title {
                font-size: 2rem;
            }
            
            .center-image {
                margin-bottom: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
        <div class="container">
            <a class="navbar-brand" href="usercare.py">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="usercare.py?id=%s">Home</a>
                    </li>
                     <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="ordersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> My Orders
                        </a>
                        <ul class="dropdown-menu">
                            
                            <li><a class="dropdown-item" href="careaprove.py?id=%s"><i class="fas fa-check-circle me-2"></i>Requests</a></li>
                            
                        </ul>
                    </li>
                   </ul> 
                </div>
            </div>
        </div>
    </nav>""" %(Uid,Uid))
for i in cares:
    useris=i[0]

    print(f"""<!-- Care Center Header -->
    <section class="center-header">
        <div class="container text-center">
            <h1 class="center-title">{i[2]}</h1>
            <p class="lead">{i[3]} | {i[5]}</p>
        </div>
    </section>

    <!-- Care Center Details Section -->
    <div class="container">
        <div class="row">
            <!-- Main Image -->
            <div class="col-lg-6 mb-4">
                <img src="./images/{i[14]}" alt="Happy Paws Veterinary" class="img-fluid center-image w-100">
            </div>
            
            <!-- Details -->
            <div class="col-lg-6">
                <div class="center-details h-100">
                    <h2 class="mb-4">About {i[2]} </h2>
                    
                    <div class="detail-item">
                        <span class="detail-label">Service Type:</span> {i[3]}
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-label">Address:</span> {i[4]}
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-label">Location:</span> {i[5]}
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-label">Contact:</span> {i[9]}
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-label">Email:</span> {i[10]}
                    </div>
                    
                    
                    
                    <div class="detail-item">
                        <span class="detail-label">Description:</span>
                        <p>{i[12]}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Service Features -->
        <div class="row service-features">
            <div class="col-md-4 text-center mb-4">
                <div class="feature-icon">
                    <i class="fas fa-stethoscope"></i>
                </div>
                <h4>Professional Staff</h4>
                <p>Our team consists of certified and experienced professionals.</p>
            </div>
            
            <div class="col-md-4 text-center mb-4">
                <div class="feature-icon">
                    <i class="fas fa-clock"></i>
                </div>
                <h4>Flexible Hours</h4>
                <p>We offer services during convenient hours including weekends.</p>
            </div>
            
            <div class="col-md-4 text-center mb-4">
                <div class="feature-icon">
                    <i class="fas fa-heart"></i>
                </div>
                <h4>Compassionate Care</h4>
                <p>We treat every pet with love and attention they deserve.</p>
            </div>
        </div>""")


    for j in cares:

            careid=j[0]
            carecenter=j[2]
            caretype=j[3]
            Location=j[4]
            Image=j[10]
            print(f"""        <!-- Service Application Form -->
                           <!-- Service Application Form -->
        <div class="application-form">
            <h3 class="text-center mb-4">Apply for Service</h3>

            <form method="post" enctype="multipart/form-data">
                <!-- Center ID: {careid} -->
                <input type="hidden" name="centerid" value="{careid}">
                <input type="hidden" name="userid" value="{Uid}">
                <input type="hidden" name="name" value="{carecenter}">
                <input type="hidden" name="location" value="{Location}">
                <input type="hidden" name="image" value="{Image}">

                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Service Type</label>
                        <select class="form-select" name="caretype" required>
                            <option value="">Select Service Type</option>""")

            # Fetch services for this care center
            services_query = "SELECT id, servicetype, serviceprice FROM serviceprice WHERE careid = %s"
            cur.execute(services_query, (careid,))
            services = cur.fetchall()

            for service in services:
                print(f"""
                            <option value="{service[0]}">{service[1]} (Rs.{service[2]})</option>""")

            print("""
                        </select>
                    </div>

                    <div class="col-md-6 mb-3">
                        <label class="form-label">Your Pet Species</label>
                        <select class="form-select" name="species" id="pet_species" required onchange="updateBreeds()">
                            <option value="">Select your pet species</option>
                            <option value="dog">Dog</option>
                            <option value="cat">Cat</option>
                            <option value="bird">Bird</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div class="col-md-6 mb-3">
                        <label class="form-label">Your Pet Breed</label>
                        <select class="form-select" name="breed" id="pet_breed" required>
                            <option value="">Select species first</option>
                        </select>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Preferred Appointment Date</label>
                        <input type="date" class="form-control" name="date" required min="2023-07-01">
                    </div>

                    <div class="col-md-6 mb-3">
                        <label class="form-label">Special Notes</label>
                        <textarea class="form-control" name="notes" rows="1" placeholder="Any special requirements"></textarea>
                    </div>
                </div>

                <div class="text-center mt-4">
                    <input type="submit" name="submit" value="Send Application" class="btn btn-apply btn-lg">
                        
                </div>
            </form>
        </div>""")

print("""   <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                
            <div class="text-center">
                <p class="mb-0">&copy; 2023 PetMatch. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JavaScript -->
    <script>
        // Breed data
        const breedData = {
            dog: ["Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog", "Beagle", 
                 "Poodle", "Rottweiler", "Yorkshire Terrier", "Boxer", "Dachshund"],
            cat: ["Persian", "Maine Coon", "Siamese", "Ragdoll", "Bengal", 
                 "British Shorthair", "Abyssinian", "Scottish Fold", "Sphynx", "Russian Blue"],
            bird: ["Parakeet", "Cockatiel", "Lovebird", "Canary", "Finch",
                  "African Grey", "Macaw", "Cockatoo", "Amazon Parrot", "Budgerigar"],
            other: ["Rabbit", "Hamster", "Guinea Pig", "Ferret", "Turtle",
                   "Snake", "Lizard", "Fish", "Hedgehog", "Chinchilla"]
        };
        
        function updateBreeds() {
            const speciesSelect = document.getElementById('pet_species');
            const breedSelect = document.getElementById('pet_breed');
            const selectedSpecies = speciesSelect.value;
            
            // Clear existing options
            breedSelect.innerHTML = '';
            
            if (selectedSpecies) {
                // Add default option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Select breed';
                breedSelect.appendChild(defaultOption);
                
                // Add breeds for selected species
                breedData[selectedSpecies].forEach(breed => {
                    const option = document.createElement('option');
                    option.value = breed;
                    option.textContent = breed;
                    breedSelect.appendChild(option);
                });
            } else {
                // No species selected
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'Select species first';
                breedSelect.appendChild(option);
            }
        }
    </script>

</body>
</html>
      """)
Userid = form.getvalue('userid')
Name = form.getvalue('name')
Caretype = form.getvalue('caretype')  # This will now be the service ID
Location = form.getvalue('location')
Breed = form.getvalue('breed')
Prof = form.getvalue('image')
Date = form.getvalue('date')
Notes = form.getvalue('notes')
Centerid = form.getvalue('centerid')
Species = form.getvalue('species')
Submit = form.getvalue('submit')

if Submit:
    try:
        # Get the service type from serviceprice table using the ID
        service_query = "SELECT servicetype, serviceprice FROM serviceprice WHERE id = %s"
        cur.execute(service_query, (Caretype,))
        service_result = cur.fetchone()
        if service_result:
            service_type = service_result[0]
            service_price = service_result[1]
        else:
            service_type = Caretype  # Fallback to the ID if service not found
            service_price = 0

        # Insert the record with service type
        query = """INSERT INTO carebookings 
                   (centerid, centername, caretype, species, breed, prof, location, notes, date, userid, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'requested')"""
        cur.execute(query, (Centerid, Name, service_type, Species, Breed, Prof, Location, Notes, Date, Userid))
        con.commit()

        # Get the last inserted carebookingid
        booking_id = cur.lastrowid

        # Update the serviceprice table with the carebookingid
        update_query = "UPDATE serviceprice SET serviceid = %s WHERE id = %s"
        cur.execute(update_query, (booking_id, Caretype))
        con.commit()

        # Get center email from careresource_info
        email_query = "SELECT mail FROM careresource_info WHERE careid = %s"
        cur.execute(email_query, (Centerid,))
        center_email = cur.fetchone()[0]

        # Send email notification to the care center
        subject = "New Care Service Application"
        message = f"""Dear {Name} Team,

A new care service application has been submitted:

Booking ID: {booking_id}
Service Type: {service_type}
Pet Species: {Species}
Pet Breed: {Breed}
Appointment Date: {Date}
Special Notes: {Notes}

Please review this application at your earliest convenience.

Best regards,
PetMatch Team"""

        if send_email(center_email, subject, message):
            print("""
            <script>
            alert("Care Service application submitted successfully! A notification has been sent to the care center.");
            window.location.href = "usercare.py?id=" + """ + str(Userid) + """;
            </script>
            """)
        else:
            print("""
            <script>
            alert("Care Service application submitted successfully! However, there was an error sending the notification email.");
            window.location.href = "usercare.py?id=" + """ + str(Userid) + """;
            </script>
            """)
    except Exception as e:
        print(f"""
        <div class="alert alert-danger">
            <h4>Error submitting application</h4>
            <p>Error details: {str(e)}</p>
            <p>Please try again or contact support if the problem persists.</p>
        </div>
        """)
    finally:
        if 'con' in locals() and con.open:
            con.close()