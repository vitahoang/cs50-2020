window.addEventListener("load", function () {

  sessionStorage.clear();
  var input = document.querySelector("input");
  var typingTimer;

  // setup an eventListener that only calls after finished typing
  // https://stackoverflow.com/a/5926782 
  input.addEventListener("keyup", async function (e) {
    clearTimeout(typingTimer);
    // stop if user enters to query quote
    if (e.key === "Enter") {
      return;
    }
    // delete the current error
    if (document.getElementById("alert")) {
      input.parentElement.removeChild(document.getElementById("alert"));
    }

    // set timeout to prevent multiple error when typing too fast
    if (input.value) {
      typingTimer = setTimeout(async () => {
        try {
          searchTicker(input);
        } catch (error) {
          console.error(error);
        }
      }, 400);
    }
  });

  // enter to get ticker's info
  input.addEventListener("keypress", async function (e) {
    if (e.key === "Enter") {
      // check if ticker has been searched before
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
      card.innerHTML += quote_card;

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
      cardBody.innerHTML = ["Volume: ", Intl.NumberFormat().format(quote["volume"])].join("");
    }
  });
});
