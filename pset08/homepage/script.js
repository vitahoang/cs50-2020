function activeNav() {
  var nav_node = genNav(navbar);
  document
    .getElementById("nav-items")
    .insertAdjacentHTML("beforeend", nav_node);
  var file_name = window.location.pathname.split("/").pop();
  var nav_items = document.querySelectorAll("a.nav-link");
  for (let i = 0; i < nav_items.length; i++) {
    const item = nav_items[i];
    if (item.getAttribute("href") == file_name) {
      item.classList.add("active");
    }
  }
  if (file_name == "index.html") {
    genIndex();
  }
  if (file_name == "computer.html") {
    genComputer();
  }
  if (file_name == "book.html") {
    genBook();
  }
  if (file_name == "product.html") {
    genProduct();
  }
  if (file_name == "contact.html") {
    genContact();
  }
}

function genNav(nav_list) {
  let nav_html = `
  ${nav_list
    .map(
      (nav) => `
      <li class="nav-item">
        <a class="nav-link" href="${nav.href}">${nav.name}</a>
      </li>`
    )
    .join("")}`;
  return nav_html;
}

function genSections(sections) {
  let sections_html = `
    ${sections
      .map(
        (section) => `
    <div class="row mt-2 mb-5" id="${section.name.toLowerCase()}">
        <div class="col-3 border-end border-primary" id="section-name">
            <p class="fs-5">${section.name}</p>
        </div>
        <div class="col" id="section-items"></div>
    </div>
    `
      )
      .join("")}`;
  return sections_html;
}

function genCards(cards) {
  let cards_html = `
        ${cards
          .map(
            (item) => `
        <div class="row mb-2 ms-2">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${item.title}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${item.subitle}</h6>
                    <p class="card-text">
                        ${item.description}
                    </p>
                </div>
            </div>
        </div>
        `
          )
          .join("")}`;
  return cards_html;
}

const navbar = [
  {
    name: "About me",
    href: "index.html",
  },
  {
    name: "Computer",
    href: "computer.html",
  },
  {
    name: "Product",
    href: "product.html",
  },
  {
    name: "Book",
    href: "book.html",
  },
  {
    name: "Contact",
    href: "contact.html",
  },
];

const experiment = [
  {
    title: "Senior Product Manager, Tiki",
    subitle: "Nov 2021 - Present",
    description: "description",
  },
  {
    title: "Technical Product Manager, Got It Inc.",
    subitle: "Aug 2019 - Nov 2021",
    description: "description",
  },
  {
    title: "Senior Product Owner, VinID",
    subitle: "Sep 2018 - Jul 2019",
    description: "description",
  },
  {
    title: "Product Owner, TrueMoney",
    subitle: "Oct 2016 - Sep 2018",
    description: "description",
  },
  {
    title: "Marketing Specialist & Business Analyst, MOG",
    subitle: "Jul 2016 - Oct 2016",
    description: "description",
  },
  {
    title: "Marketing Specialist, New Ocean Group",
    subitle: "May 2015 - May 2016",
    description: "description",
  },
  {
    title: "Account Executive, Metan Vietnam",
    subitle: "Oct 2013 - May 2014",
    description: "description",
  },
];

const skills = [
  {
    title: "Product management",
    subitle:
      "Effective communication skills: Product evangelism, stakeholder management & negotiation, group presentation",
    description: "description",
  },
  {
    title: "Technical knowledge",
    subitle: "Basic knowledge of computer science and programming languages",
    description: "",
  },
];
const education = [
  {
    title: "Bachelor of Sciences in Biotechnology, Phuong Dong University",
    subitle: "Sep 2011 - May 2018",
    description: "",
  },
  {
    title: "Certificates",
    subitle: "subtitle",
    description: "",
  },
];
const info = [
  {
    title: "Social Impacts",
    subitle:
      "Volunteer Product Manager for Helpme! project (http://giuptoi.vn/)",
    description: "",
  },
  {
    title: "Personal Interest",
    subitle: "Reading books, running",
    description: "",
  },
];
const profile = [
  {
    title: "",
    subitle:
      "With 5+ years of experience in building and launching software products from conception to fruition, bringing forth the ability to:",
    description: "",
  },
];

const sections = [
  { name: "Profile" },
  { name: "Experiment" },
  { name: "Skills" },
  { name: "Education" },
  { name: "Additional Info" },
];

function genIndex() {
  var sections_node = genSections(sections);
  document
    .getElementById("resume")
    .insertAdjacentHTML("beforeend", sections_node);

  var card_node = genCards(profile);
  document
    .getElementById("profile")
    .childNodes[3].insertAdjacentHTML("beforeend", card_node);

  var card_node = genCards(experiment);
  document
    .getElementById("experiment")
    .childNodes[3].insertAdjacentHTML("beforeend", card_node);

  var card_node = genCards(skills);
  document
    .getElementById("skills")
    .childNodes[3].insertAdjacentHTML("beforeend", card_node);

  var card_node = genCards(education);
  document
    .getElementById("education")
    .childNodes[3].insertAdjacentHTML("beforeend", card_node);

  var card_node = genCards(info);
  document
    .getElementById("additional info")
    .childNodes[3].insertAdjacentHTML("beforeend", card_node);
}

function showAlert(event, alert) {
  let form = event.target.parentNode;
  form.insertAdjacentHTML("beforeend", alert);
}

var success_alert = `
  <div class="alert alert-success" role="alert">
    Your question has been submitted <a href="#" class="alert-link">successfully</a>.
  </div>`;
