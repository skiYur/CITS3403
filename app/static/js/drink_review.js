document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("drink-review-form");
    const ratingStars = document.querySelectorAll("#rating-stars .star");

    function highlightStars(selectedStar) {
        ratingStars.forEach(star => {
            if (parseInt(star.getAttribute("data-value")) <= selectedStar) {
                star.classList.remove("far");
                star.classList.add("fas");
                star.classList.add("filled");
            } else {
                star.classList.add("far");
                star.classList.remove("fas");
                star.classList.remove("filled");
            }
        });
    }

    function resetStars() {
        ratingStars.forEach(star => {
            star.classList.remove("hovered");
            star.classList.remove("filled");
        });
    }

    ratingStars.forEach(star => {
        star.addEventListener("mouseover", function() {
            resetStars();
            highlightStars(this.dataset.value);
        });

        star.addEventListener("mouseout", function() {
            resetStars();
            if (document.getElementById("rating").value) {
                highlightStars(document.getElementById("rating").value);
            }
        });

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
                window.location.reload();
            } else {
                alert("Failed to submit the review. Please try again.");
            }
        }).catch(error => {
            console.error('Error submitting review:', error);
            alert("Error submitting the review.");
        });
    });

    window.deleteReview = function(reviewId) {
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

    window.likePost = function(postId, action) {
        fetch(`/like_post/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: action })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  document.getElementById(`like-count-${postId}`).innerText = data.likes;
                  document.getElementById(`super-like-count-${postId}`).innerText = data.super_likes;
                  document.getElementById(`dislike-count-${postId}`).innerText = data.dislikes;
              } else {
                  alert(data.message);
              }
          }).catch(error => {
              console.error('Error:', error);
              alert('Error updating like status.');
          });
    }

    function displayStars() {
        const ratings = document.querySelectorAll('.review-rating');
        ratings.forEach(rating => {
            const ratingValue = parseInt(rating.getAttribute('data-rating'));
            for (let i = 1; i <= 5; i++) {
                const star = document.createElement('i');
                star.classList.add('fa-star');
                if (i <= ratingValue) {
                    star.classList.add('fas');
                } else {
                    star.classList.add('far');
                }
                rating.appendChild(star);
            }
        });
    }

    displayStars();

    document.getElementById('toggle-review-form').addEventListener('click', function() {
        var formContainer = document.getElementById('review-form-container');
        if (formContainer.style.display === 'none' || formContainer.style.display === '') {
            formContainer.style.display = 'block';
        } else {
            formContainer.style.display = 'none';
        }
    });
});
