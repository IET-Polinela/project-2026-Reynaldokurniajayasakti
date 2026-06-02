// Jalankan pengecekan session saat aplikasi pertama kali dibuka
(function initApp() {
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
        // Jika token ditemukan, arahkan langsung ke dashboard
        if (!window.location.hash || window.location.hash === '#login') {
            window.location.hash = '#dashboard';
        }
    } else {
        // Jika tidak ada token, paksa kembali ke halaman login
        window.location.hash = '#login';
    }
})();