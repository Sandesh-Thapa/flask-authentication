passwordInput = document.getElementById("password-register")
passwordStatus = document.getElementById("passwordStatus")

passwordInput.addEventListener("keyup", (e) => {
    password = e.target.value
    if (password.length > 0) {
        var strongRegex = new RegExp("^(?=.{14,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
        var mediumRegex = new RegExp("^(?=.{10,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
        
        if (strongRegex.test(password)) {
            passwordStatus.innerHTML = 'Password Strength: <span class="strong" style="color:green">Strong!</span>';
        } else if (mediumRegex.test(password)) {
            passwordStatus.innerHTML = 'Password Strength: <span class="strong" style="color:orange">Medium!</span>';
        } else {
            passwordStatus.innerHTML = 'Password Strength: <span class="strong" style="color:red">Weak!</span>';
        }
    }else {
        passwordStatus.innerHTML = ""
    }
})


// Weak – If the length is less than 10 characters and doesn’t contain a combination of symbols, caps, text.
// Medium – If the length is 10 characters or more and has a combination of symbols, caps, text.
// Strong – If the length is 14 characters or more and has a combination of symbols, caps, text.
