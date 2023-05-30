window.addEventListener('load', function() {
  sessionStorage.clear();
  const inputSearch = document.querySelector('input');
  const ctaBuy = document.getElementById('cta-buy');
  const inputSize = document.getElementById('input-size');
  let typingTimer;

  // setup an eventListener that only calls after finished typing
  // https://stackoverflow.com/a/5926782
  inputSearch.addEventListener('keyup', async function(e) {
    clearTimeout(typingTimer);
    // stop if user enters to query quote
    if (e.key === 'Enter') {
      return;
    }

    // delete the current 404 error
    if (document.getElementById('alert')) {
      inputSearch.parentElement.removeChild(document.getElementById('alert'));
    }

    // set timeout to prevent multiple error when typing too fast
    if (inputSearch.value) {
      typingTimer = setTimeout(async () => {
        try {
          searchTicker(inputSearch);
        } catch (error) {
          console.error(error);
        }
      }, 400);
    }
  });

  // enter to get ticker's info
  let quote = null;
  inputSearch.addEventListener('keypress', async function(e) {
    if (e.key === 'Enter') {
      const response = await fetch(
          '/quote?q=' + inputSearch.value + '&scope=quote',
      );
      quote = await response.json();
      sessionStorage.setItem(sessionStorage.length, inputSearch.value);

      // show the quote card
      const buyCard = document.getElementById('card').lastElementChild;
      buyCard.classList.remove('d-none');

      // show quote's info on the card
      const cardHeader = buyCard.firstElementChild.firstElementChild;
      let cardBody = cardHeader.nextElementSibling.firstElementChild;
      cardHeader.firstElementChild.innerHTML = quote['symbol'];
      cardBody.innerHTML = ['Price: ', quote['currentPrice']].join('');
      cardBody = cardBody.nextElementSibling;
      cardBody.innerHTML = [
        'Change: ',
        quote['change'],
        ' (',
        quote['changePercent'],
        ')',
      ].join('');
      if (quote['change'] >= 0) {
        cardBody.classList.add('text-success');
      } else {
        cardBody.classList.add('text-danger');
      }
    }
  });

  // calculate position value
  inputSize.addEventListener('input', async function() {
    let totalvalue = 0;
    if (inputSize.value) {
      try {
        // reset the addon message
        const message = document.getElementById('quote-card-addon-message');
        message.innerHTML = '';
        message.setAttribute('class', 'form-text');

        // enable cta button
        if (inputSize.value > 0) {
          ctaBuy.removeAttribute('disabled', '');
        }

        // show total value
        totalvalue = calPositionValue(inputSize.value, quote['currentPrice']);
        document
            .getElementById('total-value')
            .setAttribute('value', totalvalue);

        // show error if total value > balance
        const balance = parseFloat(
            sessionStorage.getItem('account_balance').replace(/,/, ''),
        );
        if (parseFloat(totalvalue.replace(/,/, '')) > balance) {
          message.classList.add('text-danger');
          message.innerHTML = 'Your balance is too low for this call';
          ctaBuy.setAttribute('disabled', '');
        }
      } catch (error) {
        console.log(error);
      }
    }
  });

  // Submit a bid
  ctaBuy.addEventListener('click', async function() {
    const req = await fetch('/buy', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        txn_type: 'buy',
        ticker: quote['symbol'],
        size: inputSize.value,
      },
      ),
    });
    const res = await req.json();
    console.log(res);
  });
});
