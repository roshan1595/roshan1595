import requests
import json
from datetime import datetime

def get_github_data(username):
    """Fetch actual GitHub data for the user"""
    base_url = "https://api.github.com"
    
    # Get user data
    user_response = requests.get(f"{base_url}/users/{username}")
    if user_response.status_code == 200:
        user_data = user_response.json()
        
        # Get repositories
        repos_response = requests.get(f"{base_url}/users/{username}/repos?sort=updated&per_page=100")
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Calculate stats
        total_repos = len(repos_data)
        languages = {}
        total_stars = 0
        total_forks = 0
        
        for repo in repos_data:
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
            total_stars += repo.get('stargazers_count', 0)
            total_forks += repo.get('forks_count', 0)
        
        # Create summary
        top_language = max(languages.items(), key=lambda x: x[1])[0] if languages else "No data"
        
        stats = {
            "name": user_data.get('name', username),
            "public_repos": user_data.get('public_repos', 0),
            "followers": user_data.get('followers', 0),
            "following": user_data.get('following', 0),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "top_language": top_language,
            "languages": languages,
            "account_created": user_data.get('created_at', '')[:10],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return stats
    return None

if __name__ == "__main__":
    username = "roshan1595"
    stats = get_github_data(username)
    
    if stats:
        print("✅ GitHub Profile Stats Retrieved Successfully!")
        print(f"📊 Public Repositories: {stats['public_repos']}")
        print(f"👥 Followers: {stats['followers']}")
        print(f"💫 Following: {stats['following']}")
        print(f"⭐ Total Stars: {stats['total_stars']}")
        print(f"🍴 Total Forks: {stats['total_forks']}")
        print(f"🎯 Top Language: {stats['top_language']}")
        print(f"📅 Account Created: {stats['account_created']}")
        
        print("\n🌐 Language Breakdown:")
        for lang, count in sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {lang}: {count} repositories")
    else:
        print("❌ Could not fetch GitHub data")