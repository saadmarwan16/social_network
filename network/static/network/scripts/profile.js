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
        button.addEventListener('click', event => {
            event.preventDefault();
            const follow = button.parentElement;

            fetch('/follow', {
                method: 'PUT',
                body: JSON.stringify({
                    followee: follow.querySelector('.followee').value
                })
            })
            .then(response => response.json())
            .then(results => {
                if (results.message === 'Successful') {
                    button.style.display = 'none'
                    follow.querySelector('.unfollow-btn').style.display = 'inline-block';
                }
            })
        })
    })

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
                if (results.message === 'Successful') {
                    button.style.display = 'none';
                    follow.querySelector('.follow-btn').style.display = 'inline-block';
                }
            })
        })
    })
})