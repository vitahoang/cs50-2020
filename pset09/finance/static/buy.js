window.addEventListener("load", function () {

  sessionStorage.clear();
  var input_search = document.querySelector("input");
  var cta_buy = document.getElementById("cta-buy");
  var typingTimer;

  // setup an eventListener that only calls after finished typing
  // https://stackoverflow.com/a/5926782 
  input_search.addEventListener("keyup", async function (e) {
    clearTimeout(typingTimer);
    // stop if user enters to query quote
    if (e.key === "Enter") {
      return;
    }

    // delete the current 404 error
    if (document.getElementById("alert")) {
      input_search.parentElement.removeChild(document.getElementById("alert"));
    }

    // set timeout to prevent multiple error when typing too fast
    if (input_search.value) {
      typingTimer = setTimeout(async () => {
        try {
          searchTicker(input_search);
        } catch (error) {
          console.error(error);
        }
      }, 400);
    }
  });

  // enter to get ticker's info
  let quote = null;
  input_search.addEventListener("keypress", async function (e) {
    if (e.key === "Enter") {
      let response = await fetch("/quote?q=" + input_search.value + "&scope=quote");
      quote = await response.json();
      sessionStorage.setItem(sessionStorage.length, input_search.value);

      //show the quote card
      const buyCard = document.getElementById("card").lastElementChild;
      buyCard.classList.remove("d-none");

      // show quote's info on the card
      let cardHeader = buyCard.firstElementChild.firstElementChild;
      let cardBody = cardHeader.nextElementSibling.firstElementChild; 
      cardHeader.firstElementChild.innerHTML = quote["symbol"];
      cardBody.innerHTML = ["Price: ", quote["currentPrice"]].join("");
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = [
        "Change: ",
        quote["change"],
        " (",
        quote["changePercent"],
        ")",
      ].join("");
      if (quote["change"] >= 0) {
        cardBody.classList.add("text-success")
      } else{
        cardBody.classList.add("text-danger")
      }
    }
  });

  // calculate position value
  let input_size = document.getElementById("input-size");
  input_size.addEventListener("input", async function () {
    let total_value = 0
    if (input_size.value) {
      try {
        // reset the addon message
        let message = document.getElementById("quote-card-addon-message");
        message.innerHTML = "";
        message.setAttribute("class", "form-text");

        // enable cta button
        cta_buy.removeAttribute('disable', '');

        // show total value
        total_value = calPositionValue(input_size.value, quote["currentPrice"]);
        document.getElementById("total-value").setAttribute("value", total_value);

        // show error if total value > balance 
        let balance = parseFloat(sessionStorage.getItem("account_balance").replace(/,/,""));
        console.log(parseFloat(total_value.replace(/,/,"")));
        if (parseFloat(total_value.replace(/,/,"")) > balance) {
          message.classList.add("text-danger");
          message.innerHTML = "Your balance is too low for this call"
          cta_buy.setAttribute('disable', '');
        }
      } catch (error) {
        console.log(error);
      }
    }
  })

  //Submit a bid 


  
});
