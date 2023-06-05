window.addEventListener('load', function() {
  sellCards = document.querySelectorAll('.card');
  for (const card of sellCards) {
    const ticker = card
        .querySelector('.card-header')
        .firstElementChild
        .innerText;
    const inputSellSize = card.
        querySelector('[aria-label="Input Position Size"]');
    inputSize(card, inputSellSize);
    sellBtn = card.querySelector('.btn');
    clickSell(sellBtn, ticker, inputSellSize);
  }
});

// eslint-disable-next-line require-jsdoc
function clickSell(btn, ticker, input) {
  btn.addEventListener('click', async function() {
    const size = input.value;
    const req = await fetch('/sell', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({txn_type: 'sell', ticker: ticker, size: size}),
    });
    if (req.ok) {
      try {
        const res = await req.json();
        console.log(res);
        updateCardAfterSell(res);
      } catch (error) {
        console.log(error);
      }
    }
  });
}

// eslint-disable-next-line require-jsdoc
function updateCardAfterSell(sellRes) {
  const order = sellRes['order'];
  updatedCard = document.getElementById(
      ['sell-card-', order['ticker']].join(''));

  // remove card if size = 0
  if (sellRes['updated_portfolio'] == null) {
    updatedCard.remove();
  }

  // update new size
  updatedCard
      .querySelector('[aria-label="Current Size"]')
      .setAttribute('value', sellRes['updated_portfolio']['size']);

  // show message
  const message = updatedCard
      .querySelector('.form-text');
  message.innerHTML = sellRes['message'];

  updateAccountBalance();
}

// eslint-disable-next-line require-jsdoc
function inputSize(card, inputSellSize) {
  inputSellSize.addEventListener('input', async function() {
    if (inputSellSize.value) {
      const size = inputSellSize.value;
      inputSellSize.setAttribute('value', size);
      // reset the addon message
      const message = card
          .querySelector('.form-text');
      message.innerHTML = '';

      // enable cta button
      if (inputSellSize.value > 0) {
        ctaSell = card.querySelector('.cta-sell');
        ctaSell.removeAttribute('disabled', '');
      }

      // show total value
      const price = card.querySelector('.card-title').innerText.split(' ')[1];
      totalvalue = calPositionValue(inputSellSize.value,
          price);
      card
          .querySelector('[aria-label="Total Value"]')
          .setAttribute('value', totalvalue);

      // show error if sell size > current size
      const currentSize = card
          .querySelector('[aria-label="Current Size"]').value;
      console.log(currentSize);
      console.log(size);
      if (parseInt(size) > parseInt(currentSize)) {
        message.innerHTML = 'Your portfolio is too low for this call ';
      }
    }
  });
}
