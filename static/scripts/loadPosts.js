function populatePosts() {
    fetch("/forum/getposts?numPosts=10")
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            const container = document.getElementById("postsContainer");
            const loadingWidget = document.getElementById("loadingWidget");

            data.forEach((item) => {
                const postDiv = document.createElement("div");
                const relativeTime = getRelativeTime(item.timestamp);
                postDiv.innerHTML = `
                <div class="postContainer">
                    <div class="postTitle">
                        <a href="/forum/post/${item.post_id}">${item.title}</a>
                    </div>

                    <div class="userInfo">
                        <div class="userAvatar"><img src="static/images/avatar2.png" /></div>
                        <div>
                            <div class="postUser"><a href="/user/${item.owner}">${item.owner_name}</a></div>
                            <div class="postTimestamp">${relativeTime}</div>
                        </div>
                    </div>
                
                    <div class="postBody">
                        <p>${item.text_content}</p>
                    </div>
                <div>
                `; // off-brand jsx
                container.appendChild(postDiv);
                console.log(item.owner)
            });
            loadingWidget.remove();
        })
        .catch((error) => console.error("Error fetching posts:", error));
}

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

console.log(populatePosts());
