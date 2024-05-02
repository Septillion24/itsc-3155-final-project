function postComment() {
    var commentContent = document.getElementById("commentContent").value;
    console.log("Comment content:", commentContent); // Add this line for debugging
    fetch("/forum/makeComment", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "commentContent=" + encodeURIComponent(commentContent) + `&postID=${postID}`
    }).then(response => {
        if (response.ok) {
            window.location.reload(); // Reload the page after successful comment creation
        } else {
            console.error("Error creating comment:", response);
        }
    }).catch(error => {
        console.error("Error creating comment:", error);
    });
}
