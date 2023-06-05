window.addEventListener('load', function() {
  sessionStorage.clear();
  const input = document.querySelector('input');
  let typingTimer;

  // setup an eventListener that only calls after finished typing
  // https://stackoverflow.com/a/5926782
  input.addEventListener('keyup', async function(e) {
    clearTimeout(typingTimer);
    // stop if user enters to query quote
    if (e.key === 'Enter') {
      return;
    }
    // delete the current error
    if (document.getElementById('alert')) {
      input.parentElement.removeChild(document.getElementById('alert'));
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
  input.addEventListener('keypress', async function(e) {
    if (e.key === 'Enter') {
      // check if ticker has been searched before
      for (let id = 0; id < sessionStorage.length; id++) {
        if (sessionStorage.getItem(sessionStorage.key(id)) == input.value) {
          return;
        }
      }

      const response = await fetch('/quote?q=' + input.value + '&scope=quote');
      const quote = await response.json();
      sessionStorage.setItem(sessionStorage.length, input.value);

      // add a quote card to html
      const card = document.getElementById('card');
      card.innerHTML += quoteCard;
      btn = document.getElementsByClassName('btn'); // get new btn

      // add quote's info to the card
      const cardHeader = card.lastElementChild
          .firstElementChild.firstElementChild;
      cardHeader.firstElementChild.innerHTML = quote['symbol'];
      let cardBody = cardHeader.nextElementSibling.firstElementChild;
      cardBody.innerHTML = quote['currentPrice'];
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = [
        'Change: ',
        quote['change'],
        ' (',
        quote['changePercent'],
        ')',
      ].join('');
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = ['Open: ', quote['open']].join('');
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML =
      // eslint-disable-next-line new-cap
      ['Volume: ', Intl.NumberFormat().format(quote['volume'])].join('');
      cardBody = cardBody.nextElementSibling;
      clickBuySell(cardBody, quote['symbol']);
      cardBody = cardBody.nextElementSibling;
      clickBuySell(cardBody, quote['symbol']);
    }
  });
});

/**
* Attaches a click event listener to the provided button element and sets
its href attribute based on its inner text.
*
* @param {object} btn - The button element where the click event listener needs
to be attached.
* @param {string} ticker - The stock ticker value that will be used to construct
the value of the href attribute.
*
* @return {void}
*/
function clickBuySell(btn, ticker) {
  btn.addEventListener('click', function() {
    if (btn.innerText == 'BUY') {
      this.setAttribute('href', ['/buy?ticker=', ticker].join(''));
    } else {
      this.setAttribute('href', ['/sell?ticker=', ticker].join(''));
    }
  });
}
