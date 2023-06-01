// eslint-disable-next-line no-unused-vars
const quoteCard = `
  <div class="col-lg-3 p-3">
    <div class="card shadow" id="quote-card">
      <div class="card-header" id="card-header">   
        <h4></h4>
      </div>
      <div class="card-body" id="card-body">
        <h5 class="card-title"></h5>
        <p class="card-text"></p>
        <p class="card-text"></p>
        <p class="card-text"></p>
        <a href="/buy" class="btn btn-primary">BUY</a>
        <a href="/sell" class="btn btn-danger">SELL</a>
      </div>
    </div>
  </div>
`;

// eslint-disable-next-line no-unused-vars
const buyCard = `
<div class="col-lg-3 p-3 d-none">
        <div class="card shadow" id="quote-card">
            <div class="card-header" id="card-header">
                <h4></h4>
            </div>
            <div class="card-body" id="card-body">
                <h5 class="card-title"></h5>
                <p class="card-text"></p>
                <div class="input-group mb-3">
                    <span class="input-group-text" id="inputGroup-sizing-default">Position Size</span>
                    <input type="number" class="form-control" aria-label="Input Position Size"
                        aria-describedby="inputGroup-sizing-default" value="0" min="0" id="input-size">
                </div>
                <div class="mb-3">
                    <div class="input-group">
                        <span class="input-group-text" style="padding: 0.375rem 1.2rem 0.375rem 0.75rem;">Total</span>
                        <span class="input-group-text" style="padding: 0.375rem 1.25rem 0.375rem 1.25rem;">$</span>
                        <input type="text" class="form-control"
                            aria-label="Dollar amount (with dot and two decimal places)" readonly id="total-value" disabled>
                    </div>
                    <div class="form-text" id="quote-card-addon-message"></div>
                </div>
                <p class="card-text"></p>
                <button class="btn btn-primary" id="cta-buy" disabled>CONFIRM BUY</button>
            </div>
        </div>
    </div>
`;
