


function includeHTML(id, url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const element = document.getElementById(id);
            element.innerHTML = data;

            // Manually execute any scripts that were included
            const scripts = element.getElementsByTagName('script');
            for (let i = 0; i < scripts.length; i++) {
                const script = document.createElement('script');
                script.text = scripts[i].innerText; // Inline scripts
                if (scripts[i].src) {
                    script.src = scripts[i].src; // External scripts
                }
                document.body.appendChild(script); // Append to the body or head
            }
        })
        .catch(error => console.error('Error loading the HTML:', error));
}


// Load the header and footer
document.addEventListener("DOMContentLoaded", function() {
    includeHTML('header', '../components/header.html');
    includeHTML('footer', '../components/footer.html');
    includeHTML('header_1', '../components/header_1.html');
    includeHTML('main_footer', '../components/main_footer.html');
    includeHTML('sidebar', '../components/sidebar.html');
    includeHTML('topbar', '../components/topbar.html');

});

