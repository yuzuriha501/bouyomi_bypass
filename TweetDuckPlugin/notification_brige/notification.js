run(){
  // executed every time a new notification is displayed
  const fullnameElement = window.document.getElementsByClassName("fullname");
  const userNameElement = window.document.getElementsByClassName("username");

  var fullName = "";
  var userName = "";
  if (fullnameElement.length > 0) {
    fullName = fullnameElement[0].textContent;
  }
  if (userNameElement.length > 0) {
    userName = userNameElement[0].textContent;
  }
  if (fullName === "TweetDuck" && userName === "@TryMyAwesomeApp") {
    return; // Sample Notification
  }

  const tweetTextElement = window.document.getElementsByClassName("tweet-text");
  var tweetText = "";
  if (tweetTextElement.length > 0) {
    tweetText = tweetTextElement[0].textContent;
  }
  if (tweetText.length == 0) {
    return;
  }

  const curTime = Date.now();
  const exportData = fullName + "\n" + userName + "\n" + tweetText;
  const extension = ".ducktxt";
  const exportPath = curTime + extension;

  $TDP.writeFile(this.$token, exportPath, exportData).then(() => {
    //$TD.alert("info", "File was written successfully!");
  }).catch(err => {
    console.error("Problem creating or writing file: " + err.message);
    //$TD.alert("error", "Problem creating or writing file: " + err.message);
  });
}
