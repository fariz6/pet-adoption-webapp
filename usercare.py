#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")
import pymysql, cgi, cgitb, os

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Cid = form.getvalue("centerid")
Uid = form.getvalue("id")

# Handle case where Uid might be a list
if isinstance(Uid, list):
    Uid = Uid[0]  # Take the first value if it's a list

# Build links with ID
approve_link1 = "careaprove.py"
approve_link2 = "newuserdash.py"
approve_link3 = "care.py"
if Uid:
    approve_link1 += f"?id={Uid}"
    approve_link2 += f"?id={Uid}"
    approve_link3 += f"?id={Uid}"

# Get user ID properly
user_id = None
if Uid:
    s = "SELECT * FROM usereg WHERE id=%s"
    cur.execute(s, (Uid,))
    res = cur.fetchone()
    if res:
        user_id = res[0]  # Assuming the first column is the user ID

view_all = form.getvalue("view_all")
Sservices = form.getvalue("services")
Search = form.getvalue("search")

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Care Resources | PetMatch</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4e73df;
            --secondary-color: #f0f2ff;
            --accent-color: #1cc88a;
            --dark-color: #343A40;
            --light-color: #f8f9fa;
            --border-color: #e3e6f0;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--secondary-color);
            color: var(--dark-color);
        }

        .navbar {
            background-color: var(--primary-color) !important;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
        }

        .navbar-brand {
            font-weight: 600;
            font-size: 1.3rem;
            color: white !important;
        }

        .nav-link {
            font-weight: 500;
            padding: 0.5rem 1rem;
            color: rgba(255, 255, 255, 0.8) !important;
        }

        .nav-link:hover, .nav-link.active {
            color: white !important;
        }

        /* Search Section */
        .search-section {
            background-color: #f0f2ff
            padding: 2.5rem 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
        }

        .search-container {
            max-width: 800px;
            margin: 0 auto;
        }

        .search-title {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 1.5rem;
        }

        .search-card {
            border: none;
            border-radius: 0.5rem;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
            padding: 1.5rem;
        }

        .search-form {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .search-select {
            flex: 1;
            min-width: 200px;
            border: 1px solid var(--border-color);
            border-radius: 0.35rem;
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
        }

        .search-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.35rem;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }

        .search-btn:hover {
            background-color: #3a5bc7;
        }

        /* Care Center Cards */
        .card-section {
            padding: 2rem 0;
        }

        .section-title {
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 1.5rem;
            position: relative;
            padding-bottom: 0.75rem;
        }

        .section-title:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 50px;
            height: 3px;
            background-color: var(--primary-color);
        }

        .care-card {
            border: none;
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
            height: 100%;
            background: white;
        }

        .care-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 0.5rem 1.5rem 0 rgba(58, 59, 69, 0.2);
        }

        .card-img-container {
            height: 180px;
            overflow: hidden;
        }

        .card-img-top {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .care-card:hover .card-img-top {
            transform: scale(1.03);
        }

        .card-body {
            padding: 1.5rem;
        }

        .card-title {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: var(--dark-color);
        }

        .card-badge {
            display: inline-block;
            background-color: var(--accent-color);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
        }

        .card-text {
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .card-detail {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
        }

        .card-detail i {
            width: 20px;
            color: var(--primary-color);
            margin-right: 0.5rem;
        }

        .btn-view {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.35rem;
            padding: 0.5rem 1.25rem;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.2s;
            width: 100%;
            margin-top: 1rem;
        }

        .btn-view:hover {
            background-color: #3a5bc7;
            color: white;
        }

        .no-results {
            text-align: center;
            padding: 3rem;
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
        }

        .no-results i {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        footer {
            background-color: var(--dark-color);
            color: white;
            padding: 1.5rem 0;
            margin-top: 3rem;
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-paw me-2"></i>PetMatch
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link active" href="newuserdash.py?id=""" + str(Uid) + """">Home</a></li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="ordersDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-shopping-cart me-1"></i> My Bookings
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href=""" + approve_link1 + """"><i class="fas fa-check-circle me-2"></i>Requests</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Search Section -->
    <section class="search-section">
        <div class="container search-container">
            <h2 class="search-title text-center">Find Pet Care Services</h2>
            <div class="search-card">
                <form method="post" action="">
                    <div class="search-form">
                        <select class="search-select" name="services" id="serviceType">
                            <option selected value="All Services">All Services</option>
                            <option value="Veterinary Clinic">Veterinary Clinics</option>
                            <option value="Pet Spa">Pet Spas</option>
                            <option value="Training Center">Training Centers</option>
                        </select>
                        <input type="submit" value="Search" class="search-btn" name="search">
                        <input type="hidden" name="id" value=""" + str(Uid) + """>
                    </div>
                </form>
            </div>
        </div>
    </section>
""")


# Function to display care centers
def display_care_centers(centers, title, is_search=False):
    print(f"""
    <section class="card-section">
        <div class="container">
            <h2 class="section-title">{title}</h2>
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">""")

    if centers:
        for i in centers:
            # Create the view details link with careid
            view_details_link = f'viewpare.py?careid={i[0]}'
            if user_id:
                view_details_link += f'&id={user_id}'

            print(f"""
            <div class="col">
                <div class="care-card">
                    <div class="card-img-container">
                        <img src="./images/{i[14]}" class="card-img-top" alt="{i[2]}">
                    </div>
                    <div class="card-body">
                        <span class="card-badge">{i[3]}</span>
                        <h5 class="card-title">{i[2]}</h5>
                        <div class="card-text">
                            <div class="card-detail">
                                <i class="fas fa-map-marker-alt"></i>
                                <span>{i[5]},{i[6]},{i[7]}</span>
                            </div>
                            <div class="card-detail">
                                <i class="fas fa-phone"></i>
                                <span>{i[9]}</span>
                            </div>
                            
                        </div>
                        <a href="{view_details_link}" class="btn btn-view">
                            <i class="fas fa-eye me-2"></i>View Center
                        </a>
                    </div>
                </div>
            </div>
            """)
    else:
        print("""
        <div class="col-12">
            <div class="no-results">
                <i class="fas fa-search fa-2x"></i>
                <h5>No centers found</h5>
                <p>Try adjusting your search criteria</p>
            </div>
        </div>
        """)

    print("""
            </div>
        </div>
    </section>
    """)


# Check if we're searching for a specific service
if Search is not None and Sservices != "All Services":
    try:
        # Search functionality for specific service type
        a = "SELECT * FROM careresource_info WHERE centertype=%s and status='approved' "
        cur.execute(a, (Sservices,))
        search_results = cur.fetchall()

        if search_results:
            print("""
            <script>
            location.href="#card"
            </script>
            """)

        display_care_centers(search_results, f"{Sservices} Centers", is_search=True)

        # Also show all centers below search results
        cur.execute("SELECT * FROM careresource_info where status='approved' ")
        all_centers = cur.fetchall()
        display_care_centers(all_centers, "All Care Centers")

    except Exception as e:
        print(f"""
        <div class="container mt-4">
            <div class="alert alert-danger">
                An error occurred: {str(e)}
            </div>
        </div>
        """)
else:
    # Default view - show all care centers
    try:
        cur.execute("SELECT * FROM careresource_info where status='approved' ")
        all_centers = cur.fetchall()
        display_care_centers(all_centers, "All Care Centers")
    except Exception as e:
        print(f"""
        <div class="container mt-4">
            <div class="alert alert-danger">
                An error occurred: {str(e)}
            </div>
        </div>
        """)

print("""
    <footer class="text-center py-3">
        <div class="container">
            <p class="mb-0">&copy; 2024 PetMatch. All rights reserved.</p>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()