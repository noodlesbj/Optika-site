// Main JavaScript for Optics Platform
document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle Logic
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const themeIcon = themeToggle?.querySelector('svg');

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        body.setAttribute('data-theme', 'light');
    }

    themeToggle?.addEventListener('click', () => {
        const isLight = body.classList.toggle('light-theme');
        const theme = isLight ? 'light' : 'dark';
        localStorage.setItem('theme', theme);
        body.setAttribute('data-theme', theme);
        
        // Visual feedback
        console.log(`Theme switched to: ${theme}`);
    });

    // Lecture Search Logic
    const searchInput = document.getElementById('lecture-search');
    const lectureCards = document.querySelectorAll('.lecture-card');

    searchInput?.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        lectureCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const desc = card.querySelector('p').textContent.toLowerCase();
            if (title.includes(term) || desc.includes(term)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
