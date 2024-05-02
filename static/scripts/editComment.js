function editComment(commentID, newContent) {
    const newCommentContent = prompt('Enter your new username:');
    
    fetch('/edit/comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            commentID: commentID,
            newContent: newCommentContent
        })
    })
    .then(response => {
        if (response.ok) {
            // If the update was successful, you can handle the response here if needed
            console.log('Comment edited successfully');
            window.location.href = `/forum/post/${postID}`;
        } else {
            console.error('Failed to edit comment:', response.status);
        }
    })
    .catch(error => console.error('Error editing comment:', error));
}
