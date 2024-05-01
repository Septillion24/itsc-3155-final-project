function populateProfileComments() {
    fetch(`/forum/post/${postID}/comments`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            const container = document.getElementById("commentsContainer");
            data.forEach((item) => {
                const postDiv = document.createElement("div");
                const relativeTime = getRelativeTime(item.timestamp);
                postDiv.innerHTML = `
                <div class="commentContainer">
                    <div class="userInfo">
                        <div class="userAvatar"><img src="static/images/avatar2.png" /></div>
                        <div>
                            <div class="commentUser">${item.owner}</div>
                            <div class="commentTimestamp">${relativeTime}</div>
                        </div>
                    </div>
                
                    <div class="commentBody">
                        <p>${item.content}</p>
                    </div>
                <div>
            `;
                container.appendChild(postDiv);
            });
        })
        .catch((error) => console.error("Error fetching posts:", error));
    commentsPopulated = true;
}
