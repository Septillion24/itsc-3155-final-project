function addDeleteButton() {
    if (owner === true) {
        const container = document.getElementById("deleteButtonContainer");
        const postDiv = document.createElement("div");
        postDiv.innerHTML = `<button class="deleteButton" onclick="deleteUser()">Delete</button>`;
    }
}

function deleteUser() {
    fetch("/delete/user", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ userID: userID }),
    }).then((response) => {
        if (response.status === 200) {
            window.location.href = '/';
        }
    });
}
