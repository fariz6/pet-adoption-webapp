<?php
include 'config.php';

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

header('Content-Type: application/json');

if (isset($_POST['user_id'])) {
    $user_id = mysqli_real_escape_string($conn, $_POST['user_id']);
    
    $query = "SELECT * FROM users WHERE id = '$user_id'";
    $result = mysqli_query($conn, $query);
    
    if (!$result) {
        echo json_encode(['error' => 'Database query failed: ' . mysqli_error($conn)]);
        exit;
    }
    
    if (mysqli_num_rows($result) > 0) {
        $user = mysqli_fetch_assoc($result);
        echo json_encode([
            'name' => $user['name'] ?? 'Not available',
            'email' => $user['email'] ?? 'Not available',
            'phone' => $user['phone'] ?? 'Not available',
            'address' => $user['address'] ?? 'Not available',
            'city' => $user['city'] ?? 'Not available',
            'state' => $user['state'] ?? 'Not available'
        ]);
    } else {
        echo json_encode(['error' => 'User not found']);
    }
} else {
    echo json_encode(['error' => 'User ID not provided']);
}
?> 