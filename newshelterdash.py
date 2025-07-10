#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os, time

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Sid = form.getvalue("shelter_id")
r = """ select * from shelter_info where shelter_id="%s" """ % (Sid)
cur.execute(r)
res = cur.fetchall()



# HTML Form
print("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PetMatch - Shelter Dashboard</title>
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <!-- Font Awesome -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --dark-color: #2d3748;
        --light-color: #f8fafc;
        --card-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f0f2ff !important;
        color: var(--dark-color);
        line-height: 1.6;
        min-height: 100vh;
    }
    .nav{
    background: #6C63FF !important;
    }

    /* Navigation */
    .navbar {
        background: #6C63FF !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 0.8rem 1rem;
    }

    .navbar-brand {
        font-weight: 600;
        color: white !important;
        font-size: 1.5rem;
    }

    .navbar .nav-link {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .navbar .nav-link:hover {
        color: white !important;
        transform: translateY(-2px);
    }

    .navbar-toggler {
        border-color: rgba(255, 255, 255, 0.5);
        padding: 0.25rem 0.5rem;
    }

    .navbar-toggler:focus {
        box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
    }

    .dropdown-menu {
        border: none;
        box-shadow: var(--card-shadow);
        border-radius: 8px;
        padding: 0.5rem;
    }

    .dropdown-item {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.2s;
    }

    .dropdown-item:hover {
        background: var(--primary-gradient);
        color: white;
        transform: translateX(5px);
    }

    /* Dashboard Cards */
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--card-shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    /* Stats Cards */
    .stat-card {
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: var(--card-shadow);
        transition: transform 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
    }

    .stat-card i {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .stat-card h3 {
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .stat-card.pets {
        background: var(--primary-gradient);
    }

    .stat-card.requests {
        background: var(--secondary-gradient);
    }

    .stat-card.adopted {
        background: var(--success-gradient);
    }

    /* Pet Cards */
    .pet-card {
        border: none;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }

    .pet-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    .pet-card img {
        height: 200px;
        object-fit: cover;
        transition: transform 0.5s ease;
    }

    .pet-card:hover img {
        transform: scale(1.05);
    }

    .pet-card .card-body {
        padding: 1.25rem;
    }

    .pet-card .badge {
        font-weight: 500;
        padding: 0.35em 0.65em;
    }

    /* Modals */
    .modal-content {
        border: none;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }

    .modal-header {
        background: var(--primary-gradient);
        color: white;
        border-bottom: none;
        padding: 1.5rem;
    }

    .modal-header .btn-close {
        filter: brightness(0) invert(1);
    }

    /* Pet View Modal */
    .pet-view-modal .modal-body {
        padding: 2rem;
    }

    .pet-view-modal .pet-image {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    .pet-view-modal .pet-details {
        margin-bottom: 1.5rem;
    }

    .pet-view-modal .pet-details h5 {
        color: var(--dark-color);
        margin-bottom: 1rem;
    }

    .pet-view-modal .pet-details p {
        margin-bottom: 0.5rem;
    }

    .pet-view-modal .pet-details .badge {
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
    }

    .pet-view-modal .pet-description {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
    }

    /* Profile Modal Specific */
    .profile-pic-container {
        position: relative;
        width: 150px;
        height: 150px;
        margin: 0 auto 1.5rem;
        cursor: pointer;
    }

    .profile-pic {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border: 4px solid white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-radius: 50%;
    }

    .upload-overlay {
        position: absolute;
        bottom: 10px;
        right: 10px;
        background: var(--primary-gradient);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .profile-pic-container:hover .upload-overlay {
        transform: scale(1.1);
    }

    /* Form Elements */
    .form-control {
        border-radius: 8px;
        padding: 0.75rem 1rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .form-control:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .btn {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .btn-primary {
        background: var(--primary-gradient);
        border: none;
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.3);
    }

    /* Responsive Adjustments */
    @media (max-width: 992px) {
        .navbar-nav {
            margin-top: 1rem;
        }

        .nav-link {
            margin: 0.25rem 0;
        }
    }

    @media (max-width: 768px) {
        .stat-card {
            margin-bottom: 1rem;
        }

        .stat-card i {
            font-size: 2rem;
        }

        .stat-card h3 {
            font-size: 1.75rem;
        }
    }
    

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-fade {
        animation: fadeIn 0.5s ease-out forwards;
    }
    /* Cover Section CSS */
.shelter-cover-section {
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                url('https://images.unsplash.com/photo-1450778869180-41d0601e046e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1586&q=80');
    background-size: cover;
    background-position: center;
    color: white;
    padding: 6rem 0;
    text-align: center;
    margin-bottom: 3rem;
}

.shelter-cover-section h1 {
    font-size: 3rem;
    position:relative;
    margin-top: 10px;
    margin-bottom: 1.5rem;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

.shelter-cover-section p.lead {
    font-size: 1.3rem;
    max-width: 700px;
    margin: 0 auto 2rem;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.shelter-action-btn {
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.3s;
}

.shelter-action-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

        .form-container {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 3rem;
        }

        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 2rem 0;
            margin-top: 2rem;
        }

        .footer-links h5 {
            margin-bottom: 1rem;
            position: relative;
        }

        .footer-links h5:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -8px;
            width: 40px;
            height: 2px;
            background-color: var(--primary-color);
        }

        .footer-links ul {
            list-style: none;
            padding-left: 0;
        }

        .footer-links li {
            margin-bottom: 0.3rem;
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
            padding-top: 1rem;
            margin-top: 1.5rem;
        }

        .hidden {
            display: none;
        }
        #viewPets{
        background-color:#f0f2ff;
        }
</style>
        </head>""")
for i in res:
    Image = i[10]
    Name = i[2]
    shelterid=i[0]

    print(""""<body>
            <!-- Navigation Bar -->
            <nav class="navbar navbar-expand-lg  fixed-top">
                <div class="container-fluid">
                    <a class="navbar-brand" href="#">
                        <i class="fas fa-paw"></i> PetMatch Shelter
                    </a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto">
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="petsDropdown" role="button" data-bs-toggle="dropdown">
                                    <i class="fas fa-dog"></i> Pets
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="petsDropdown">
                                    <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#addPetModal"><i class="fas fa-plus"></i> Post</a></li>
                                    <li><a class="dropdown-item" href="#viewPets"><i class="fas fa-eye"></i> View</a></li>
                                </ul>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="ordersDropdown" role="button" data-bs-toggle="dropdown">
                                    <i class="fas fa-shopping-cart"></i> Order Requests
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="ordersDropdown">
                                    <li><a class="dropdown-item" href="shelterrecent.py?shelter_id=%s"><i class="fas fa-clock"></i> Recent</a></li>
                                    <li><a class="dropdown-item" href="shelterrejected.py?shelter_id=%s"><i class="fas fa-clock"></i> Rejected</a></li>
                                    
                                    <li><a class="dropdown-item" href="usercompleted.py?shelter_id=%s"><i class="fas fa-check-circle"></i> Aproved</a></li>
                                </ul>
                            </li>
                        </ul>
                        <ul class="navbar-nav">
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                                    <img src="./images/%s" alt="User" height="50px" width="50px"  style="border-radius: 50%%; object-fit: cover;"> %s
                                </a>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                    <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#profileModal"><i class="fas fa-user"></i> Profile</a></li>
                                    <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#changePasswordModal"><i class="fas fa-cog"></i> Change Password</a></li>
                                   
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>""" % (i[0],i[0],i[0],i[10], i[2]))
print("""
<!-- Cover Section HTML -->
<section class="shelter-cover-section">
    <div class="container">
        <h1>Shelter Management Dashboard</h1>
        <p class="lead">Manage your shelter operations, animals, and adoptions all in one place</p>

    </div>
</section>
""")



print("""
<!-- View Pets Section -->
<div class="row mt-4" id="viewPets">
    <div class="col-12">
        <div class="dashboard-card">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5><i class="fas fa-dog"></i> My Pets</h5>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addPetModal">
                    <i class="fas fa-plus me-1"></i> Add New Pet
                </button>
            </div>
            <hr>
            <div class="row">""")

# Query database for pets belonging to this shelter
Sid = form.getvalue("shelter_id")
r = """SELECT * FROM shelter_info WHERE shelter_id="%s" """ % (Sid)
cur.execute(r)
res = cur.fetchone()  # Using fetchone() since we're getting a single shelter

# Extract shelter name from the result
Sheltername = res[1]
try:
    pet_query = """SELECT * FROM product_info WHERE Sheltername=%s"""

    cur.execute(pet_query, (Sheltername,))
    shelter_pets = cur.fetchall()

    if shelter_pets:
        for pet in shelter_pets:
            pet_id = pet[0]  # Assuming first column is ID
            pet_name = pet[5]  # Petname column
            species = pet[6]  # Species column
            breed = pet[7]  # Breed column
            age = pet[10]  # Age column
            image = pet[12]  # Animalimg column
            gender = pet[8]  # Gender column
            description = pet[11]  # Description column
            status = pet[15]  # Status column

            # Determine badge color based on species
            species_badge = {
                'Dog': 'bg-primary',
                'Cat': 'bg-info',
                'Rabbit': 'bg-warning',
                'Bird': 'bg-secondary'
            }.get(species, 'bg-dark')

            # Determine status badge color
            status_badge = {
                'accepted': 'bg-success',
                'adopted': 'bg-info',
                'pending': 'bg-warning',
                'rejected': 'bg-danger'
            }.get(status.lower(), 'bg-secondary')

            print(f"""
                <!-- Pet Card -->
                <div class="col-md-4 mb-4">
                    <div class="card pet-card">
                        <img src="./images/{pet[12]}" class="card-img-top" alt="{pet_name}">
                        <div class="card-body">
                            <h5 class="card-title">{pet_name}</h5>
                            <p class="card-text">
                                <span class="badge {species_badge}">{species}</span>
                                <span class="badge {status_badge}">{status}</span>
                            </p>
                            <p class="card-text">{breed}, {age} years old</p>
                            <div class="d-flex justify-content-between">
                                <button type="button" class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#viewPetModal" 
                                    onclick="viewPet('{pet_id}', '{pet_name}', '{species}', '{breed}', '{age}', '{image}', '{gender}', '{description}', '{status}')">
                                    View Pet
                                </button>
                                <button class="btn btn-sm btn-outline-danger" 
            onclick="return confirmDelete('{pet_id}', '{Sid}')">
        Remove
    </button>
                            </div>
                        </div>
                    </div>
                </div>""")
    else:
        print("""
                <div class="col-12">
                    <div class="alert alert-info">No pets found. Add your first pet!</div>
                </div>""")

except Exception as e:
    print(f"""
                <div class="col-12">
                    <div class="alert alert-danger">Error loading pets: {str(e)}</div>
                </div>""")

print("""
            </div>
        </div>
    </div>
</div>""")

print("""
<!-- View Pet Modal -->
<div class="modal fade" id="viewPetModal" tabindex="-1" aria-labelledby="viewPetModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header bg-primary text-white">
                <h5 class="modal-title" id="viewPetModalLabel">Pet Details</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="row">
                    <div class="col-md-6">
                        <img id="petModalImage" src="" class="img-fluid rounded" alt="Pet Image">
                    </div>
                    <div class="col-md-6">
                        <h4 id="petModalName" class="mb-3"></h4>
                        <div class="mb-3">
                            <span class="badge bg-primary me-2" id="petModalSpecies"></span>
                            <span class="badge bg-success" id="petModalStatus">Available</span>
                        </div>
                        <div class="mb-3">
                            <h6>Breed:</h6>
                            <p id="petModalBreed"></p>
                        </div>
                        <div class="mb-3">
                            <h6>Age:</h6>
                            <p id="petModalAge"></p>
                        </div>
                        <div class="mb-3">
                            <h6>Gender:</h6>
                            <p id="petModalGender"></p>
                        </div>
                        <div class="mb-3">
                            <h6>Description:</h6>
                            <p id="petModalDescription" class="text-muted"></p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>

<script>
function viewPet(id, name, species, breed, age, image, gender, description, status) {
    document.getElementById('petModalName').textContent = name;
    document.getElementById('petModalSpecies').textContent = species;
    document.getElementById('petModalBreed').textContent = breed;
    document.getElementById('petModalAge').textContent = age + ' years old';
    document.getElementById('petModalGender').textContent = gender;
    document.getElementById('petModalImage').src = './images/' + image;
    document.getElementById('petModalDescription').textContent = description;
    document.getElementById('petModalStatus').textContent = status;
    
    // Update status badge color
    const statusBadge = document.getElementById('petModalStatus');
    statusBadge.className = 'badge ' + {
        'accepted': 'bg-success',
        'adopted': 'bg-info',
        'pending': 'bg-warning',
        'rejected': 'bg-danger'
    }[status.toLowerCase()] || 'bg-secondary';
}
</script>
""")

m = """ select * from shelter_info where shelter_id="%s" """ % (Sid)
cur.execute(m)
result = cur.fetchall()

for i in result:
    shelterid=i[0]
    Ownername = i[2]
    Sheltername = i[1]
    Email = i[7]
    Location = i[4]

    print("""<!-- Modal for Adding Pet -->
    <div class="modal fade" id="addPetModal" tabindex="-1" aria-labelledby="addPetLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="addPetLabel">Add a New Pet</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form method="post" enctype="multipart/form-data">
                        <div class="mb-3">
                            <input type="hidden" value="%s" name="shelterid">
                            <input type="hidden" value="%s" class="form-control" name="ownername">
                        </div>
                        <div class="mb-3">
                            <input type="hidden" value="%s" class="form-control" id="shelterName" name="sheltername">
                        </div>
                        <div class="mb-3">
                            <input type="hidden" value="%s" class="form-control" name="email">
                        </div>
                        <div class="mb-3">
                            <label for="petName" class="form-label">Pet Name</label>
                            <input type="text" class="form-control" id="petName" name="petname" placeholder="Enter pet name" required>
                        </div>
                        <div class="mb-3">
                            <label for="species" class="form-label">Species</label>
                            <input type="text" class="form-control" id="species" name="species" placeholder="Enter species (e.g., Dog, Cat)" required>
                        </div>
                        <div class="mb-3">
                            <label for="breed" class="form-label">Breed</label>
                            <input type="text" class="form-control" id="breed" name="breed" placeholder="Enter breed" required>
                        </div>
                         <div class="mb-3">
                          <label for="petType" class="form-label">Gender</label>
                                <select class="form-select" id="petType" name="gender">
                                    <option selected>Any</option>
                                    <option>Male</option>
                                    <option>Female</option>
                                </select>
                        </div>
                        <div class="mb-3">
                            <input type="hidden" value="%s" class="form-control" name="location">
                        </div>
                        <div class="mb-3">
                            <label for="breed" class="form-label">Age</label>
                            <input type="text" class="form-control" id="age" name="age" placeholder="Enter age" required>
                        </div>
                        <div class="mb-3">
                            
                            <label for="breed" class="form-label">Description</label>
                           <input type="description" row="5" name="desc" placeholder="Enter a description..."></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="breed" class="form-label">Pet Photo</label>
                            <input type="file" class="form-control" name="photo"  required>
                        </div>
                         <div class="mb-3">
                            <label for="breed" class="form-label">Pet Photo 2</label>
                            <input type="file" class="form-control" name="photo1"  required>
                        </div> <div class="mb-3">
                            <label for="breed" class="form-label">Pet Photo 3</label>
                            <input type="file" class="form-control" name="photo2"  required>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary" name="add">Add Pet</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>""" % (shelterid,Ownername, Sheltername, Email, Location))

p = """ select * from shelter_info where shelter_id="%s" """ % (Sid)
cur.execute(p)
res = cur.fetchall()

for i in res:
    Mage = i[10]
    Sheltername = i[1]
    Oname = i[2]
    Email = i[7]

    Location = i[4]

    print("""    <!-- Add this modal code right before the closing </body> tag -->
<!-- Profile View Modal -->
<div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header bg-primary text-white">
        <h5 class="modal-title" id="profileModalLabel">Shelter Profile</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="text-center mb-4">
          <img src="./images/%s" class="rounded-circle border border-3 border-primary mb-3" style="width: 150px; height: 150px; object-fit: cover;" alt="Profile Picture">
          <h4 class="text-primary">%s</h4>
          
        </div>

        <div class="bg-light p-4 rounded-3">
          <div class="d-flex align-items-center mb-3">
            <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
              <i class="fas fa-user"></i>
            </div>
            <div class="ms-3">
              <h6 class="mb-0 text-primary">Owner Name</h6>
              <p class="mb-0">%s</p>
            </div>
          </div>

          <div class="d-flex align-items-center mb-3">
            <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
              <i class="fas fa-envelope"></i>
            </div>
            <div class="ms-3">
              <h6 class="mb-0 text-primary">Email Address</h6>
              <p class="mb-0">%s</p>
            </div>
          </div>



          <div class="d-flex align-items-center">
            <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
              <i class="fas fa-map-marker-alt"></i>
            </div>
            <div class="ms-3">
              <h6 class="mb-0 text-primary">Location</h6>
              <p class="mb-0">%s,Tamilnadu</p>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal">
          <i class="fas fa-edit me-2"></i>Edit Profile
        </button>
      </div>
    </div>
  </div>
</div>""" % (Mage, Sheltername, Oname, Email, Location))
for i in res:
    Mage = i[10]
    
    print(f"""<!-- Edit Profile Modal -->
<div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header bg-primary text-white">
        <h5 class="modal-title" id="editProfileModalLabel">Edit Shelter Profile</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form method="post" enctype="multipart/form-data">
          <div class="text-center mb-4">
            <label for="profileImageUpload" style="cursor: pointer;">
              <img src="./images/{Mage}" class="rounded-circle border border-3 border-primary mb-2" style="width: 150px; height: 150px; object-fit: cover;" alt="Profile Picture" id="profileImagePreview">
              <div class="text-primary small mt-1">
                <i class="fas fa-camera me-1"></i>Change Photo
              </div>
              <input type="file" id="profileImageUpload" name="Img" accept="image/*" class="d-none">
            </label>
          </div>

          <div class="mb-3">
            <label for="editShelterName" class="form-label">Shelter Name</label>
            <input type="text" class="form-control" id="editShelterName" name="usheltername" value="Happy Paws Shelter">
          </div>

          <div class="mb-3">
            <label for="editOwnerName" class="form-label">Owner Name</label>
            <input type="text" class="form-control" id="editOwnerName" name="uname" value="John Doe">
          </div>


          <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
        <input type="submit" name="savech" value="Save changes" class="btn btn-primary" data-bs-dismiss="modal">


        </form>
      </div>
      <div class="modal-footer">

      </div>
    </div>
  </div>
</div>""")

print("""<!-- Add this JavaScript for image preview -->
<script>
  document.getElementById('profileImageUpload').addEventListener('change', function(e) {
    if (e.target.files.length) {
      const reader = new FileReader();
      reader.onload = function(e) {
        document.getElementById('profileImagePreview').src = e.target.result;
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  });
</script>""")
for j in res:
    Old = j[9]
    print("""<div class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="changePasswordModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="changePasswordModalLabel">Change Password</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form method="post">
                        <div class="mb-3">
                           
                            <input type="hidden" class="form-control" value="%s" id="oldPassword" name="old" required>
                        </div>
                        <div class="mb-3">
                            <label for="oldPassword" class="form-label">Old Password</label>
                            <input type="password" class="form-control" id="oldPassword" name="old_password" required>
                        </div>
                        <div class="mb-3">
                            <label for="newPassword" class="form-label">New Password</label>
                            <input type="password" class="form-control" id="newPassword" name="new_password" required>
                        </div>
                        <div class="mb-3">
                            <label for="confirmPassword" class="form-label">Confirm New Password</label>
                            <input type="password" class="form-control" id="confirmPassword" name="confirm_password" required>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <input type="submit" value"Changepassword" class="btn btn-primary" name="change_password">
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div> 
    <footer >
        
            
                
            <div class="copyright text-center">
                <p class="mb-0">&copy; 2023 PetMatch Care Resources. All rights reserved.</p>
            </div>
        </div>
    </footer>
    

        <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
function confirmDelete(petId, shelterId) {
    if(confirm('Are you sure you want to delete this pet? This process cannot be undone')) {
        window.location.href = 'delete_pet.py?pet_id=' + petId + '&shelter_id=' + shelterId;
    }
    return false;
}
</script>
    </body>
    </html>""" % (Old))

Sid = form.getvalue("shelter_id")
Uname = form.getvalue("uname")
Usheltername = form.getvalue("usheltername")
Usave = form.getvalue("savech")

if Usave != None:
    try:
        # Check if images directory exists, if not create it
        if not os.path.exists("images"):
            os.makedirs("images")
            
        Prof = form['Img']
        a = os.path.basename(Prof.filename)
        
        # Ensure the filename is valid
        a = "".join(c for c in a if c.isalnum() or c in ('-', '_', '.'))
        
        # Add timestamp to prevent filename conflicts
        timestamp = str(int(time.time()))
        a = f"{timestamp}_{a}"
        
        try:
            with open(os.path.join("images", a), 'wb') as f:
                f.write(Prof.file.read())
                
            # Correct parameterized query
            u = """UPDATE shelter_info 
                   SET sheltername = %s, 
                       ownername = %s, 
                       profile_pic = %s 
                   WHERE shelter_id = %s"""

            # Execute with parameters
            cur.execute(u, (Usheltername, Uname, a, Sid))
            con.commit()

            print("""
                <script>
                alert("Profile updated successfully!");
                location.href="newshelterdash.py?shelter_id=%s"
                </script>
                """ % Sid)
        except Exception as e:
            print(f"""
                <script>
                alert("Error saving image: {str(e)}") 
                window.history.back();
                </script>""")
    except Exception as e:
        print(f"""
            <script>
            alert("Error processing upload: {str(e)}") 
            window.history.back();
            </script>""")
    finally:
        con.close()

Old = form.getvalue("old")
old_password = form.getvalue("old_password")
new_password = form.getvalue("new_password")
confirm_password = form.getvalue("confirm_password")
change_pwd = form.getvalue("change_password")
if change_pwd != None:
    if Old == old_password:
        if Old != new_password:
            if new_password == confirm_password:
                # Add these validation checks
                if len(new_password) < 8:
                    print("""
                        <script>
                            alert("Password must be at least 8 characters long!");
                            window.history.back();
                        </script>
                    """)
                elif not any(char.isupper() for char in new_password):
                    print("""
                        <script>
                            alert("Password must contain at least one uppercase letter!");
                            window.history.back();
                        </script>
                    """)
                elif not any(char.islower() for char in new_password):
                    print("""
                        <script>
                            alert("Password must contain at least one lowercase letter!");
                            window.history.back();
                        </script>
                    """)
                elif not any(char.isdigit() for char in new_password):
                    print("""
                        <script>
                            alert("Password must contain at least one number!");
                            window.history.back();
                        </script>
                    """)
                else:
                    # If all validations pass
                    ch = """UPDATE shelter_info 
                           SET pass = %s 
                           WHERE shelter_id = %s"""
                    cur.execute(ch, (confirm_password, Sid))
                    con.commit()
                    print(f"""
                        <script>
                            alert("Password changed successfully!");
                            location.href="newshelterdash.py?shelter_id={Sid}"

                        </script>
                    """)
                con.close()
            else:
                print("""
                                       <script>
                                       alert("new password and confirm new password should be same")
                                        window.history.back();
                                       </script>        
                                       """)
        else:
            print("""
                                  <script>
                                  alert("old password and  new password should'nt be same")
                                   window.history.back();
                                  </script>        
                                  """)
    else:
        print("""
            <script>
                          alert("Od password is wrong")
                           window.history.back();
                          </script>  
           """)
Shelterid=form.getvalue("shelterid")
Ownername = form.getvalue("ownername")
Sheltername = form.getvalue("sheltername")
Email = form.getvalue("email")
Petname = form.getvalue("petname")
Species = form.getvalue("species")
Breed = form.getvalue("breed")
Gender = form.getvalue("gender")
Location = form.getvalue("location")
Age = form.getvalue("age")
Desc = form.getvalue("desc")
Submit = form.getvalue("add")
if Submit != None:
    try:
        # Check if images directory exists, if not create it
        if not os.path.exists("images"):
            os.makedirs("images")
            
        Prof = form['photo']
        Prof1 = form['photo1']
        Prof2 = form['photo2']

        a = os.path.basename(Prof.filename)
        b = os.path.basename(Prof1.filename)
        c = os.path.basename(Prof2.filename)

        # Ensure the filenames are valid
        a = "".join(c for c in a if c.isalnum() or c in ('-', '_', '.'))
        b = "".join(c for c in b if c.isalnum() or c in ('-', '_', '.'))
        c = "".join(c for c in c if c.isalnum() or c in ('-', '_', '.'))

        # Add timestamp to prevent filename conflicts
        timestamp = str(int(time.time()))
        a = f"{timestamp}_{a}"
        b = f"{timestamp}_{b}"
        c = f"{timestamp}_{c}"

        try:
            with open(os.path.join("images", a), 'wb') as f:
                f.write(Prof.file.read())
            with open(os.path.join("images", b), 'wb') as f:
                f.write(Prof1.file.read())
            with open(os.path.join("images", c), 'wb') as f:
                f.write(Prof2.file.read())

            q = """insert into product_info(shelter_id,Ownername,Sheltername,Email,Petname,Species,Breed,gender,location,Age,description,Animalimg,Animalimg2,Animalimg3) 
                   values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cur.execute(q, (Shelterid,Ownername, Sheltername, Email, Petname, Species, Breed, Gender, Location, Age,Desc, a, b, c))
            con.commit()

            print("""
                      <script>
                      alert("Pet Added successfully!") 
                      location.href="newshelterdash.py?shelter_id=%s";
                      </script> """ % Sid)
        except Exception as e:
            print(f"""
                <script>
                alert("Error saving images: {str(e)}") 
                window.history.back();
                </script>""")
    except Exception as e:
        print(f"""
            <script>
            alert("Error processing upload: {str(e)}") 
            window.history.back();
            </script>""")
    finally:
        con.close()
