function editPost() {
    var postContentElement = document.getElementById('postContent');
    var editedContent = prompt('Edit your post:', postContentElement.textContent);

    if (editedContent !== null) {
        postContentElement.textContent = editedContent;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var editPostButton = document.getElementById('editPostButton');
    if (editPostButton) {
        editPostButton.addEventListener('click', editPost);
    }
});
