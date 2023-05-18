function showMessage(element, message, status) {
  let alert = document.createElement("div");
  alert.setAttribute('id','alert');
  alert.innerHTML = [`<div class="mt-3 alert alert-`,status, ` mb-0 text-center" role="alert">`,message,`</div>`].join("");
  element.appendChild(alert);
}

async function searchTicker(input) {
          // search for tickers 
          var response = await fetch("/quote?q=" + input.value + "&scope=ticker");
          if (response.status == 404) {
            showMessage(input.parentElement,"Ticker not Found","danger");
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
}

function calPositionValue(size, price) {
  try {
    let value = Intl.NumberFormat("en-US", {style: "decimal", maximumSigificantDigits: 2}).format(
      parseFloat(size) * parseFloat(price)
    );
    return value
  } catch (error) {
    console.log(error)
  }
}