import mysql.connector
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, message):
    try:
        # Email configuration
        sender_email = "your_email@gmail.com"  # Replace with your email
        sender_password = "your_password"      # Replace with your email password
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to SMTP server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def update_booking_status(booking_id, status):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="your_database_name"
        )
        
        cursor = conn.cursor()
        
        # Update booking status
        update_query = "UPDATE carebookings SET status = %s WHERE carebookingid = %s"
        cursor.execute(update_query, (status, booking_id))
        conn.commit()
        
        # Get user email for notification
        cursor.execute("SELECT userid FROM carebookings WHERE carebookingid = %s", (booking_id,))
        user_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT email FROM usereg WHERE id = %s", (user_id,))
        user_email = cursor.fetchone()[0]
        
        # Send email notification
        subject = f"Booking Status Update - {status}"
        message = f"Your booking (ID: {booking_id}) has been {status}."
        send_email(user_email, subject, message)
        
        return True
    except mysql.connector.Error as err:
        print(f"Error updating status: {err}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_recent_orders(shelter_id):
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="your_database_name"
        )
        
        cursor = conn.cursor(dictionary=True)
        
        # Query to get recent orders with adopted status
        query = """
        SELECT 
            cb.carebookingid, 
            cb.centerid, 
            cb.userid, 
            cb.species, 
            cb.breed,
            cb.date,
            cb.status,
            ci.centername,
            ci.centertype,
            ci.address,
            ci.city,
            ci.state,
            ci.mob,
            ci.mail,
            ci.description,
            ci.image,
            ur.email AS user_email,
            cr.careresourcername,
            cr.careresourcetype
        FROM 
            carebookings cb
        INNER JOIN 
            careresource_info ci ON cb.centerid = ci.careid
        INNER JOIN 
            care_reg cr ON ci.centerid = cr.centreid
        LEFT JOIN 
            usereg ur ON cb.userid = ur.id
        WHERE 
            cr.centreid = %s
        AND
            cb.status = 'adopted'
        ORDER BY 
            cb.carebookingid DESC
        """
        
        cursor.execute(query, (shelter_id,))
        results = cursor.fetchall()
        
        if not results:
            print("No recent orders found.")
            return
        
        # Display results in a table format
        headers = ["Booking ID", "Species", "Breed", "Date", "Status", "Center Name", "User Email", "Actions"]
        table_data = []
        
        for row in results:
            table_data.append([
                row['carebookingid'],
                row['species'],
                row['breed'],
                row['date'],
                row['status'],
                row['centername'],
                row['user_email'],
                f"[1] Accept | [2] Reject"
            ])
        
        print("\nRecent Orders:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Handle user action
        booking_id = input("\nEnter Booking ID to take action (or press Enter to skip): ")
        if booking_id:
            action = input("Enter action (1 for Accept, 2 for Reject): ")
            if action == "1":
                if update_booking_status(booking_id, "accepted"):
                    print("Booking accepted successfully!")
            elif action == "2":
                if update_booking_status(booking_id, "rejected"):
                    print("Booking rejected successfully!")
            else:
                print("Invalid action!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Example usage
    shelter_id = input("Enter shelter ID: ")
    get_recent_orders(shelter_id) 