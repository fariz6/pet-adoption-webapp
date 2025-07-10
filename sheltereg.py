#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os
import re
import json

cgitb.enable()

# Dictionary of Indian states and their cities
states_cities = {
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"],
    # Add more states and cities as needed
}

def safe_write_file(filepath, content):
    """Helper function to safely write files with proper encoding"""
    try:
        with open(filepath, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {filepath}: {str(e)}")
        raise

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shelter Registration</title>
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
            min-height: 100vh;
            margin: 0;
            padding: 0;
            background: url('images/shelter-bg.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .registration-container {
            max-width: 800px;
            width: 90%;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            margin: 20px;
        }

        .registration-header {
            background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }

        .registration-header i {
            font-size: 3rem;
            margin-bottom: 15px;
        }

        .registration-body {
            padding: 30px;
        }

        .form-control {
            border-radius: 8px;
            padding: 12px 15px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s;
        }

        .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.25rem rgba(108, 99, 255, 0.25);
        }

        .btn-register {
            background: linear-gradient(135deg, #6c63ff 0%, #4a43d6 100%);
            border: none;
            padding: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s;
        }

        .btn-register:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3);
        }

        .invalid-feedback {
            display: none;
            color: #dc3545;
            font-size: 0.875em;
            margin-top: 5px;
        }

        .was-validated .form-control:invalid ~ .invalid-feedback,
        .form-control.is-invalid ~ .invalid-feedback {
            display: block;
        }

        .was-validated .form-control:invalid,
        .form-control.is-invalid {
            border-color: #dc3545;
        }

        @media (max-width: 768px) {
            .registration-container {
                margin: 20px;
                border-radius: 10px;
            }

            .registration-body {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="registration-container">
        <div class="registration-header">
            <i class="fas fa-home"></i>
            <h2>Shelter Registration</h2>
        </div>
        <div class="registration-body">
            <form method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="shelterName" class="form-label">Shelter Name</label>
                    <input type="text" class="form-control" id="shelterName" name="name" placeholder="Enter your shelter name" required>
                </div>
                <div class="mb-3">
                    <label for="ownerName" class="form-label">Owner Name</label>
                    <input type="text" class="form-control" id="ownerName" name="owner" placeholder="Enter owner name" required>
                </div>
                <div class="mb-3">
                    <label for="street" class="form-label">Street/Door No.</label>
                    <input type="text" class="form-control" id="street" name="street" placeholder="Enter your street/door no." required>
                </div>
                <div class="mb-3">
                    <label for="state" class="form-label">State</label>
                    <select class="form-control" id="state" name="state" required onchange="updateCities()">
                        <option value="">Select State</option>
                        <option value="Kerala">Kerala</option>
                        <option value="Tamil Nadu">Tamil Nadu</option>
                        <option value="Karnataka">Karnataka</option>
                        <option value="Maharashtra">Maharashtra</option>
                        <option value="Delhi">Delhi</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="place" class="form-label">City</label>
                    <select class="form-control" id="place" name="place" required>
                        <option value="">Select City</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input type="text" class="form-control" id="pincode" name="pin" placeholder="Enter your pincode" required>
                </div>
                <div class="mb-3">
                    <label for="mobile" class="form-label">Mobile Number</label>
                    <input type="number" class="form-control" id="mobile" name="mobile" placeholder="Enter your mobile number" required>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                </div>

                <div class="mb-3">
                    <label for="profilePic" class="form-label">Profile Picture</label>
                    <input type="file" class="form-control" id="profilePic" name="profile" required>
                </div>
                <div class="mb-3">
                    <label for="adhaarProof" class="form-label">Adhaar Proof</label>
                    <input type="file" class="form-control" id="adhaarProof" name="aadhar" required>
                </div>
                <div class="mb-3">
                    <label for="shelterLicense" class="form-label">Shelter License</label>
                    <input type="file" class="form-control" id="shelterLicense" name="license" required>
                </div>
                <input type="submit" value="Register" name="register" class="btn btn-primary btn-register w-100">
            </form>
        </div>
    </div>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const statesCities = {
            "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
            "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
            "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"]
        };

        function updateCities() {
            const stateSelect = document.getElementById('state');
            const citySelect = document.getElementById('place');
            const selectedState = stateSelect.value;

            // Clear current options
            citySelect.innerHTML = '<option value="">Select City</option>';

            if (selectedState && statesCities[selectedState]) {
                statesCities[selectedState].forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            }
        }
    </script>
</body>
</html>
""")

form = cgi.FieldStorage()
Shelter = form.getvalue("name")
Owner = form.getvalue("owner")
DOB = form.getvalue("dob")
Street = form.getvalue("street")
Place = form.getvalue("place")
Pincode = form.getvalue("pin")
State = form.getvalue("state")
Mobile = form.getvalue("mobile")
Email = form.getvalue("email")

Submit = form.getvalue("register")

if Submit != None:
    # Validation checks
    validation_passed = True
    error_messages = []

    # Indian mobile number validation (10 digits starting with 6-9)
    if not Mobile or not Mobile.isdigit() or len(Mobile) != 10 or Mobile[0] not in ['6', '7', '8', '9']:
        validation_passed = False
        error_messages.append("Please enter a valid 10-digit Indian mobile number starting with 6, 7, 8 or 9")

    # Pincode validation (6 digits)
    if not Pincode or not Pincode.isdigit() or len(Pincode) != 6:
        validation_passed = False
        error_messages.append("Please enter a valid 6-digit pincode")

    # Email format validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not Email or not re.match(email_regex, Email):
        validation_passed = False
        error_messages.append("Please enter a valid email address")

    # Check if email already exists in database
    if Email:
        cur.execute("SELECT COUNT(*) FROM shelter_info WHERE email = %s", (Email,))
        email_count = cur.fetchone()[0]
        if email_count > 0:
            validation_passed = False
            error_messages.append("This email is already registered. Please use a different email address.")

    if not validation_passed:
        print("<script>alert('" + "\\n".join(error_messages) + "')</script>")
        con.close()
        exit()

    # Continue with file upload and database insertion if validation passed
    Prof = form['profile']
    Aadharr = form['aadhar']
    License = form['license']
    a = os.path.basename(Prof.filename)
    b = os.path.basename(Aadharr.filename)
    c = os.path.basename(License.filename)
    open("images/" + a,'wb').write(Prof.file.read())
    open("images/" + b,'wb').write(Aadharr.file.read())
    open("images/" + c,'wb').write(License.file.read())
    c = """insert into shelter_info(sheltername,ownername,street,city,pin,state,mob,email,profile_pic,proof_attachment,license) values
    ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" % (
        Shelter, Owner, Street, Place, Pincode, State, Mobile, Email, a, b, c)
    cur.execute(c)
    con.commit()
    print("""
              <script>
              alert("Registration successful! Your login credentials sent to your mail once the admin approve it.")
              location.href="homepage.py" 
              </script>
        """)

con.close()