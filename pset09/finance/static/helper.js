/**
 * Displays a message on the target element with a given status.
 *
 * @param {HTMLElement} element - The target HTML element
 * to append the message to.
 * @param {string} message - The message to be displayed.
 * @param {string} status - The status of the message,
 * such as success, warning or danger.
 *
 * @return {void}
 */
function showMessage(element, message, status) {
  const alert = document.createElement('div');
  alert.setAttribute('id', 'alert');
  alert.innerHTML = [`<div class="mt-3 alert alert-`,
    status, ` mb-0 text-center" role="alert">`, message, `</div>`].join('');
  element.appendChild(alert);
}


/**
 * Searches for ticker symbols based on user input and displays them in a
 * dropdown list.
 *
 * @async
 * @function searchTicker
 * @param {HTMLInputElement} input - The HTML input element containing the
 * user's search query.
 * @return {Promise<void>} A promise that resolves when the ticker symbols
 * have been retrieved and displayed.
 * @throws {Error} If the server returns a 404 error status code.
 */
// eslint-disable-next-line no-unused-vars, require-jsdoc
async function searchTicker(input) {
  // search for tickers
  const response = await fetch('/quote?q=' + input.value + '&scope=ticker');
  if (response.status == 404) {
    showMessage(input.parentElement, 'Ticker not Found', 'danger');
  }
  const symbols = await response.json();
  let html = '';
  for (const id in symbols) {
    if (symbols.hasOwnProperty(id)) {
      const symbol = String(symbols[id]['symbol'])
          .replace('<', 'Slt;')
          .replace('&', 'Samp;');
      html += '<option>' + symbol + '</option>';
    }
  }
  document.querySelector('datalist').innerHTML = html;
}


/**
 * Calculates the total position value based on a given size and price.
*
* @param {number|string} size The size of the position.
* @param {number|string} price The price of the asset.
* @return {string} A formatted string representing the total position value.
*/
// eslint-disable-next-line no-unused-vars, require-jsdoc
function calPositionValue(size, price) {
  const floatFormat = function() {
    return new Intl.NumberFormat('en-US', {
      style: 'decimal',
      maximumSigificantDigits: 2,
    });
  };
  try {
    const value = floatFormat().format(parseFloat(size) * parseFloat(price));
    return value;
  } catch (error) {
    console.log(error);
  }
}


