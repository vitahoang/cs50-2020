window.addEventListener('load', async function() {
  try {
    updateAccountBalance();
  } catch (error) {
    console.log(error);
  }
});

// eslint-disable-next-line require-jsdoc
async function updateAccountBalance() {
  const res = await fetch('/profile');
  const user = await res.json();
  sessionStorage.setItem('account_balance', user['account_balance']);
  const html = document.getElementById('account-balance');
  html.innerHTML = ['Balance: $', user['account_balance']].join('');
}
