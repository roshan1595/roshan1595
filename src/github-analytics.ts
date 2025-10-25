/**
 * GitHub Profile Analytics Dashboard
 * TypeScript implementation for advanced data visualization
 * Author: Roshan Kumar Singh
 */

interface GitHubUser {
  login: string;
  id: number;
  avatar_url: string;
  name: string;
  company?: string;
  blog?: string;
  location?: string;
  email?: string;
  bio?: string;
  public_repos: number;
  public_gists: number;
  followers: number;
  following: number;
  created_at: string;
  updated_at: string;
}

interface Repository {
  id: number;
  name: string;
  full_name: string;
  description?: string;
  language?: string;
  size: number;
  stargazers_count: number;
  watchers_count: number;
  forks_count: number;
  created_at: string;
  updated_at: string;
  pushed_at: string;
}

interface LanguageStats {
  [language: string]: {
    count: number;
    bytes: number;
    percentage: number;
  };
}

interface ContributionData {
  date: string;
  count: number;
  level: 0 | 1 | 2 | 3 | 4;
}

class GitHubAnalytics {
  private readonly apiBase: string = 'https://api.github.com';
  private readonly username: string;
  private readonly token?: string;

  constructor(username: string, token?: string) {
    this.username = username;
    this.token = token;
  }

  private async makeRequest<T>(endpoint: string): Promise<T> {
    const headers: Record<string, string> = {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': `github-analytics-${this.username}`
    };

    if (this.token) {
      headers['Authorization'] = `token ${this.token}`;
    }

    try {
      const response = await fetch(`${this.apiBase}${endpoint}`, { headers });
      
      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Failed to fetch ${endpoint}:`, error);
      throw error;
    }
  }

  async getUserProfile(): Promise<GitHubUser> {
    return this.makeRequest<GitHubUser>(`/users/${this.username}`);
  }

  async getRepositories(): Promise<Repository[]> {
    const repos: Repository[] = [];
    let page = 1;
    const perPage = 100;

    while (true) {
      const pageRepos = await this.makeRequest<Repository[]>(
        `/users/${this.username}/repos?page=${page}&per_page=${perPage}&sort=updated`
      );

      if (pageRepos.length === 0) break;

      repos.push(...pageRepos);
      
      if (pageRepos.length < perPage) break;
      page++;
    }

    return repos;
  }

  async getLanguageStatistics(): Promise<LanguageStats> {
    const repositories = await this.getRepositories();
    const languageStats: LanguageStats = {};
    let totalBytes = 0;

    for (const repo of repositories) {
      if (!repo.language) continue;

      try {
        const languages = await this.makeRequest<Record<string, number>>(
          `/repos/${repo.full_name}/languages`
        );

        for (const [lang, bytes] of Object.entries(languages)) {
          if (!languageStats[lang]) {
            languageStats[lang] = { count: 0, bytes: 0, percentage: 0 };
          }
          languageStats[lang].bytes += bytes;
          totalBytes += bytes;
        }

        if (repo.language && languageStats[repo.language]) {
          languageStats[repo.language].count++;
        }
      } catch (error) {
        console.warn(`Could not fetch languages for ${repo.full_name}`);
      }
    }

    // Calculate percentages
    for (const lang in languageStats) {
      languageStats[lang].percentage = (languageStats[lang].bytes / totalBytes) * 100;
    }

    return languageStats;
  }

  calculateProductivityMetrics(repos: Repository[]): {
    avgCommitsPerRepo: number;
    mostActiveMonth: string;
    recentActivity: number;
    collaborationScore: number;
  } {
    const now = new Date();
    const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    
    const recentRepos = repos.filter(repo => 
      new Date(repo.pushed_at) > thirtyDaysAgo
    );

    const monthlyActivity: Record<string, number> = {};
    
    repos.forEach(repo => {
      const month = new Date(repo.updated_at).toISOString().slice(0, 7);
      monthlyActivity[month] = (monthlyActivity[month] || 0) + 1;
    });

    const mostActiveMonth = Object.entries(monthlyActivity)
      .sort(([,a], [,b]) => b - a)[0]?.[0] || 'Unknown';

    const collaborationScore = repos.reduce((score, repo) => {
      return score + repo.forks_count + repo.stargazers_count;
    }, 0) / repos.length;

    return {
      avgCommitsPerRepo: repos.length > 0 ? repos.reduce((sum, repo) => sum + repo.size, 0) / repos.length : 0,
      mostActiveMonth,
      recentActivity: recentRepos.length,
      collaborationScore: Math.round(collaborationScore * 100) / 100
    };
  }

  async generateInsights(): Promise<{
    profile: GitHubUser;
    repositories: Repository[];
    languages: LanguageStats;
    metrics: ReturnType<GitHubAnalytics['calculateProductivityMetrics']>;
    summary: string;
  }> {
    try {
      const [profile, repositories] = await Promise.all([
        this.getUserProfile(),
        this.getRepositories()
      ]);

      const languages = await this.getLanguageStatistics();
      const metrics = this.calculateProductivityMetrics(repositories);

      const topLanguage = Object.entries(languages)
        .sort(([,a], [,b]) => b.percentage - a.percentage)[0]?.[0] || 'Unknown';

      const summary = `
        ${profile.name || profile.login} is an active developer with ${profile.public_repos} public repositories.
        Primary language: ${topLanguage} (${languages[topLanguage]?.percentage.toFixed(1)}% of codebase).
        Recent activity: ${metrics.recentActivity} repositories updated in the last 30 days.
        Community engagement: ${profile.followers} followers, ${profile.following} following.
        Collaboration score: ${metrics.collaborationScore}/10.
      `.trim();

      return {
        profile,
        repositories,
        languages,
        metrics,
        summary
      };
    } catch (error) {
      console.error('Failed to generate insights:', error);
      throw error;
    }
  }
}

// Export for use in other modules
export { GitHubAnalytics, GitHubUser, Repository, LanguageStats, ContributionData };

// Global declaration for browser environment
declare global {
  interface Window {
    GitHubAnalytics: typeof GitHubAnalytics;
  }
}

// Example usage
if (typeof window !== 'undefined') {
  // Browser environment
  window.GitHubAnalytics = GitHubAnalytics;
} else if (typeof module !== 'undefined' && module.exports) {
  // Node.js environment
  module.exports = { GitHubAnalytics };
}