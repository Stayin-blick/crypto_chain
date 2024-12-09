

/*
 * Initializes edit functionality for the provided edit buttons.
 * 
 * For each button in the `editButtons` collection:
 * - Retrieves the associated comment's ID upon click.
 * - Fetches the content of the corresponding comment.
 * - Populates the `commentText` input/textarea with the comment's content for editing.
 * - Updates the submit button's text to "Update".
 * - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
 */


/*
 * Initializes deletion functionality for the provided delete buttons.
 * 
 * For each button in the `deleteButtons` collection:
 * - Retrieves the associated comment's ID upon click.
 * - Updates the `deleteConfirm` link's href to point to the 
 * deletion endpoint for the specific comment.
 * - Displays a confirmation modal (`deleteModal`) to prompt 
 * the user for confirmation before deletion.
 */

document.addEventListener("DOMContentLoaded", function () {
    const commentText = document.getElementById("id_body");
    const commentForm = document.getElementById("commentForm");
    const submitButton = document.getElementById("submitButton");

    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("btn-delete");
    const deleteConfirm = document.getElementById("deleteConfirm");

    // Handle comment edit
    const editButtons = document.getElementsByClassName("btn-edit");
    for (let button of editButtons) {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            let commentContent = document.getElementById(`comment${commentId}`).innerText;
            commentText.value = commentContent;
            submitButton.innerText = "Update";
            commentForm.setAttribute("action", `edit_comment/${commentId}/`);
        });
    }

    // Handle comment delete
    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            deleteConfirm.href = `delete_comment/${commentId}`;
            deleteModal.show();
        });
    }

    // Handle like/unlike for comments and posts
    const likeButtons = document.querySelectorAll(".btn-like");
    for (let button of likeButtons) {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("data-comment_id");
            let postSlug = e.target.getAttribute("data-post_slug");

            // CSRF token handling
            let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // AJAX for liking/unliking comments
            fetch(`/like_comment/${commentId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    comment_id: commentId,
                    post_slug: postSlug,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update like button state and like count
                    e.target.innerText = data.liked ? "Unlike" : "Like";
                    let likeCount = document.getElementById(`like-count-${commentId}`);
                    likeCount.innerText = `${data.like_count} like(s)`;
                    e.target.classList.toggle("liked", data.liked);
                } else {
                    alert('There was an error processing your like/unlike request.');
                }
            });
        });
    }
});
