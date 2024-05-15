document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("drink-review-form");
    const ratingStars = document.querySelectorAll("#rating-stars .star");

    function highlightStars(selectedStar) {
        ratingStars.forEach(star => {
            if (parseInt(star.getAttribute("data-value")) <= selectedStar) {
                star.classList.remove("far");
                star.classList.add("fas");
            } else {
                star.classList.add("far");
                star.classList.remove("fas");
            }
        });
    }

    ratingStars.forEach(star => {
        star.addEventListener("click", function() {
            const selectedStar = parseInt(this.getAttribute("data-value"));
            document.getElementById("rating").value = selectedStar;
            highlightStars(selectedStar);
        });
    });





    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                // Assuming you want to fetch and display the reviews or refresh the page
                window.location.reload();
            } else {
                alert("Failed to submit the review. Please try again.");
            }
        }).catch(error => {
            console.error('Error submitting review:', error);
            alert("Error submitting the review.");
        });
    });



    function deleteReview(reviewId) {
        if (confirm('Are you sure you want to delete this review?')) {
            fetch(`/delete_review/${reviewId}`, {
                method: 'DELETE'
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      alert('Review deleted successfully');
                      window.location.reload();
                  } else {
                      alert('Failed to delete review. Please try again.');
                  }
              }).catch(error => {
                  console.error('Error deleting review:', error);
                  alert('Error deleting the review.');
              });
        }
    }
    
    
});
