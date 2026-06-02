function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    
    if (!loginForm) return;

    loginForm.addEventListener('submit', async function (event) {
        // Mencegah halaman reload/refresh otomatis agar password tidak bocor ke URL
        event.preventDefault();

        // Ambil nilai dari input form
        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        // Siapkan payload data untuk dikirim
        const payload = {
            username: usernameInput,
            password: passwordInput
        };

        try {
            // Kirim request POST ke endpoint JWT token Django menggunakan fungsi di api.js
            const response = await requestAPI('/api/token/', 'POST', payload);

            if (response.status === 200) {
                // Parsing data JSON respons dari server
                const data = await response.json();

                // Simpan sepasang token JWT ke memori lokal browser (localStorage)
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                // Berikan notifikasi sukses kepada user
                alert('Login Berhasil! Selamat datang di Portal Citizen.');

                // Pindahkan rute halaman SPA ke dashboard secara instan menggunakan Hash
                window.location.hash = '#dashboard';
            } else {
                // Jika status bukan 200 (misal 401 Unauthorized karena salah password)
                alert('Login Gagal! Username atau password salah.');
            }
        } catch (error) {
            console.error('Proses Autentikasi Eror:', error);
        }
    });
}