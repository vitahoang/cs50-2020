window.addEventListener("load", async function(){
  try {
    let res = await fetch("/profile")
    let user = await res.json();
    let html = document.getElementById("account-balance")
    html.innerHTML = ["Balance: $", user["account_balance"]].join("");
    sessionStorage.setItem("account_balance", user["account_balance"])
  } catch (error) {
    console.log(error)
  }
});