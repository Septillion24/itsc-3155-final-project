document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.body;

    function applyTheme(isDarkMode) {
        body.classList.toggle('dark-mode', isDarkMode);
        themeToggleBtn.textContent = isDarkMode ? '☀️' : '🌙';
        localStorage.setItem('theme', isDarkMode ? 'dark-mode' : 'light-mode');
    }

    const isDarkMode = localStorage.getItem('theme') === 'dark-mode';
    applyTheme(isDarkMode);

    themeToggleBtn.addEventListener('click', function() {
        const isCurrentlyDark = body.classList.contains('dark-mode');
        body.classList.add('transitioning');
        setTimeout(() => {
            applyTheme(!isCurrentlyDark);
            body.classList.remove('transitioning');
        }, 300);
    });
});
