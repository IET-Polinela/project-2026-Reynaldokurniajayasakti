const BASE_URL = 'http://127.0.0.1:8000'; // Alamat server backend Django

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    // Siapkan konfigurasi dasar header request
    const headers = {
        'Content-Type': 'application/json'
    };

    // Otomatis ambil token JWT dari localStorage jika ada
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        // Sisipkan token ke dalam header Authorization dengan format Bearer
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    // Bangun konfigurasi fetch
    const config = {
        method: method,
        headers: headers
    };

    // Jika ada data yang dikirim (misal pas POST login), masukkan ke body config
    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        // Lakukan request ke endpoint backend Django
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        return response;
    } catch (error) {
        console.error('Koneksi API Gagal:', error);
        alert('Gagal terhubung ke server backend Django. Pastikan Django sudah dijalankan!');
        throw error;
    }
}