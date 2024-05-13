document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("drink-review-form");
    const reviewsContainer = document.getElementById("drink-reviews");
    const ratingStars = document.querySelectorAll("#rating-stars .star");

    // Function to highlight stars based on user's selection
    function highlightStars(selectedStar) {
        ratingStars.forEach(star => {
            if (parseInt(star.getAttribute("data-value")) <= selectedStar) {
                star.classList.remove("far");
                star.classList.add("fas");
            } else {
                star.classList.remove("fas");
                star.classList.add("far");
            }
        });
    }

    // Event listener to handle star rating selection
    ratingStars.forEach(star => {
        star.addEventListener("click", function() {
            const selectedStar = parseInt(this.getAttribute("data-value"));
            document.getElementById("rating").value = selectedStar;
            highlightStars(selectedStar);
        });
    });

    // Event listener to handle form submission
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        const drinkName = formData.get("drinkName");
        const review = formData.get("review");
        const rating = formData.get("rating");
        const instructions = formData.get("instructions");
        const ingredients = formData.get("ingredients");
        const reviewTemplate = `
            <div class="card mt-3">
                <div class="card-body">
                    <h5 class="card-title">${drinkName} (${rating} stars)</h5>
                    <p class="card-text">${review}</p>
                    <button class="btn btn-primary" data-toggle="collapse" data-target="#${drinkName.replace(/\s+/g, '-').toLowerCase()}">View Details</button>
                    <div class="collapse mt-2" id="${drinkName.replace(/\s+/g, '-').toLowerCase()}">
                        <h6>Instructions:</h6>
                        <p>${instructions}</p>
                        <h6>Ingredients:</h6>
                        <p>${ingredients}</p>
                    </div>
                </div>
            </div>
        `;
        reviewsContainer.insertAdjacentHTML("afterbegin", reviewTemplate);
        form.reset();
        document.getElementById("rating").value = "0";
        highlightStars(0); // Reset star ratings
    });
});
