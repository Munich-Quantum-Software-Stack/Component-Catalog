// Fetch GitHub stars for all components using GraphQL
document.addEventListener('DOMContentLoaded', function() {
  const starsElements = document.querySelectorAll('.github-stars');
  
  // Build a map of repo info
  const repos = [];
  const elementMap = new Map();
  
  starsElements.forEach(element => {
    const repoUrl = element.getAttribute('data-repo');
    const match = repoUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    
    if (match) {
      const owner = match[1];
      const repo = match[2];
      const key = `${owner}/${repo}`;
      
      repos.push({ owner, repo, key });
      elementMap.set(key, element);
    }
  });
  
  if (repos.length === 0) return;
  
  // Build GraphQL query for all repos in one request
  let queryParts = [];
  repos.forEach((repoInfo, index) => {
    const alias = `repo${index}`;
    queryParts.push(`
      ${alias}: repository(owner: "${repoInfo.owner}", name: "${repoInfo.repo}") {
        stargazerCount
      }
    `);
  });
  
  const query = `query {
    ${queryParts.join('')}
  }`;
  
  // Fetch all stars with single GraphQL request
  fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('GraphQL request failed');
      }
      return response.json();
    })
    .then(result => {
      if (result.errors) {
        throw new Error(result.errors[0].message);
      }
      
      // Update all star counts
      repos.forEach((repoInfo, index) => {
        const alias = `repo${index}`;
        const repoData = result.data[alias];
        
        if (repoData && repoData.stargazerCount !== undefined) {
          const element = elementMap.get(repoInfo.key);
          const starsCount = element.querySelector('.stars-count');
          starsCount.textContent = repoData.stargazerCount.toLocaleString();
        }
      });
    })
    .catch(error => {
      console.error('Error fetching GitHub stars:', error);
      // Set all to error state
      starsElements.forEach(element => {
        const starsCount = element.querySelector('.stars-count');
        starsCount.textContent = '—';
      });
    });
});
