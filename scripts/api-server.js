const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

// GitHub Profile API Handler
class GitHubProfileService {
    constructor(username) {
        this.username = username;
        this.apiBase = 'https://api.github.com';
    }

    async getUserData() {
        try {
            const response = await axios.get(`${this.apiBase}/users/${this.username}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching user data:', error.message);
            return null;
        }
    }

    async getRepositories() {
        try {
            const response = await axios.get(`${this.apiBase}/users/${this.username}/repos?sort=updated&per_page=100`);
            return response.data;
        } catch (error) {
            console.error('Error fetching repositories:', error.message);
            return [];
        }
    }

    async getLanguageStats() {
        const repos = await this.getRepositories();
        const languageCount = {};
        
        for (const repo of repos) {
            if (repo.language) {
                languageCount[repo.language] = (languageCount[repo.language] || 0) + 1;
            }
        }
        
        return Object.entries(languageCount)
            .sort((a, b) => b[1] - a[1])
            .reduce((obj, [key, value]) => {
                obj[key] = value;
                return obj;
            }, {});
    }

    async getContributionData() {
        // This would require authentication for private repos
        // For demo purposes, we'll return mock data
        return {
            totalContributions: 150,
            currentStreak: 15,
            longestStreak: 42
        };
    }
}

// API Routes
app.get('/api/profile/:username', async (req, res) => {
    const { username } = req.params;
    const service = new GitHubProfileService(username);
    
    try {
        const userData = await service.getUserData();
        const repos = await service.getRepositories();
        const languages = await service.getLanguageStats();
        const contributions = await service.getContributionData();
        
        res.json({
            user: userData,
            repositories: repos.length,
            languages,
            contributions,
            lastUpdated: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch profile data' });
    }
});

app.get('/api/languages/:username', async (req, res) => {
    const { username } = req.params;
    const service = new GitHubProfileService(username);
    
    try {
        const languages = await service.getLanguageStats();
        res.json(languages);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch language data' });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        service: 'GitHub Profile Analytics API'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 GitHub Profile API Server running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(`👤 Profile API: http://localhost:${PORT}/api/profile/roshan1595`);
});

module.exports = app;