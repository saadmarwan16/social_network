document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.all-posts-jumbotron').forEach(post => {

        isLiked(post);

        if (post.querySelector('.edit-link') !== null) {

            const editForm = post.querySelector('.edit-post-jumbotron');

            post.querySelector('.edit-link').addEventListener('click', () => {
                post.querySelector('.no-edit').style.display = 'none';
                editForm.style.display = 'block';
            })

            editForm.querySelector('.cancel-btn').addEventListener('click', () => {
                editForm.style.display = 'none';
            })

            editForm.querySelector('.save-btn').addEventListener('click', event => {
                event.preventDefault();

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
                        post.querySelector('.content').innerText = editForm.querySelector('.post').value
                        editForm.style.display = 'none';
                    } else {
                        post.querySelector('.no-edit').innerText = results.message;
                        post.querySelector('.no-edit').style.display = 'block';
                    }
                })
            })
        }
    })
})