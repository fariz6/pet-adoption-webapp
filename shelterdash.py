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

# HTML Form


form=cgi.FieldStorage()
Sid = form.getvalue("shelter_id")
r= """ select * from shelter_info where shelter_id="%s" """ %(Sid)
cur.execute(r)
res = cur.fetchall()
print(
                """
                <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Shelter Dashboard</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="styles.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        </head>
        <style>
            /* General Styling */
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            padding: 0;
        }
        
        h1, h2, h3, .section-title {
            font-weight: bold;
        }
        
        .container {
            max-width: 1200px;
        }
        
        /* Navbar */
        .navbar {
            background-color: black;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .navbar-brand {
            font-size: 1.5rem;
            font-weight: bold;
            color: #fff !important;
            transition: color 0.3s;
        }
        
        .navbar-brand:hover {
            color: #ffd54f !important;
        }
        
        .navbar-nav .nav-link {
            font-size: 1.1rem;
            color: #fff !important;
            transition: color 0.3s ease-in-out;
        }
        
        .navbar-nav .nav-link:hover {
            color: #ffd54f !important;
        }
        
        .btn-danger {
            background-color: #ffd54f;
            border: none;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        
        .btn-danger:hover {
            background-color: rgb(246, 195, 100);
            transform: scale(1.05);
        }
        
        /* Hero Section */
        header {
            background: linear-gradient(90deg, #4CAF50 30%, #f6c364);
            color: #fff;
            text-align: center;
            padding: 60px 20px;
        }
        
        header h1 {
            font-size: 2.8rem;
            margin-bottom: 20px;
        }
        
        header p {
            font-size: 1.2rem;
        }
        
        header .btn {
            background-color: #ffd54f;
            color: #333;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-size: 1rem;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        
        header .btn:hover {
            background-color: #ffc107;
            transform: scale(1.1);
        }
        
        /* Sections */
        section {
            padding: 60px 20px;
        }
        
        .section-title {
            font-size: 2.2rem;
            color: #333;
            margin-bottom: 20px;
        }
        
        .section-description {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 40px;
            line-height: 1.8;
        }
        
        /* Pet Listings Table */
        .table {
            border-radius: 5px;
            overflow: hidden;
            background-color: white;
        }
        
        .table-bordered th, .table-bordered td {
            vertical-align: middle;
            text-align: center;
        }
        
        .table th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        .table tbody tr:hover {
            background-color: #f1f1f1;
            transition: background-color 0.3s ease;
        }
        
        .badge {
            font-size: 0.9rem;
            padding: 5px 10px;
            border-radius: 12px;
        }
        
        .badge-success {
            background-color: #4CAF50;
        }
        
        .badge-secondary {
            background-color: #9E9E9E;
        }
        
        /* Buttons in Table */
        .btn-warning, .btn-danger, .btn-info {
            border: none;
            font-size: 0.9rem;
            padding: 7px 12px;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        
        .btn-warning:hover {
            background-color: #FFCA28;
            transform: translateY(-3px);
        }
        
        .btn-danger:hover {
            background-color: #E53935;
            transform: translateY(-3px);
        }
        
        .btn-info:hover {
            background-color: #039BE5;
            transform: translateY(-3px);
        }
        
        /* Messages Section */
        .list-group-item {
            font-size: 1.1rem;
            padding: 15px;
            border-left: 4px solid #4CAF50;
            transition: all 0.3s ease;
        }
        
        .list-group-item:hover {
            background-color: #e8f5e9;
            border-left: 4px solid #3f51b5;
        }
        
        /* Footer (Optional if applicable) */
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 15px;
            margin-top: 20px;
        }
        
        footer a {
            color: #FFD54F;
            text-decoration: none;
        }
        
        footer a:hover {
            text-decoration: underline;
        }
        
        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .navbar-brand {
                font-size: 1.3rem;
            }
        
            header h1 {
                font-size: 2rem;
            }
        
            header p {
                font-size: 1rem;
            }
        }
        
        </style>""")
for i in res:


        Image=i[10]
        Name=i[2]
        print("""
        <body>
      <!-- Navbar -->
            <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top shadow">
                <div class="container-fluid">
                    <a class="navbar-brand" href="#"><i class="fas fa-paw"></i> Shelter Dashboard</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav ms-auto">
                            <li class="nav-item"><a class="nav-link active" href="#dashboard">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="#pet-listings">Pet Listings</a></li>
                            <li class="nav-item"><a class="nav-link" href="#adoption-status">Adoption Status</a></li>
                            <li class="nav-item"><a class="nav-link" href="#messages">Messages</a></li>
                            <li class="nav-item"><a class="nav-link btn btn-danger text-white ms-lg-3" href="#">Logout</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        
            <!-- Hero Section -->
            <header id="dashboard" class="bg-light text-center py-5">
                <div class="container">
                    <h1>Welcome to Your Shelter Dashboard</h1>
                    <p class="lead">Easily manage your pet listings, track adoptions, and communicate with adopters from one place.</p>
                    <button class="btn btn-primary btn-lg" data-bs-toggle="modal" data-bs-target="#addPetModal"><i class="fas fa-plus"></i> Add a New Pet</button>
                </div>
            </header>
        
            <!-- Pet Listings Section -->
            <section id="pet-listings" class="py-5 bg-light">
                <div class="container">
                    <h2 class="section-title">Pet Listings</h2>
                    <p>Manage and update your shelter's pet information to ensure accuracy.</p>
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead class="table-primary">
                                <tr>
                                    <th>Pet Name</th>
                                    <th>Species</th>
                                    <th>Breed</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Max</td>
                                    <td>Dog</td>
                                    <td>Golden Retriever</td>
                                    <td><span class="badge bg-success">Available</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-warning"><i class="fas fa-edit"></i></button>
                                        <button class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Whiskers</td>
                                    <td>Cat</td>
                                    <td>Persian</td>
                                    <td><span class="badge bg-secondary">Adopted</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-warning"><i class="fas fa-edit"></i></button>
                                        <button class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>""") %(i[10],i[2])
        
for i in res:

        Ownername = i[2]
        Sheltername = i[1]
        Email = i[7]
        Location=i[4]
        print("""            <!-- Modal for Adding Pet -->
        <div class="modal fade" id="addPetModal" tabindex="-1" aria-labelledby="addPetLabel" aria-hidden="true">
                         <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="addPetLabel">Add a New Pet</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                        <form  method="post" enctype="multipart/form-data">
                            
                                <div class="mb-3">
                                    <label for="ownerName" class="form-label">Owner Name</label>
                                    <input type="hidden" value="%s" class="form-control" id="ownerName" name="ownername" placeholder="Enter owner name">
                                </div>
                                <div class="mb-3">
                                    <label for="shelterName" class="form-label">Shelter Name</label>
                                    <input type="hidden" value="%s" class="form-control" id="shelterName" name="sheltername" placeholder="Enter shelter name">
                                </div>
                                <div class="mb-3">
                                    <label for="mobileNumber" class="form-label">Email</label>
                                    <input type="hidden" value="%s" class="form-control" id="" name="email" placeholder="Enter mobile number">
                                </div>
                                 <div class="mb-3">
                                    <label for="petName" class="form-label">Pet Name</label>
                                    <input type="text" class="form-control" id="petName" name="petname" placeholder="Enter pet name">
                                </div>
                                <div class="mb-3">
                                    <label for="species" class="form-label">Species</label>
                                    <input type="text" class="form-control" id="species" name="species" placeholder="Enter species (e.g., Dog, Cat)">
                                </div>
                                <div class="mb-3">
                                    <label for="breed" class="form-label">Breed</label>
                                    <input type="text" class="form-control" id="breed" name="breed" placeholder="Enter breed">
                                </div>
                                
                                <div class="mb-3">
                                    <label for="ownerName" class="form-label">Location</label>
                                    <input type="hidden" value="%s" class="form-control" id="ownerName" name="location" placeholder="Enter owner name">
                                </div>
                                 <div class="mb-3">
                                    <label for="breed" class="form-label">Age</label>
                                    <input type="text" class="form-control" id="age" name="age" placeholder="Enter age">
                                </div>
                                 <div class="mb-3">
                                    <label for="breed" class="form-label">animalPhoto</label>
                                    <input type="file" class="form-control" id="age" name="photo" placeholder="Enter age">
                                </div>
                                <input type="submit" value="add" name="add" class="btn btn-primary">
                            </form>
                        </div>
           </div>
        </div>
        </div>""" % (Ownername,Sheltername,Email,Location))

print(""" <section id="adoption-status" class="py-5">
        <div class="container">
            <h2 class="section-title">Adoption Status</h2>
            <p>View and manage the progress of adoption applications for your pets.</p>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead class="table-dark">
                        <tr>
                            <th>Application ID</th>
                            <th>Pet Name</th>
                            <th>Adopter Name</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1001</td>
                            <td>Max</td>
                            <td>John Doe</td>
                            <td><span class="badge bg-warning text-dark">Pending</span></td>
                            <td>
                                <button class="btn btn-sm btn-info"><i class="fas fa-eye"></i> View</button>
                                <button class="btn btn-sm btn-success"><i class="fas fa-check"></i> Approve</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Messages Section -->
    <section id="messages" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title">Messages</h2>
            <p>Stay connected with adopters and address their queries about pets.</p>
            <div class="list-group">
                <a href="#" class="list-group-item list-group-item-action">
                    <strong>John Doe:</strong> Interested in adopting Max.
                </a>
                <a href="#" class="list-group-item list-group-item-action">
                    <strong>Jane Smith:</strong> Is Whiskers available for adoption?
                </a>
            </div>
        </div>
    </section>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")
Ownername=form.getvalue("ownername")
Sheltername=form.getvalue("sheltername")
Email=form.getvalue("email")
Petname=form.getvalue("petname")
Species=form.getvalue("species")
Breed=form.getvalue("breed")

Location=form.getvalue("location")
Age=form.getvalue("age")
Submit=form.getvalue("add")
if Submit != None:
        Prof = form['photo']

        a = os.path.basename(Prof.filename)
        safe_write_file("images/" + a, Prof.file.read())

        q="""insert into product_info(Ownername,Sheltername,Email,Petname,Species,Breed,location,Age,Animalimg) values("%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %(Ownername,Sheltername,Email,Petname,Species,Breed,Location,Age,a)
        cur.execute(q)
        con.commit()

        print("""
                  <script>
                  alert("Data inserted successfully!") 
                                                     </script> """)
        con.close()

def safe_write_file(filepath, content):
    """Helper function to safely write files with proper encoding"""
    try:
        with open(filepath, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {filepath}: {str(e)}")
        raise
