window.onload = function () {

  sessionStorage.clear();
  var input_search = document.querySelector("input");
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

  let quote = null;
  // enter to get ticker's info
  input_search.addEventListener("keypress", async function (e) {
    if (e.key === "Enter") {
      let response = await fetch("/quote?q=" + input_search.value + "&scope=quote");
      quote = await response.json();
      sessionStorage.setItem(sessionStorage.length, input_search.value);

      const buyCard = document.getElementById("card").lastElementChild;
      buyCard.classList.remove("d-none");

      // add quote's info to the card
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
      cardBody = cardBody.nextElementSibling.nextElementSibling;
    }
  });

  // calculate position value
  let input_size = document.getElementById("input-size");
  input_size.addEventListener("input", async function () {
    let total_value = 0
    if (input_size.value) {
      try {
        total_value = calPositionValue(input_size.value, quote["currentPrice"]);
        document.getElementById("total-value").setAttribute("value", total_value);
      } catch (error) {
        console.log(error);
      }
    }
    
  })
};
