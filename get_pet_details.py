#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: application/json\n\n")
import pymysql, cgi, json

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()

# Get the pet ID from the request
form = cgi.FieldStorage()
pet_id = form.getvalue("pet_id")

# Query the database for pet details
query = """SELECT p.*, s.shelter_name, s.location, s.email, s.owner_name, s.phone, s.available_hours,
           p.product_name, p.product_description, p.product_price, p.product_category, p.product_stock
           FROM product_info p 
           JOIN shelter_info s ON p.shelter_id = s.shelter_id 
           WHERE p.product_id = %s"""
cur.execute(query, (pet_id,))
result = cur.fetchone()

# Create response dictionary
response = {
    "shelter_name": result[1] if result else None,
    "location": result[6] if result else None,
    "email": result[2] if result else None,
    "owner_name": result[0] if result else None,
    "phone": result[7] if result else None,
    "available_hours": result[8] if result else None,
    "description": result[11] if result else None,
    "health_status": result[12] if result else None,
    "vaccination_status": result[13] if result else None,
    "temperament": result[14] if result else None,
    "special_needs": result[15] if result else None,
    "activity_level": result[16] if result else None,
    "good_with": result[17] if result else None,
    "medical_history": result[18] if result else None,
    "product_name": result[19] if result else None,
    "product_description": result[20] if result else None,
    "product_price": result[21] if result else None,
    "product_category": result[22] if result else None,
    "product_stock": result[23] if result else None
}

# Return JSON response
print(json.dumps(response))

# Close database connection
con.close() 