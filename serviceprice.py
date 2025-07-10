#!C:/Users/abdfa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n\n")

import pymysql
import cgi
import cgitb


cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="petmatch")
cur = con.cursor()
form = cgi.FieldStorage()
Cid = form.getvalue("centreid")
s = """select * from care_reg where centreid="%s" """ % (Cid)
cur.execute(s)
res = cur.fetchall()

# HTML Form
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pet Center Services</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .service-modal .modal-body {
            max-height: 70vh;
            overflow-y: auto;
        }
        .service-item {
            display: flex;
            justify-content: space-between;
            padding: 8px;
            border-bottom: 1px solid #eee;
        }
        .service-item:last-child {
            border-bottom: none;
        }
        .remove-service {
            color: #dc3545;
            cursor: pointer;
            margin-left: 10px;
        }
        #servicesList {
            margin-top: 15px;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 10px;
            max-height: 200px;
            overflow-y: auto;
        }
        .service-total {
            font-weight: bold;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #dee2e6;
        }
        .service-type-badge {
            font-size: 0.75rem;
            margin-left: 5px;
        }
    </style>
</head>
<body>

<!-- Service Selection Modal -->
<div class="modal fade" id="serviceSelectionModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Add Services</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="serviceForm">
                    <input type="hidden" id="centerId" name="center_id">
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="serviceCategory" class="form-label">Service Category</label>
                            <select class="form-select" id="serviceCategory" name="service_category">
                                <option value="">-- Select Category --</option>
                                <option value="veterinary">Veterinary</option>
                                <option value="spa">Spa & Grooming</option>
                                <option value="training">Training</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label for="serviceType" class="form-label">Service Type</label>
                            <select class="form-select" id="serviceType" name="service_type" disabled>
                                <option value="">-- Select Service --</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="servicePrice" class="form-label">Price ($)</label>
                            <input type="number" class="form-control" id="servicePrice" name="service_price" min="0" step="0.01">
                        </div>
                        <div class="col-md-6 d-flex align-items-end">
                            <button type="button" class="btn btn-primary" id="addServiceBtn">Add Service</button>
                        </div>
                    </div>
                    
                    <div class="card mt-3">
                        <div class="card-header">
                            <h5 class="mb-0">Selected Services</h5>
                        </div>
                        <div class="card-body">
                            <div id="servicesList">
                                <p class="text-muted">No services added yet</p>
                            </div>
                            <div class="service-total">
                                Total: <span id="totalPrice">$0.00</span>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-success" id="saveServicesBtn">Save Services</button>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
    // Sample service data (replace with actual API calls)
    const serviceData = {
        veterinary: [
            { id: 1, name: "General Checkup" },
            { id: 2, name: "Vaccination" },
            { id: 3, name: "Dental Cleaning" },
            { id: 4, name: "Spay/Neuter" },
            { id: 5, name: "Emergency Visit" }
        ],
        spa: [
            { id: 6, name: "Basic Grooming" },
            { id: 7, name: "Deluxe Spa Package" },
            { id: 8, name: "Nail Trimming" },
            { id: 9, name: "Ear Cleaning" },
            { id: 10, name: "Medicated Bath" }
        ],
        training: [
            { id: 11, name: "Basic Obedience" },
            { id: 12, name: "Advanced Training" },
            { id: 13, name: "Behavior Correction" },
            { id: 14, name: "Puppy Training" },
            { id: 15, name: "Service Dog Training" }
        ]
    };

    let selectedServices = [];
    let currentCenterId = null;

    // Initialize modal functionality
    document.addEventListener('DOMContentLoaded', function() {
        const serviceModal = document.getElementById('serviceSelectionModal');
        const serviceCategory = document.getElementById('serviceCategory');
        const serviceType = document.getElementById('serviceType');
        const servicePrice = document.getElementById('servicePrice');
        const addServiceBtn = document.getElementById('addServiceBtn');
        const saveServicesBtn = document.getElementById('saveServicesBtn');
        
        // When category changes, populate service types
        serviceCategory.addEventListener('change', function() {
            serviceType.disabled = !this.value;
            serviceType.innerHTML = '<option value="">-- Select Service --</option>';
            
            if (this.value) {
                const services = serviceData[this.value];
                services.forEach(service => {
                    const option = document.createElement('option');
                    option.value = service.id;
                    option.textContent = service.name;
                    serviceType.appendChild(option);
                });
            }
        });
        
        // Add service to list
        addServiceBtn.addEventListener('click', function() {
            const category = serviceCategory.value;
            const typeId = serviceType.value;
            const typeName = serviceType.options[serviceType.selectedIndex].text;
            const price = parseFloat(servicePrice.value);
            
            if (!category || !typeId || isNaN(price) || price <= 0) {
                alert('Please select a valid service and enter a price');
                return;
            }
            
            selectedServices.push({
                category,
                typeId,
                typeName,
                price
            });
            
            updateServicesList();
            
            // Reset form
            servicePrice.value = '';
        });
        
        // Save services to server
        saveServicesBtn.addEventListener('click', function() {
            if (selectedServices.length === 0) {
                alert('Please add at least one service');
                return;
            }
            
            const formData = new FormData();
            formData.append('center_id', currentCenterId);
            formData.append('services', JSON.stringify(selectedServices));
            
            fetch('save_services.py', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Services saved successfully!');
                    bootstrap.Modal.getInstance(serviceModal).hide();
                } else {
                    alert('Error saving services: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving services');
            });
        });
    });
    
    // Function to open the modal
    function openServiceModal(centerId) {
        currentCenterId = centerId;
        selectedServices = [];
        
        // Reset form
        document.getElementById('serviceForm').reset();
        document.getElementById('serviceType').disabled = true;
        document.getElementById('servicesList').innerHTML = '<p class="text-muted">No services added yet</p>';
        document.getElementById('totalPrice').textContent = '$0.00';
        
        // Set center ID
        document.getElementById('centerId').value = centerId;
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('serviceSelectionModal'));
        modal.show();
    }
    
    // Update the services list display
    function updateServicesList() {
        const servicesList = document.getElementById('servicesList');
        
        if (selectedServices.length === 0) {
            servicesList.innerHTML = '<p class="text-muted">No services added yet</p>';
            document.getElementById('totalPrice').textContent = '$0.00';
            return;
        }
        
        servicesList.innerHTML = '';
        let total = 0;
        
        selectedServices.forEach((service, index) => {
            total += service.price;
            
            const serviceItem = document.createElement('div');
            serviceItem.className = 'service-item';
            serviceItem.innerHTML = `
                <div>
                    <span>${service.typeName}</span>
                    <span class="badge bg-secondary service-type-badge">${service.category}</span>
                </div>
                <div>
                    <span>$${service.price.toFixed(2)}</span>
                    <span class="remove-service" onclick="removeService(${index})">×</span>
                </div>
            `;
            servicesList.appendChild(serviceItem);
        });
        
        document.getElementById('totalPrice').textContent = `$${total.toFixed(2)}`;
    }
    
    // Remove service from list
    function removeService(index) {
        selectedServices.splice(index, 1);
        updateServicesList();
    }
</script>
</body>
</html>
""")
