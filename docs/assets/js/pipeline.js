(function() {
  'use strict';

  // Copy article to clipboard
  function copyArticle(button) {
    const article = button.closest('.pipeline-article');
    const { section, title, url, author, authorUrl, description } = article.dataset;

    const markdown = `<!-- SECTION: ${section} -->

### [${title}](${url})

[${author}](${authorUrl})

${description}`;

    navigator.clipboard.writeText(markdown)
      .then(() => {
        button.textContent = 'Copied!';
        button.classList.add('copied');
        setTimeout(() => {
          button.textContent = 'Copy';
          button.classList.remove('copied');
        }, 2000);
      })
      .catch(() => {
        button.textContent = 'Error';
        setTimeout(() => button.textContent = 'Copy', 2000);
      });
  }

  // Toggle form visibility
  function toggleForm() {
    const formContent = document.getElementById('formContent');
    const formHeader = document.getElementById('formHeader');
    const formContainer = document.getElementById('addArticleContainer');
    const toggleButton = document.getElementById('toggleButton');
    const isExpanded = formContent.classList.contains('expanded');

    if (isExpanded) {
      formContent.classList.remove('expanded');
      formHeader.classList.remove('expanded');
      formContainer.classList.remove('expanded');
      toggleButton.textContent = '+';
      toggleButton.setAttribute('aria-expanded', 'false');
    } else {
      formContent.classList.add('expanded');
      formHeader.classList.add('expanded');
      formContainer.classList.add('expanded');
      toggleButton.textContent = '−';
      toggleButton.setAttribute('aria-expanded', 'true');
      setTimeout(() => document.getElementById('articleUrl').focus(), 150);
    }
  }

  // Add article to pipeline via GitHub
  async function addToPipeline(event) {
    event.preventDefault();

    const urlInput = event.target.url;
    const url = urlInput.value.trim();
    if (!url) return;

    try {
      // Fetch metadata
      let title = 'Untitled Article';
      let author = 'Unknown Author';
      let publishDate = null;

      try {
        const response = await fetch(`https://api.microlink.io/?url=${encodeURIComponent(url)}`);
        const { status, data } = await response.json();

        if (status === 'success' && data) {
          title = data.title || title;
          author = data.author || author;
          publishDate = data.date || data.published || data.publishedTime || data.created || data.createdTime;
        }
      } catch (error) {
        console.warn('Metadata fetch failed:', error);
      }

      // Generate filename
      const dateStr = publishDate
        ? new Date(publishDate).toISOString().split('T')[0]
        : new Date().toISOString().split('T')[0];

      const titleSlug = title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');

      const filename = `${dateStr}-${titleSlug}.md`;

      // Generate markdown content
      const content = `---
title: "${title.replace(/"/g, '\\"')}"
url: "${url}"
author_name: "${author.replace(/"/g, '\\"')}"
author_url: ""
section: "Framework"
tags: ['Framework']
description: ""
published_date: "${dateStr}"
---
<!-- SECTION: Framework -->

### [${title}](${url})

[${author}]()

`;

      // Redirect to GitHub
      const githubUrl = `https://github.com/Snapp-Mobile/ios-newsletter/new/main?filename=docs/_pipeline/${encodeURIComponent(filename)}&value=${encodeURIComponent(content)}`;
      window.location.href = githubUrl;

    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  }

  // Event listeners
  document.addEventListener('DOMContentLoaded', function() {
    // Copy buttons
    document.querySelectorAll('.copy-button').forEach(button => {
      button.addEventListener('click', function() {
        copyArticle(this);
      });
    });

    // Form toggle
    const formHeader = document.getElementById('formHeader');
    if (formHeader) {
      formHeader.addEventListener('click', toggleForm);
    }

    // Form submission
    const form = document.getElementById('addArticleForm');
    if (form) {
      form.addEventListener('submit', addToPipeline);
    }
  });
})();
