document.forms.login_form.onsubmit = async (e) => {
    e.preventDefault()

    var bodyFormData = new FormData();
    bodyFormData.set("login", document.forms.login_form.login.value)
    bodyFormData.set("password", document.forms.login_form.password.value)
    bodyFormData.set("csrf_token", document.forms.login_form.csrf_token.value)

    let res = await axios.post("api/profile/auth/login", bodyFormData, {"Content-Type": "multipart/form-data"})
    console.log(res)
    if(res.status == 200) {
        window.location.href = "/"
    }
}