<template>
    <div
        :class="{
            error: player.warn,
            lobby_container: true,
            player_container: true,
        }"
    >
        <div
            class="player_inner_container"
            @click="open($event)"
            @mouseenter="active = true"
            @mouseleave="active = false"
        >
            <p class="player_username">{{ player.Player.Username }}</p>
            <div class="sr_lobby" v-if="!active">
                <div class="sr_lobby_icon" v-if="!player.isFlex">
                    <img
                        :src="'/img/' + role.role + '_icon.png'"
                        alt=""
                        width="15"
                        :class="{ role_icon: true, innactive: !role.active }"
                        v-for="(role, index) in player.Roles"
                        :key="index"
                    />
                </div>
                <img
                    src="/img/flex.svg"
                    alt=""
                    v-if="player.isFlex"
                    width="16"
                />
            </div>
            <p class="author-right">{{ player.Creator.username }}</p>
            <p class="X" v-if="active" @click="deleteFromLobby">✖</p>
        </div>
        <div class="lobby_menu" :style="styleObj">
            <hr />
            <div class="sr lobby_sr">
                <template v-for="(role, index) in player.Roles">
                    <RoleComponent :role="role" :custom="player" :key="index" />
                    <p
                        :key="index + player.ID * 10000"
                        :class="{
                            switch_button: true,
                            opacity_disable: !isPerm('change_player_roles'),
                        }"
                        v-if="index != 2 && !player.isFlex"
                        @click="swapRoles(index)"
                    >
                        ⇆
                    </p>
                </template>
                <img
                    src="/img/flex.svg"
                    alt=""
                    width="30"
                    :class="{
                        role_icon: true,
                        innactive: !player.isFlex,
                    }"
                    @click="toggleFlex"
                />
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import RoleComponent from "./RoleComponent.vue";

export default {
    props: ["player"],
    components: {
        RoleComponent,
    },
    data() {
        return {
            menuOpened: false,
            active: false,
        };
    },
    created(){
        this.eventBus.$on("lobbyCustomMenuOpen", (e) => {
            if(e != this) this.close()
        })
    },
    methods: {
        open(event) {
            if (event.target.classList.contains("X")) return;
            if (this.menuOpened) {this.close(); return}
            this.menuOpened = true;
            this.eventBus.$emit("lobbyCustomMenuOpen", this)
        },
        close() {
            this.menuOpened = false;
        },
        async deleteFromLobby() {
            await sendPOST("/api/lobby/deleteFromLobby", {
                id: this.player.ID,
            });
            this.eventBus.$emit("updateLobby");
        },
        async swapRoles(index) {
            if(this.player.isFlex) return;
            let newRoleStr = "";
            let roleIndex;
            for (roleIndex in this.player.Roles) {
                let role = this.player.Roles[roleIndex];
                if (role.active) newRoleStr += role.role;
            }
            let tempMass = newRoleStr.split("");
            let tempChar = tempMass[index];
            tempMass[index] = tempMass[index + 1];
            tempMass[index + 1] = tempChar;
            await sendPOST("/api/players/setRoles", {
                id: this.player.ID,
                roles: tempMass.join(""),
            });
            this.eventBus.$emit("updateLobby");
        },
        async toggleFlex() {
            await sendPOST("/api/players/setFlex", {
                id: this.player.ID,
                status: !this.player.isFlex,
            });
            this.eventBus.$emit("updateLobby");
        },
    },
    computed: {
        styleObj: function () {
            return {
                display: this.menuOpened ? "block" : "none",
            };
        },
    },
};
async function sendPOST(url, params) {
    await axios.post(url, params);
}
</script>

<style scoped>
@import "../assets/css/global.css";
@import "../assets/css/playerContainer.css";

.error {
    box-shadow: 0 1px 0 #c72727a8;
}
.sr_lobby_icon {
    display: flex;
}

.role_icon {
    margin-left: 4px;
    cursor: pointer;
}

.lobby_sr {
    padding: 0 20px 0 20px;
}

.role {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-content: center;
    align-items: center;
}

.role > p {
    text-align: center;
    margin: 0;
}

.innactive {
    filter: brightness(0.3);
}

.X {
    margin-left: auto;
    justify-content: flex-end;
    margin: 0;
    flex-wrap: wrap;
    align-content: center;
    padding: 5px;
}

.author-right {
    position: absolute;
    color: #3b4b5f;
    bottom: 2px;
    right: 12px;
    width: max-content;
    margin: 0;
    font-size: 12px;
}

.sr {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.switch_button {
    font-size: 30px;
    margin: 0;
    cursor: pointer;
}

.lobby_sr_input {
    width: 35px;
    background-color: #171e27;
    color: white;
    border: none;
    text-align: center;
    font-size: 16px;
    -moz-appearance: textfield;
    appearance: none;
}
.role_with_swap {
    display: flex;
}
</style>