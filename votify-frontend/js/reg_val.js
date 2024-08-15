document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Matriculation Number Format: YYYY/ND/Dept/###
    const matricNumberPattern = /^\d{4}\/ND\/\w+\/\d{3}$/;
    const matricNumber = document.getElementById("matricNumber").value;

    if (!matricNumberPattern.test(matricNumber)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Input',
            text: 'Invalid Matriculation Number format. Please use YYYY/ND/Dept/###.'
        });
        return;
    }

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const fullName = document.getElementById("fullName").value;
    const department = document.getElementById("department").value;

    if (email === "" || password === "" || fullName === "" || department === "") {
        Swal.fire({
            icon: 'warning',
            title: 'Incomplete Information',
            text: 'All fields are required.'
        });
        return;
    } 

    // Submit the form
    this.submit();
});

document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Matriculation Number Format: YYYY/ND/Dept/###
    const matricNumberPattern = /^\d{4}\/ND\/\w+\/\d{3}$/;
    const matricNumber = document.getElementById("matricNumber").value;

    if (!matricNumberPattern.test(matricNumber)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Input',
            text: 'Invalid Matriculation Number format. Please use YYYY/ND/Dept/###.'
        });
        return;
    }

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const fullName = document.getElementById("fullName").value;
    const department = document.getElementById("department").value;

    if (email === "" || password === "" || fullName === "" || department === "") {
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
                    // Perform form submission via AJAX or redirect directly
                    // Simulate form submission
                    // Redirect to another page
                    window.location.replace("../index.html"); // Replace with your actual redirect URL
                }
            });
});

// Login Form
 document.getElementById("loginForm").addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the form from submitting

            // Simulate successful login
            Swal.fire({
                icon: 'success',
                title: 'Login Successful',
                text: 'You have logged in successfully!',
                showConfirmButton: true,
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirect to another page and replace current entry in history
                    window.location.replace("dashboard.html"); // Replace with your actual redirect URL
                }
            });
        });
