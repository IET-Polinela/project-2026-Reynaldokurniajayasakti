// Jalankan pengecekan session saat aplikasi pertama kali dibuka
(function initApp() {
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
        // Jika token ditemukan, arahkan langsung ke dashboard
        if (!window.location.hash || window.location.hash === '#login') {
            window.location.hash = '#dashboard';
        } else {
            // Pengaman: Jika sudah berada di #dashboard saat dimuat, picu fungsi render secara manual
            if (typeof handleRouting === 'function') {
                handleRouting();
            }
        }
    } else {
        // Jika tidak ada token, paksa kembali ke halaman login
        window.location.hash = '#login';
        // Pengaman: Picu fungsi render rute login secara manual
        if (typeof handleRouting === 'function') {
            handleRouting();
        }
    }
})();