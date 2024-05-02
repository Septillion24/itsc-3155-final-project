// function addDeleteButton() {
//     const container = document.getElementById("deleteButtonContainer");
//     const buttonDiv = document.createElement("div");
//     buttonDiv.innerHTML = `<button class="deleteButton" onclick="deleteUser()">Delete</button>`;
//     container.appendChild(buttonDiv);
// }

function deleteUser() {
    fetch("/delete/user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ userID: userID }),
    }).then((response) => {
        if (response.status === 200) {
            window.location.href = "/";
        } else {
            console.log(response);
        }
    });
}

addDeleteButton();
