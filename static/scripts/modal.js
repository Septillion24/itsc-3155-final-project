function openModal() {
    document.getElementById('createPostModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('createPostModal').style.display = 'none';
}

function submitPost() {
// Get input values
var title = document.getElementById('title').value;
var content = document.getElementById('postContent').value;

// Create post HTML
var postHTML = `
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">${title}</h5>
            <p class="card-text">${content}</p>
        </div>
    </div>
`;

// Add post HTML to posts container
var postsContainer = document.getElementById('postsContainer');
postsContainer.innerHTML += postHTML;

closeModal();
}