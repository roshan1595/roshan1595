#!/usr/bin/env python3
"""
Force refresh all GitHub stats widgets by busting their caches
"""
import re
from datetime import datetime, timezone

def force_refresh_widgets():
    """Force refresh all widgets by updating cache parameters"""
    
    # Read current README
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Generate fresh timestamp for cache busting
    cache_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    
    print(f"🔄 Force refreshing widgets with timestamp: {cache_timestamp}")
    
    # Update cache_seconds to force refresh (reduce cache time)
    readme_content = re.sub(r'cache_seconds=\d+', 'cache_seconds=300', readme_content)
    
    # Update cache_bust parameter for custom SVG
    readme_content = re.sub(r'cache_bust=\d+', f'cache_bust={cache_timestamp}', readme_content)
    
    # Add random parameter to other widgets to force refresh
    vercel_pattern = r'(github-readme-stats\.vercel\.app/api[^"]*)'
    def add_random_param(match):
        url = match.group(1)
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}v={cache_timestamp}"
    
    readme_content = re.sub(vercel_pattern, add_random_param, readme_content)
    
    # Update streak stats with fresh timestamp
    streak_pattern = r'(github-readme-streak-stats\.herokuapp\.com[^"]*)'
    def add_streak_param(match):
        url = match.group(1)
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}v={cache_timestamp}"
    
    readme_content = re.sub(streak_pattern, add_streak_param, readme_content)
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Widget URLs updated with fresh cache-busting parameters!")
    print("🚀 Push to GitHub to see refreshed widgets")
    
    # Show what widgets will be refreshed
    print("\n📊 Widgets that will refresh:")
    print("- GitHub Stats Card")
    print("- GitHub Streak Stats") 
    print("- Top Languages Chart")
    print("- Custom Language Distribution SVG")
    print("- Activity Graph")
    
    return cache_timestamp

if __name__ == "__main__":
    print("🔄 Force refreshing GitHub stats widgets...")
    timestamp = force_refresh_widgets()
    print(f"\n⏰ Cache-busting timestamp: {timestamp}")
    print("💡 Run 'git add . && git commit -m \"🔄 Force refresh widgets\" && git push' to deploy")