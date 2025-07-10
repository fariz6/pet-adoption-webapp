                    <thead>
                        <tr>
                            <th>S.No</th>
                            <th>Center Name</th>
                            <th>Service Type</th>
                            <th>Species</th>
                            <th>Breed</th>
                            <th>Request Date</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $sno = 1;
                        while ($row = mysqli_fetch_assoc($result)) {
                            $center_id = $row['center_id'];
                            $center_query = "SELECT * FROM centers WHERE id = '$center_id'";
                            $center_result = mysqli_query($conn, $center_query);
                            $center = mysqli_fetch_assoc($center_result);
                        ?>
                            <tr>
                                <td><?php echo $sno++; ?></td>
                                <td>
                                    <div class="d-flex align-items-center">
                                        <img src="../uploads/<?php echo $center['image']; ?>" class="rounded-circle me-2" width="40" height="40" alt="Center Image">
                                        <span><?php echo $center['name']; ?></span>
                                    </div>
                                </td>
                                <td><?php echo $row['service_type']; ?></td>
                                <td><?php echo $row['species']; ?></td>
                                <td><?php echo $row['breed']; ?></td>
                                <td><?php echo date('d-m-Y', strtotime($row['request_date'])); ?></td>
                                <td>
                                    <span class="badge bg-<?php echo $row['status'] == 'pending' ? 'warning' : ($row['status'] == 'approved' ? 'success' : 'danger'); ?>">
                                        <?php echo ucfirst($row['status']); ?>
                                    </span>
                                </td>
                                <td>
                                    <button type="button" class="btn btn-primary btn-sm view-btn" data-bs-toggle="modal" data-bs-target="#viewModal" 
                                            data-id="<?php echo $row['id']; ?>"
                                            data-user-id="<?php echo $row['user_id']; ?>">
                                        <i class="fas fa-eye"></i> View
                                    </button>
                                </td>
                            </tr>
                        <?php } ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- View Modal -->
    <div class="modal fade" id="viewModal" tabindex="-1" aria-labelledby="viewModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="viewModalLabel">User Information</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Name:</strong> <span id="view-name"></span></p>
                            <p><strong>Email:</strong> <span id="view-email"></span></p>
                            <p><strong>Phone:</strong> <span id="view-phone"></span></p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Address:</strong> <span id="view-address"></span></p>
                            <p><strong>City:</strong> <span id="view-city"></span></p>
                            <p><strong>State:</strong> <span id="view-state"></span></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        $(document).ready(function() {
            $('.view-btn').click(function() {
                var userId = $(this).data('user-id');
                console.log('Fetching user info for ID:', userId); // Debug log
                
                $.ajax({
                    url: 'get_user_info.php',
                    type: 'POST',
                    data: { user_id: userId },
                    dataType: 'json',
                    success: function(response) {
                        console.log('Response received:', response); // Debug log
                        
                        if (response.error) {
                            alert('Error: ' + response.error);
                            return;
                        }
                        
                        $('#view-name').text(response.name);
                        $('#view-email').text(response.email);
                        $('#view-phone').text(response.phone);
                        $('#view-address').text(response.address);
                        $('#view-city').text(response.city);
                        $('#view-state').text(response.state);
                    },
                    error: function(xhr, status, error) {
                        console.error('AJAX Error:', status, error); // Debug log
                        alert('Error fetching user information. Please try again.');
                    }
                });
            });
        });
    </script>
</body>
</html> 