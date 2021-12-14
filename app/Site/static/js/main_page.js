let app = {};
document.addEventListener("DOMContentLoaded", async () => {
    let res = (await axios.get("/static/html/main_page_content.html")).data;
    document.getElementById("app_content").innerHTML = res;

    document.body.addEventListener("mousedown", (e) => {
        if (!e.target.closest(".customSelect")) {
            app.$refs.CustomMenu.close();
        }
        if (!e.target.closest(".lobby_container")) {
            if (app.activeLobbyMenu) {
                app.activeLobbyMenu.close();
            }
        }
    })
    Vue.component("sr-input", {
        template: '<input type="number" v-model="sr" class="lobby_sr_input" onFocus="this.select()" @keydown.enter="this.blur()"></input>',
        props: ["CustomID", "role"],
        methods: {
            ratingSet(value) {
                sendPOST("/api/customs/changeRoleSr", { "role": this.role.role, "rating": value, "customId": this.CustomID })
                app.updateLobby()
            },
            isPerm(perm) {
                return app.isPerm(perm)
            }
        },
        computed: {
            sr: {
                get() { return this.role.sr },
                set(v) {
                    if (v > 5000) {
                        this.role.sr = 5000;
                    } else if (v < 0) {
                        this.role.sr = 0;
                    } else {
                        this.role.sr = v;
                    }

                    this.ratingSet(this.role.sr)
                }
            }
        },
    });

    Vue.component('player-container', {
        props: ["player", "index"],
        data() {
            return {
                active: false
            }
        },
        template: (await axios.get('static/html/player_pattern.html')).data,

        methods: {
            openCustomsMenu() {
                if (!this.isPerm("add_customs_tolobby")) return;
                this.active = true;
                app.$refs.CustomMenu.open(this);
            },
            isPerm(perm) {
                return app.isPerm(perm)
            }
        }
    });

    Vue.component('lobby-player-container', {
        props: ["player", "opened"],
        data() {
            return {
                menuOpened: false,
                active: false
            }
        },
        methods: {
            open(event) {
                if (app.activeLobbyMenu == this) { this.close(); return; }
                if (app.activeLobbyMenu) {
                    app.activeLobbyMenu.close();
                }
                if (event.target.classList.contains("X")) return;
                app.activeLobbyMenu = this;
                this.menuOpened = true;
                app.activeLobbyId = this.player.CustomID;
            },
            close() {
                this.menuOpened = false;
                app.activeLobbyMenu = null;
                app.activeLobbyId = null;
            },
            async deleteFromLobby() {
                await sendPOST("/api/lobby/deleteFromLobby", { 'id': this.player.CustomID })
                app.updateLobby();
            },
            async toggleRole(ARGrole) {
                let newRoleStr = "";
                for (roleIndex in this.player.RolesPriority) {
                    let role = this.player.RolesPriority[roleIndex]
                    let tempActive = role.active;
                    if (role.role == ARGrole) tempActive = !tempActive;
                    if (tempActive) newRoleStr += role.role;
                }
                await sendPOST("/api/players/setRoles", { "id": this.player.CustomID, "roles": newRoleStr })
                app.updateLobby()
            },
            async swapRoles(index) {
                let newRoleStr = "";
                for (roleIndex in this.player.RolesPriority) {
                    let role = this.player.RolesPriority[roleIndex]
                    if (role.active) newRoleStr += role.role;
                }
                let tempMass = newRoleStr.split("");
                let tempChar = tempMass[index]
                tempMass[index] = tempMass[index + 1]
                tempMass[index + 1] = tempChar
                await sendPOST("/api/players/setRoles", { "id": this.player.CustomID, "roles": tempMass.join("") })
                app.updateLobby()
            },
            async toggleFlex() {
                await sendPOST("/api/players/setFlex", { "id": this.player.CustomID, "status": !this.player.isFlex })
                app.updateLobby();
            },
            isPerm(perm) {
                return app.isPerm(perm)
            }
        },
        created() {
            this.menuOpened = this.opened;
        },
        computed: {
            styleObj: function () {
                return {
                    display: this.menuOpened ? "block" : "none"
                }
            }
        },
        template:  (await axios.get('static/html/lobby_pattern.html')).data
    });

    Vue.component('custom-select-container', {
        data() {
            return {
                customList: [],
                target: null,
                customMenuVisible: false
            }
        },
        methods: {
            async open(target) {
                this.target = target;
                const res = await axios.get('/api/customs/getCustoms/' + target.player.id);
                const resData = res.data;
                if (resData.type == 'custom') {
                    this.close();
                    await sendPOST('/api/lobby/addToLobby', { 'id': resData.data.CustomID });
                    app.updateLobby();
                    return;
                }
                if (resData.data) {
                    this.customList = resData.data;
                } else {
                    this.customList = [];
                }
                this.customMenuVisible = true;
            },

            close() {
                if (this.target) this.target.active = false;
                this.customMenuVisible = false;
            },

            async createCustom() {
                await sendPOST("/api/customs/createCustom", { "id": this.target.player.id });
                this.close();
                app.updateLobby();
            },
            isPerm(perm) {
                return app.isPerm(perm)
            }
        },
        computed: {
            styleObj: function () {
                if (!this.customMenuVisible) return { "display": "none" }
                let lineRect = this.target.$el.getBoundingClientRect();
                let customerRect = this.$el.getBoundingClientRect();
                let totalHeight = lineRect.y;
                if (lineRect.y + 200 > document.documentElement.clientHeight - 20) {
                    totalHeight -= lineRect.y + 200 - document.documentElement.clientHeight + 20;
                }
                return {
                    top: totalHeight + 'px',
                    left: (lineRect.x + lineRect.width + 10) + 'px',
                    display: "block"
                }
            }
        },
        template:  (await axios.get('static/html/custom_select_pattern.html')).data
    });

    Vue.component("custom-pattern", {
        props: ["custom"],
        methods: {
            async addToLobby() {
                app.$refs.CustomMenu.close();
                await sendPOST('/api/lobby/addToLobby', { 'id': this.custom.CustomID })
                app.updateLobby();
            },
            isPerm(perm) {
                return app.isPerm(perm)
            }
        },
        template:  (await axios.get('static/html/custom_pattern.html')).data
    });

    app.isPerm = (perm) => { }
    app = new Vue({
        el: "#app_content",

        data() {
            return {
                createPlayerNickname: "",
                playersNicknameFilter: "",
                playerList: [],
                lobbyPlayerList: [],
                activeLobbyMenu: null,
                activeLobbyId: null,
                imageSrc: "/static/img/balance_alt.png",
                balanceLenght: 0,
                currentImageIndex: 0,
                perms: []
            }
        },

        methods: {

            async createPlayer() {
                await sendPOST("/api/players/createPlayer", { "Username": this.createPlayerNickname });
                this.createPlayerNickname = "";
                this.updatePlayers();
            },

            createPlayerEnter(e) {
                if (e.code === "Enter") this.createPlayer();
            },

            updatePlayers() {
                axios.get('/api/players/getPlayers/')
                    .then(response => (this.playerList = response.data));
            },

            updateLobby() {
                axios.get('/api/lobby/getLobby')
                    .then(response => (this.lobbyPlayerList = response.data));
            },

            getPermissions() {
                axios.get('/api/profile/getPermissions')
                    .then(response => (this.perms = response.data));
            },

            async clearLobby() {
                await sendPOST("/api/lobby/clearLobby", {})
                this.updateLobby();
            },

            changeImageIndex(deff) {
                let index = parseInt(localStorage.getItem("balance_index"))
                let newIndex = index + deff
                if (newIndex < 0) return;
                if (newIndex >= this.balanceLenght) return;
                localStorage.setItem("balance_index", newIndex)
                this.setCurrentImageIndex();
                this.updateImage();
            },

            async getBalances() {
                this.imageSrc = "/static/img/balance_load.png"
                let res = await axios.get('/api/profile/getBalances');
                let balance = res.data;
                if (balance["ok"] && balance.Balances.length > 0) {
                    localStorage.setItem("balance", JSON.stringify(balance))
                    localStorage.setItem("balance_index", 0)
                    this.updateImage()
                } else {
                    this.imageSrc = "/static/img/balance_404.png"
                    if (localStorage.getItem("balance")) localStorage.removeItem("balance")
                    if (localStorage.getItem("balance_index")) localStorage.removeItem("balance_index")
                }
                this.setCurrentImageIndex()
                this.setBalanceLenght()
            },

            setCurrentImageIndex() {
                let index = localStorage.getItem("balance_index")
                if (index) {
                    this.currentImageIndex = parseInt(index) + 1
                } else {
                    this.currentImageIndex = 0
                }
            },

            setBalanceLenght() {
                let balances = localStorage.getItem("balance")
                if (balances) {
                    this.balanceLenght = JSON.parse(balances).Balances.length
                } else {
                    this.balanceLenght = 0
                }
            },

            async updateImage() {
                let index = parseInt(localStorage.getItem("balance_index"))
                let balances = JSON.parse(localStorage.getItem("balance"))
                if (!balances) return;
                current_balance = balances["Balances"][index]
                let image = await axios.post('/api/profile/balanceImage', { "playersData": current_balance, "theme": localStorage.getItem("theme") != null ? parseInt(localStorage.getItem("theme")) : 0 }, { responseType: 'blob' })
                imageBlob = image.data
                let urlCreator = window.URL || window.webkitURL;
                let imageUrl = urlCreator.createObjectURL(imageBlob);
                this.imageSrc = imageUrl
            },

            isPerm(perm) {
                return this.perms.includes(perm)
            }
        },

        computed: {
            filteredPlayerList() {
                let player = this.playersNicknameFilter.toLowerCase();
                let players = this.playerList;
                let filteredPlayers = players.filter(function (elem) {
                    if (player === '') return true;
                    else return elem.Username.toLowerCase().indexOf(player) > -1;
                })
                return filteredPlayers;
            },

            lobbyPlayerCount() {
                return this.lobbyPlayerList.length
            }
        },

        async created() {
            this.updatePlayers();
            this.updateLobby();
            this.setCurrentImageIndex();
            this.setBalanceLenght();
            this.updateImage();
            this.getPermissions();
        }
    });

    async function sendPOST(url, params) {
        await axios.post(url, params)
    }
})