window.onload = function () {

  sessionStorage.clear();
  var input = document.querySelector("input");
  var typingTimer;

  // setup an eventListener that only calls after finished typing
  // https://stackoverflow.com/a/5926782 
  input.addEventListener("keyup", async function () {
    clearTimeout(typingTimer);
    // delete the current error
    if (document.getElementById("alert")) {
      input.parentElement.removeChild(document.getElementById("alert"));
    }

    if (input.value) {
      typingTimer = setTimeout(async () => {
        try {
          // search for tickers 
          var response = await fetch("/quote?q=" + input.value + "&scope=ticker");
          if (response.status == 404) {
            showMessage(input.parentElement,"Ticker not Found","danger")
          }
          let symbols = await response.json();
          let html = "";
          for (let id in symbols) {
            let symbol = String(symbols[id]["symbol"])
              .replace("<", "Slt;")
              .replace("&", "Samp;");
            html += "<option>" + symbol + "</option>";
          }
          document.querySelector("datalist").innerHTML = html;
        } catch (error) {
          console.error(error);
        }
      }, 400);
    }
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

  // enter to get ticker's info
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
      cardHeader.firstElementChild.innerHTML = quote["symbol"];
      cardBody.innerHTML = quote["currentPrice"];
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = [
        "Change: ",
        quote["change"],
        " (",
        quote["changePercent"],
        ")",
      ].join("");
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = ["Open: ", quote["open"]].join("");
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = ["Volume: ", quote["volume"]].join("");
    }
  });
};
