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
});
