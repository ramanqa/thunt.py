var captcha = function(){
    canvasContext = document.getElementById("notABotCanvas").getContext('2d');
    captchaImage = document.getElementById("notABotCaptchaImg");
    canvasContext.font = "30px courier";
    canvasContext.filter = 'blur(2px) invert()';
    canvasContext.strokeText("{{word[0]}}", 5, 30);
    canvasContext.strokeText("{{word[1]}}", 25, 40);
    canvasContext.strokeText("{{word[2]}}", 45, 30);
    canvasContext.strokeText("{{word[3]}}", 65, 30);
    canvasContext.strokeText("{{word[4]}}", 75, 45);
    captchaImage.src = canvasContext.canvas.toDataURL();
}

$(document).ready(function(){
    console.log('captcha ready();');
    captcha();
});

document.getElementById("notABotCaptchaSubmit").onclick= function() {
    document.getElementById("notABotCaptchaWord").value="{{word[::-1]}}"
    document.getElementById("notABotForm").submit();
}

