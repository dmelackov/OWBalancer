<template>
    <div
        :class="{
            player_container: true,
            my_custom_warn: isMyCustom,
        }"
        @click="addToLobby"
    >
        <div class="player_inner_container">
            <p class="player_username">{{ custom.Player.Username }}</p>
            <div class="sr">
                <div class="sr_icon">
                    <img
                        src="../../public/img/T_icon.png"
                        alt=""
                        width="12"
                        :class="{
                            innactive: !roles.T,
                            role_icon: true,
                        }"
                    />
                    <img
                        src="../../public/img/D_icon.png"
                        alt=""
                        width="12"
                        :class="{
                            innactive: !roles.D,
                            role_icon: true,
                        }"
                    />
                    <img
                        src="../../public/img/H_icon.png"
                        alt=""
                        width="12"
                        :class="{
                            innactive: !roles.H,
                            role_icon: true,
                        }"
                    />
                </div>

                <div class="sr_numbers">
                    <p>{{ SR.T }}</p>
                    <p>{{ SR.D }}</p>
                    <p>{{ SR.H }}</p>
                </div>
            </div>
            <p class="author-left">by {{ custom.Creator.username }}</p>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    props: ["custom"],
    data() {
        return {
            roles: {},
            SR: {},
            isMyCustom: false,
        };
    },
    methods: {
        async addToLobby() {
            this.eventBus.$emit("closeCustomMenu");
            await axios.post("/api/lobby/addToLobby", {
                id: this.custom.ID,
            });
            this.eventBus.$emit("updateLobby");
        },
        getRolesInfo() {
            for (const key in this.custom.Roles) {
                const element = this.custom.Roles[key];
                this.roles[element.role] = element.active;
                this.SR[element.role] = element.sr;
            }
            return false;
        },
    },
    created() {
        this.getRolesInfo();
        if (this.custom.Creator.ID == this.UserInfo.ID) this.isMyCustom = true;
    },
};
</script>

<style scoped>
@import "../assets/css/global.css";
@import "../assets/css/playerContainer.css";

.my_custom_warn {
    box-shadow: 0 1px 0 #1abe5fa8;
}

.sr {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.sr_icon {
    margin-left: 2px;
    padding-top: 7px;
}

.role_icon {
    display: block;
    margin-bottom: 1px;
    cursor: pointer;
}

.sr_numbers {
    display: inline-block;
    line-height: 1px;
    font-size: 12px;
}

.author-left {
    position: absolute;
    color: #3b4b5f;
    bottom: 4px;
    left: 12px;
    width: max-content;
    margin: 0;
    font-size: 12px;
}

.innactive {
    filter: brightness(0.3);
}
</style>