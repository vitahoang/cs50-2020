function showMessage(element, message, status) {
  let alert = document.createElement("div");
  alert.setAttribute('id','alert');
  alert.innerHTML = [`<div class="mt-3 alert alert-`,status, ` mb-0 text-center" role="alert">`,message,`</div>`].join("");
  element.appendChild(alert);
}