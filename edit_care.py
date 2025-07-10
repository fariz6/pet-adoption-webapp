#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql
import cgi
import cgitb
import os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

form = cgi.FieldStorage()
careid = form.getvalue("careid")

# Fetch the care center details
cur.execute("SELECT * FROM careresource_info WHERE careid=%s", (careid,))
center = cur.fetchone()

if form.getvalue("update"):
    try:
        # Get form values
        centername = form.getvalue("centername")
        centertype = form.getvalue("centertype")
        address = form.getvalue("address")
        city = form.getvalue("city")
        state = form.getvalue("state")
        pin = form.getvalue("pin")
        mob = form.getvalue("mob")
        mail = form.getvalue("mail")
        description = form.getvalue("description")
        
        # Handle file upload
        if 'image' in form:
            fileitem = form['image']
            if fileitem.filename:
                # Save the uploaded file
                fn = os.path.basename(fileitem.filename)
                open('images/' + fn, 'wb').write(fileitem.file.read())
                # Update database with new image
                cur.execute("""
                    UPDATE careresource_info 
                    SET centername=%s, centertype=%s, address=%s, city=%s, state=%s, 
                        pin=%s, mob=%s, mail=%s, description=%s, Image=%s
                    WHERE careid=%s
                """, (centername, centertype, address, city, state, pin, mob, mail, description, fn, careid))
            else:
                # Update without changing image
                cur.execute("""
                    UPDATE careresource_info 
                    SET centername=%s, centertype=%s, address=%s, city=%s, state=%s, 
                        pin=%s, mob=%s, mail=%s, description=%s
                    WHERE careid=%s
                """, (centername, centertype, address, city, state, pin, mob, mail, description, careid))
        
        con.commit()
        print("""
        <script>
            alert("Care center updated successfully!");
            window.location.href = "care.py";
        </script>
        """)
    except Exception as e:
        print(f"""
        <script>
            alert("Error updating care center: {str(e)}");
        </script>
        """)

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Care Center</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            background-color: #f8f9fa;
            padding-top: 2rem;
        }
        .form-container {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .form-label {
            font-weight: 500;
        }
        .btn-primary {
            background-color: #4CAF50;
            border-color: #4CAF50;
        }
        .btn-primary:hover {
            background-color: #45a049;
            border-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="form-container">
                    <h2 class="text-center mb-4">Edit Care Center</h2>
                    <form method="post" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label class="form-label">Center Name</label>
                            <input type="text" class="form-control" name="centername" value="{}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Center Type</label>
                            <select class="form-select" name="centertype" required>
                                <option value="Veterinary Clinic" {}>Veterinary Clinic</option>
                                <option value="Pet Shelter" {}>Pet Shelter</option>
                                <option value="Training Center" {}>Training Center</option>
                                <option value="Pet Spa" {}>Pet Spa</option>
                                <option value="Other" {}>Other</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Address</label>
                            <input type="text" class="form-control" name="address" value="{}" required>
                        </div>
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label class="form-label">City</label>
                                <input type="text" class="form-control" name="city" value="{}" required>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">State</label>
                                <input type="text" class="form-control" name="state" value="{}" required>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">PIN Code</label>
                                <input type="text" class="form-control" name="pin" value="{}" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Mobile Number</label>
                                <input type="tel" class="form-control" name="mob" value="{}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="mail" value="{}" required>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea class="form-control" name="description" rows="3" required>{}</textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Center Image</label>
                            <input type="file" class="form-control" name="image" accept="image/*">
                            <small class="text-muted">Leave empty to keep current image</small>
                        </div>
                        <div class="text-center">
                            <input type="submit" name="update" class="btn btn-primary" value="Update Center">
                            <a href="care.py" class="btn btn-secondary">Cancel</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
""".format(
    center[2],  # centername
    'selected' if center[3] == 'Veterinary Clinic' else '',
    'selected' if center[3] == 'Pet Shelter' else '',
    'selected' if center[3] == 'Training Center' else '',
    'selected' if center[3] == 'Pet Spa' else '',
    'selected' if center[3] == 'Other' else '',
    center[4],  # address
    center[5],  # city
    center[6],  # state
    center[7],  # pin
    center[8],  # mob
    center[9],  # mail
    center[10]  # description
)) 