/* jshint esversion: 6 */
/**
 * main.js - Shared UI logic for Marcus Inigo Portfolio
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detect if we are in a subfolder (like /portfolio/)
    const isSubfolder = window.location.pathname.includes('/portfolio/');
    const basePath = isSubfolder ? '../' : './';

    // Load Header
    const headerContainer = document.getElementById('header-container');
    if (headerContainer) {
        fetch(basePath + 'components/header.html')
            .then(response => response.text())
            .then(data => {
                headerContainer.innerHTML = data;
                
                // Path Correction for navigation links
                headerContainer.querySelectorAll('[data-nav-link]').forEach(link => {
                    const href = link.getAttribute('href');
                    if (href) {
                        if (isSubfolder && !href.startsWith('../')) {
                            link.setAttribute('href', '../' + href);
                        } else if (!isSubfolder && href.startsWith('../')) {
                            link.setAttribute('href', href.replace('../', ''));
                        }
                    }
                });
            })
            .catch(err => console.error('Error loading header:', err));
    }

    // Load Footer
    const footerContainer = document.getElementById('footer-container');
    if (footerContainer) {
        fetch(basePath + 'components/footer.html')
            .then(response => response.text())
            .then(data => {
                footerContainer.innerHTML = data;
            })
            .catch(err => console.error('Error loading footer:', err));
    }

    // Generate Floating Particles
    createParticles();
    
    // Scroll Reveal Animation Observer
    initScrollReveal();
});

function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    
    const particleCount = 40;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Randomize properties
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Store initial positions for parallax
        particle.dataset.initialTop = particle.style.top;
        particle.dataset.initialLeft = particle.style.left;
        particle.dataset.baseSpeed = 0.1 + (i % 5) * 0.05;
        particle.dataset.floatSpeed = 3 + Math.random() * 5;
        particle.dataset.floatOffset = Math.random() * Math.PI * 2; // Random start phase
        particle.dataset.initialY = Math.random() * 100;
        
        // Random size
        const size = Math.random() * 4 + 2;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        particlesContainer.appendChild(particle);
    }
    
    // Start animation loop for floating
    let startTime = Date.now();
    function animateParticles() {
        const elapsed = (Date.now() - startTime) / 1000;
        const scrollY = window.scrollY;
        
        document.querySelectorAll('.particle').forEach(particle => {
            const baseSpeed = parseFloat(particle.dataset.baseSpeed);
            const floatSpeed = parseFloat(particle.dataset.floatSpeed);
            const floatOffset = parseFloat(particle.dataset.floatOffset);
            const initialY = parseFloat(particle.dataset.initialY);
            
            // Calculate parallax offset
            const parallaxOffset = scrollY * baseSpeed;
            
            // Calculate float offset
            const floatY = Math.sin(elapsed * floatSpeed + floatOffset) * 50;
            
            // Combine both offsets
            particle.style.transform = `translateY(${parallaxOffset + floatY}px) translateX(${Math.cos(elapsed * floatSpeed * 0.5 + floatOffset) * 30}px)`;
            
            // Animate opacity slightly
            const opacity = 0.2 + 0.3 * Math.abs(Math.sin(elapsed * floatSpeed * 0.3 + floatOffset));
            particle.style.opacity = opacity;
        });
        
        requestAnimationFrame(animateParticles);
    }
    
    animateParticles();
}

function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all elements with reveal classes
    document.querySelectorAll('.reveal-up, .reveal-left').forEach(el => {
        el.style.opacity = '0';
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });
}
