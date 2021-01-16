document.addEventListener('DOMContentLoaded', () => {
    const postsView = document.querySelector('#posts-view');
    const followersView = document.querySelector('#followers-view');
    const followingView = document.querySelector('#following-view');

    // Load the post view by default
    postsView.style.display = 'block';

    document.querySelector('.single-profile-row').addEventListener('click', event => {
        if (event.target.id === 'single-posts') {
            
            // Hide other views and show the posts view
            followersView.style.display = 'none';
            followingView.style.display = 'none';
            postsView.style.display = 'block';
        } else if (event.target.id === 'single-followers') {
            
            // Hide other views and show the followers view
            followingView.style.display = 'none';
            postsView.style.display = 'none';
            followersView.style.display = 'block';
        } else if (event.target.id === 'single-following') {
            
            // Hide other views and show the following view
            followersView.style.display = 'none';
            postsView.style.display = 'none';
            followingView.style.display = 'block';
        }
    })

    document.querySelectorAll('.follow-btn').forEach(button => {

        // A follow button is clicked
        button.addEventListener('click', event => {
            event.preventDefault();
            const follow = button.parentElement;

            // Send a PUT request to update the database
            fetch('/follow', {
                method: 'PUT',
                body: JSON.stringify({
                    followee: follow.querySelector('.followee').value
                })
            })
            .then(response => response.json())
            .then(results => {

                // User tries to follow a user he / she is not already following
                if (results.message === 'Successful') {
                    
                    document.querySelectorAll('.follow-btn').forEach(followBtn => {
                        followBtn.style.display = 'none';
                    })

                    document.querySelectorAll('.unfollow-btn').forEach(unFollowBtn => {
                        unFollowBtn.style.display = 'inline-block';
                    })
                }
            })
        })
    })

    // Send a PUT request to update the database
    document.querySelectorAll('.unfollow-btn').forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault();
            const follow = button.parentElement;

            fetch('/unfollow', {
                method: 'PUT',
                body: JSON.stringify({
                    followee: follow.querySelector('.followee').value
                })
            })
            .then(response => response.json())
            .then(results => {

                // User tries to unfollow a user he / she is already following
                if (results.message === 'Successful') {

                    document.querySelectorAll('.unfollow-btn').forEach(unFollowBtn => {
                        unFollowBtn.style.display = 'none';
                    })

                    document.querySelectorAll('.follow-btn').forEach(followBtn => {
                        followBtn.style.display = 'inline-block';
                    })
                }
            })
        })
    })
})