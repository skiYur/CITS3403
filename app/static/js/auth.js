document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/login_status')
        .then(response => response.json())
        .then(data => {
            if (!data.isLoggedIn) {
                const restrictedLinks = document.querySelectorAll('.restricted-link');
                const restrictedButtons = document.querySelectorAll('.restricted-button');
                
                restrictedLinks.forEach(link => {
                    link.addEventListener('click', function(event) {
                        event.preventDefault();
                        alert('Please log in or sign up to use this feature.');
                    });
                });

                restrictedButtons.forEach(button => {
                    button.addEventListener('click', function(event) {
                        event.preventDefault();
                        alert('Please log in or sign up to use this feature.');
                    });
                });
            }
        })
        .catch(error => console.error('Error fetching login status:', error));
});
