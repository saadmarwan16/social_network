function isLiked(post) {

    const statusContainer = post.querySelector('.like-status');
    const unLikeLink = post.querySelector('.unlike-link');
    const likeLink = post.querySelector('.like-link');

    // Send a POST request to know whether user has liked this post
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            post_id: post.id
        })
    })
    .then(response => response.json())
    .then(result => {

        // Give user and unlike option if the user already liked this post
        if (result.liked) {

            // Show the unlike icon and hide the like icon
            unLikeLink.style.display = 'none';
            likeLink.style.display = 'block';
        } else {

            // Show the like icon and hide the unlike icon
            likeLink.style.display = 'none';
            unLikeLink.style.display = 'block';
        }
    })

    // User clicks on the like status container to like or dislike a post
    statusContainer.addEventListener('click', event => {
        
        // If the user clicks on the already liked post dislike it, otherwise like it
        if (event.target.className === 'material-icons liked') {

            // Send a PUT request to update the database
            fetch('/like', {
                method: 'PUT',
                body: JSON.stringify({
                    post_id: post.id,
                    is_liked: false
                })
            })
            .then(response => response.json())
            .then(result => {
                
                // Update number of likes a post have  if a user is signed in and unlikes a post, else display
                // a must sign in message
                if (result.status === "Successful") {

                    // Show the like icon and hide the unlike icon
                    likeLink.style.display = 'none';
                    unLikeLink.style.display = 'block';

                    // Update the number of likes on the client side
                    let numOfLikes = post.querySelector(`.num-of-likes`).innerText;
                    numOfLikes--;
                    post.querySelector(`.num-of-likes`).innerText = numOfLikes;
                } else if (result.status === "Anonymous User") {
                    
                    // Display a must login or sign up message
                    post.querySelector('.no-like').style.display = 'inline';
                }
            })
        } else if (event.target.className === 'material-icons unliked') {

            // Send a PUT request to update the database
            fetch('/like', {
                method: 'PUT',
                body: JSON.stringify({
                    post_id: post.id,
                    is_liked: true
                })
            })
            .then(response => response.json())
            .then(result => {

                // Update number of likes a post have  if a user is signed in and likes a post, else display
                // a must sign in message
                if (result.status === "Successful") {

                    // Show the unlike icon and hide the like icon
                    unLikeLink.style.display = 'none';
                    likeLink.style.display = 'block';
                    
                    // Update the number of likes on the client side
                    let numOfLikes = post.querySelector(`.num-of-likes`).innerText;
                    numOfLikes++;
                    post.querySelector(`.num-of-likes`).innerText = numOfLikes;
                } else if (result.status === "Anonymous User") {

                    // Display a must login or sign up message
                    post.querySelector('.no-like').style.display = 'inline';
                    setTimeout(() => hideNoLike(post), 3000);
                }
            })
        }
    })
}

function hideNoLike(post) {
    
    // Display a must login or sign up message
    post.querySelector('.no-like').style.display = 'none';
}