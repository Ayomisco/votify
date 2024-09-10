// Function to handle form submission
function handleFormSubmission(event) {
    event.preventDefault();

    // Matriculation Number Format: YYYY/mtbm/HND/### or YYYY/mtbm/HN/###
    const matricNumberPattern = /^\d{4}\/mtbm\/(HND|HN)\/\d{3}$/;
    const matricNumber = document.getElementById("matricNumber").value;

    if (!matricNumberPattern.test(matricNumber)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Input',
            text: 'Invalid Matriculation Number format. Please use YYYY/mtbm/HND/### or YYYY/mtbm/HN/###.'
        });
        return;
    }

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const fullName = document.getElementById("fullName").value;
    const department = document.getElementById("department").value;

    if (!email || !password || !fullName || !department) {
        Swal.fire({
            icon: 'warning',
            title: 'Incomplete Information',
            text: 'All fields are required.'
        });
        return;
    }

    // All validations passed, show success message
    Swal.fire({
        icon: 'success',
        title: 'Registration Successful',
        text: 'Your registration has been completed successfully!',
        showConfirmButton: true,
        confirmButtonText: 'OK'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.replace("dashboard.html"); // Replace with your actual redirect URL
        }
    });
}

// Attach event listener to the registration form
document.getElementById("registrationForm").addEventListener("submit", handleFormSubmission);


// Function to handle form submission
function handleAdminFormSubmission(event) {
    event.preventDefault();

    

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    const fullName = document.getElementById("fullName").value;

    if (!email || !password || !confirm_password || !fullName || !department) {
        Swal.fire({
            icon: 'warning',
            title: 'Incomplete Information',
            text: 'All fields are required.'
        });
        return;
    }

    // All validations passed, show success message
    Swal.fire({
        icon: 'success',
        title: 'Registration Successful',
        text: 'Your registration has been completed successfully!',
        showConfirmButton: true,
        confirmButtonText: 'OK'
    })
}

// Attach event listener to the registration form
document.getElementById("adminregistrationForm").addEventListener("submit", handleAdminFormSubmission);


// Login Form submission handling
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Simulate successful login
    Swal.fire({
        icon: 'success',
        title: 'Login Successful',
        text: 'You have logged in successfully!',
        showConfirmButton: true,
        confirmButtonText: 'OK'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.replace("dashboard.html"); // Replace with your actual redirect URL
        }
    });
});
