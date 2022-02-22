<template>
    <div class="header">
        <nav class="menu">
            <div class="menu-left">
                <a href="/">Games</a>
                <a href="/balancer">Balancer</a>
                <a href="/settings">Settings</a>
            </div>
            <div class="menu-right">
                <a href="/api/profile/auth/logout" data-tooltip="Quit" v-if="Username != null">{{
                    Username
                }}</a>
                <a href="/login" v-if="Username == null">Authorization</a>
            </div>
        </nav>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            Username: "",
        };
    },
    methods: {
        async getUserData() {
            let info = await axios.get("/api/profile/getCurrentUserInfo");
            let infoContent = info.data;
            this.Username = infoContent.Username;
        },
    },
    created() {
        this.getUserData();
    },
};
</script>

<style scoped>
@import "../assets/css/global.css";

.header {
    height: 32px;
    background-color: #161b22;
    padding: 16px 32px;
    display: flex;
}

.menu {
    display: flex;
    flex-direction: row;
    align-content: center;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}


[data-tooltip] {
    position: relative;
}

[data-tooltip]::after {
    content: attr(data-tooltip);
    position: absolute;
    width: max-content;
    left: 50%;
    transform: translate(-50%, 0);
    top: 0;
    background: #444444;
    color: #fff;
    padding: 0.5em;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    pointer-events: none;
    opacity: 0;
    transition: 0.5s;
    border-radius: 6px;
}

[data-tooltip]:hover::after {
    opacity: 0.3;
    top: 2em;
}
</style>