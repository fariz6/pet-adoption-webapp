#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os, re
from datetime import datetime

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

form = cgi.FieldStorage()

def safe_write_file(filepath, content):
    """Helper function to safely write files with proper encoding"""
    try:
        with open(filepath, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {filepath}: {str(e)}")
        raise

def validate_mobile(mob):
    if not mob:
        return False, "Mobile number is required"
    if not re.match(r'^[6-9]\d{9}$', mob):
        return False, "Please enter a valid 10-digit Indian mobile number starting with 6,7,8 or 9"
    return True, ""

# Function to validate email uniqueness
def validate_email(email):
    if not email or '@' not in email:
        return False, "Please enter a valid email address"
    cur.execute("SELECT COUNT(*) FROM usereg WHERE email = %s", (email,))
    count = cur.fetchone()[0]
    if count > 0:
        return False, "This email is already registered"
    return True, ""

# Function to validate pincode
def validate_pincode(pin):
    if not pin:
        return False, "Pincode is required"
    if not re.match(r'^[1-9]\d{5}$', pin):
        return False, "Please enter a valid 6-digit pincode (cannot start with 0)"
    return True, ""

# Function to validate age (18+)
def validate_age(dob):
    if not dob:
        return False, "Date of birth is required"
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return False, "You must be at least 18 years old to register"
        return True, ""
    except ValueError:
        return False, "Invalid date format"

# Function to validate password
def validate_password(password):
    if not password:
        return False, "Password is required"
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        return False, "Password must contain at least 8 characters with uppercase, lowercase, number and special character"
    return True, ""

# Process form submission
if 'reg' in form:
    name = form.getvalue("name")
    email = form.getvalue("email")
    mob = form.getvalue("mob")
    password = form.getvalue("pass")
    dob = form.getvalue("dob")
    pin = form.getvalue("pin")
    gender = form.getvalue("gender")
    street = form.getvalue("street")
    state = form.getvalue("state")
    city = form.getvalue("city")

    # Validate all fields
    errors = []

    # Name validation
    if not name or len(name) < 3:
        errors.append("Name must be at least 3 characters long")

    # Email validation
    email_valid, email_error = validate_email(email)
    if not email_valid:
        errors.append("email_error")

    # Mobile validation
    mobile_valid, mobile_error = validate_mobile(mob)
    if not mobile_valid:
        errors.append("mobile_error")

    # Password validation
    password_valid, password_error = validate_password(password)
    if not password_valid:
        errors.append("password_error")

    # Age validation
    age_valid, age_error = validate_age(dob)
    if not age_valid:
        errors.append("age_error")

    # Pincode validation
    pincode_valid, pincode_error = validate_pincode(pin)
    if not pincode_valid:
        errors.append("pincode_error")

    # Gender validation
    if not gender:
        errors.append("Please select your gender")

    # Address validation
    if not street:
        errors.append("Please enter your street address")

    # State validation
    if not state:
        errors.append("Please select your state")

    # City validation
    if not city:
        errors.append("Please select your city")

    # Check if files were uploaded
    if 'img1' not in form or not form['img1'].filename:
        errors.append("Please upload a profile picture")
    if 'img2' not in form or not form['img2'].filename:
        errors.append("Please upload your ID proof")

    if not errors:
        try:
            Prof = form['img1']
            Aadharr = form['img2']
            a = os.path.basename(Prof.filename)
            b = os.path.basename(Aadharr.filename)
            open("images/" + a,'wb').write(Prof.file.read())
            open("images/" + b,'wb').write(Aadharr.file.read())

            q = """INSERT INTO usereg(name, email, mob, pass, dob, gender, 
                            street, city, pin, state, profile_pic, proof_attachment) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(q, (
                name, email, mob, password, dob, gender,
                street, city, pin, state, a, b
            ))
            con.commit()

            # Success message
            print("""
                    <script>
                    alert("Registration successful!\\n\\nYou can now login with your credentials.");
                    window.location.href = "userlogin.py";
                    </script>
                    """)
            cur.close()
            con.close()
            exit()
        except Exception as e:
            errors.append(f"An error occurred during registration: {str(e)}")

    # If there are errors, show them
    if errors:
        error_message = "\\n• ".join([""] + errors)  # Add bullet points
        print(f"""
                <script>
                alert("Please correct the following errors:\\n{error_message}");
                history.back();
                </script>
                """)
        exit()

# HTML Form (same as before)
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pet Adoption - User Registration</title>
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
            background: url('images/pet-bg.jpg') no-repeat center center fixed;
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
            <i class="fas fa-paw"></i>
            <h2>User Registration</h2>
        </div>
        <div class="registration-body">
            <form id="registrationForm" method="post" enctype="multipart/form-data">
                <!-- Full Name -->
                <div class="mb-4">
                    <label for="fullName" class="form-label">Full Name</label>
                    <input type="text" class="form-control" id="fullName" name="name" required minlength="3">
                    <div class="invalid-feedback">
                        Please enter a valid name (minimum 3 characters)
                    </div>
                </div>

                <!-- Email -->
                <div class="mb-4">
                    <label for="email" class="form-label">Email Address</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                    <div class="invalid-feedback">
                        Please enter a valid email address
                    </div>
                     <div class="password-requirements">
             Please enter a valid email address
        </div>
                </div>

              

                <!-- Password with Toggle -->
                <div class="mb-4">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="pass" required 
                           pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$">
                    <div class="invalid-feedback">
                        Password must contain at least 8 characters, including uppercase, lowercase, number, and special character
                    </div>
                    <small class="form-text text-muted">
                        Minimum 8 characters with at least one uppercase, one lowercase, one number and one special character (@$!%*?&)
                    </small>
                </div>
                  <!-- Mobile Number -->
                <div class="mb-4">
                    <label for="mobile" class="form-label">Mobile Number</label>
                    <input type="tel" class="form-control" id="mobile" name="mob" pattern="[6-9][0-9]{9}" required>
                    <div class="invalid-feedback">
                        Please enter a valid 10-digit Indian mobile number starting with 6,7,8 or 9
                    </div>
                      <div class="password-requirements">
                     
                        Please enter a valid 10-digit Indian mobile number starting with 6,7,8 or 9
                    </div>
                </div>

                <!-- Date of Birth -->
                <div class="mb-4">
                    <label for="dob" class="form-label">Date of Birth</label>
                    <input type="date" class="form-control" id="dob" name="dob" required max="">
                    <div class="invalid-feedback">
                        You must be at least 18 years old to register
                    </div>
                    <div class="password-requirements">
             You must be at least 18 years old to register
        </div>
                </div>

                <!-- Gender -->
                <div class="mb-4">
                    <label class="form-label">Gender</label>
                    <div class="gender-options">
                        <div class="gender-option">
                            <input type="radio" id="male" name="gender" value="Male" required>
                            <label for="male">Male</label>
                        </div>
                        <div class="gender-option">
                            <input type="radio" id="female" name="gender" value="Female">
                            <label for="female">Female</label>
                        </div>
                        <div class="gender-option">
                            <input type="radio" id="other" name="gender" value="Other">
                            <label for="other">Other</label>
                        </div>
                    </div>
                    <div class="invalid-feedback">
                        Please select your gender
                    </div>
                </div>

                <!-- Address -->
                <div class="mb-4">
                    <label for="street" class="form-label">Street Address</label>
                    <input type="text" class="form-control" id="street" name="street" required>
                    <div class="invalid-feedback">
                        Please enter your street address
                    </div>
                </div>

                <div class="row mb-4">
                    <div class="col-md-6">
                        <label for="state" class="form-label">State</label>
                        <select class="form-control" id="state" name="state" required>
                            <option value="">Select State</option>
                            <option value="Tamil Nadu">Tamil Nadu</option>
                            <option value="Andhra Pradesh">Andhra Pradesh</option>
                            <option value="Karnataka">Karnataka</option>
                            <option value="Kerala">Kerala</option>
                            <option value="Telangana">Telangana</option>
                            <option value="Maharashtra">Maharashtra</option>
                            <option value="Delhi">Delhi</option>
                            <option value="Other">Other</option>
                        </select>
                        <div class="invalid-feedback">
                            Please select your state
                        </div>
                    </div>
                    <div class="col-md-6">
                        <label for="city" class="form-label">City</label>
                        <select class="form-control" id="city" name="city" required>
                            <option value="">Select City</option>
                            <!-- Cities will be populated based on state selection -->
                        </select>
                        <div class="invalid-feedback">
                            Please select your city
                        </div>
                    </div>
                </div>

                <div class="mb-4">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input type="text" class="form-control" id="pincode" name="pin" pattern="[1-9][0-9]{5}" required>
                    <div class="invalid-feedback">
                        Please enter a valid 6-digit pincode (cannot start with 0)
                    </div>
                     <div class="password-requirements">
                     
                         Please enter a valid 6-digit pincode (cannot start with 0)
                    </div>
                </div>

                <!-- Profile Picture -->
                <div class="mb-4">
                    <label for="profilePic" class="form-label">Profile Picture</label>
                    <input type="file" class="form-control" id="profilePic" name="img1" accept="image/*" required>
                    <div class="invalid-feedback">
                        Please upload a profile picture
                    </div>
                </div>

                <!-- Proof Attachment -->
                <div class="mb-4">
                    <label for="proofAttachment" class="form-label">ID Proof (Aadhaar/Passport/Driving License)</label>
                    <input type="file" class="form-control" id="proofAttachment" name="img2" required>
                    <div class="invalid-feedback">
                        Please upload your ID proof
                    </div>
                </div>

                <!-- Submit Button -->
                <input type="submit" name="reg" class="btn btn-primary btn-register w-100 py-3">
            </form>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Set max date for DOB (18 years ago)
            var today = new Date();
            var maxDate = new Date();
            maxDate.setFullYear(today.getFullYear() - 18);
            document.getElementById('dob').max = maxDate.toISOString().split('T')[0];
        });
    </script>
    <script>
    // State-City mapping
    const stateCities = {
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Vellore", "Erode", "Thoothukudi", "Dindigul", "Thanjavur", "Hosur"],
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Rajahmundry", "Tirupati", "Kakinada", "Kadapa", "Anantapur"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi", "Davanagere", "Ballari", "Tumakuru", "Shivamogga", "Raichur"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Palakkad", "Kollam", "Alappuzha", "Kannur", "Kottayam", "Malappuram"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam", "Mahbubnagar", "Nalgonda", "Adilabad", "Suryapet"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Amravati", "Kolhapur", "Nanded", "Sangli"],
        "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi"],
        "Other": ["Other City"]
    };

    // Function to populate cities based on selected state
    function populateCities() {
        const stateSelect = document.getElementById('state');
        const citySelect = document.getElementById('city');
        
        // Clear existing options
        citySelect.innerHTML = '<option value="">Select City</option>';
        
        // Get selected state
        const selectedState = stateSelect.value;
        
        // If a state is selected, add its cities
        if (selectedState && stateCities[selectedState]) {
            stateCities[selectedState].forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        }
    }

    // Add event listener to state dropdown
    document.addEventListener('DOMContentLoaded', function() {
        // Set max date for DOB (18 years ago)
        var today = new Date();
        var maxDate = new Date();
        maxDate.setFullYear(today.getFullYear() - 18);
        document.getElementById('dob').max = maxDate.toISOString().split('T')[0];
        
        // Add event listener to state dropdown
        document.getElementById('state').addEventListener('change', populateCities);

        // Initialize cities if state is already selected
        if (document.getElementById('state').value) {
            populateCities();
        }
    });
    </script>
</body>
</html>""")