#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

Pid = form.getvalue("product_id")


# Fetch all pets from the database
s = """select * from product_info where product_id="%s" """ % (Pid)
cur.execute(s)
pets = cur.fetchall()

Uid = form.getvalue("id")
u = """select * from usereg where id="%s" """ % (Uid)
cur.execute(u)
user = cur.fetchall()



# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meet Max - Pet Adoption</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Chewy&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color:#4e73df;
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
            color: var(--primary-color);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .navbar-brand {
            font-family: 'Chewy', cursive;
            font-size: 1.8rem;
            color: var(--primary-color) !important;
        }

        .pet-header {
            background: linear-gradient(rgba(78, 115, 223, 0.1), rgba(78, 115, 223, 0.05));
            padding: 3rem 0;
            margin-bottom: 3rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }

        .pet-title {
            font-family: 'Chewy', cursive;
            color: var(--primary-color);
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        }

        .pet-image {
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
            height: 100%%;
            object-fit: cover;
        }

        .pet-image:hover {
            transform: scale(1.02);
        }

        .pet-details {
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

        .btn-adopt {
            background-color: var(--secondary-color);
            border: none;
            padding: 12px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(28, 200, 138, 0.3);
        }

        .btn-adopt:hover {
            background-color: #17a673;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(28, 200, 138, 0.4);
        }

        .pet-features {
            margin-top: 3rem;
        }

        .feature-icon {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        .gallery-item {
            margin-bottom: 1.5rem;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }

        .gallery-item img {
            transition: transform 0.5s ease;
        }

        .gallery-item:hover img {
            transform: scale(1.1);
        }

        footer {
          
            color: black;
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

        @media (max-width: 768px) {
            .pet-header {
                padding: 2rem 0;
            }

            .pet-title {
                font-size: 2rem;
            }

            .pet-image {
                margin-bottom: 2rem;
            }
        }

        .adoption-modal .modal-content {
            border-radius: 15px;
            overflow: hidden;
            border: none;
        }

        .adoption-modal .modal-header {
            background-color: var(--primary-color);
            color: white;
            border-bottom: none;
            padding: 1.5rem;
        }

        .adoption-modal .modal-header .btn-close {
            filter: invert(1);
            opacity: 0.8;
        }

        .adoption-modal .modal-header .btn-close:hover {
            opacity: 1;
        }

        .adoption-modal .modal-body {
            padding: 2rem;
        }

        .adoption-modal .pet-info {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px dashed #eee;
        }

        .adoption-modal .pet-image {
            width: 80px;
            height: 80px;
            border-radius: 10px;
            object-fit: cover;
            margin-right: 1rem;
        }

        .adoption-modal .pet-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: var(--dark-color);
        }

        .adoption-modal .pet-details {
            color: #6c757d;
            font-size: 0.9rem;
        }

        .adoption-steps {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            position: relative;
        }

        .adoption-steps:before {
            content: '';
            position: absolute;
            top: 15px;
            left: 0;
            right: 0;
            height: 2px;
            background-color: #e9ecef;
            z-index: 1;
        }

        .step {
            text-align: center;
            position: relative;
            z-index: 2;
        }

        .step-number {
            width: 32px;
            height: 32px;
            border-radius: 50%%;
            background-color: #e9ecef;
            color: #6c757d;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.5rem;
            font-weight: 600;
        }

        .step.active .step-number {
            background-color: var(--primary-color);
            color: white;
        }

        .step.completed .step-number {
            background-color: var(--secondary-color);
            color: white;
        }

        .step-label {
            font-size: 0.8rem;
            color: #6c757d;
            font-weight: 500;
        }

        .step.active .step-label {
            color: var(--primary-color);
            font-weight: 600;
        }

        .step.completed .step-label {
            color: var(--secondary-color);
        }

        .form-section {
            display: none;
        }

        .form-section.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .form-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #eee;
        }

        .btn-prev {
            background-color: #f8f9fa;
            color: var(--dark-color);
            border: 1px solid #dee2e6;
            padding: 0.5rem 1.5rem;
        }

        .btn-next, .btn-submit {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
        }

        .btn-next:hover, .btn-submit:hover {
            background-color: #5a52e0;
            color: white;
        }

        .form-check-input:checked {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }

        .form-control:focus, .form-select:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.25rem rgba(108, 99, 255, 0.25);
        }

        .thank-you-content {
            text-align: center;
            padding: 2rem 0;
        }

        .thank-you-icon {
            font-size: 4rem;
            color: var(--secondary-color);
            margin-bottom: 1.5rem;
        }

        .thank-you-content h4 {
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
         /* Custom styles for the modal */
        .adoption-modal .modal-header {
            background: linear-gradient(135deg, #6C63FF 0%%, #FF6584 100%%);
            color: white;
        }
        
        .thank-you-message {
            background-color: #f0f8ff;
            border-left: 5px solid #6C63FF;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        .pet-image-modal {
            width: 100%%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        
        .btn-adopt {
            background: linear-gradient(135deg, #6C63FF 0%%, #FF6584 100%%);
            border: none;
            padding: 10px 25px;
            font-weight: 600;
        }
        
        .btn-adopt:hover {
            opacity: 0.9;
        }
        
        .user-info-display {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw me-2"></i>PetAdopt
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="browsepet.py?id=%s">Home</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="myOrdersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> Pet Bookings
                        </a>
                        
                        <ul class="dropdown-menu">
                             <li><a class="dropdown-item" href="userrecent.py?id=%s">Recent</a></li>
                           
                            <li><a class="dropdown-item" href="userejected.py?id=%s">Rejected</a></li>
                            <li><a class="dropdown-item" href="usercomplete.py?id=%s">Approved</a></li>
                        </ul>
                    </li>
                </ul>
                
            </div>
        </div>
    </nav>""" %(Uid,Uid,Uid,Uid))

for i in pets:
    Petname = i[5]
    Breed = i[7]
    Age = i[10]
    Gender = i[8]
    Animalimg = i[12]
    Animalimg2 = i[13]
    Animalimg3 = i[14]
    desc=i[11]

    print(f"""    <!-- Pet Header -->
    <section class="pet-header">
        <div class="container text-center">
            <h1 class="pet-title">Meet {Petname} </h1>
            <p class="lead">{Breed} | {Age} years old | {Gender}</p>
        </div>
    </section>

    <!-- Pet Details Section -->
    <div class="container">
        <div class="row">
            <!-- Main Image -->
            <div class="col-lg-6 mb-4">
                <img src="./images/{Animalimg}" alt="{Petname}" class="img-fluid pet-image w-100" style="height: 500px;">
            </div>

            <!-- Details -->
            <div class="col-lg-6">
                <div class="pet-details h-100">
                    <h2 class="mb-4">About {Petname}</h2>

                    <div class="detail-item">
                        <span class="detail-label">Breed:</span> {Breed}
                    </div>

                    <div class="detail-item">
                        <span class="detail-label">Age:</span> {Age} years
                    </div>






                    <div class="detail-item">
                        <span class="detail-label">Description:</span>
                        <p>{desc}</p>
                    </div>

                    <div class="text-center mt-4">
                        <input type="submit" value="Adopt {Petname}" class="btn btn-adopt btn-lg" id="adoptBtn" data-bs-toggle="modal" data-bs-target="#adoptionModal">

                    </div>
                </div>
            </div>
        </div>

        

        <!-- Photo Gallery -->
        <h3 class="text-center mb-4">More Photos of {Petname}</h3>
        <div class="row">
            <div class="col-md-4 gallery-item">
                <img src="./images/{Animalimg}" alt="{Petname} playing" class="img-fluid w-100" style="height: 250px; object-fit: cover;">
            </div>
            <div class="col-md-4 gallery-item">
                <img src="./images/{Animalimg2}" alt="{Petname} with ball" class="img-fluid w-100" style="height: 250px; object-fit: cover;">
            </div>
            <div class="col-md-4 gallery-item">
                <img src="./images/{Animalimg3}" alt="{Petname} smiling" class="img-fluid w-100" style="height: 250px; object-fit: cover;">
            </div>
        </div>
    </div>

   <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                
           
            <div class="text-center">
                <p class="mb-0">&copy; 2023 PetAdopt. All rights reserved.</p>
            </div>
        </div>
    </footer>""")

# Fetch user data for the modal (only once)

    for i in pets:
        Petname = i[5]
        Species = i[6]
        Breed = i[7]
        Age = i[10]
        Gender = i[8]
        Animalimg = i[12]
        Animalimg2 = i[13]
        Animalimg3 = i[14]

        print(f"""  
 <!-- Adoption Modal -->
<div class="modal fade adoption-modal" id="adoptionModal" tabindex="-1" aria-labelledby="adoptionModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="adoptionModalLabel"><i class="fas fa-paw me-2"></i> Pet Adoption Application</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <!-- Thank You Message -->
                <div class="thank-you-message">
                    <h6><i class="fas fa-heart text-danger me-2"></i> Thank You for Adopting!</h6>
                    <p class="mb-0">By adopting a pet, you're giving an animal a second chance at life.</p>
                </div>
                
                <!-- Pet Image -->
                
                
                <!-- Adoption Form -->
                <form id="adoptionForm" method="post" enctype="multipart/form-data">
                    <!-- Hidden Fields -->
                    <input type="hidden" id="userId" name="species" value="{Species}">
                    
                    <input type="hidden" id="productId" name="productid" value="{Pid}">
                     <input type="hidden" id="userId" name="name" value="{Petname}">
                    <input type="hidden" id="userProfile" name="breed" value="{Breed}">
                    <input type="hidden" id="userProfile" name="prof" value="{Animalimg}">
                    <input type="hidden" id="userProfile" name="userid" value="{Uid}">

                    <!-- Add Booking Date Field -->
                    <div class="mb-3">
                        <label for="bookingDate" class="form-label">Preferred Adoption Date</label>
                        <input type="date" class="form-control" id="bookingDate" name="bookingDate" required>
                    </div>
                    
                    <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <input type="submit" value="Send Application" name="submitS" class="btn btn-adopt text-white" id="submitAdoption">
                   
            </div>
                   
                </form>
            </div>
            
        </div>
    </div>
</div>""")

print(""" <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
       

            // Add modal to body
            document.body.insertAdjacentHTML('beforeend', modalHTML);

            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('adoptModal'));
            modal.show();

            // Remove modal after it's hidden
            document.getElementById('adoptModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
        });
         // Step navigation
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', function() {
            const nextStep = this.getAttribute('data-next');
            document.querySelector('.form-section.active').classList.remove('active');
            document.getElementById('step' + nextStep).classList.add('active');

            // Update step indicators
            document.querySelector('.step.active').classList.remove('active');
            document.querySelector(`.step[data-step="${nextStep}"]`).classList.add('active');
        });
    });

    document.querySelectorAll('.btn-prev').forEach(button => {h
        button.addEventListener('click', function() {
            const prevStep = this.getAttribute('data-prev');
            document.querySelector('.form-section.active').classList.remove('active');
            document.getElementById('step' + prevStep).classList.add('active');

            // Update step indicators
            document.querySelector('.step.active').classList.remove('active');
            document.querySelector(`.step[data-step="${prevStep}"]`).classList.add('active');
        });
    });

    // Toggle current pets field based on pet experience
    document.querySelectorAll('input[name="petExperience"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.getElementById('currentPetsContainer').style.display = 
                this.value === 'yes' && this.id === 'experienceYes' ? 'block' : 'none';
        });
    });

    // Form submission
    document.getElementById('submitApplication').addEventListener('click', function() {
        // Validate form
        if (!document.getElementById('agreeTerms').checked) {
            alert('Please agree to the Terms of Adoption');
            return;
        }

        // In a real app, you would submit the form data to your server here
        // For demo, we'll just show the thank you message

        // Hide current form and show thank you message
        document.querySelector('.form-section.active').classList.remove('active');
        document.getElementById('thankYou').style.display = 'block';

        // Mark all steps as completed
        document.querySelectorAll('.step').forEach(step => {
            step.classList.add('completed');
            step.classList.remove('active');
        });
    });

    // Populate review sections (in a real app, this would be more dynamic)
    // This is just a simple example
    document.querySelectorAll('.btn-next[data-next="4"]').forEach(button => {
        button.addEventListener('click', function() {
            // Personal Info
            document.getElementById('reviewPersonalInfo').innerHTML = `
                <p><strong>Name:</strong> ${document.getElementById('firstName').value} </p>
                <p><strong>Email:</strong> ${document.getElementById('email').value}</p>
                <p><strong>Phone:</strong> ${document.getElementById('phone').value}</p>
                <p><strong>Address:</strong> ${document.getElementById('address').value}, ${document.getElementById('city').value}, ${document.getElementById('state').value} ${document.getElementById('zip').value}</p>
            `;

            
            
            
            document.getElementById('reviewHomeDetails').innerHTML = `
                <p><strong>Housing Type:</strong> ${document.getElementById('housingType').value}</p>
                <p><strong>Ownership:</strong> ${document.getElementById('ownership').value}</p>
                <p><strong>Yard:</strong> ${document.querySelector('input[name="yard"]:checked')?.value || 'Not specified'}</p>
            `;
            
            // Experience
            document.getElementById('reviewExperience').innerHTML = `
                <p><strong>Previous Pets:</strong> ${document.querySelector('input[name="petExperience"]:checked')?.value === 'yes' ? 'Yes' : 'No'}</p>
                ${document.getElementById('currentPets').value ? `<p><strong>Current Pets:</strong> ${document.getElementById('currentPets').value}</p>` : ''}
                <p><strong>Daily Routine:</strong> ${document.getElementById('dailyRoutine').value}</p>
                <p><strong>Adoption Reason:</strong> ${document.getElementById('adoptionReason').value}</p>
            `;
        });
    });
    $(document).ready(function() {
    // Handle form submission
    $('#submitAdoption').click(function() {
        // Validate form
        if (!$('#experience').val()) {
            alert('Please select your pet experience level');
            return;
        }
        
        // Collect form data
        const formData = {
            userId: $('#userId').val(),
            userName: $('#userName').val(),
            userEmail: $('#userEmail').val(),
            userCity: $('#userCity').val(),
            userProfile: $('#userProfile').val(),
            productId: $('#productId').val(),
            experience: $('#experience').val(),
            comments: $('#comments').val()
        };
        
        // Simulate AJAX submission (replace with actual AJAX call)
        console.log('Submitting adoption:', formData);
        
        // Show success message
        alert('Application sent successfully! Thank you for adopting.');
        
        // Close the modal after 1 second
        setTimeout(function() {
            $('#adoptionModal').modal('hide');
            
            // Optional: Reset form
            $('#adoptionForm')[0].reset();
            
            // Optional: Redirect or do something else
            // window.location.href = 'thank-you.html';
        }, 1000);
    });
    
    // You can populate the modal with dynamic data when it's shown
    $('#adoptionModal').on('show.bs.modal', function (event) {
        // Example of how to populate with dynamic data
        // In a real app, you would fetch this from your backend
        /*
        const userData = {
            id: "12345",
            name: "John Doe",
            email: "john@example.com",
            city: "New York",
            profile: "profile.jpg",
            petId: "PET-789"
        };
        
        $('#userId').val(userData.id);
        $('#userName').val(userData.name);
        $('.user-info-display:eq(0) div').text(userData.name);
        // ... and so on for other fields
        */
    });
});
    </script>
</body>
</html>
      """)


# Fetch form data using CGI

# Fetch form data using CGI
Userid = form.getvalue('userid')
Petname = form.getvalue('name')
Breed = form.getvalue('breed')
Prof= form.getvalue('prof')
Productid = form.getvalue('productid')
Species= form.getvalue('species')
Submit = form.getvalue('submitS')
BookingDate = form.getvalue('bookingDate')  # Get the booking date

# Debugging output


if Submit:
    try:
        # Reconnect if connection is closed
        if not con.open:
            con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
            cur = con.cursor()

        # Debug: Show bookings table structure


        # Insert the record with booking date
        query = """INSERT INTO bookings (id, product_id, animalname, species, breed, animalprof, day) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(query, (Userid, Productid, Petname, Species, Breed, Prof, BookingDate))
        con.commit()

        print("""
        <script>
        alert("Adoption application submitted successfully!");
        window.location.href
        </script>
        """)
    except Exception as e:
        print(f"""
        <div class="alert alert-danger">
            <h4>Error submitting application</h4>
            <p>{str(e)}</p>
            <p>Last executed query: {cur._last_executed if 'cur' in locals() else 'N/A'}</p>
        </div>
        """)
    finally:
        if 'con' in locals() and con.open:
            con.close()