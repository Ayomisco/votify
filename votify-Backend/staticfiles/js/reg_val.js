// Function to handle form submission
function handleFormSubmission(event) {
    event.preventDefault();

    // Matriculation Number Format: YYYY/DEPT/YEAR/###
    const matricNumberPattern = /^\d{4}\/[A-Z]+\/\d{4}\/\d{3}$/;
    const matricNumber = document.getElementById("matricNumber").value;

    if (!matricNumberPattern.test(matricNumber)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Input',
            text: 'Invalid Matriculation Number format. Please use YYYY/DEPT/YEAR/###.'
        });
        return;
    }

    // Get other field values
    const fullName = document.getElementById("fullName").value;
    const department = document.getElementById("department").value;
    const schoolLevel = document.getElementById("schoolLevel").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    // Check for empty fields
    if (!fullName || !department || !schoolLevel || !email || !password || !confirmPassword) {
        Swal.fire({
            icon: 'warning',
            title: 'Incomplete Information',
            text: 'All fields are required.'
        });
        return;
    }

    // Email format validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Email',
            text: 'Please enter a valid email address.'
        });
        return;
    }

    // Password validation (minimum length of 8 characters)
    if (password.length < 8) {
        Swal.fire({
            icon: 'error',
            title: 'Weak Password',
            text: 'Password must be at least 8 characters long.'
        });
        return;
    }

    // Confirm Password validation
    if (password !== confirmPassword) {
        Swal.fire({
            icon: 'error',
            title: 'Password Mismatch',
            text: 'Password and Confirm Password do not match.'
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
            document.getElementById("registrationForm").submit(); // Submit the form after successful validation
        }
    });
}

// Attach event listener to the registration form
document.getElementById("registrationForm").addEventListener("submit", handleFormSubmission);
