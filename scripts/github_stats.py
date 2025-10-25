"""
GitHub Profile README Generator
A Python script for generating dynamic GitHub profile statistics
"""

import requests
import json
from datetime import datetime

class GitHubProfileStats:
    def __init__(self, username):
        self.username = username
        self.api_base = "https://api.github.com"
    
    def get_user_stats(self):
        """Fetch user statistics from GitHub API"""
        url = f"{self.api_base}/users/{self.username}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    
    def get_repositories(self):
        """Get all public repositories for the user"""
        url = f"{self.api_base}/users/{self.username}/repos"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else []
    
    def calculate_language_stats(self):
        """Calculate language usage statistics"""
        repos = self.get_repositories()
        languages = {}
        
        for repo in repos:
            if repo['language']:
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
        
        return languages
    
    def generate_readme_stats(self):
        """Generate README statistics section"""
        stats = self.get_user_stats()
        if not stats:
            return "Unable to fetch user statistics"
        
        return f"""
## 📊 GitHub Statistics

- **Public Repositories:** {stats.get('public_repos', 0)}
- **Followers:** {stats.get('followers', 0)}
- **Following:** {stats.get('following', 0)}
- **Account Created:** {stats.get('created_at', 'Unknown')[:10]}
"""

if __name__ == "__main__":
    # Example usage
    profile = GitHubProfileStats("roshan1595")
    print("GitHub Profile Statistics")
    print("=" * 30)
    
    # Get basic stats
    user_stats = profile.get_user_stats()
    if user_stats:
        print(f"Name: {user_stats.get('name', 'N/A')}")
        print(f"Bio: {user_stats.get('bio', 'N/A')}")
        print(f"Location: {user_stats.get('location', 'N/A')}")
        print(f"Public Repos: {user_stats.get('public_repos', 0)}")
    
    # Get language stats
    languages = profile.calculate_language_stats()
    print("\nLanguage Usage:")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang}: {count} repositories")