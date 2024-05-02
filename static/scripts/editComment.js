function editComment(commentID, newContent) {
    fetch('/edit/comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            commentID: commentID,
            newContent: newContent
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
