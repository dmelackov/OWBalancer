<template>
    <div class="role">
        <img
            :src="'/img/' + role.role + '_icon.png'"
            alt=""
            width="30"
            :class="{
                role_icon: true,
                innactive: !role.active,
            }"
            @click="toggleRole(role.role)"
        />
        <input
            type="number"
            v-model="role.sr"
            v-if="custom.editable"
            class="lobby_sr_input"
            @focus="$event.target.select()"
            @keydown.enter="$event.target.blur()"
            @change="setSR()"
        />
        <p v-if="!custom.editable">{{ role.sr }}</p>
    </div>
</template>

<script>
import axios from "axios";

export default {
    props: ["role", "custom"],
    data() {
        return {
        };
    },
    methods: {
        async toggleRole(ARGrole) {
            if (this.custom.isFlex) return;
            let newRoleStr = "";
            let roleIndex;
            for (roleIndex in this.custom.Roles) {
                let role = this.custom.Roles[roleIndex];
                let tempActive = role.active;
                if (role.role == ARGrole) tempActive = !tempActive;
                if (tempActive) newRoleStr += role.role;
            }
            await axios.post("/api/players/setRoles", {
                id: this.custom.ID,
                roles: newRoleStr,
            });
            this.eventBus.$emit("updateLobby");
        },
        async setSR() {
            if (this.role.sr > 5000) {
                this.role.sr = 5000;
            } else if (this.role.sr < 0) {
                this.role.sr = 0;
            }
            await axios.post("/api/customs/changeRoleSr", { "role": this.role.role, "rating": this.role.sr, "customId": this.custom.ID })
            this.eventBus.$emit("updateLobby")
        },
    },
};
</script>

<style scoped>
@import "../assets/css/global.css";

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

.lobby_sr_input {
    width: 35px;
    background-color: #171e27;
    color: white;
    border: none;
    text-align: center;
    font-size: 16px;
    -moz-appearance: textfield;
}

.role_icon {
    display: block;
    margin-bottom: 1px;
    cursor: pointer;
}
</style>