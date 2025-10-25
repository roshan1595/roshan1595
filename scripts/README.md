# GitHub Profile Analytics Scripts

This directory contains utility scripts for generating and managing GitHub profile statistics.

## Files

### `github_stats.py`
Python script for fetching GitHub user statistics and repository data.

**Features:**
- Fetch user profile information
- Calculate language usage statistics
- Generate README statistics sections
- Repository analysis

**Usage:**
```python
from github_stats import GitHubProfileStats

profile = GitHubProfileStats("roshan1595")
stats = profile.get_user_stats()
languages = profile.calculate_language_stats()
```

### `api-server.js`
Node.js Express API server for serving GitHub profile data.

**Features:**
- RESTful API endpoints
- Real-time profile data
- Language statistics
- Repository information

**Usage:**
```bash
npm install express axios
node api-server.js
```

**Endpoints:**
- `GET /api/profile/:username` - Full profile data
- `GET /api/languages/:username` - Language statistics
- `GET /health` - Health check

## Requirements

### Python Dependencies
```
requests
json
datetime
```

### Node.js Dependencies
```
express
axios
```

## Environment Setup

1. Install Python dependencies:
   ```bash
   pip install requests
   ```

2. Install Node.js dependencies:
   ```bash
   npm install express axios
   ```

## Notes

- GitHub API has rate limits (60 requests/hour for unauthenticated requests)
- For production use, consider implementing authentication
- The API server includes error handling and logging
- Scripts are designed to work with public repositories