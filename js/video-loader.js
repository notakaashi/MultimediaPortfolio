// Video folder detection and loading system
class VideoGallery {
    constructor() {
        this.videosPath = './videos/';
        this.supportedFormats = ['.mp4', '.webm', '.mov', '.avi'];
        this.init();
    }

    async init() {
        try {
            const videos = await this.scanVideoFolder();
            this.renderVideoGallery(videos);
        } catch (error) {
            console.error('Error loading video gallery:', error);
            this.renderFallbackGallery();
        }
    }

    async scanVideoFolder() {
        // In a real implementation, this would scan the folder
        // For now, return expected video structure
        return {
            source: 'source.mp4',
            final: 'final.mp4',
            weeks: [
                { week: 1, file: 'week1.mp4' },
                { week: 2, file: 'week2.mp4' }
                // Future weeks will be added here
            ]
        };
    }

    renderVideoGallery(videos) {
        // Update source video
        const sourceVideo = document.querySelector('video[autoplay] source');
        if (sourceVideo && videos.source) {
            sourceVideo.src = this.videosPath + videos.source;
        }

        // Update final video
        const finalVideo = document.querySelector('.video-section:nth-child(2) video source');
        if (finalVideo && videos.final) {
            finalVideo.src = this.videosPath + videos.final;
        }

        // Update weekly videos
        videos.weeks.forEach((weekData, index) => {
            const weekVideo = document.querySelectorAll('.week-card video source')[index];
            if (weekVideo) {
                weekVideo.src = this.videosPath + weekData.file;
            }
        });

        // Load all videos
        this.loadAllVideos();
    }

    loadAllVideos() {
        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            video.load();
        });
    }

    renderFallbackGallery() {
        console.log('Using fallback gallery structure');
    }

    // Method to add new week videos dynamically
    addWeekVideo(weekNumber, filename) {
        const weekGrid = document.querySelector('.week-grid');
        const weekCard = document.createElement('div');
        weekCard.className = 'week-card';
        weekCard.innerHTML = `
            <div class="week-header">Week ${weekNumber}</div>
            <div class="week-content">
                <div class="video-wrapper">
                    <video controls>
                        <source src="${this.videosPath + filename}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
        `;
        weekGrid.appendChild(weekCard);
    }
}

// Initialize video gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new VideoGallery();
});
