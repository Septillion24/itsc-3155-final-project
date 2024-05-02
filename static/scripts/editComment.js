function editComment(commentID) {
    var newContent = prompt('Edit your comment:');
    
    if (newContent !== null) {
        fetch('/edit/comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain', 
            },
            body: newContent
        })
        .then(response => {
            if (response.ok) {
                console.log('Comment edited successfully');
            } else {
                console.error('Failed to edit comment:', response.status);
            }
        })
        .catch(error => console.error('Error editing comment:', error));
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var editCommentButton = document.getElementById('editCommentButton');
    if (editCommentButton) {
        var commentID = editCommentButton.dataset.commentId;
        editCommentButton.addEventListener('click', function() {
            editComment(commentID);
        });
    }
});
