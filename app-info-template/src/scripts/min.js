function setBgColor(color) {
    document.documentElement.style.setProperty('--bg', color);
    try { localStorage.setItem('app_bg_color', color); } catch (e) { /* noop */ }
}

document.addEventListener('DOMContentLoaded', function () {
    try {
        const saved = localStorage.getItem('app_bg_color');
        if (saved) document.documentElement.style.setProperty('--bg', saved);
    } catch (e) { /* noop */ }
});