document.addEventListener('DOMContentLoaded', (event) => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;


    // Set light mode as default unless dark mode is explicitly set
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        themeToggleBtn.textContent = '☀️';
        themeIcon.style.display = "";
        themeIcon.textContent = '🌙';
    } else {
        // Ensure light mode is active by default
        body.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
        themeToggleBtn.textContent = '🌙';
        themeIcon.style.display = "none";
        themeIcon.textContent = '☀️';
    }


    themeToggleBtn.addEventListener('click', function() {
        var isDarkMode = body.classList.toggle('dark-mode');
        if (isDarkMode) {
            localStorage.setItem('theme', 'dark');
            themeToggleBtn.textContent = '☀️';
            themeIcon.style.display = "";
            themeIcon.textContent = '🌙';
        } else {
            localStorage.setItem('theme', 'light');
            themeToggleBtn.textContent = '🌙';
            themeIcon.style.display = "none";
            themeIcon.textContent = '☀️';
        }
    });
});