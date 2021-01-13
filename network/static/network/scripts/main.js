document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.all-posts-jumbotron').forEach(post => {

        isLiked(post);

        // This post was created by this current user
        if (post.querySelector('.edit-link') !== null) {

            const editForm = post.querySelector('.edit-post-jumbotron');

            // If user clicks on the edit link then show the edit form
            post.querySelector('.edit-link').addEventListener('click', () => {
                post.querySelector('.no-edit').style.display = 'none';
                editForm.style.display = 'block';
            })

            // If user clicks on the close button then hide the edit form
            editForm.querySelector('.cancel-btn').addEventListener('click', () => {
                editForm.style.display = 'none';
            })

            // User clicks on the save button to save an edited post
            editForm.querySelector('.save-btn').addEventListener('click', event => {
                event.preventDefault();

                // Send a PUT request to edit the database to change the content of the post
                fetch('/edit-post', {
                    method: 'PUT',
                    body: JSON.stringify({
                        post_id: post.id,
                        post_content: editForm.querySelector('.post').value
                    })
                })
                .then(response => response.json())
                .then(results => {
                    if (results.message === 'Successful') {

                        // After post has been successfully edit, change post's content and remove the edit form
                        post.querySelector('.content').innerText = editForm.querySelector('.post').value
                        editForm.style.display = 'none';
                    }
                    
                    // User does not input anything into edit form and then submit
                    else {
                        post.querySelector('.no-edit').innerText = results.message;
                        post.querySelector('.no-edit').style.display = 'block';
                    }
                })
            })
        }
    })
})