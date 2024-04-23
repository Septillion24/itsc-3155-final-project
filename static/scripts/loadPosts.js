function populatePosts() {
    fetch("/forum/getposts?numPosts=10")
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            const container = document.getElementById("postsContainer");
            data.forEach((item) => {
                const postDiv = document.createElement("div");
                postDiv.innerHTML = `<strong>Post ID:</strong> ${item.id} <br> <strong>Content:</strong> ${item.content}`;
                container.appendChild(postDiv);
            });
        })
        .catch((error) => console.error("Error fetching posts:", error));
}

console.log(populatePosts())