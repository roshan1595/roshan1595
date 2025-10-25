import requests
import json
from datetime import datetime
import os

class DynamicGitHubStats:
    def __init__(self, username):
        self.username = username
        self.api_base = "https://api.github.com"
    
    def get_github_data(self):
        """Fetch comprehensive GitHub data"""
        try:
            # Get user data
            user_response = requests.get(f"{self.api_base}/users/{self.username}")
            if user_response.status_code != 200:
                return None
                
            user_data = user_response.json()
            
            # Get repositories
            repos_response = requests.get(f"{self.api_base}/users/{self.username}/repos?sort=updated&per_page=100")
            repos_data = repos_response.json() if repos_response.status_code == 200 else []
            
            # Calculate language statistics
            languages = {}
            total_bytes = 0
            
            for repo in repos_data:
                if repo.get('language'):
                    # Get detailed language stats for each repo
                    lang_response = requests.get(f"{self.api_base}/repos/{repo['full_name']}/languages")
                    if lang_response.status_code == 200:
                        repo_languages = lang_response.json()
                        for lang, bytes_count in repo_languages.items():
                            languages[lang] = languages.get(lang, 0) + bytes_count
                            total_bytes += bytes_count
            
            # Calculate percentages
            language_percentages = {}
            for lang, bytes_count in languages.items():
                percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
                language_percentages[lang] = round(percentage, 1)
            
            # Sort by percentage
            sorted_languages = dict(sorted(language_percentages.items(), key=lambda x: x[1], reverse=True))
            
            return {
                "user": user_data,
                "repositories": repos_data,
                "languages": sorted_languages,
                "total_repos": len(repos_data),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error fetching GitHub data: {e}")
            return None
    
    def generate_language_svg(self, languages, width=400, height=200):
        """Generate SVG for language distribution"""
        if not languages:
            return self.create_no_data_svg()
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .lang-text {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 14px; fill: #ffffff; }}
            .percent-text {{ font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; fill: #58a6ff; }}
            .bar {{ rx: 4; ry: 4; }}
        </style>
    </defs>
    
    <rect width="{width}" height="{height}" fill="#0d1117" rx="10"/>
    
    <text x="20" y="30" class="lang-text" font-weight="bold" font-size="16">🌐 Language Distribution</text>'''
        
        y_pos = 60
        colors = ['#3178c6', '#3776ab', '#f1c40f', '#e74c3c', '#9b59b6', '#2ecc71']
        
        for i, (lang, percentage) in enumerate(list(languages.items())[:6]):  # Top 6 languages
            color = colors[i % len(colors)]
            bar_width = (percentage / 100) * (width - 120)
            
            svg_content += f'''
    <text x="20" y="{y_pos}" class="lang-text">{lang}</text>
    <rect x="120" y="{y_pos - 12}" width="{bar_width}" height="15" fill="{color}" class="bar" opacity="0.8"/>
    <text x="{width - 60}" y="{y_pos}" class="percent-text">{percentage}%</text>'''
            
            y_pos += 25
        
        svg_content += '''
    <text x="20" y="{}" class="percent-text" opacity="0.7">Updated: {}</text>
</svg>'''.format(height - 10, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        return svg_content
    
    def create_no_data_svg(self):
        """Create SVG when no data is available"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="200" fill="#0d1117" rx="10"/>
    <text x="200" y="100" text-anchor="middle" fill="#58a6ff" font-family="Arial" font-size="16">📊 Loading language data...</text>
    <text x="200" y="130" text-anchor="middle" fill="#666" font-family="Arial" font-size="12">GitHub is analyzing repositories</text>
</svg>'''
    
    def update_readme_stats(self, data):
        """Update README with dynamic stats"""
        if not data:
            return "📊 Unable to fetch current statistics"
        
        languages = data['languages']
        user = data['user']
        
        # Create language distribution text
        lang_text = ""
        for lang, percentage in list(languages.items())[:5]:  # Top 5
            bar_length = int(percentage / 2.5)  # Scale for display
            bar = "█" * bar_length + "░" * (40 - bar_length)
            lang_text += f"{lang:<12} {bar} {percentage}%\n"
        
        stats_table = f'''| 📊 **Metric** | 🔢 **Value** | 📈 **Details** |
|---------------|--------------|----------------|
| 📁 **Public Repositories** | `{user.get('public_repos', 0)}` | Active development portfolio |
| 👥 **Followers** | `{user.get('followers', 0)}` | Growing professional network |
| 💫 **Following** | `{user.get('following', 0)}` | Curated tech influencers |
| 🎯 **Primary Languages** | `{', '.join(list(languages.keys())[:3])}` | Full-stack development |
| 📅 **Account Since** | `{user.get('created_at', '')[:10]}` | Years of consistent coding |
| ⭐ **Total Stars** | `Building...` | Projects gaining recognition |'''
        
        return {
            "table": stats_table,
            "languages": lang_text.strip(),
            "top_language": list(languages.keys())[0] if languages else "No data"
        }
    
    def save_language_svg(self, languages):
        """Save language distribution as SVG file"""
        svg_content = self.generate_language_svg(languages)
        
        # Ensure assets/svg directory exists
        os.makedirs("assets/svg", exist_ok=True)
        
        with open("assets/svg/language-stats.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        print("✅ Language stats SVG updated: assets/svg/language-stats.svg")

def main():
    username = "roshan1595"
    stats = DynamicGitHubStats(username)
    
    print(f"🔄 Fetching GitHub data for {username}...")
    data = stats.get_github_data()
    
    if data:
        print("✅ Data fetched successfully!")
        
        # Generate and save language SVG
        stats.save_language_svg(data['languages'])
        
        # Update stats
        updated_stats = stats.update_readme_stats(data)
        
        print("\n📊 Current Statistics:")
        print(f"📁 Repositories: {data['total_repos']}")
        print(f"👥 Followers: {data['user'].get('followers', 0)}")
        print(f"🎯 Top Language: {updated_stats['top_language']}")
        
        print("\n🌐 Language Distribution:")
        print(updated_stats['languages'])
        
        # Save data for README update
        with open("github_stats_data.json", "w") as f:
            json.dump({
                "stats": updated_stats,
                "raw_data": data,
                "generated_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print("\n✅ Stats saved to github_stats_data.json")
        
    else:
        print("❌ Failed to fetch GitHub data")

if __name__ == "__main__":
    main()