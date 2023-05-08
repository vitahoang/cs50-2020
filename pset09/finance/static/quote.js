window.onload = function () {
  sessionStorage.clear();
  var input = document.querySelector("input");
  input.addEventListener("input", async function () {
    let response = await fetch("/quote?q=" + input.value + "&scope=ticker");
    let symbols = await response.json();
    let html = "";
    for (let id in symbols) {
      let symbol = String(symbols[id]["symbol"])
        .replace("<", "Slt;")
        .replace("&", "Samp;");
      html += "<option>" + symbol + "</option>";
    }
    document.querySelector("datalist").innerHTML = html;
  });

  var quoteCard = `
    <div class="col-lg-3 p-3">
      <div class="card shadow" id="quoteCard">
        <div class="card-header" id="cardHeader">   
          <h4></h4>
        </div>
        <div class="card-body" id="cardBody">
          <h5 class="card-title"></h5>
          <p class="card-text"></p>
          <p class="card-text"></p>
          <p class="card-text"></p>
          <a href="#" class="btn btn-primary">BUY</a>
          <a href="#" class="btn btn-danger">SELL</a>
        </div>
      </div>
    </div>
  `;
  input.addEventListener("keypress", async function (e) {
    if (e.key === "Enter") {
      for (let id = 0; id < sessionStorage.length; id++) {
        if (sessionStorage.getItem(sessionStorage.key(id)) == input.value){
          return;
        } else {
          console.log("fail");
        }
      }

      let response = await fetch("/quote?q=" + input.value + "&scope=quote");
      let quote = await response.json();
      sessionStorage.setItem(sessionStorage.length, input.value);

      // add a quote card to html
      const card = document.getElementById("card");
      card.innerHTML += quoteCard;

      // add quote's info to the card
      let cardHeader = card.lastElementChild.firstElementChild.firstElementChild;
      let cardBody = cardHeader.nextElementSibling.firstElementChild; 
      cardHeader.firstElementChild.innerHTML = quote["01. symbol"];
      cardBody.innerHTML = quote["05. price"];
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = [
        "Change: ",
        quote["09. change"],
        "(",
        quote["10. change percent"],
        ")",
      ].join("");
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = ["Open: ", quote["02. open"]].join("");
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = ["Volume: ", quote["06. volume"]].join("");
    }
  });
};
