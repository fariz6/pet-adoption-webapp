#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()

# Initialize user_id variable
b = None

# Get user ID if available
Uid = form.getvalue("id")
if Uid:
    try:
        s = """SELECT * FROM usereg WHERE id=%s"""
        cur.execute(s, (Uid,))
        res = cur.fetchall()
        if res:
            a = res[0]
            b = a[0]
    except Exception as e:
        print("<div class='alert alert-danger'>Error fetching user data: {}</div>".format(str(e)))

# Get search parameters
Stype = form.getvalue("species")
Sbreed = form.getvalue("breed")
Sgender = form.getvalue("gender")
Sage = form.getvalue("age")
Slocation = form.getvalue("location")
Sstatus = form.getvalue("status")
Search = form.getvalue("search")

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PetMatch - Browse Pets</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="demo.css">
    <style>
     /* Basic Reset */
        /* Basic Reset */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f0f2ff;  /* Light purple-blue tint to match the theme */
    min-height: 100vh;
}}

/* Navbar */
.navbar {{
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    background-color: #4e73df !important;  /* Primary theme color */
}}

.navbar-brand {{
    font-weight: 600;
    color: white !important;
}}

.navbar .nav-link {{
    color: rgba(255, 255, 255, 0.9) !important;
}}

.navbar .nav-link:hover {{
    color: white !important;
}}

.navbar-toggler {{
    border-color: rgba(255, 255, 255, 0.5);
}}

.navbar-toggler-icon {{
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.75%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}}

/* Main Content */
.container {{
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}}

.section-title {{
    margin-bottom: 20px;
    color: #6C63FF;
}}

/* Search Section */
.search-container {{
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

.advanced-filter {{
    display: none;
}}

.advanced-filter.show {{
    display: block;
}}

/* Pet Cards */
.pet-card {{
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}}

.pet-card:hover {{
    transform: translateY(-5px);
}}

.pet-card img {{
    width: 100%;
    height: 200px;
    object-fit: cover;
}}

.pet-info {{
    padding: 15px;
}}

.pet-name {{
    color: #6C63FF;
    margin-bottom: 10px;
}}

.pet-details {{
    margin: 15px 0;
}}

.detail-label {{
    font-weight: 600;
}}


/* Buttons */
.btn-primary {{
    background-color:#4e73df;
    border-color: #4e73df;
}}

.btn-primary:hover {{
    background-color: #5a52e0;
    border-color: #5a52e0;
}}

/* Responsive Grid */
.row-cols-1 > * {{
    flex: 0 0 100%;
    max-width: 100%;
}}

@media (min-width: 768px) {{
    .row-cols-md-2 > * {{
        flex: 0 0 50%;
        max-width: 50%;
    }}
}}

@media (min-width: 992px) {{
    .row-cols-lg-3 > * {{
        flex: 0 0 33.333%;
        max-width: 33.333%;
    }}
}}

@media (min-width: 1200px) {{
    .row-cols-xl-4 > * {{
        flex: 0 0 25%;
        max-width: 25%;
    }}
}}

/* Utility Classes */
.mt-3 {{ margin-top: 1rem; }}
.mb-3 {{ margin-bottom: 1rem; }}
.mt-4 {{ margin-top: 1.5rem; }}
.mb-4 {{ margin-bottom: 1.5rem; }}
.py-1 {{ padding-top: 0.25rem; padding-bottom: 0.25rem; }}
.border-bottom {{ border-bottom: 1px solid #eee; }}
.text-muted {{ color: #6c757d; }}
.small {{ font-size: 0.875rem; }}
.text-primary {{ color: #6C63FF; }}
<style>
.footer {{
    background-color: #343A40;
    color: white;
    padding: 20px 0;
    width: 100%;
    position: relative;
    bottom: 0;
    left: 0;
    right: 0;
}}

.footer p {{
    margin: 0;
}}
</style>
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand text-primary" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="newuserdash.py?id={0}">
                            <i class="fas fa-tachometer-alt me-1"></i> Home
                        </a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="myOrdersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> Pet Bookings
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="userrecent.py?id={0}">Recent</a></li>
                            <li><a class="dropdown-item" href="usercomplete.py?id={0}">Approved</a></li>
                            <li><a class="dropdown-item" href="userejected.py?id={0}">Rejected</a></li>
                            
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container my-5">
        <div class="row">
            <div class="col-12">
                <h2 class="section-title">Browse Pets</h2>
            </div>
        </div>

        <!-- Search Section -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="search-container">
                    <form id="searchForm" method="GET" action="">
                        <input type="hidden" name="id" value="{0}">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <label for="species" class="form-label">Species</label>
                                <select class="form-select" id="species" name="species">
                                    <option value="" selected>Any Species</option>
                                    <option value="Dog" {1}>Dog</option>
                                    <option value="Cat" {2}>Cat</option>
                                    <option value="Rabbit" {3}>Rabbit</option>
                                    <option value="Bird" {4}>Bird</option>
                                    <option value="Other" {5}>Other</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <label for="location" class="form-label">Location</label>

                                <select class="form-select" id="species" name="location" value="{6}">
                                    <option value="" selected>Any Location</option>

                                    <option value="Tirunelveli" >Tiunelveli</option>
                                    <option value="Tuticorin" >Tuticorin</option>
                                    <option value="coimbatore" >Coimbatore</option>
                                </select>
                            </div>


                            <div class="col-12 text-end">
                                <input type="submit" value="Search" name="search" class="btn btn-primary px-4">
                                <a href="#" id="toggleAdvanced" class="text-primary ms-3">Advanced Filters <i class="fas fa-chevron-down"></i></a>
                            </div>

                            <div class="col-12 advanced-filter">
                                <div class="filter-section mt-3">
                                    <div class="row g-3">
                                        <div class="col-md-4">
                                            <label for="gender" class="form-label">Gender</label>
                                            <select class="form-select" id="gender" name="gender">
                                                <option value="" selected>Any Gender</option>
                                                <option value="Male" {8}>Male</option>
                                                <option value="Female" {9}>Female</option>
                                            </select>
                                        </div>


                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
""".format(
    b if b else "",
    'selected' if Stype == "Dog" else "",
    'selected' if Stype == "Cat" else "",
    'selected' if Stype == "Rabbit" else "",
    'selected' if Stype == "Bird" else "",
    'selected' if Stype == "Other" else "",
    Slocation if Slocation else "",
    Sbreed if Sbreed else "",
    'selected' if Sgender == "Male" else "",
    'selected' if Sgender == "Female" else "",
    'selected' if Sage == "0-1" else "",
    'selected' if Sage == "1-3" else "",
    'selected' if Sage == "3-5" else "",
    'selected' if Sage == "5+" else "",
    'selected' if Sstatus == "Available" else "",
    'selected' if Sstatus == "Adopted" else ""
))

# Build the query based on search criteria
query = "SELECT * FROM product_info WHERE Status = 'Available'"
params = []

if Stype and Stype != "":
    query += " AND Species = %s"
    params.append(Stype)
if Slocation and Slocation != "":
    query += " AND location LIKE %s"
    params.append(f"%{Slocation}%")
if Sbreed and Sbreed != "":
    query += " AND Breed LIKE %s"
    params.append(f"%{Sbreed}%")
if Sgender and Sgender != "":
    query += " AND gender = %s"
    params.append(Sgender)
if Sage and Sage != "":
    if Sage == "0-1":
        query += " AND Age BETWEEN 0 AND 1"
    elif Sage == "1-3":
        query += " AND Age BETWEEN 1 AND 3"
    elif Sage == "3-5":
        query += " AND Age BETWEEN 3 AND 5"
    elif Sage == "5+":
        query += " AND Age >= 5"

# Show results if search was submitted or if no search was performed
try:
    # Execute the query
    cur.execute(query, params)
    pets = cur.fetchall()

    # Show results section
    print("""
    <!-- Pets Listing Section -->
    <div class="container mt-4" id="card">
        <div class="row">
            <div class="col-12">
                <h4 class="mb-4">{0}</h4>
            </div>
        </div>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">""".format(
        "Search Results" if Search is not None else "All Pets"
    ))

    if pets:
        for pet in pets:
            # Make sure to use correct indices for pet attributes
            Productid = pet[0]
            Animalimg = pet[12] if len(pet) > 10 else ""
            Name = pet[5] if len(pet) > 4 else ""
            Location = pet[9]
            Age = pet[10] if len(pet) > 8 else ""
            Species = pet[6] if len(pet) > 5 else ""
            Breed = pet[7] if len(pet) > 6 else ""
            Gender = pet[10] if len(pet) > 9 else ""  # Changed from 7 to 9 for gender

            print("""
            <div class="col">
                <div class="pet-card h-100">
                    <img src="./images/{}" class="card-img-top img-fluid" alt="Pet image">
                    <div class="pet-info p-3">
                        <h2 class="pet-name h5">{}</h2>
                        <div class="pet-location d-flex align-items-center mb-2">                                                                                                       
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" class="me-1">
                                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                            </svg>
                            <span class="text-muted small">{}</span>
                        </div>
                        <div class="pet-details">
                            <div class="detail-item d-flex justify-content-between py-1 border-bottom">
                                <span class="detail-label">Species</span>
                                <span class="detail-value">{}</span>
                            </div>
                            <div class="detail-item d-flex justify-content-between py-1">
                                <span class="detail-label">Breed</span>
                                <span class="detail-value">{}</span>
                            </div>
                        </div>
                        <a href="petdetails.py?product_id={}&id={}" class="btn btn-primary w-100 mt-3">
                            View Pet
                        </a>
                    </div>
                </div>
            </div>""".format(Animalimg, Name, Location, Species, Breed, Productid, Uid))
    else:
        print("""
            <div class="col-12">
                <div class="alert alert-info">No pets found matching your search criteria.</div>
            </div>""")

    print("""       
            </div>
        </div>""")

except Exception as e:
    print("""
    <div class="alert alert-danger">
        <h4>Error fetching pets</h4>
        <p>{}</p>
    </div>
    """.format(str(e)))

# Footer
print("""
    </div>
</div>

<!-- Footer -->
<footer class="footer">
    <div class="container">
        <p class="text-center"> 2024 PetMatch. All rights reserved.</p>
    </div>
</footer>



<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Custom JS -->
<script>
    // Toggle advanced filters
    document.getElementById('toggleAdvanced').addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector('.advanced-filter').classList.toggle('show');
        const icon = this.querySelector('i');
        if (icon.classList.contains('fa-chevron-down')) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        } else {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    });

    // Scroll to results if search was performed
    if(window.location.href.indexOf('search=') > -1) {
        document.getElementById('card').scrollIntoView();
    }
</script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()