class LoginManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupTheme();
        this.addRippleEffects();
        this.checkRememberedUser();
    }
    
    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Login form
        const loginForm = document.getElementById('login-form');
        loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        
        // Demo button
        const demoBtn = document.getElementById('demo-btn');
        demoBtn.addEventListener('click', () => this.fillDemoCredentials());
        
        // Password toggle
        const togglePassword = document.getElementById('toggle-password');
        togglePassword.addEventListener('click', () => this.togglePasswordVisibility());
        
        // Input validation
        const inputs = document.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateInput(input));
            input.addEventListener('input', () => this.clearError(input));
        });
    }
    
    setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
    }
    
    setTheme(theme) {
        document.body.className = `${theme}-theme`;
        const themeToggle = document.getElementById('theme-toggle');
        const icon = themeToggle.querySelector('.material-icons');
        
        if (theme === 'dark') {
            icon.textContent = 'dark_mode';
        } else {
            icon.textContent = 'light_mode';
        }
        
        localStorage.setItem('theme', theme);
    }
    
    toggleTheme() {
        const currentTheme = document.body.className.includes('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
    
    fillDemoCredentials() {
        document.getElementById('username').value = 'a';
        document.getElementById('password').value = 'a';
        
        // Add visual feedback
        const demoBtn = document.getElementById('demo-btn');
        const originalText = demoBtn.innerHTML;
        demoBtn.innerHTML = '<span class="material-icons">check</span> Demo credentials filled!';
        demoBtn.style.backgroundColor = 'var(--success-color)';
        demoBtn.style.color = 'white';
        
        setTimeout(() => {
            demoBtn.innerHTML = originalText;
            demoBtn.style.backgroundColor = '';
            demoBtn.style.color = '';
        }, 2000);
    }
    
    togglePasswordVisibility() {
        const passwordInput = document.getElementById('password');
        const toggleBtn = document.getElementById('toggle-password');
        const icon = toggleBtn.querySelector('.material-icons');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.textContent = 'visibility_off';
        } else {
            passwordInput.type = 'password';
            icon.textContent = 'visibility';
        }
    }
    
    validateInput(input) {
        const container = input.closest('.input-container');
        const formGroup = input.closest('.form-group');
        
        // Remove existing error
        this.clearError(input);
        
        if (!input.value.trim()) {
            this.showError(container, formGroup, `${input.name} is required`);
            return false;
        }
        
        return true;
    }
    
    showError(container, formGroup, message) {
        container.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<span class="material-icons" style="font-size: 16px;">error</span> ${message}`;
        
        formGroup.appendChild(errorDiv);
    }
    
    clearError(input) {
        if (!input) return;
        
        const container = input.closest('.input-container');
        const formGroup = input.closest('.form-group');
        
        if (!container || !formGroup) return;
        
        const errorMessage = formGroup.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
        
        container.classList.remove('error');
    }
    
    async handleLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        const rememberMe = document.getElementById('remember-me').checked;
        const loginBtn = document.querySelector('.login-btn');
        
        // Clear previous errors
        document.querySelectorAll('input').forEach(input => this.clearError(input));
        
        // Validate inputs
        let isValid = true;
        if (!this.validateInput(document.getElementById('username'))) isValid = false;
        if (!this.validateInput(document.getElementById('password'))) isValid = false;
        
        if (!isValid) return;
        
        // Show loading state
        loginBtn.classList.add('loading');
        
        try {
            // Simulate API call
            await this.simulateLogin(username, password);
            
            // Store user data
            const userData = {
                username: username,
                loginTime: new Date().toISOString(),
                theme: localStorage.getItem('theme') || 'light'
            };
            
            localStorage.setItem('currentUser', JSON.stringify(userData));
            
            if (rememberMe) {
                localStorage.setItem('rememberedUser', username);
            }
            
            // Show success and redirect
            this.showSuccess();
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
            
        } catch (error) {
            this.showLoginError(error.message);
            console.error('Login error:', error);
        } finally {
            loginBtn.classList.remove('loading');
        }
    }
    
    async simulateLogin(username, password) {
        return new Promise((resolve, reject) => {
            try {
                // Check demo credentials
                if (username === 'a' && password === 'a') {
                    console.log('Demo credentials accepted');
                    resolve();
                    return;
                }
                
                // For other credentials, simulate API call
                setTimeout(() => {
                    reject(new Error('Invalid username or password'));
                }, 1500);
            } catch (error) {
                console.error('Login simulation error:', error);
                reject(error);
            }
        });
    }
    
    showLoginError(message) {
        const formGroup = document.querySelector('.form-group:last-of-type');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.marginTop = '16px';
        errorDiv.style.textAlign = 'center';
        errorDiv.innerHTML = `<span class="material-icons" style="font-size: 16px;">error</span> ${message}`;
        
        // Remove existing error
        const existingError = document.querySelector('.form-group .error-message');
        if (existingError) existingError.remove();
        
        formGroup.appendChild(errorDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
    
    showSuccess() {
        const loginBtn = document.querySelector('.login-btn');
        loginBtn.innerHTML = '<span class="material-icons">check</span> Login Successful!';
        loginBtn.style.background = 'var(--success-color)';
    }
    
    checkRememberedUser() {
        const rememberedUser = localStorage.getItem('rememberedUser');
        if (rememberedUser) {
            document.getElementById('username').value = rememberedUser;
            document.getElementById('remember-me').checked = true;
        }
    }
    
    addRippleEffects() {
        const buttons = document.querySelectorAll('.ripple');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple-effect');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
}

// Initialize the login manager
document.addEventListener('DOMContentLoaded', () => {
    new LoginManager();
});

// Add ripple effect styles
const style = document.createElement('style');
style.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);