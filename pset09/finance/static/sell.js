window.addEventListener('load', function() {
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

  // redirect when click CTA BUY or SELL
  // eslint-disable-next-line require-jsdoc
  function clickBuySell(btn, ticker) {
    btn.addEventListener('click', function() {
      if (btn.innerText == 'BUY') {
        this.setAttribute('href', ['/buy?ticker=', ticker].join(''));
      } else {
        this.setAttribute('href', ['/sell?ticker=', ticker].join(''));
      }
    });
  }
});