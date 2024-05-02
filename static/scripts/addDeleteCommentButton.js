function addDeleteButton() {
    const container = document.getElementById("deleteButtonContainer");
    const buttonDiv = document.createElement("div");
    buttonDiv.innerHTML = `<button class="deleteButton" onclick="deleteComment()">Delete</button>`;
    container.appendChild(buttonDiv);
}

function deleteComment() {
    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ postID: postID }),
    }).then((response) => {
        if (response.status === 200) {
            window.location.href = "/";
        }
    });
}

addDeleteButton();
