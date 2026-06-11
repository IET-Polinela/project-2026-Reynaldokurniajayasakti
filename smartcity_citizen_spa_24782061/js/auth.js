// js/auth.js

/**
 * =====================================================================
 * FUNGSI UTAMA: INISIALISASI AUTENTIKASI (LOGIN & REGISTER)
 * =====================================================================
 * Fungsi ini dipanggil oleh router / app.js setiap kali halaman login 
 * selesai di-render dari elemen <template id="login-template">.
 */
function initAuth() {
    // Ambil semua referensi elemen DOM yang dibutuhkan
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginContainer = document.getElementById('login-container');
    const registerContainer = document.getElementById('register-container');
    const linkToRegister = document.getElementById('link-to-register');
    const linkToLogin = document.getElementById('link-to-login');

    // -----------------------------------------------------------------
    // 1. LOGIKA INTERAKSI PERPINDAHAN FORM (TOGGLE SWITCHER)
    // -----------------------------------------------------------------
    if (linkToRegister && linkToLogin) {
        // Pindah ke Tampilan Form Register
        linkToRegister.addEventListener('click', function (e) {
            e.preventDefault();
            if (loginContainer && registerContainer) {
                loginContainer.style.display = 'none';
                registerContainer.style.display = 'block';
            }
        });

        // Pindah Kembali ke Tampilan Form Login
        linkToLogin.addEventListener('click', function (e) {
            e.preventDefault();
            if (loginContainer && registerContainer) {
                registerContainer.style.display = 'none';
                loginContainer.style.display = 'block';
            }
        });
    }

    // -----------------------------------------------------------------
    // 2. EVENT LISTENER: SUBMIT FORM LOGIN
    // -----------------------------------------------------------------
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            // Ambil nilai dari input form login
            const usernameInput = document.getElementById('loginUsername').value;
            const passwordInput = document.getElementById('loginPassword').value;

            const payload = {
                username: usernameInput,
                password: passwordInput
            };

            try {
                // Kirim request POST ke endpoint JWT token Django
                const response = await requestAPI('/api/token/', 'POST', payload);

                if (response && response.status === 200) {
                    const data = await response.json();

                    // Simpan sepasang token JWT ke localStorage browser
                    localStorage.setItem('access_token', data.access);
                    localStorage.setItem('refresh_token', data.refresh);

                    alert('Login Berhasil! Selamat datang di Portal Citizen.');

                    // Ubah hash rute halaman SPA ke dashboard
                    window.location.hash = '#dashboard';
                } else {
                    alert('Login Gagal! Username atau password salah.');
                }
            } catch (error) {
                console.error('Proses Autentikasi Eror:', error);
                alert('Terjadi kesalahan jaringan atau server tidak merespon.');
            }
        });
    }

    // -----------------------------------------------------------------
    // 3. EVENT LISTENER: SUBMIT FORM REGISTRASI WARGA
    // -----------------------------------------------------------------
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            // Ambil nilai dari input form registrasi
            const usernameInput = document.getElementById('regUsername').value.trim();
            const emailInput = document.getElementById('regEmail').value.trim();
            const passwordInput = document.getElementById('regPassword').value;

            const payload = {
                username: usernameInput,
                email: emailInput,
                password: passwordInput
            };

            try {
                // Gunakan fungsi requestAPI global dari api.js ke endpoint backend
                const response = await requestAPI('/api/register/', 'POST', payload);

                if (response && (response.status === 201 || response.status === 200)) {
                    alert('Registrasi Akun Warga Berhasil! Silakan masuk menggunakan akun baru Anda.');
                    
                    // Reset isi field formulir setelah sukses
                    registerForm.reset();
                    
                    // Otomatis kembalikan tampilan kontainer ke form login
                    if (loginContainer && registerContainer) {
                        registerContainer.style.display = 'none';
                        loginContainer.style.display = 'block';
                    }
                } else if (response) {
                    // Ambil dan olah pesan error detail dari Django backend
                    const errorData = await response.json().catch(() => ({}));
                    let errorMsg = "";
                    
                    for (const key in errorData) {
                        errorMsg += `\n- ${key}: ${errorData[key]}`;
                    }
                    
                    alert('Gagal Mendaftar: ' + (errorMsg || 'Data tidak valid atau username/email sudah digunakan.'));
                } else {
                    alert('Gagal terhubung ke server untuk melakukan pendaftaran.');
                }
            } catch (error) {
                console.error('Proses Registrasi Eror:', error);
                alert('Terjadi kesalahan sistem saat mencoba mengirim data pendaftaran.');
            }
        });
    }
}

// Menjaga kompatibilitas jika fungsi lama dipanggil di file router.js/app.js Anda
function setupLoginForm() { initAuth(); }
function setupRegisterForm() { initAuth(); }