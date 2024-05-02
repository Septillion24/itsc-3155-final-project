function editComment(commentID, newContent) {
    const newUsername = prompt('Enter your new username:', currentUsername);
    
    fetch('/edit/comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            commentID: commentID,
            newContent: newUsername
        })
    })
    .then(response => {
        if (response.ok) {
            // If the update was successful, you can handle the response here if needed
            console.log('Comment edited successfully');
        } else {
            console.error('Failed to edit comment:', response.status);
        }
    })
    .catch(error => console.error('Error editing comment:', error));
}
