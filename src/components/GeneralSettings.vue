<template>
    <SettingsColumn>
        <template slot="default">
            <div class="checkbox_container">
                <input
                    type="checkbox"
                    class="checkbox_input"
                    v-model="Settings.AutoCustom"
                    @change="sendNewSettings"
                />
                <p class="checkbox_title">Custom Autochoice</p>
            </div>
            <div class="checkbox_container">
                <input
                    type="checkbox"
                    class="checkbox_input"
                    v-model="Settings.ExtendedLobby"
                    @change="sendNewSettings"
                />
                <p class="checkbox_title">Extended Lobby</p>
            </div>
            <div class="checkbox_container">
                <input
                    type="checkbox"
                    class="checkbox_input"
                    v-model="Settings.Autoincrement"
                    @change="sendNewSettings"
                />
                <p class="checkbox_title">Autoincrement</p>
            </div>
            <hr />
            <div class="column_title">Balance</div>
            <div class="checkbox_container">
                <input
                    type="checkbox"
                    class="checkbox_input"
                    v-model="Settings.Network"
                    @change="sendNewSettings"
                />
                <p class="checkbox_title">Neuro Network</p>
            </div>
            <div class="balance_limit">
                <p class="checkbox_title">Balance Limit</p>
                <input
                    type="number"
                    class="custom_input"
                    v-model="Settings.BalanceLimit"
                    @change="sendNewSettings"
                />
            </div>
            <hr />
            <div class="column_title">Role amount settings</div>
            <div class="role_count_settings">
                <div class="role">
                    <img src="/img/T_icon.png" alt="" width="30" />
                    <input
                        type="number"
                        class="custom_input"
                        v-model="Settings.Amount.T"
                        @change="sendNewSettings"
                    />
                </div>
                <div class="role">
                    <img src="/img/D_icon.png" alt="" width="30" />
                    <input
                        type="number"
                        class="custom_input"
                        v-model="Settings.Amount.D"
                        @change="sendNewSettings"
                    />
                </div>
                <div class="role">
                    <img src="/img/H_icon.png" alt="" width="30" />
                    <input
                        type="number"
                        class="custom_input"
                        v-model="Settings.Amount.H"
                        @change="sendNewSettings"
                    />
                </div>
            </div>
            <hr />
            <div class="column_title">Team Names</div>
            <div class="team_name_settings">
                <div class="team">
                    <p class="title">Team 1:</p>
                    <input
                        type="text"
                        class="custom_input"
                        v-model="Settings.TeamNames['1']"
                        @change="sendNewSettings"
                    />
                </div>
                <div class="team">
                    <p class="title">Team 2:</p>
                    <input
                        type="text"
                        class="custom_input"
                        v-model="Settings.TeamNames['2']"
                        @change="sendNewSettings"
                    />
                </div>
            </div>
            <hr />
            <p class="column_title">Balance Design</p>
            <select name="theme" v-model="theme" class="custom_input">
                <option value="0">Design 1</option>
                <option value="1">Design 2</option>
            </select>
            <img class="balance_preview" :src="themeImgSrc" alt="" />
        </template>
    </SettingsColumn>
</template>

<script>
import SettingsColumn from "./SettingsColumn.vue";
import Vue from "vue";
import axios from "axios";
export default {
    components: {
        SettingsColumn,
    },
    data() {
        return {
            Settings: {},
            themeID: 0,
        };
    },
    async created() {
        this.getValuesFromServer();
        this.themeID = this.getTheme();
    },
    methods: {
        async getValuesFromServer() {
            this.Settings = (
                await axios.get("/api/profile/settings/getSettings")
            ).data;
        },
        async sendNewSettings() {
            let seti = this.Settings;
            seti.Amount.T = parseInt(seti.Amount.T)
            seti.Amount.D = parseInt(seti.Amount.D)
            seti.Amount.H = parseInt(seti.Amount.H)
            seti.BalanceLimit = parseInt(seti.BalanceLimit)
            await axios.post(
                "/api/profile/settings/setSettings",
                seti
            );
        },
        getTheme() {
            return localStorage.getItem("theme") != null
                ? parseInt(localStorage.getItem("theme"))
                : 0;
        },
    },
    computed: {
        theme: {
            set(v) {
                localStorage.setItem("theme", v);
                this.themeID = v;
            },
            get() {
                return this.themeID;
            },
        },
        themeImgSrc: {
            get() {
                return "/img/theme" + this.themeID + ".jpg";
            },
        },
    },
};
</script>

<style scoped>
@import "../assets/css/global.css";

.role {
    margin: auto;
    display: flex;
}
.role_count_settings {
    display: flex;
}
.checkbox_container {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
}
.checkbox_title {
    margin: 0;
    margin-left: 2px;
}
.column_title {
    margin-bottom: 12px;
}
.team,
.balance_limit {
    display: flex;
    align-items: center;
    margin-bottom: 3px;
    height: max-content;
}
.team > .title,
.balance_limit > .title {
    min-width: max-content;
    margin: 0;
    margin-right: 6px;
}
.team > input,
.balance_limit > input {
    height: 30px;
    margin: 0;
}
.balance_preview {
    margin-top: 12px;
    width: 100%;
}
</style>