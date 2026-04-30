// Apply all saved preferences immediately on load (prevents flash)
(function () {
    const theme    = localStorage.getItem('ai_theme')    || 'dark';
    const accent   = localStorage.getItem('ai_accent')   || 'indigo';
    const fontSize = localStorage.getItem('ai_fontSize') || 'medium';
    const density  = localStorage.getItem('ai_density')  || 'comfortable';
    const html = document.documentElement;
    html.setAttribute('data-theme',     theme);
    html.setAttribute('data-accent',    accent);
    html.setAttribute('data-font-size', fontSize);
    html.setAttribute('data-density',   density);
})();
