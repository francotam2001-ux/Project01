// Tutorial data
const tutorials = [
    {
        title: "Getting Started with ChatGPT",
        description: "Complete beginner's guide to using ChatGPT effectively",
        level: "beginner",
        steps: "8 Steps",
        duration: "30 min",
        content: [
            "Create your OpenAI account",
            "Understanding the interface",
            "Writing your first prompt",
            "Basic conversation techniques",
            "Using ChatGPT for different tasks",
            "Understanding limitations",
            "Best practices for prompts",
            "Troubleshooting common issues"
        ]
    },
    {
        title: "Mastering Prompt Engineering",
        description: "Learn to write prompts that get amazing results",
        level: "intermediate",
        steps: "12 Steps",
        duration: "45 min",
        content: [
            "Understanding prompt structure",
            "The CLEAR framework",
            "Role-based prompting",
            "Context setting techniques",
            "Chain of thought prompting",
            "Few-shot learning examples",
            "Prompt templates and formats",
            "Advanced prompt techniques",
            "Debugging bad prompts",
            "A/B testing your prompts",
            "Industry-specific prompting",
            "Measuring prompt effectiveness"
        ]
    },
    {
        title: "DALL-E 3 Image Generation",
        description: "Create stunning images with AI from text descriptions",
        level: "intermediate",
        steps: "10 Steps",
        duration: "40 min",
        content: [
            "Setting up DALL-E 3 access",
            "Understanding image prompts",
            "Style and composition basics",
            "Aspect ratios and dimensions",
            "Advanced prompt techniques",
            "Editing and variations",
            "Commercial use guidelines",
            "Quality optimization tips",
            "Troubleshooting generation issues",
            "Building a prompt library"
        ]
    },
    {
        title: "Midjourney Complete Guide",
        description: "Master the most popular AI art generator",
        level: "intermediate",
        steps: "15 Steps",
        duration: "60 min",
        content: [
            "Joining Midjourney Discord",
            "Understanding the interface",
            "Basic /imagine commands",
            "Parameters and settings",
            "Style references and inspiration",
            "Aspect ratios and quality settings",
            "Advanced parameters",
            "Upscaling and variations",
            "Blending and remixing",
            "Style consistency techniques",
            "Commercial licensing",
            "Community guidelines",
            "Troubleshooting common issues",
            "Building your art style",
            "Portfolio creation tips"
        ]
    },
    {
        title: "GitHub Copilot for Developers",
        description: "Boost your coding productivity with AI assistance",
        level: "intermediate",
        steps: "12 Steps",
        duration: "50 min",
        content: [
            "Installing GitHub Copilot",
            "IDE setup and configuration",
            "Understanding suggestions",
            "Writing effective comments",
            "Code completion techniques",
            "Function and class generation",
            "Test writing with Copilot",
            "Documentation generation",
            "Debugging assistance",
            "Code review and optimization",
            "Best practices and limitations",
            "Advanced Copilot features"
        ]
    },
    {
        title: "Building Custom AI Workflows",
        description: "Create automated AI-powered processes",
        level: "advanced",
        steps: "20 Steps",
        duration: "90 min",
        content: [
            "Understanding AI APIs",
            "Setting up development environment",
            "API authentication and keys",
            "Making your first API call",
            "Handling responses and errors",
            "Chaining multiple AI services",
            "Building workflow logic",
            "Data preprocessing techniques",
            "Output formatting and parsing",
            "Error handling and retries",
            "Rate limiting and optimization",
            "Monitoring and logging",
            "Deployment strategies",
            "Scaling considerations",
            "Security best practices",
            "Cost optimization",
            "Testing AI workflows",
            "Documentation and maintenance",
            "Real-world use cases",
            "Future-proofing your workflows"
        ]
    },
    {
        title: "AI Ethics and Responsible Use",
        description: "Understanding the ethical implications of AI",
        level: "beginner",
        steps: "8 Steps",
        duration: "35 min",
        content: [
            "Understanding AI bias",
            "Privacy and data protection",
            "Transparency and explainability",
            "Fairness in AI systems",
            "Environmental impact",
            "Job displacement concerns",
            "Misinformation and deepfakes",
            "Building ethical AI practices"
        ]
    },
    {
        title: "Voice AI and Speech Synthesis",
        description: "Create and manipulate audio with AI",
        level: "advanced",
        steps: "14 Steps",
        duration: "70 min",
        content: [
            "Understanding voice AI technology",
            "Text-to-speech basics",
            "Voice cloning fundamentals",
            "ElevenLabs setup and usage",
            "Murf AI for voiceovers",
            "Speech-to-text conversion",
            "Audio editing with AI",
            "Voice modulation techniques",
            "Multi-language support",
            "Real-time voice processing",
            "Integration with applications",
            "Quality optimization",
            "Legal and ethical considerations",
            "Commercial applications"
        ]
    },
    {
        title: "AI Video Generation Basics",
        description: "Create videos using AI tools and techniques",
        level: "intermediate",
        steps: "11 Steps",
        duration: "55 min",
        content: [
            "Introduction to AI video tools",
            "Runway ML basics",
            "Pika Labs video generation",
            "Stable Video Diffusion",
            "Text-to-video prompting",
            "Image-to-video conversion",
            "Video editing with AI",
            "Style transfer techniques",
            "Animation and motion control",
            "Quality enhancement",
            "Export and optimization"
        ]
    }
];

// Load tutorials into the grid
function loadTutorials(filter = 'all') {
    const grid = document.getElementById('tutorials-grid');
    grid.innerHTML = '';
    
    const filteredTutorials = filter === 'all' 
        ? tutorials 
        : tutorials.filter(tutorial => tutorial.level === filter);
    
    filteredTutorials.forEach((tutorial, index) => {
        const tutorialCard = document.createElement('div');
        tutorialCard.className = 'tutorial-card';
        tutorialCard.innerHTML = `
            <div class="tutorial-meta">
                <span class="difficulty ${tutorial.level}">${tutorial.level}</span>
                <span class="tutorial-steps">${tutorial.steps}</span>
            </div>
            <h3>${tutorial.title}</h3>
            <p>${tutorial.description}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #6b7280; font-size: 0.9rem;">⏱️ ${tutorial.duration}</span>
                <button class="btn btn-primary" onclick="showTutorial(${index})" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Start Tutorial</button>
            </div>
        `;
        grid.appendChild(tutorialCard);
    });
}

// Show tutorial details
function showTutorial(index) {
    const tutorial = tutorials[index];
    const modal = document.createElement('div');
    modal.className = 'tutorial-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${tutorial.title}</h2>
                <span class="close-modal">&times;</span>
            </div>
            <div class="modal-body">
                <p><strong>Description:</strong> ${tutorial.description}</p>
                <p><strong>Level:</strong> <span class="difficulty ${tutorial.level}">${tutorial.level}</span></p>
                <p><strong>Duration:</strong> ${tutorial.duration}</p>
                <h3>Tutorial Steps:</h3>
                <ol class="tutorial-steps-list">
                    ${tutorial.content.map(step => `<li>${step}</li>`).join('')}
                </ol>
                <div class="modal-actions">
                    <button class="btn btn-primary" onclick="startTutorial('${tutorial.title}')">Begin Tutorial</button>
                    <button class="btn btn-secondary" onclick="closeModal()">Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal functionality
    modal.querySelector('.close-modal').onclick = closeModal;
    modal.onclick = (e) => {
        if (e.target === modal) closeModal();
    };
}

function closeModal() {
    const modal = document.querySelector('.tutorial-modal');
    if (modal) {
        modal.remove();
    }
}

function startTutorial(title) {
    alert(`Starting tutorial: ${title}\n\nThis would normally open the detailed step-by-step guide. In a full implementation, this would navigate to a dedicated tutorial page with interactive content.`);
    closeModal();
}

// Filter functionality
function setupFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');
            // Load filtered tutorials
            const filter = btn.dataset.filter;
            loadTutorials(filter);
        });
    });
}

// Smooth scrolling for navigation
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Mobile menu toggle
function setupMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
}

// Progress tracking (localStorage)
function initProgressTracking() {
    const completedTutorials = JSON.parse(localStorage.getItem('completedTutorials') || '[]');
    
    // Mark completed tutorials
    completedTutorials.forEach(tutorialTitle => {
        const tutorialCards = document.querySelectorAll('.tutorial-card');
        tutorialCards.forEach(card => {
            const title = card.querySelector('h3').textContent;
            if (title === tutorialTitle) {
                card.classList.add('completed');
                card.innerHTML += '<div class="completion-badge">✓ Completed</div>';
            }
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadTutorials();
    setupFilters();
    setupSmoothScrolling();
    setupMobileMenu();
    initProgressTracking();
});