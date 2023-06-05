window.addEventListener('load', function() {
  sellCards = document.querySelectorAll('.card');

  for (const card of sellCards) {
    const ticker = card
        .querySelector('.card-header')
        .firstElementChild
        .innerText;
    inputSellSize = card.querySelector('[aria-label="Input Position Size"]');
    inputSize(card, inputSellSize);
  }
});

// eslint-disable-next-line require-jsdoc
function clickSell(btn, ticker, input) {
  size = input.value;
  btn.addEventListener('click', async function() {
    const res = await fetch('/sell?ticker=' + ticker + '&size=' + size);
    try {
      if (res.ok) {
        const portfolio = await res.json();
        console.log(portfolio);
      }
    } catch (error) {
      console.log(error);
    }
  });
}

// eslint-disable-next-line require-jsdoc
function inputSize(card, inputSellSize) {
  inputSellSize.addEventListener('input', async function() {
    if (inputSellSize.value) {
      const size = inputSellSize.value;
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
      if (size > currentSize) {
        message.innerHTML = 'Your portfolio is too low for this call ';
      }
    }
  });
}
