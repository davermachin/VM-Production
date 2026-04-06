function displayPagePicker(divId) {
  const items = [
    ["index.html", "Search"],
    {
      group: "Browse",
      pages: [
        ["browse.html", "World Map"],
        ["browse_f.html", "Fiction Titles"],
        ["https://airtable.com/app5Q6OlJ3iMkJ8cd/shrD0s6Tu2cU0XDWL/tblARt16RFYyr6j42", "Master List"],
        ["https://airtable.com/app5Q6OlJ3iMkJ8cd/shrAX8erJY6tr0t3s", "Alternate Images"]
        
      ]
    },
    {
      group: "Games",
      pages: [
        ["trivia.html", "Quiz"],
        ["vmm.html", "View-MasterMIND"],
        ["bog.html", "Word Snake"]
      ]
    },
    {
      group: "Info",
      pages: [
        ["vmt.html", "View Master Travels"],
        ["about.html", "About Me"],
        ["resources.html", "Resources"]
      ]
    }    
  ];

  // Flatten for current page detection
  const allPages = [];
  items.forEach(item => {
    if (Array.isArray(item)) {
      allPages.push(item);
    } else {
      item.pages.forEach(p => allPages.push(p));
    }
  });

  const currentPage = window.location.pathname.split("/").pop() || "index.html";



  let html = `<div class="page-picker">`;

  items.forEach(item => {
    // Simple page
    if (Array.isArray(item)) {
      const [file, title] = item;
      if (file === currentPage) {
        html += `<span class="page-item selected">${title}</span>`;
      } else {
        html += `<a class="page-item" href="${file}">${title}</a>`;
      }
    } 
    // Group
    else {
      const isSelected = item.pages.some(p => p[0] === currentPage);

      html += `
        <div class="page-group">
          <span class="page-item group-toggle ${isSelected ? 'selected' : ''}">
            ${item.group} ▾
          </span>
          <div class="page-dropdown">
      `;

      item.pages.forEach(([file, title]) => {
        if (file === currentPage) {
          html += `<span class="dropdown-item selected">${title}</span>`;
        } else {
          html += `<a class="dropdown-item" href="${file}">${title}</a>`;
        }
      });

      html += `
          </div>
        </div>
      `;
    }
  });

  html += `</div>`;

  document.getElementById(divId).innerHTML = html;


setTimeout(() => {
  const groups = document.querySelectorAll(".page-group");

  groups.forEach(group => {
    const toggle = group.querySelector(".group-toggle");

    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      // Close other open groups
      groups.forEach(g => {
        if (g !== group) g.classList.remove("open");
      });

      // Toggle this one
      group.classList.toggle("open");
    });
  });

  // Click anywhere else closes menus
  document.addEventListener("click", () => {
    groups.forEach(g => g.classList.remove("open"));
  });

}, 0);  
}