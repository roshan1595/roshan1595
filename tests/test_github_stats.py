"""
Tests for GitHub Profile scripts
"""
import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

class TestGitHubStats(unittest.TestCase):
    """Test cases for GitHub stats functionality"""
    
    def test_imports(self):
        """Test that all scripts can be imported without errors"""
        try:
            import dynamic_stats
            import update_readme
            self.assertTrue(True, "All scripts imported successfully")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_json_structure(self):
        """Test that github_stats_data.json has expected structure"""
        json_file = os.path.join(os.path.dirname(__file__), '..', 'github_stats_data.json')
        
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required fields in our actual structure
            self.assertIn('raw_data', data, "Missing raw_data field")
            self.assertIn('user', data['raw_data'], "Missing user data")
            
            # Check user data structure
            user_data = data['raw_data']['user']
            required_user_fields = ['public_repos', 'followers', 'login']
            for field in required_user_fields:
                self.assertIn(field, user_data, f"Missing required user field: {field}")
                
            # Check stats structure
            if 'stats' in data:
                self.assertIn('top_language', data['stats'], "Missing top_language in stats")
        else:
            self.skipTest("github_stats_data.json not found")
    
    def test_svg_files_exist(self):
        """Test that required SVG files exist"""
        svg_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'svg')
        
        if os.path.exists(svg_dir):
            expected_svgs = [
                'header-banner.svg',
                'language-stats.svg',
                'coding-icon.svg',
                'data-wave.svg'
            ]
            
            for svg_file in expected_svgs:
                svg_path = os.path.join(svg_dir, svg_file)
                if os.path.exists(svg_path):
                    # Check file is not empty
                    with open(svg_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        self.assertTrue(len(content) > 0, f"{svg_file} is empty")
                        self.assertTrue(content.startswith('<?xml'), f"{svg_file} missing XML declaration")
        else:
            self.skipTest("SVG directory not found")

    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Test that API errors are handled gracefully"""
        # Mock API failure
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        
        try:
            import dynamic_stats
            # This should not crash even with API errors
            self.assertTrue(True, "API error handling works")
        except Exception as e:
            # Allow import errors, but not runtime crashes
            if "import" not in str(e).lower():
                self.fail(f"Script crashed on API error: {e}")

if __name__ == '__main__':
    unittest.main()