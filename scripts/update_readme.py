import json
import re
from datetime import datetime
import requests

def load_stats_data():
    """Load the latest stats data"""
    try:
        with open('github_stats_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Stats data not found, generating fresh data...")
        # Generate fresh data if file doesn't exist
        import subprocess
        subprocess.run(['python', 'scripts/dynamic_stats.py'])
        
        with open('github_stats_data.json', 'r') as f:
            return json.load(f)

def update_readme_stats():
    """Update README.md with the latest stats"""
    # Load current stats
    stats_data = load_stats_data()
    stats = stats_data['stats']
    raw_data = stats_data['raw_data']
    
    # Read current README
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Update the stats table
    new_table = f"""| 📊 **Metric** | 🔢 **Value** | 📈 **Details** |
|---------------|--------------|----------------|
| 📁 **Public Repositories** | `{raw_data['user']['public_repos']}` | Active development portfolio |
| 👥 **Followers** | `{raw_data['user']['followers']}` | Growing professional network |
| 💫 **Following** | `{raw_data['user']['following']}` | Curated tech influencers |
| 🎯 **Primary Languages** | `{', '.join(list(raw_data['languages'].keys())[:3])}` | Full-stack development |
| 📅 **Account Since** | `{raw_data['user']['created_at'][:10]}` | Years of consistent coding |
| ⭐ **Total Stars** | `Building...` | Projects gaining recognition |"""

    # Update language distribution
    languages = raw_data['languages']
    lang_distribution = ""
    for lang, percentage in list(languages.items())[:5]:
        bar_length = int(percentage / 2.5)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        lang_distribution += f"{lang:<12} {bar} {percentage}%\n"

    # Update the README sections
    # Update stats table
    table_pattern = r'\| 📊 \*\*Metric\*\* \| 🔢 \*\*Value\*\* \| 📈 \*\*Details\*\* \|.*?\| ⭐ \*\*Total Stars\*\* \| `[^`]*` \| Projects gaining recognition \|'
    readme_content = re.sub(table_pattern, new_table, readme_content, flags=re.DOTALL)
    
    # Update language distribution
    lang_pattern = r'```\n([^\n]*)\s+[█░\s]+\s+\d+\.\d+%.*?\n```'
    new_lang_block = f"```\n{lang_distribution.strip()}\n```"
    readme_content = re.sub(lang_pattern, new_lang_block, readme_content, flags=re.DOTALL)
    
    # Update "Last Updated" timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    updated_pattern = r'\*GitHub analytics services are.*?\*'
    new_update_text = f"*Last updated: {current_time} • Auto-refreshes every 6 hours*"
    readme_content = re.sub(updated_pattern, new_update_text, readme_content)
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ README updated with latest stats!")
    print(f"📊 Repositories: {raw_data['user']['public_repos']}")
    print(f"👥 Followers: {raw_data['user']['followers']}")
    print(f"🎯 Top Language: {list(languages.keys())[0] if languages else 'None'}")
    print(f"⏰ Updated at: {current_time}")

def create_dynamic_stats_endpoint():
    """Create a simple stats endpoint for real-time data"""
    username = "roshan1595"
    
    # This could be expanded to create a simple HTTP server
    # For now, we'll just update the JSON file
    stats_data = load_stats_data()
    
    # Create a simple HTML stats page (optional)
    html_stats = f"""<!DOCTYPE html>
<html>
<head>
    <title>GitHub Stats - {username}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; background: #0d1117; color: #ffffff; padding: 20px; }}
        .stat {{ margin: 10px 0; padding: 10px; background: #21262d; border-radius: 6px; }}
        .value {{ color: #58a6ff; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📊 Live GitHub Stats for {username}</h1>
    <div class="stat">📁 Repositories: <span class="value">{stats_data['raw_data']['user']['public_repos']}</span></div>
    <div class="stat">👥 Followers: <span class="value">{stats_data['raw_data']['user']['followers']}</span></div>
    <div class="stat">💫 Following: <span class="value">{stats_data['raw_data']['user']['following']}</span></div>
    <div class="stat">🎯 Top Language: <span class="value">{list(stats_data['raw_data']['languages'].keys())[0] if stats_data['raw_data']['languages'] else 'None'}</span></div>
    <div class="stat">⏰ Last Updated: <span class="value">{stats_data['generated_at']}</span></div>
    
    <h2>🌐 Language Distribution</h2>
    <pre style="background: #161b22; padding: 15px; border-radius: 6px; font-family: 'Courier New', monospace;">
{stats_data['stats']['languages']}
    </pre>
</body>
</html>"""
    
    with open('stats.html', 'w', encoding='utf-8') as f:
        f.write(html_stats)
    
    print("✅ Dynamic stats endpoint created: stats.html")

if __name__ == "__main__":
    print("🔄 Updating GitHub profile stats...")
    update_readme_stats()
    create_dynamic_stats_endpoint()
    print("🎉 Profile stats updated successfully!")