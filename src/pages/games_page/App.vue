<template>
    <div id="app">
        <HeaderMenu />
        <div class="content">
            <p class="indev">В разработке :/</p>
        </div>
    </div>
</template>

<script>
import LobbyColumn from "../../components/LobbyColumn.vue";
import PlayerColumn from "../../components/PlayerColumn.vue";
import CustomSelectContainer from "../../components/CustomSelectContainer.vue";
import BalanceContainer from "../../components/BalanceContainer.vue";
import HeaderMenu from "../../components/HeaderMenu.vue";
import Vue from "vue";
import axios from "axios";

let perms = [];
axios
    .get("/api/profile/getPermissions")
    .then((response) => (perms = response.data));

let UserInfo = {};
axios.get("/api/profile/getCurrentUserInfo").then((response) => {
    UserInfo = response.data;
});




Vue.mixin({
    data() {
        return {
            UserInfo: UserInfo
        };
    },
    methods: {
        isPerm() {
            return perms;
        }
    },
});

Vue.prototype.eventBus = new Vue();

axios.get("/api/profile/auth/getCSRF").then((token) => {
    axios.defaults.headers.common["X-CSRF-TOKEN"] = token.data;
    new Vue().eventBus.$emit("updateBalanceImage");
});

document.body.addEventListener("mousedown", (e) => {
    if (!e.target.closest(".customSelect")) {
        new Vue().eventBus.$emit("closeCustomMenu");
    }
});

export default {
    components: {
        LobbyColumn,
        PlayerColumn,
        CustomSelectContainer,
        BalanceContainer,
        HeaderMenu,
    },
    data() {
        return { perms: [] };
    },
    methods: {}
};
</script>


<style scoped>
@import "../../assets/css/global.css";
.content {
    height: 92%;
    max-width: 100vw;
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    
}
.indev {
    width: 99vw;
    height: 100%;
    font-size: 8.1vw;
    text-align: center;
    margin: 0;
}
</style>