// Fetch GitHub stars for all components
document.addEventListener('DOMContentLoaded', function() {
  const starsElements = document.querySelectorAll('.github-stars');
  
  starsElements.forEach(element => {
    const repoUrl = element.getAttribute('data-repo');
    
    // Extract owner and repo name from GitHub URL
    // Expected format: https://github.com/owner/repo
    const match = repoUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    
    if (match) {
      const owner = match[1];
      const repo = match[2];
      
      // Fetch stars from GitHub API
      fetch(`https://api.github.com/repos/${owner}/${repo}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('API request failed');
          }
          return response.json();
        })
        .then(data => {
          const stars = data.stargazers_count;
          const starsCount = element.querySelector('.stars-count');
          
          // Format number with comma separators for readability
          starsCount.textContent = stars.toLocaleString();
        })
        .catch(error => {
          console.error(`Error fetching stars for ${owner}/${repo}:`, error);
          const starsCount = element.querySelector('.stars-count');
          starsCount.textContent = '—';
        });
    }
  });
});
