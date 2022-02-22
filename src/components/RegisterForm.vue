<template>
    <div class="login_form">
        <div class="title">
            <p>Registration</p>
        </div>
        <div class="form" @submit.prevent="submit">
            <form action="" name="register_form">
                <p>
                    <input
                        class="field form-control custom_input"
                        id="login"
                        name="login"
                        placeholder="Login"
                        required=""
                        type="text"
                        v-model="form.login"
                    />
                </p>
                <p>
                    <input
                        class="field form-control custom_input"
                        id="password"
                        name="password"
                        placeholder="Password"
                        required=""
                        type="password"
                        v-model="form.password"
                    />
                </p>
                <p>
                    <input
                        class="field form-control custom_input"
                        id="password_again"
                        name="password_again"
                        placeholder="Password"
                        required=""
                        type="password"
                        v-model="form.repeat_password"
                    />
                </p>
                <p>
                    <input
                        class="btn btn-submit custom_input"
                        id="submit"
                        name="submit"
                        type="submit"
                        value="Enter"
                    />
                </p>
                <p class="form_error" v-if="form_error.length != 0">
                    {{ form_error }}
                </p>
            </form>
        </div>
    </div>
</template>


<script>
import axios from "axios";
export default {
    data() {
        return {
            csrf: "",
            form: {
                login: "",
                password: "",
                repeat_password: "",
            },
            form_error: "",
        };
    },
    created() {
        this.updateCSRF();
    },
    methods: {
        async updateCSRF() {
            this.csrf = (await axios.get("/api/profile/auth/getCSRF")).data;
        },
        async submit() {
            this.form_error = "";
            let bodyFormData = new FormData();
            bodyFormData.set("csrf_token", this.csrf);
            bodyFormData.set("login", this.form.login);
            bodyFormData.set("password", this.form.password);
            bodyFormData.set("password_again", this.form.repeat_password);
            let res = await axios.post(
                "/api/profile/auth/registration",
                bodyFormData,
                { headers: { "Content-Type": "multipart/form-data" } }
            );
            let ResData = res.data;
            if (ResData.status == 200) {
                window.location.href = "/login";
            } else {
                if (ResData.status == 400 && ResData.message) {
                    this.form_error = ResData.message;
                }
            }
        },
    },
};
</script>


<style scoped>
.login_form {
    width: max-content;
    height: max-content;
    border-radius: 6px;
    padding: 20px;
    background-color: #11161d;
    border: solid 1px #444444;
}

.login_form > .title > p {
    text-align: center;
    font-size: 25px;
}

#submit {
    margin-left: auto;
    margin-right: auto;
    display: block;
}

.error-message {
    font-size: 11px;
}

.error {
    border: solid 1px #a30000 !important;
}

input.error {
    border: solid 1px #da0000;
}

.form_error {
    color: #da0000;
    font-size: 12px;
}
</style>