document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.btn-like');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const commentId = button.getAttribute('data-comment_id');
            const postSlug = button.getAttribute('data-post_slug');
            
            fetch(`/post/${postSlug}/comment/${commentId}/like/`, {
                
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked === 1) {
                    button.textContent = 'Unlike';
                } else {
                    button.textContent = 'Like';
                }

                // Update the like count
                document.getElementById(`like-count-${commentId}`).textContent = `${data.likes_count} like(s)`;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});