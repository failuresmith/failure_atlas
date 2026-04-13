(function () {
  const searchModal = document.getElementById("search-modal");
  const openSearchButton = document.getElementById("open-search");
  const closeSearchButton = document.getElementById("close-search");
  const searchOverlay = document.getElementById("search-overlay");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  const filterDomain = document.getElementById("filter-domain");
  const filterMechanism = document.getElementById("filter-mechanism");
  const filterType = document.getElementById("filter-type");
  const filterKeyword = document.getElementById("filter-keyword");
  const clearFiltersButton = document.getElementById("clear-filters");
  const visibleCount = document.getElementById("visible-count");

  const atlasRows = Array.from(document.querySelectorAll(".atlas-row"));
  const searchIndexUrl = document.body.dataset.searchIndexUrl;

  let searchIndex = [];
  let searchLoaded = false;

  const normalize = (value) => (value || "").toString().toLowerCase().trim();
  const tokenize = (value) =>
    normalize(value)
      .split(/[^a-z0-9_]+/)
      .filter(Boolean);

  const escapeRegExp = (value) => (value || "").toString().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const escapeHtml = (unsafe) =>
    (unsafe || "")
      .toString()
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  const highlightText = (text, terms) => {
    const haystack = (text || "").toString();
    const activeTerms = Array.from(new Set(terms || [])).filter(Boolean);
    if (!activeTerms.length) {
      return escapeHtml(haystack);
    }

    const pattern = activeTerms
      .map(escapeRegExp)
      .sort((a, b) => b.length - a.length)
      .join("|");

    if (!pattern) {
      return escapeHtml(haystack);
    }

    const regex = new RegExp(pattern, "gi");
    let lastIndex = 0;
    let result = "";
    let match;

    while ((match = regex.exec(haystack))) {
      result += escapeHtml(haystack.slice(lastIndex, match.index));
      result += `<span class="search-highlight">${escapeHtml(match[0])}</span>`;
      lastIndex = match.index + match[0].length;
    }

    result += escapeHtml(haystack.slice(lastIndex));
    return result;
  };

  const resolveEntryUrl = (rawUrl) => {
    if (!rawUrl) return "#";
    if (/^[a-z]+:\/\//i.test(rawUrl)) return rawUrl;
    const cleaned = rawUrl.replace(/^\.\//, "");
    const inEntriesPage = window.location.pathname.includes("/entries/");
    return inEntriesPage ? `../${cleaned}` : cleaned;
  };

  const openSearch = () => {
    if (!searchModal) return;
    searchModal.classList.remove("hidden");
    document.body.classList.add("modal-open");
    if (searchInput) {
      searchInput.focus();
      searchInput.select();
    }
    if (!searchLoaded) {
      loadSearchIndex();
    }
  };

  const closeSearch = () => {
    if (!searchModal) return;
    searchModal.classList.add("hidden");
    document.body.classList.remove("modal-open");
  };

  const renderSearchResults = (items, terms) => {
    if (!searchResults) return;
    if (!items.length) {
      searchResults.innerHTML = `<p class="empty-state">No matches found.</p>`;
      return;
    }

    const highlightValue = (value) => highlightText(value, terms);

    searchResults.innerHTML = items
      .map(
        (item) => `
          <article class="search-result">
            <h3><a href="${escapeHtml(resolveEntryUrl(item.url))}">${highlightValue(item.id)} · ${highlightValue(item.title)}</a></h3>
            <p class="search-meta">${highlightValue(`${item.type} · ${item.failure_domain || "No domain"} · ${item.mechanism || "No mechanism"}`)}</p>
            <p class="search-summary">${highlightValue(item.summary || "No summary available.")}</p>
          </article>
        `
      )
      .join("");
  };

  const applySearch = () => {
    if (!searchInput || !searchLoaded) return;
    const query = normalize(searchInput.value);

    if (!query) {
      searchResults.innerHTML = `<p class="empty-state">Type a keyword to search.</p>`;
      return;
    }

    const terms = tokenize(query);
    const matches = searchIndex
      .filter((item) => {
        if (!terms.length) return false;
        const tokens = item._tokens || [];

        return terms.every((term) => {
          if (term.length <= 2) {
            return tokens.includes(term);
          }

          return tokens.some((token) => token === term || token.startsWith(term));
        });
      })
      .slice(0, 50);

    renderSearchResults(matches, terms);
  };

  const loadSearchIndex = async () => {
    if (!searchIndexUrl || !searchResults) return;
    searchResults.innerHTML = `<p class="empty-state">Loading index…</p>`;
    try {
      const response = await fetch(searchIndexUrl, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`Failed to load search index (${response.status})`);
      }
      const payload = await response.json();
      searchIndex = Array.isArray(payload)
        ? payload.map((item) => ({
            ...item,
            _tokens: tokenize(item.searchable_text || ""),
          }))
        : [];
      searchLoaded = true;
      applySearch();
    } catch (error) {
      searchResults.innerHTML = `<p class="empty-state">Search index unavailable.</p>`;
      console.error(error);
    }
  };

  const applyRowFilters = () => {
    if (!atlasRows.length) return;

    const domainValue = normalize(filterDomain?.value);
    const mechanismValue = normalize(filterMechanism?.value);
    const typeValue = normalize(filterType?.value);
    const keywordValue = normalize(filterKeyword?.value);
    const keywords = keywordValue.split(/\s+/).filter(Boolean);

    let visible = 0;

    atlasRows.forEach((row) => {
      const rowDomain = normalize(row.dataset.domain);
      const rowMechanism = normalize(row.dataset.mechanism);
      const rowType = normalize(row.dataset.type);
      const haystack = normalize(
        [row.dataset.id, row.dataset.title, row.dataset.domain, row.dataset.mechanism, row.dataset.summary].join(" ")
      );

      const passDomain = !domainValue || rowDomain === domainValue;
      const passMechanism = !mechanismValue || rowMechanism === mechanismValue;
      const passType = !typeValue || rowType === typeValue;
      const passKeyword = !keywords.length || keywords.every((term) => haystack.includes(term));

      const show = passDomain && passMechanism && passType && passKeyword;
      row.hidden = !show;
      if (show) visible += 1;
    });

    if (visibleCount) {
      visibleCount.textContent = `${visible} visible ${visible === 1 ? "entry" : "entries"}`;
    }
  };

  const initScrollReveal = () => {
    const revealNodes = Array.from(document.querySelectorAll(".reveal-on-scroll"));
    if (!revealNodes.length) return;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reducedMotion || !("IntersectionObserver" in window)) {
      revealNodes.forEach((node) => node.classList.add("is-visible"));
      return;
    }

    const isNearViewport = (node) => {
      const rect = node.getBoundingClientRect();
      return rect.top < window.innerHeight * 0.92;
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.remove("pending-reveal");
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        rootMargin: "0px 0px -8% 0px",
        threshold: 0.08,
      }
    );

    revealNodes.forEach((node) => {
      if (isNearViewport(node)) {
        node.classList.add("is-visible");
        return;
      }

      node.classList.add("pending-reveal");
      observer.observe(node);
    });
  };

  if (openSearchButton) {
    openSearchButton.addEventListener("click", openSearch);
  }
  if (closeSearchButton) {
    closeSearchButton.addEventListener("click", closeSearch);
  }
  if (searchOverlay) {
    searchOverlay.addEventListener("click", closeSearch);
  }
  if (searchInput) {
    searchInput.addEventListener("input", applySearch);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && searchModal && !searchModal.classList.contains("hidden")) {
      closeSearch();
    }
  });

  [filterDomain, filterMechanism, filterType].forEach((element) => {
    if (element) {
      element.addEventListener("change", applyRowFilters);
    }
  });

  if (filterKeyword) {
    filterKeyword.addEventListener("input", applyRowFilters);
  }

  if (clearFiltersButton) {
    clearFiltersButton.addEventListener("click", () => {
      if (filterDomain) filterDomain.value = "";
      if (filterMechanism) filterMechanism.value = "";
      if (filterType) filterType.value = "";
      if (filterKeyword) filterKeyword.value = "";
      applyRowFilters();
    });
  }

  applyRowFilters();
  initScrollReveal();
})();
