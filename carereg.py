#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os
import re
cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
def is_valid_mobile(mobile):
    return re.fullmatch(r"[6-9]\d{9}", mobile)

def is_valid_pincode(pincode):
    return re.fullmatch(r"\d{6}", pincode)

def is_unique_email(email):
    cur.execute("SELECT COUNT(*) FROM careresource_info WHERE mail=%s", (email,))
    return cur.fetchone()[0] == 0

def safe_write_file(filepath, content):
    """Helper function to safely write files with proper encoding"""
    try:
        with open(filepath, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {filepath}: {str(e)}")
        raise

print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Care Resource Registration</title>
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
            background: url('images/care-bg.jpg') no-repeat center center fixed;
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
            <i class="fas fa-user-md"></i>
            <h2>Care Resource Registration</h2>
        </div>
        <div class="registration-body">
            <form id="careResourceForm" method="post" enctype="multipart/form-data">
                <!-- Resource Information -->
                <div class="form-section">
                    <h5 class="mb-3 text-primary"><i class="fas fa-user-tie me-2"></i>Resource Information</h5>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="careresourcertype" class="form-label required-field">CareResource Type</label>
                            <select class="form-select" id="careresourcertype" name="careresourcertype" required>
                                <option value="" selected disabled>Select Resource Type</option>
                                <option value="Veterinarian">Vetnary</option>
                                <option value="Pet Groomer">Pet Groom</option>
                                <option value="Pet Trainer">Pet Train</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="careresourcername" class="form-label required-field">Resourcer Name</label>
                            <input type="text" class="form-control" id="careresourcername" name="careresourcername" required>
                        </div>
                    </div>
                </div>

                <!-- Center Information -->
                <div class="form-section">
                    <h5 class="mb-3 text-primary"><i class="fas fa-home me-2"></i>Center Information</h5>
                    <div class="mb-3">
                        <label for="carecentrename" class="form-label required-field">Center Name</label>
                        <input type="text" class="form-control" id="carecentrename" name="carecentername" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="street" class="form-label required-field">Street Address</label>
                        <input type="text" class="form-control" id="street" name="street" required>
                    </div>
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label for="state" class="form-label required-field">State</label>
                            <select class="form-select" id="state" name="state" required>
                                <option value="" selected disabled>Select State</option>
                                <option value="Tamil Nadu">Tamil Nadu</option>
                                <option value="Kerala">Kerala</option>
                                <option value="Karnataka">Karnataka</option>
                                <option value="Andhra Pradesh">Andhra Pradesh</option>
                                <option value="Telangana">Telangana</option>
                            </select>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="city" class="form-label required-field">City</label>
                            <select class="form-select" id="city" name="city" required >
                                <option value="" selected disabled>Select City</option>
                                <option value="Chennai">Chennai</option>
                                <option value="Coimbatore">Coimbatore</option>
                                <option value="Madurai">Madurai</option>
                                <option value="Tiruchirappalli">Tiruchirappalli</option>
                                <option value="Salem">Salem</option>
                                <option value="Tirunelveli">Tirunelveli</option>
                                <option value="Thanjavur">Thanjavur</option>
                                <option value="Vellore">Vellore</option>
                                <option value="Erode">Erode</option>
                                <option value="Thoothukudi">Thoothukudi</option>
                            </select>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="pincode" class="form-label required-field">Pincode</label>
                            <input type="text" class="form-control" id="pincode" name="pincode" maxlength="6" required>
                        </div>
                    </div>
                </div>

                <!-- Contact -->
                <div class="form-section">
                    <h5 class="mb-3 text-primary"><i class="fas fa-address-book me-2"></i>Contact Information</h5>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label required-field">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="mobile" class="form-label required-field">Mobile Number</label>
                            <input type="tel" class="form-control" id="mobile" name="mobile" pattern="[0-9]{10}" required>
                            
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label required-field">Description</label>
                        <textarea class="form-control" id="description" name="description" rows="4" required></textarea>
                    </div>
                </div>

                <!-- Uploads -->
                <div class="form-section">
                    <h5 class="mb-3 text-primary"><i class="fas fa-file-upload me-2"></i>Document Uploads</h5>
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label for="profilepic" class="form-label required-field">Profile Picture</label>
                            <div class="upload-btn btn btn-outline-primary w-100">
                                
                                <input type="file" value="Upload photo" id="profilepic" name="profilepic" required>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="centerpic" class="form-label required-field">Center Picture</label>
                            <div class="upload-btn btn btn-outline-primary w-100">
                                
                                <input type="file" value="Upload Center Photo" id="centerpic" name="centerpic" required>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="idproof" class="form-label required-field">ID Proof</label>
                            <div class="upload-btn btn btn-outline-primary w-100">
                                
                                <input type="file" value="Upload ID proof" id="idproof" name="idproof" required>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="licenserpic" class="form-label required-field">Center Licenser Photo</label>
                            <div class="upload-btn btn btn-outline-primary w-100">
                                
                                <input type="file" value="Upload Licenser Photo" id="licenserpic" name="licenserpic" required>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="d-grid gap-2 mt-4">
                    <input type="submit" name="register" value="Register" class="btn btn-primary btn-lg">
                </div>
            </form>
        </div>
    </div>
     <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
    document.getElementById('state').addEventListener('change', function() {
      const districtSelect = document.getElementById('city');
      
      if (this.value) {
        districtSelect.classList.add('active');
        districtSelect.setAttribute('required', '');
      } else {
        districtSelect.classList.remove('active');
        districtSelect.removeAttribute('required');
    });
    </script>
</body>
</html>
""")

form = cgi.FieldStorage()
Resourcetype = form.getvalue("careresourcertype")
Resourcername = form.getvalue("careresourcername")
Centername = form.getvalue("carecentername")

Street = form.getvalue("street")
Pincode = form.getvalue("pincode")
State = form.getvalue("state")
City = form.getvalue("city")
Email = form.getvalue("email")
Mobile = form.getvalue("mobile")
Description = form.getvalue("description")
Submit = form.getvalue("register")

if Submit is not None:
    if not is_unique_email(Email):
        print("""
            <script>
            alert("Email already exists. Please use a different email.");
            history.back();
            </script>
        """)
    elif not is_valid_pincode(Pincode):
        print("""
            <script>
            alert("Invalid pincode. Pincode must be exactly 6 digits.");
            history.back();
            </script>
        """)
    elif not is_valid_mobile(Mobile):
        print("""
            <script>
            alert("Invalid mobile number. Enter a valid Indian mobile number.");
            history.back();
            </script>
        """)
    else:
        Prof = form['profilepic']
        Centerpic = form['centerpic']
        Idproof = form['idproof']
        Licenserpic = form['licenserpic']
        if Prof.filename and Centerpic.filename and Idproof.filename and Licenserpic.filename:
            a = os.path.basename(Prof.filename)
            b = os.path.basename(Centerpic.filename)
            c = os.path.basename(Idproof.filename)
            d = os.path.basename(Licenserpic.filename)
            open("images/" + a,'wb').write( Prof.file.read())
            open("images/" + b,'wb').write (Centerpic.file.read())
            open("images/" + c,'wb').write( Idproof.file.read())
            open("images/" + d,'wb').write( Licenserpic.file.read())

            i = """INSERT INTO careresource_info(
                        centername,
                        centertype,
                        resourcername,
                        address,
                        city,
                        state,
                        pin,
                        mob,
                        mail,
                        description,
                        Image,
                        centerpic,
                        idproof,
                        license
                        
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            cur.execute(i, ( Centername,Resourcetype, Resourcername , Street,City,  State,Pincode ,Mobile, Email , Description, a, b, c,d))
            con.commit()
            print("""
                <script>
                alert("Registration successful!  Your login credentials sent to your mail once the admin approve it.");
                location.href="homepage.py";
                </script>
            """)
        else:
            print("""
                <script>
                alert("Please upload all the required files.");
                history.back();
                </script>
            """)
    con.close()
