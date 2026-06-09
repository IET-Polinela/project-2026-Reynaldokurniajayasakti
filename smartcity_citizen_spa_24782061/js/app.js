// js/app.js

// =====================================================================
// 1. INITIALIZATION APP & SESSION CHECK
// =====================================================================
(function initApp() {
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
        if (!window.location.hash || window.location.hash === '#login') {
            window.location.hash = '#dashboard';
        }
    } else {
        window.location.hash = '#login';
    }
})();

// =====================================================================
// 2. STATE GLOBAL & NAVIGATION TAB
// =====================================================================
let currentTab = 'feed';      // Default tab adalah Feed Kota
let currentPage = 1;          // Halaman aktif saat ini
let allReports = [];          // Array global menampung hasil data dari backend
let totalPages = 1;           // Total halaman yang dikalkulasi
let editingReportId = null;   // ID laporan yang sedang diedit (null jika buat baru)

/**
 * Fungsi untuk menangani perpindahan tab (Feed Kota vs Laporan Saya)
 */
function switchTab(tabName) {
    currentTab = tabName;
    currentPage = 1; // Reset kembali ke halaman 1 setiap pindah tab
    
    // Atur kelas aktif pada tombol nav-link di UI HTML Bootstrap 5
    document.getElementById('tab-feed')?.classList.toggle('active', tabName === 'feed');
    document.getElementById('tab-my-reports')?.classList.toggle('active', tabName === 'my_reports');
    
    // Tarik ulang data dari halaman pertama tanpa refresh halaman
    loadDashboardData(currentTab, currentPage);
}

// =====================================================================
// 3. CORE FUNCTION: FETCH PAGINATED LIST & SUMMARY STATS
// =====================================================================
async function loadDashboardData(tab = currentTab, page = currentPage) {
    currentTab = tab;
    currentPage = page;

    // Tampilkan animasi loading sebelum melakukan fetch data jika data global masih kosong
    const reportContainer = document.getElementById('report-container') || document.getElementById('listContainer');
    if (reportContainer && allReports.length === 0) {
        reportContainer.innerHTML = `
            <div class="text-center text-muted p-5 bg-white rounded shadow-sm w-100">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2 mb-0 small">Menghubungkan & memuat data dari database...</p>
            </div>`;
    }

    try {
        // Menembak API Backend dengan parameter tab dan nomor halaman
        const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');
        
        if (response && response.status === 200) {
            // Konversi response mentah menjadi data JSON secara aman
            const data = await response.json();
            
            // ADAPTIF: Memeriksa bentuk struktur data balikan dari Django API (Paginasi vs Non-Paginasi)
            if (Array.isArray(data)) {
                allReports = data;
                totalPages = 1; 
            } else if (data && typeof data === 'object') {
                allReports = data.results || [];
                const totalData = data.count || 0;
                totalPages = Math.ceil(totalData / 10) || 1; // Mengasumsikan paginasi 10 data per halaman
            } else {
                allReports = [];
                totalPages = 1;
            }

            // Pemicu Perbaruan UI (Sinkronisasi Antarmuka)
            renderList();
            renderPagination();

            // Kalkulasi Rekap Status di Sidebar
            await loadSummaryStats();

        } else {
            console.error(`Request gagal dengan status HTTP: ${response ? response.status : 'No Response'}`);
            handleFetchError();
        }
    } catch (error) {
        console.error('Gagal merender data dashboard:', error);
        handleFetchError();
    }
}

/**
 * Kalkulasi Rekap Status di Sidebar (Bypass Pagination)
 */
async function loadSummaryStats() {
    try {
        // PERBAIKAN UTAMA: Menggunakan disable_pagination=true agar memanggil semua data lama dan baru
        const response = await requestAPI('/api/report/?tab=my_reports&disable_pagination=true', 'GET');
        
        if (response && response.status === 200) {
            const data = await response.json();
            const reports = Array.isArray(data) ? data : (data.results || []);
            
            // 1. Filter kuantitas laporan status DRAFT
            const totalDraft = reports.filter(report => report.status === 'DRAFT').length;
            
            // 2. Filter kuantitas laporan status DIPROSES (Membaca Reported, Verified, In Progress, Diproses)
            const totalDiproses = reports.filter(report => 
                report.status === 'REPORTED' || 
                report.status === 'VERIFIED' || 
                report.status === 'IN_PROGRESS' || 
                report.status === 'DIPROSES'
            ).length;
            
            // 3. Filter kuantitas laporan status SELESAI
            const totalSelesai = reports.filter(report => report.status === 'RESOLVED' || report.status === 'SELESAI').length;
            
            // Sinkronisasikan hasilnya langsung ke elemen antarmuka Sidebar
            const elDraft = document.getElementById('sidebar-draft-count');
            const elDiproses = document.getElementById('sidebar-progress-count');
            const elSelesai = document.getElementById('sidebar-resolved-count');
            
            if (elDraft) elDraft.textContent = totalDraft;
            if (elDiproses) elDiproses.textContent = totalDiproses;
            if (elSelesai) elSelesai.textContent = totalSelesai;
        }
    } catch (error) {
        console.error('Gagal memuat statistik ringkasan sidebar:', error);
    }
}

// =====================================================================
// 4. DYNAMIC UI RENDERING FUNCTIONS (KARTU LAPORAN & PAGINASI)
// =====================================================================
function renderList() {
    const reportContainer = document.getElementById('report-container') || document.getElementById('listContainer');
    if (!reportContainer) return;

    reportContainer.innerHTML = '';

    // FALLBACK JIKA DATABASE KOSONG / BELUM ADA DATA SAMA SEKALI
    if (allReports.length === 0) {
        reportContainer.innerHTML = `
            <div class="card shadow-sm border-0 text-center p-5 mb-4 w-100">
                <div class="card-body">
                    <i class="bi bi-chat-square-dots text-muted" style="font-size: 3rem;"></i>
                    <h5 class="mt-3 fw-bold text-dark">Belum Ada Laporan Warga</h5>
                    <p class="text-muted small mb-0">Hubungan API ke server Django aman. Klik tombol <strong>Laporan Baru</strong> untuk memasukkan data laporan pertama Anda ke dalam database MySQL.</p>
                </div>
            </div>`;
        return;
    }

    allReports.forEach(report => {
        let progressPercent = 0;
        let progressColor = 'bg-secondary';
        
        if (report.status === 'DRAFT') {
            progressPercent = 15;
            progressColor = 'bg-warning text-dark';
        } else if (report.status === 'REPORTED' || report.status === 'PUBLISHED') {
            progressPercent = 35;
            progressColor = 'bg-info';
        } else if (report.status === 'VERIFIED') {
            progressPercent = 55;
            progressColor = 'bg-primary';
        } else if (report.status === 'IN_PROGRESS' || report.status === 'DIPROSES') {
            progressPercent = 75;
            progressColor = 'bg-warning text-dark';
        } else if (report.status === 'RESOLVED' || report.status === 'SELESAI') {
            progressPercent = 100;
            progressColor = 'bg-success';
        }

        // Tombol Aksi Edit/Hapus khusus untuk DRAFT milik user sendiri
        let actionButtons = '';
        if (report.is_owner && report.status === 'DRAFT') {
            actionButtons = `
                <div class="mt-3 d-flex gap-2 justify-content-end">
                    <button type="button" class="btn btn-sm btn-outline-primary" onclick="openEditModal(${report.id})">
                        <i class="bi bi-pencil-square"></i> Edit Draft
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteReport(${report.id})">
                        <i class="bi bi-trash"></i> Hapus
                    </button>
                </div>`;
        }

        const cardHTML = `
            <div class="card mb-3 shadow-sm w-100 border-0">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title text-truncate fw-bold text-dark mb-0" style="max-width: 70%;">${report.title}</h5>
                        <span class="badge bg-light text-primary border border-primary-subtle px-2 py-1 small">${report.category}</span>
                    </div>
                    <h6 class="card-subtitle mb-3 text-muted small mt-2">
                        <i class="bi bi-person-circle"></i> ${report.reporter || 'Anonim'} | 
                        <i class="bi bi-calendar3"></i> ${report.updated_at ? new Date(report.updated_at).toLocaleDateString('id-ID') : '-'}
                    </h6>
                    <p class="card-text text-secondary small">${report.description}</p>
                    <p class="card-text small text-muted mb-2"><i class="bi bi-geo-alt-fill text-danger me-1"></i>${report.location || '-'}</p>
                    
                    <div class="mt-3 small text-muted d-flex justify-content-between">
                        <span>Status: <strong class="text-dark">${report.status}</strong></span>
                        <span>${progressPercent}%</span>
                    </div>
                    <div class="progress mt-1" style="height: 6px;">
                        <div class="progress-bar ${progressColor}" role="progressbar" style="width: ${progressPercent}%" aria-valuenow="${progressPercent}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>

                    ${actionButtons}
                </div>
            </div>`;
        
            reportContainer.insertAdjacentHTML('beforeend', cardHTML);
    });
}

function renderPagination() {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    paginationContainer.innerHTML = '';
    if (totalPages <= 1) return;

    let paginationHTML = `<ul class="pagination justify-content-center mt-4">`;

    // Tombol Sebelumnya
    paginationHTML += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <button class="page-link" type="button" onclick="loadDashboardData('${currentTab}', ${currentPage - 1})">Sebelumnya</button>
        </li>`;

    // Loop Nomor Halaman
    for (let i = 1; i <= totalPages; i++) {
        paginationHTML += `
            <li class="page-item ${currentPage === i ? 'active' : ''}">
                <button class="page-link" type="button" onclick="loadDashboardData('${currentTab}', ${i})">${i}</button>
            </li>`;
    }

    // Tombol Selanjutnya
    paginationHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <button class="page-link" type="button" onclick="loadDashboardData('${currentTab}', ${currentPage + 1})">Selanjutnya</button>
        </li>`;

    paginationHTML += `</ul>`;
    paginationContainer.innerHTML = paginationHTML;
}

// =====================================================================
// 5. CRUD ACTIONS: SUBMIT, EDIT, DELETE FORM LAPORAN
// =====================================================================

/**
 * Mengirim form untuk membuat laporan baru ATAU memperbarui draft lama
 */
async function submitReportForm(status) {
    const title = document.getElementById('reportTitle').value.trim();
    const category = document.getElementById('reportCategory').value;
    const location = document.getElementById('reportLocation').value.trim();
    const description = document.getElementById('reportDescription').value.trim();

    // Validasi form manual sebelum dikirim ke API
    if (!title || !category || !location || !description) {
        alert('Mohon lengkapi seluruh field formulir laporan!');
        return;
    }

    const payload = {
        title: title,
        category: category,
        location: location,
        description: description,
        status: status // Berisi 'DRAFT' atau 'REPORTED'
    };

    try {
        let response;
        if (editingReportId) {
            // Jika sedang dalam mode edit, gunakan metode PUT ke ID spesifik
            response = await requestAPI(`/api/report/${editingReportId}/`, 'PUT', payload);
        } else {
            // Jika laporan baru, gunakan metode POST
            response = await requestAPI('/api/report/', 'POST', payload);
        }

        if (response && (response.status === 200 || response.status === 201)) {
            alert(editingReportId ? 'Laporan berhasil diperbarui!' : 'Laporan baru berhasil diterbitkan!');
            
            // 1. Reset isian form HTML agar kosong kembali saat nanti dibuka ulang
            document.getElementById('reportForm')?.reset();

            // 2. SOLUSI UTAMA: Sembunyikan modal secara terprogram via core Bootstrap 5
            const modalElement = document.getElementById('reportModal');
            if (modalElement) {
                const modalInstance = bootstrap.Modal.getInstance(modalElement) || bootstrap.Modal.getOrCreateInstance(modalElement);
                modalInstance.hide();
            }
            
            // 3. Bersihkan sisa backdrop gelap di belakang agar layar tidak membeku (unfreeze)
            document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('padding-right');
            
            // 4. Muat ulang isi data dashboard ter-update agar list langsung diperbarui
            loadDashboardData();
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert('Gagal menyimpan data: ' + (JSON.stringify(errorData) || 'Terjadi gangguan internal server.'));
        }
    } catch (error) {
        console.error('Koneksi Gagal saat submit form laporan:', error);
        alert('Terjadi kesalahan sistem saat mencoba mengirim data laporan.');
    }
}

/**
 * Membuka Modal Form dan Mengisinya dengan Data Draft yang Dipilih untuk Diedit
 */
function openEditModal(id) {
    const report = allReports.find(r => r.id === id);
    if (!report) return;

    // Set status global ke mode edit
    editingReportId = id;

    // Isikan data lama ke dalam elemen form input modal
    document.getElementById('reportTitle').value = report.title || '';
    document.getElementById('reportCategory').value = report.category || '';
    document.getElementById('reportLocation').value = report.location || '';
    document.getElementById('reportDescription').value = report.description || '';

    // Ubah judul modal di UI agar informatif
    const modalTitle = document.getElementById('reportModalLabel');
    if (modalTitle) modalTitle.innerHTML = `<i class="bi bi-pencil-square me-2"></i>Edit Draft Laporan`;

    // Tampilkan modal secara programmatik via Bootstrap 5 Instance
    const modalElement = document.getElementById('reportModal');
    if (modalElement) {
        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
        modalInstance.show();
    }
}

/**
 * Menghapus Data Draft Laporan Berdasarkan ID Laporan
 */
async function deleteReport(id) {
    if (!confirm('Apakah Anda yakin ingin menghapus permanen draft laporan ini?')) return;

    try {
        const response = await requestAPI(`/api/report/${id}/`, 'DELETE');
        if (response && (response.status === 200 || response.status === 204)) {
            alert('Draft laporan berhasil dihapus.');
            loadDashboardData();
        } else {
            alert('Gagal menghapus draft laporan.');
        }
    } catch (error) {
        console.error('Gagal menghapus laporan:', error);
    }
}

/**
 * Menangani Tampilan Error jika Koneksi Backend Port 8000 Bermasalah
 */
function handleFetchError() {
    const reportContainer = document.getElementById('report-container') || document.getElementById('listContainer');
    if (reportContainer) {
        reportContainer.innerHTML = `
            <div class="alert alert-danger text-center w-100 shadow-sm border-0" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i> Gagal memuat data laporan dari server.<br>
                <span class="small opacity-75">Pastikan server backend Django Port 8000 Anda sudah berjalan dan konfigurasi CORS diizinkan.</span>
            </div>`;
    }
}

// =====================================================================
// 6. EVENT LIFECYCLE MONITORING (PENGAMAN RESET FORM)
// =====================================================================
// Bersihkan status id edit menjadi null kembali serta reset form inputan saat modal ditutup
document.addEventListener('hidden.bs.modal', function (event) {
    if (event.target.id === 'reportModal') {
        document.getElementById('reportForm')?.reset();
        editingReportId = null;
        
        // Kembalikan judul modal menjadi sedia kala
        const modalTitle = document.getElementById('reportModalLabel');
        if (modalTitle) modalTitle.innerHTML = `<i class="bi bi-pencil-square me-2"></i>Buat Laporan Baru`;
    }
});