function getRelativeTime(timestamp) {
    const time = new Date(timestamp);
    const now = new Date();
    const diffInSeconds = Math.floor((now - time) / 1000);

    if (diffInSeconds < 60) {
        return "just now";
    } else if (diffInSeconds < 3600) {
        const diff = Math.floor(diffInSeconds / 60);
        return `${diff} minute${diff === 1 ? "" : "s"} ago`;
    } else if (diffInSeconds < 86400) {
        const diff = Math.floor(diffInSeconds / 3600);
        return `${diff} hour${diff === 1 ? "" : "s"} ago`;
    } else {
        const diff = Math.floor(diffInSeconds / 86400);
        return `${diff} day${diff === 1 ? "" : "s"} ago`; // i am a master of js, bow to me.
    }
}



function populatePostComments() {
    fetch(`/forum/${postID}/comments`)
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
                            <div class="userAvatar"><img src="/static/images/avatar2.png" /></div>
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


populatePostComments()