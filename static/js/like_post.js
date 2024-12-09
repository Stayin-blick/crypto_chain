document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const postSlug = this.getAttribute('data-post-slug');
            const button = this.querySelector('.like-button');

            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update the button text based on the new like status
                if (data.liked === 1) {
                    button.textContent = 'Unlike';
                } else {
                    button.textContent = 'Like';
                }
                // Update the likes count
                const likeCount = document.getElementById(`like-count-${postSlug}`);
                if (likeCount) {
                    likeCount.textContent = `${data.likes_count} Likes`;
                }
            });
        });
    });
});
