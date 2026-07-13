// js/api.js
const BASE_URL = 'http://127.0.0.1:8000'; // Alamat server backend Django

/**
 * Fungsi utilitas global untuk melakukan request HTTP ke Django REST API dengan Interseptor JWT
 * @param {string} endpoint - Rute rute API (misal: '/api/report/')
 * @param {string} method - Metode HTTP ('GET', 'POST', 'PUT', 'DELETE')
 * @param {Object|null} bodyData - Data payload yang akan dikirim (opsional)
 * @returns {Promise<Response|null>} - Mengembalikan object response utuh atau null jika koneksi gagal
 */
async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    // Siapkan konfigurasi dasar header request
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json' // Memastikan Django selalu mengembalikan data berformat JSON
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

    // Jika ada data yang dikirim (misal pas POST/PUT), masukkan ke body config setelah di-stringfy
    if (bodyData && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        // Lakukan request ke endpoint backend Django
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        
        // INTERSEPTOR OTOMATIS: Jika token kedaluwarsa / tidak valid (Status 401 Unauthorized)
        if (response.status === 401) {
            // PENGAMAN: Jangan bersihkan storage jika error 401 berasal dari percobaan login/token awal yang salah
            if (!endpoint.includes('/login') && !endpoint.includes('/token')) {
                console.warn('Sesi habis atau token tidak valid. Membersihkan sesi penyimpanan...');
                
                // Bersihkan seluruh data sesi autentikasi di browser
                localStorage.removeItem('access_token'); 
                localStorage.removeItem('refresh_token'); 
                localStorage.removeItem('username'); 
                
                // Berikan jeda sedikit sebelum kick ke login agar user tidak bingung
                setTimeout(() => {
                    window.location.hash = '#login'; // Tendang user kembali ke halaman Login SPA
                }, 500);
            }
        }

        // SELALU kembalikan objek response utuh hasil fetch agar fungsi .json() di luar tidak crash
        return response;
    } catch (error) {
        console.error(`Koneksi ke backend bermasalah pada endpoint [${method}] ${endpoint}:`, error);
        
        // Kembalikan null agar pengondisian if(response) di file app.js mendeteksi kegalalan
        // dan mengaktifkan visual komponen penanganan error (handleFetchError) di UI secara mulus.
        return null; 
    }
}
