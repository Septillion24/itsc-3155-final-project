document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    let darkMode = localStorage.getItem('dark-mode');

    const enableDarkMode = () => {
        addTransitions();
        document.body.classList.add('dark-mode');
        localStorage.setItem('dark-mode', 'enabled');
        themeToggleBtn.textContent = '☀️';
        setTimeout(removeTransitions, 300); // Remove transitions after they complete
    };

    const disableDarkMode = () => {
        addTransitions();
        document.body.classList.remove('dark-mode');
        localStorage.setItem('dark-mode', 'disabled');
        themeToggleBtn.textContent = '🌙';
        setTimeout(removeTransitions, 300); // Remove transitions after they complete
    };

    const addTransitions = () => {
        document.body.style.transition = 'background-color 0.3s, color 0.3s';
    };

    const removeTransitions = () => {
        document.body.style.transition = '';
    };

    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        themeToggleBtn.textContent = '☀️';
    } else {
        document.body.classList.remove('dark-mode');
        themeToggleBtn.textContent = '🌙';
    }

    themeToggleBtn.addEventListener('click', () => {
        darkMode = localStorage.getItem('dark-mode');
        if (darkMode !== 'enabled') {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    });
});
