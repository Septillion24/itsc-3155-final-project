let commentsPopulated = false;
let postsPopulated = false;

console.log("aaa");

let commentsShown = false;
let postsShown = true;
defaultDisplay = document.getElementById("commentsContainer").style.display;

function toggleCommentsPosts() {
    // show posts
    if (commentsShown) {
        console.log("Switching to posts!");
        if (!postsPopulated) {
            populateProfilePosts();
        }
        commentsShown = false;
        postsShown = true;

        document.getElementById("currentlyDisplaying").innerText = "Showing comments by this user...";
        document.getElementById("commentPostsButton").innerText = "Show Posts";

        document.getElementById("postsContainer").style.display = defaultDisplay;
        document.getElementById("commentsContainer").style.display = "none";
    }
    // show comments
    else if (postsShown) {
        console.log("Switching to comments!");
        if (!commentsPopulated) {
            populateProfileComments();
        }
        commentsShown = true;
        postsShown = false;
        document.getElementById("currentlyDisplaying").innerText = "Showing posts by this user...";
        document.getElementById("commentPostsButton").innerText = "Show Comments";
        document.getElementById("postsContainer").style.display = "none";
        document.getElementById("commentsContainer").style.display = defaultDisplay;
    }
}

function populateProfileComments() {
    fetch(`/user/${userID}/comments`)
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

console.log(populateProfileComments());

function populateProfilePosts() {
    fetch(`/user/${userID}/posts`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            const container = document.getElementById("postsContainer");
            data.forEach((item) => {
                const postDiv = document.createElement("div");
                const relativeTime = getRelativeTime(item.timestamp);
                postDiv.innerHTML = `
                <div class="postContainer">
                    <div class="postTitle">
                        <p>${item.title}</p>
                    </div>

                    <div class="userInfo">
                        <div class="userAvatar"><img src="/static/images/avatar2.png" /></div>
                        <div>
                            <div class="postUser">${item.owner}</div>
                            <div class="postTimestamp">${relativeTime}</div>
                        </div>
                    </div>
                
                    <div class="postBody">
                        <p>${item.text_content}</p>
                    </div>
                    <div class="postComments">
                        <p>${item.num_comments}</p>
                    </div>
                <div>
                `;
                container.appendChild(postDiv);
            });
        })
        .catch((error) => console.error("Error fetching posts:", error));
    postsPopulated = true;
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
        return `${diff} day${diff === 1 ? "" : "s"} ago`;
    }
}

console.log(populateProfilePosts());
