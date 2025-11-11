/**
 * Bowen Education Group - Main JavaScript
 * 博文集团 - 主要 JavaScript 文件
 *
 * Handles all interactive features for the website
 */

(function() {
    'use strict';

    // ============================================================
    // 1. SMOOTH SCROLLING - 平滑滚动
    // ============================================================
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ============================================================
    // 2. DROPDOWN MENU - 下拉菜单
    // ============================================================
    function initDropdownMenus() {
        const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');

        dropdownItems.forEach(item => {
            const link = item.querySelector('.nav-link');
            const dropdown = item.querySelector('.dropdown-menu');

            if (!link || !dropdown) return;

            // Desktop hover
            item.addEventListener('mouseenter', function() {
                dropdown.style.display = 'block';
                setTimeout(() => {
                    dropdown.classList.add('show');
                }, 10);
            });

            item.addEventListener('mouseleave', function() {
                dropdown.classList.remove('show');
                setTimeout(() => {
                    dropdown.style.display = 'none';
                }, 300);
            });

            // Mobile click
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const isVisible = dropdown.style.display === 'block';

                    // Close all other dropdowns
                    document.querySelectorAll('.dropdown-menu').forEach(d => {
                        d.style.display = 'none';
                        d.classList.remove('show');
                    });

                    if (!isVisible) {
                        dropdown.style.display = 'block';
                        setTimeout(() => {
                            dropdown.classList.add('show');
                        }, 10);
                    }
                }
            });
        });

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.nav-item.has-dropdown')) {
                document.querySelectorAll('.dropdown-menu').forEach(dropdown => {
                    dropdown.classList.remove('show');
                    setTimeout(() => {
                        dropdown.style.display = 'none';
                    }, 300);
                });
            }
        });
    }

    // ============================================================
    // 3. STICKY HEADER - 固定导航栏
    // ============================================================
    function initStickyHeader() {
        const header = document.querySelector('.site-header');
        if (!header) return;

        let lastScrollTop = 0;
        let scrollThreshold = 100;

        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            if (scrollTop > scrollThreshold) {
                header.classList.add('sticky');

                // Hide on scroll down, show on scroll up
                if (scrollTop > lastScrollTop) {
                    header.classList.add('header-hidden');
                } else {
                    header.classList.remove('header-hidden');
                }
            } else {
                header.classList.remove('sticky');
                header.classList.remove('header-hidden');
            }

            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        });
    }

    // ============================================================
    // 4. FORM VALIDATION - 表单验证
    // ============================================================
    function initFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');

        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();

                let isValid = true;
                const formData = new FormData(form);

                // Remove previous error messages
                form.querySelectorAll('.error-message').forEach(el => el.remove());
                form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));

                // Validate required fields
                form.querySelectorAll('[required]').forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        showError(field, 'This field is required / 此字段必填');
                    }
                });

                // Validate email
                const emailFields = form.querySelectorAll('input[type="email"]');
                emailFields.forEach(field => {
                    if (field.value && !isValidEmail(field.value)) {
                        isValid = false;
                        showError(field, 'Please enter a valid email / 请输入有效的邮箱');
                    }
                });

                // Validate phone
                const phoneFields = form.querySelectorAll('input[type="tel"]');
                phoneFields.forEach(field => {
                    if (field.value && !isValidPhone(field.value)) {
                        isValid = false;
                        showError(field, 'Please enter a valid phone number / 请输入有效的电话号码');
                    }
                });

                if (isValid) {
                    // Submit form via AJAX or normal submit
                    submitForm(form, formData);
                }
            });
        });
    }

    function showError(field, message) {
        field.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function isValidPhone(phone) {
        return /^[\d\s\-\+\(\)]{8,20}$/.test(phone);
    }

    function submitForm(form, formData) {
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton ? submitButton.textContent : '';

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Sending... / 发送中...';
        }

        // Submit via AJAX
        fetch(form.action, {
            method: form.method || 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showFormMessage(form, 'success', data.message || 'Message sent successfully! / 消息发送成功！');
                form.reset();
            } else {
                showFormMessage(form, 'error', data.message || 'Error sending message / 发送失败');
            }
        })
        .catch(error => {
            showFormMessage(form, 'error', 'Network error. Please try again. / 网络错误，请重试。');
        })
        .finally(() => {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    }

    function showFormMessage(form, type, message) {
        // Remove existing messages
        form.querySelectorAll('.form-message').forEach(el => el.remove());

        const messageDiv = document.createElement('div');
        messageDiv.className = `form-message form-message--${type}`;
        messageDiv.textContent = message;
        form.insertBefore(messageDiv, form.firstChild);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            setTimeout(() => messageDiv.remove(), 300);
        }, 5000);
    }

    // ============================================================
    // 5. LAZY LOADING IMAGES - 图片懒加载
    // ============================================================
    function initLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');

        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // ============================================================
    // 6. BACK TO TOP BUTTON - 返回顶部按钮
    // ============================================================
    function initBackToTop() {
        const backToTopBtn = document.querySelector('.back-to-top');
        if (!backToTopBtn) return;

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });

        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ============================================================
    // 7. ACCORDION - 手风琴
    // ============================================================
    function initAccordion() {
        const accordionHeaders = document.querySelectorAll('.accordion-header');

        accordionHeaders.forEach(header => {
            header.addEventListener('click', function() {
                const item = this.parentElement;
                const content = item.querySelector('.accordion-content');
                const isActive = item.classList.contains('active');

                // Close all other accordion items
                document.querySelectorAll('.accordion-item').forEach(i => {
                    i.classList.remove('active');
                    const c = i.querySelector('.accordion-content');
                    if (c) c.style.maxHeight = null;
                });

                // Toggle current item
                if (!isActive) {
                    item.classList.add('active');
                    content.style.maxHeight = content.scrollHeight + 'px';
                }
            });
        });
    }

    // ============================================================
    // 8. TABS - 选项卡
    // ============================================================
    function initTabs() {
        const tabButtons = document.querySelectorAll('.tab-button');

        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tabGroup = this.closest('.tabs');
                const targetId = this.dataset.tab;

                // Remove active class from all buttons and panels
                tabGroup.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                tabGroup.querySelectorAll('.tab-panel').forEach(panel => {
                    panel.classList.remove('active');
                });

                // Add active class to clicked button and target panel
                this.classList.add('active');
                const targetPanel = tabGroup.querySelector(`#${targetId}`);
                if (targetPanel) {
                    targetPanel.classList.add('active');
                }
            });
        });
    }

    // ============================================================
    // 9. ANIMATION ON SCROLL (AOS) - 滚动动画
    // ============================================================
    function initScrollAnimations() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                easing: 'ease-in-out',
                once: true,
                offset: 100
            });
        }
    }

    // ============================================================
    // 10. MODAL - 模态框
    // ============================================================
    function initModals() {
        const modalTriggers = document.querySelectorAll('[data-modal-trigger]');

        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                const modalId = this.dataset.modalTrigger;
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        const modalCloses = document.querySelectorAll('[data-modal-close]');
        modalCloses.forEach(close => {
            close.addEventListener('click', function() {
                const modal = this.closest('.modal');
                if (modal) {
                    modal.classList.remove('active');
                    document.body.style.overflow = '';
                }
            });
        });

        // Close modal on overlay click
        document.querySelectorAll('.modal-overlay').forEach(overlay => {
            overlay.addEventListener('click', function() {
                const modal = this.closest('.modal');
                if (modal) {
                    modal.classList.remove('active');
                    document.body.style.overflow = '';
                }
            });
        });
    }

    // ============================================================
    // 11. COOKIE CONSENT - Cookie 同意
    // ============================================================
    function initCookieConsent() {
        const cookieBanner = document.querySelector('.cookie-consent');
        if (!cookieBanner) return;

        const cookieAccepted = localStorage.getItem('cookieConsent');

        if (!cookieAccepted) {
            cookieBanner.classList.add('show');
        }

        const acceptBtn = cookieBanner.querySelector('.cookie-accept');
        if (acceptBtn) {
            acceptBtn.addEventListener('click', function() {
                localStorage.setItem('cookieConsent', 'true');
                cookieBanner.classList.remove('show');
            });
        }
    }

    // ============================================================
    // INITIALIZATION - 初始化
    // ============================================================
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Bowen Education Group website initialized');

        // Initialize all features
        initSmoothScrolling();
        initDropdownMenus();
        initStickyHeader();
        initFormValidation();
        initLazyLoading();
        initBackToTop();
        initAccordion();
        initTabs();
        initScrollAnimations();
        initModals();
        initCookieConsent();
    });

    // Expose utilities to global scope if needed
    window.BowenEducation = {
        showMessage: showFormMessage,
        validateEmail: isValidEmail,
        validatePhone: isValidPhone
    };

})();
