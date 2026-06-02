// 1. Definisi template komponen HTML untuk setiap rute halaman (menggunakan backtick `)
const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-4 card shadow-sm border-0 p-4">
                <h4 class="text-center fw-bold mb-4">Login Warga</h4>
                <form id="loginForm">
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Username</label>
                        <input type="text" id="loginUsername" class="form-control" placeholder="Masukkan username" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label small fw-bold">Password</label>
                        <input type="password" id="loginPassword" class="form-control" placeholder="Masukkan password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 fw-bold py-2">
                        <i class="bi bi-box-arrow-in-right me-2"></i>Masuk
                    </button>
                </form>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button class="btn btn-primary btn-lg w-100 fw-bold mb-3 shadow-sm">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    <div class="list-group list-group-flush small">
                        <a href="#dashboard" class="list-group-item list-group-item-action active border-0 rounded p-2 mb-1">
                            <i class="bi bi-grid-1x2-fill me-2"></i>Semua Laporan
                        </a>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card border-0 p-5 shadow-sm text-center text-muted border-dashed bg-white">
                    <i class="bi bi-inbox-fill text-primary display-3 mb-3"></i>
                    <h5 class="fw-bold text-dark">Selamat Datang di Portal Citizen!</h5>
                    <p class="small text-secondary">Koneksi API untuk memuat dan memanipulasi data laporan riil akan kita implementasikan secara penuh pada Lab 12.</p>
                </div>
            </section>

            <aside class="col-lg-3 d-none d-lg-block">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <h6 class="fw-bold border-b pb-2 mb-3">
                        <i class="bi bi-info-circle-fill text-primary me-2"></i>Informasi Wilayah
                    </h6>
                    <p class="small text-muted mb-0">Belum ada pengumuman atau data statistik terbaru untuk wilayah koordinat Anda saat ini.</p>
                </div>
            </aside>
        </div>
    `
};

// 2. Fungsi pengendali navigasi dinamis (Routing Engine)
function handleRouting() {
    const hash = window.location.hash || '#login'; // Fallback otomatis ke halaman login jika kosong
    const appContent = document.getElementById('app-content');
    const navMenus = document.getElementById('nav-menus');
    
    // Render tampilan halaman berdasarkan hash URL saat ini
    if (appContent) {
        appContent.innerHTML = routes[hash] || routes['#login'];
    }

    // Kelola komponen navbar secara dinamis berdasarkan status halaman dengan pengaman pemeriksaan elemen DOM
    if (hash === '#dashboard') {
        if (navMenus) {
            // Tampilkan tombol logout hanya jika berada di dalam dashboard portal
            navMenus.innerHTML = `
                <button id="logoutBtn" class="btn btn-danger btn-sm fw-bold px-3">
                    <i class="bi bi-box-arrow-left me-2"></i>Keluar
                </button>
            `;
        }
        
        // Pasang event listener untuk menangani fungsi pembersihan token saat logout
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                localStorage.clear(); // Bersihkan tokens dari memori lokal browser
                alert('Anda telah keluar dari sistem.');
                window.location.hash = '#login'; // Pindahkan ke halaman login
            });
        }
    } else {
        if (navMenus) {
            // Kosongkan navbar kanan jika pengguna berada di halaman luar (login)
            navMenus.innerHTML = '';
        }
    }

    // Inisialisasi ulang event listener formulir jika rute mengarah ke halaman login
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
}

// 3. Daftarkan fungsi ke event listener bawaan browser global
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);