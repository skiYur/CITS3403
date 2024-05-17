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
                        showFlash('Please log in or sign up to use this feature.', 'danger');
                    });
                });

                restrictedButtons.forEach(button => {
                    button.addEventListener('click', function(event) {
                        event.preventDefault();
                        showFlash('Please log in or sign up to use this feature.', 'danger');
                    });
                });
            }
        })
        .catch(error => console.error('Error fetching login status:', error));
});

function showFlash(message, category) {
    const flashContainer = document.getElementById('flash-message-container');
    const flashMessage = document.createElement('div');
    flashMessage.classList.add('flash-message', 'alert', `alert-${category}`);
    flashMessage.textContent = message;
    
    flashContainer.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
    }, 3000);
}
