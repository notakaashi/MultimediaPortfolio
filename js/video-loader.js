// Solar system timing + video gallery for the available celestial bodies.
class SolarSystemGallery {
    constructor() {
        this.videosPath = this.getVideosPath();
        this.bodies = [
            {
                name: 'Mercury',
                key: 'mercury',
                file: 'mercury.mp4',
                icon: 'fa-meteor',
                age: '4.15 years',
                revolutions: '4.15',
                orbitalPeriod: '88 Earth days',
                distance: '57.9 million km',
                description: 'The smallest and innermost planet, Mercury has extreme temperature changes and a cratered surface.'
            },
            {
                name: 'Earth',
                key: 'earth',
                file: 'earth.mp4',
                icon: 'fa-globe',
                age: '1.00 year',
                revolutions: '1.00',
                orbitalPeriod: '365.25 Earth days',
                distance: '149.6 million km',
                description: 'Our home planet is the only known world confirmed to host life, with oceans and a protective atmosphere.'
            }
        ];

        this.orbitalPeriods = {
            mercury: 0.2408467,
            earth: 1.0
        };

        this.init();
    }

    getVideosPath() {
        const path = (window.location.pathname || '').replace(/\\/g, '/').toLowerCase();
        return path.includes('/portfolio/') ? '../videos/' : './videos/';
    }

    init() {
        this.renderBodies();
        this.bindCalculator();
        this.calculatePlanetaryTime();
    }

    renderBodies() {
        const grid = document.getElementById('celestial-grid');
        if (!grid) {
            return;
        }

        grid.innerHTML = this.bodies.map((body, index) => `
            <div class="col-lg-6 fade-in">
                <div class="step-card celestial-card" data-body-card="${body.key}">
                    <div class="card-body">
                        <div class="d-flex align-items-start justify-content-between gap-3 mb-3">
                            <div>
                                <h5 class="card-title mb-1">${body.name}</h5>
                                <p class="mb-0 text-secondary">Planet ${index + 1}</p>
                            </div>
                            <span class="badge planet-live-badge">Video loaded</span>
                        </div>

                        <div class="planet-stats">
                            <div class="stat-item">
                                <span class="stat-label">Age:</span>
                                <span class="stat-value age-display" data-body="${body.key}">${body.age}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Revolutions:</span>
                                <span class="stat-value revolution-display" data-body="${body.key}">${body.revolutions}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Orbital Period:</span>
                                <span class="stat-value">${body.orbitalPeriod}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Distance from Sun:</span>
                                <span class="stat-value">${body.distance}</span>
                            </div>
                        </div>

                        <div class="time-comparison mb-3">
                            <strong>Description:</strong>
                            <span class="time-comparison-text" data-body="${body.key}">${body.description}</span>
                        </div>

                        <div class="img-container planet-video-frame">
                            <video class="w-100 h-100" autoplay muted loop playsinline preload="metadata">
                                <source src="${this.videosPath + body.file}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    bindCalculator() {
        const input = document.getElementById('earthYearsInput');
        const button = document.getElementById('planetary-calc-button');

        if (button) {
            button.addEventListener('click', () => this.calculatePlanetaryTime());
        }

        if (input) {
            input.addEventListener('keypress', event => {
                if (event.key === 'Enter') {
                    this.calculatePlanetaryTime();
                }
            });
        }
    }

    calculatePlanetaryTime() {
        const input = document.getElementById('earthYearsInput');
        const earthYears = Math.max(0, parseFloat(input?.value || '0') || 0);

        Object.keys(this.orbitalPeriods).forEach(bodyName => {
            const planetYears = earthYears / this.orbitalPeriods[bodyName];

            const ageElements = document.querySelectorAll(`[data-body="${bodyName}"].age-display`);
            const revElements = document.querySelectorAll(`[data-body="${bodyName}"].revolution-display`);
            ageElements.forEach(element => {
                element.textContent = this.formatPlanetValue(planetYears);
            });

            revElements.forEach(element => {
                element.textContent = this.formatRevolutions(planetYears);
            });

            const comparisonElements = document.querySelectorAll(`.time-comparison-text[data-body="${bodyName}"]`);
            comparisonElements.forEach(element => {
                const bodyLabel = this.capitalize(bodyName);
                if (earthYears === 0 || earthYears === 1) {
                    element.textContent = `In 1 Earth year, ${bodyLabel} experiences ${(1 / this.orbitalPeriods[bodyName]).toFixed(2)} of its own years.`;
                } else {
                    element.textContent = `In ${earthYears} Earth years, ${bodyLabel} experiences ${planetYears.toFixed(2)} of its own years.`;
                }
            });
        });

        this.flashCalculateButton();
    }

    formatPlanetValue(value) {
        if (value >= 1000000) {
            return `${(value / 1000000).toFixed(2)} million years`;
        }

        if (value >= 1000) {
            return `${(value / 1000).toFixed(2)} thousand years`;
        }

        if (value >= 1) {
            return `${value.toFixed(2)} years`;
        }

        return `${value.toFixed(4)} years`;
    }

    formatRevolutions(value) {
        if (value >= 1000000) {
            return `${(value / 1000000).toFixed(2)} million`;
        }

        if (value >= 1000) {
            return `${(value / 1000).toFixed(2)} thousand`;
        }

        return value.toFixed(2);
    }

    capitalize(word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
    }

    flashCalculateButton() {
        const button = document.getElementById('planetary-calc-button');
        if (!button) {
            return;
        }

        const originalHtml = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Calculated!';
        button.classList.add('btn-success');
        button.classList.remove('btn-cosmic');

        window.setTimeout(() => {
            button.innerHTML = originalHtml;
            button.classList.remove('btn-success');
            button.classList.add('btn-cosmic');
        }, 1500);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new SolarSystemGallery();
});
