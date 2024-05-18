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

    // Search reviews function
    window.searchReviews = function(event) {
        event.preventDefault();
        const query = document.getElementById("search-input").value;

        fetch(`/search_reviews?drink_type=${encodeURIComponent(drinkType)}&query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayReviews(data.reviews);
                } else {
                    alert('No reviews found.');
                }
            }).catch(error => {
                console.error('Error fetching reviews:', error);
                alert('Error fetching reviews.');
            });
    }

    // Display reviews function
    function displayReviews(reviews) {
        const reviewsContainer = document.getElementById('drink-reviews');
        reviewsContainer.innerHTML = '';
        reviews.forEach(review => {
            const reviewElement = document.createElement('div');
            reviewElement.classList.add('review');
            reviewElement.innerHTML = `
                <div class="review-body">
                    <div class="review-header">
                        <img src="${review.user_avatar}" alt="${review.user_username}'s avatar" class="avatar">
                        <strong>${review.user_username}</strong>
                    </div>
                    <div class="review-content-container">
                        <p><strong>Drink Type:</strong> ${review.drink_type}</p>
                        <p><strong>Drink Name:</strong> ${review.drink_name}</p>
                        <p><strong>Rating:</strong> <span class="review-rating" data-rating="${review.rating}"></span></p>
                        <p><strong>Instructions:</strong> ${review.instructions}</p>
                        <p><strong>Ingredients:</strong> ${review.ingredients}</p>
                        <p><strong>Review:</strong> ${review.content}</p>
                        <p><strong>Likes:</strong> <span id="like-count-${review.id}">${review.likes}</span></p>
                        <p><strong>Super Likes:</strong> <span id="super-like-count-${review.id}">${review.super_likes}</span></p>
                        <p><strong>Dislikes:</strong> <span id="dislike-count-${review.id}">${review.dislikes}</span></p>
                    </div>
                </div>
                <small class="post-time" data-time="${review.created_at}">Posted on ${new Date(review.created_at).toLocaleString()}</small>
                <small>Review ID: ${review.id}</small>
                ${review.user_id === session_user_id ? `<button onclick="deleteReview('${review.id}')" class="btn btn-danger"><i class="fas fa-trash"></i> Delete</button>` : ''}
            `;
            reviewsContainer.appendChild(reviewElement);
        });
        displayStars();
    }

    // Display stars function
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

    // Convert server time to local time (existing code)
    const postTimes = document.querySelectorAll('.post-time');
    postTimes.forEach(function(postTime) {
        const serverTime = new Date(postTime.getAttribute('data-time') + 'Z');
        const localTime = serverTime.toLocaleString();
        postTime.textContent = `Posted on ${localTime}`;
    });

    // Toggle review form visibility
    document.getElementById('toggle-review-form').addEventListener('click', function() {
        const formContainer = document.getElementById('review-form-container');
        formContainer.style.display = formContainer.style.display === 'none' || formContainer.style.display === '' ? 'block' : 'none';
    });
});
