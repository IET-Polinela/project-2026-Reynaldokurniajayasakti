// js/router.js

function handleRouting() {
    const hash = window.location.hash || '#login';
    const appContent = document.getElementById('app-content');

    // Jaga-jaga kalau elemen utama belum ke-render di DOM
    if (!appContent) {
        console.error("Elemen #app-content tidak ditemukan!");
        return;
    }

    // PROTEKSI RUTE SPA: Ambil token JWT dari localStorage
    const token = localStorage.getItem('access_token');
    
    // Jika tidak ada token dan mencoba masuk ke dashboard, tendang kembali ke login
    if (!token && hash === '#dashboard') {
        console.warn("Akses ditolak: Token tidak ditemukan. Mengalihkan ke #login...");
        window.location.hash = '#login';
        return;
    }

    // Jika sudah punya token tetapi malah mengakses halaman login, alihkan langsung ke dashboard
    if (token && hash === '#login') {
        window.location.hash = '#dashboard';
        return;
    }

    console.log("Rute aktif saat ini:", hash);

    if (hash === '#dashboard') {
        // 1. Suntikkan HTML Dashboard secara utuh (Sudah ditambah tombol Logout)
        appContent.innerHTML = `
            <div class="row">
                <div class="col-md-3 mb-4">
                    <button type="button" class="btn btn-primary w-100 mb-3 fw-bold py-2 shadow-sm" data-bs-toggle="modal" data-bs-target="#reportModal">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    
                    <div class="list-group shadow-sm mb-3">
                        <button type="button" id="tab-feed" class="list-group-item list-group-item-action active">
                            <i class="bi bi-rss-fill me-2"></i>Feed Kota (Semua)
                        </button>
                        <button type="button" id="tab-my-reports" class="list-group-item list-group-item-action">
                            <i class="bi bi-person-bounding-box me-2"></i>Laporan Saya
                        </button>
                        <button type="button" id="btn-logout" class="list-group-item list-group-item-action text-danger fw-bold">
                            <i class="bi bi-box-arrow-left me-2"></i>Keluar / Logout
                        </button>
                    </div>

                    <div class="card shadow-sm border-0 small">
                        <div class="card-body p-3">
                            <h6 class="fw-bold mb-3 text-muted">Status Laporan Saya</h6>
                            <div class="d-flex justify-content-between mb-2">
                                <span><i class="bi bi-file-earmark-text text-warning me-2"></i>Draft</span>
                                <span id="sidebar-draft-count" class="badge bg-warning text-dark rounded-pill">0</span>
                            </div>
                            <div class="d-flex justify-content-between mb-2">
                                <span><i class="bi bi-gear-wide-connected text-info me-2"></i>Diproses</span>
                                <span id="sidebar-progress-count" class="badge bg-info rounded-pill">0</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span><i class="bi bi-check-circle-fill text-success me-2"></i>Selesai</span>
                                <span id="sidebar-resolved-count" class="badge bg-success rounded-pill">0</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 mb-4">
                    <div id="report-container" class="w-100"></div>
                    <div id="paginationContainer"></div>
                </div>

                <div class="col-md-3">
                    <div class="card shadow-sm border-0">
                        <div class="card-body">
                            <h6 class="fw-bold text-dark"><i class="bi bi-info-circle-fill text-primary me-2"></i>Informasi Wilayah</h6>
                            <p class="text-muted small mt-2 mb-0">Menampilkan data laporan real-time yang tersinkronisasi langsung dengan server Django Port 8000.</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal fade" id="reportModal" tabindex="-1" aria-labelledby="reportModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content border-0 shadow">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title fw-bold" id="reportModalLabel"><i class="bi bi-pencil-square me-2"></i>Buat Laporan Baru</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form id="reportForm">
                                <div class="mb-3">
                                    <label for="reportTitle" class="form-label small fw-bold">Judul Masalah / Laporan</label>
                                    <input type="text" class="form-control form-control-sm" id="reportTitle" required placeholder="Contoh: Jalan Berlubang di Dekat Kampus Polinela">
                                </div>
                                <div class="mb-3">
                                    <label for="reportCategory" class="form-label small fw-bold">Kategori Fasilitas</label>
                                    <select class="form-select form-select-sm" id="reportCategory" required>
                                        <option value="" disabled selected>-- Pilih Kategori --</option>
                                        <option value="Infrastruktur">Infrastruktur</option>
                                        <option value="Keamanan">Keamanan</option>
                                        <option value="Kebersihan">Kebersihan</option>
                                        <option value="Lainnya">Lainnya</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label for="reportLocation" class="form-label small fw-bold">Lokasi Kejadian</label>
                                    <input type="text" class="form-control form-control-sm" id="reportLocation" required placeholder="Nama jalan, RT/RW, atau titik koordinat GPS">
                                </div>
                                <div class="mb-3">
                                    <label for="reportDescription" class="form-label small fw-bold">Deskripsi Kronologi Lengkap</label>
                                    <textarea class="form-control form-control-sm" id="reportDescription" rows="4" required placeholder="Jelaskan secara rinci kondisi masalah di lapangan..."></textarea>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer bg-light py-2">
                            <button type="button" class="btn btn-sm btn-secondary" data-bs-dismiss="modal">Batal</button>
                            <button type="button" id="btn-save-draft" class="btn btn-sm btn-warning fw-bold text-dark">Simpan sebagai Draft</button>
                            <button type="button" id="btn-submit-report" class="btn btn-sm btn-primary fw-bold">Kirim Laporan</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Hubungkan Event Listener & Fungsi Pemuat Data Django secara dinamis
        try {
            const tFeed = document.getElementById('tab-feed');
            const tMy = document.getElementById('tab-my-reports');
            if (tFeed) tFeed.addEventListener('click', () => { if (typeof switchTab === 'function') switchTab('feed'); });
            if (tMy) tMy.addEventListener('click', () => { if (typeof switchTab === 'function') switchTab('my_reports'); });

            // Event Listener untuk Tombol Logout Baru
            const btnLogout = document.getElementById('btn-logout');
            if (btnLogout) {
                btnLogout.addEventListener('click', () => {
                    // Bersihkan token dari penyimpanan browser
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    console.log("Token dihapus. Berhasil keluar dari sesi.");
                    
                    // Alihkan ke rute login secara instan
                    window.location.hash = '#login';
                });
            }

            // Hubungkan tombol aksi simpan modal (Draft vs Kirim)
            const btnDraft = document.getElementById('btn-save-draft');
            const btnSubmit = document.getElementById('btn-submit-report');
            
            if (btnDraft && typeof submitReportForm === 'function') {
                btnDraft.addEventListener('click', () => submitReportForm('DRAFT'));
            }
            if (btnSubmit && typeof submitReportForm === 'function') {
                btnSubmit.addEventListener('click', () => submitReportForm('REPORTED'));
            }

            // Jalankan pemuatan komponen data utama
            if (typeof loadDashboardData === 'function') {
                loadDashboardData('feed', 1);
            }
        } catch (err) {
            console.warn("Fungsi inisialisasi data dashboard menanti kesiapan js/app.js:", err);
        }

    } else if (hash === '#login') {
        // 2. Suntikkan HTML Form Login secara paksa dengan ID yang SINKRON ke auth.js
        appContent.innerHTML = `
            <div class="row justify-content-center align-items-center" style="min-height: 70vh; width: 100%; margin: 0;">
                <div class="col-md-4">
                    <div class="card shadow-sm border-0 rounded-3">
                        <div class="card-body p-4">
                            <div class="text-center mb-4">
                                <i class="bi bi-shield-lock-fill text-primary" style="font-size: 3rem;"></i>
                                <h4 class="fw-bold mt-2">Masuk ke Portal</h4>
                                <p class="text-muted small">Gunakan akun warga atau admin Anda</p>
                            </div>
                            <div id="login-alert"></div>
                            <form id="loginForm">
                                <div class="mb-3">
                                    <label for="loginUsername" class="form-label small fw-bold">Username</label>
                                    <div class="input-group input-group-sm">
                                        <span class="input-group-text bg-light border-end-0"><i class="bi bi-person text-muted"></i></span>
                                        <input type="text" class="form-control border-start-0" id="loginUsername" placeholder="Masukkan username" required>
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <label for="loginPassword" class="form-label small fw-bold">Password</label>
                                    <div class="input-group input-group-sm">
                                        <span class="input-group-text bg-light border-end-0"><i class="bi bi-lock text-muted"></i></span>
                                        <input type="password" class="form-control border-start-0" id="loginPassword" placeholder="Masukkan password" required>
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary w-100 btn-sm fw-bold py-2 shadow-sm" id="btnLogin">
                                    <i class="bi bi-box-arrow-in-right me-2"></i>Masuk
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // LANGSUNG PREPARE DAN AKTIFKAN LISTENER LOGIN DARI AUTH.JS
        if (typeof setupLoginForm === 'function') {
            setupLoginForm();
        }
    } else {
        window.location.hash = '#login';
    }
}

// Jalankan perutean global browser
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);