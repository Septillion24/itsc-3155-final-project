function addDeleteButton() {
    if (owner === true) {
        const container = document.getElementById("deleteButtonContainer");
        const postDiv = document.createElement("div");
        postDiv.innerHTML = `<button class="deleteButton" onclick="deletePost()">Delete</button>`;
    }
}

function deletePost() {
    fetch("/", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ postID: postID }),
    }).then((response) => {
        if (response.status === 200) {
            window.location.href = '/';
        }
    });
}
