// 获取URL参数的函数
function getUsernameFromURL() {
  // 获取当前URL
  var currentURL = window.location.href;

  // 查找最后一个问号的位置
  var lastQuestionMarkIndex = currentURL.lastIndexOf('?');

  // 如果URL中没有问号，返回“vistor”
  if (lastQuestionMarkIndex === -1) {
    return "vistor";
  }

  // 截取问号后面的部分作为用户名
  var username = currentURL.substring(lastQuestionMarkIndex + 1);

  // 如果返回值中包含#，截取#前面的部分作为新的返回值
  if (username.indexOf('#') !== -1) {
    username = username.substring(0, username.indexOf('#'));
  }

  // 返回用户名
  return username;
}

username = getUsernameFromURL();

// 获取具有ID“username”的元素
var usernameElement = document.getElementById('username');

// 将用户名显示在元素中
usernameElement.innerHTML = username;
