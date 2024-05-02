function addDeleteButton() {
    const container = document.getElementById("deleteButtonContainer");
    const buttonDiv = document.createElement("div");
    buttonDiv.innerHTML = `<button class="deleteButton" onclick="deleteComment()">Delete</button>`;
    container.appendChild(buttonDiv);
}

function deleteComment(commentID) {
    fetch("/delete/comment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ commentID: commentID }),
    }).then((response) => {
        if (response.status === 200) {
            window.location.href = "/";
        }
    });
}

addDeleteButton();
