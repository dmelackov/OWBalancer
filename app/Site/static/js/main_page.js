let app = null;
document.addEventListener("DOMContentLoaded", async() => {
    let res = await fetch("/static/html/main_page_content.html");
    document.getElementById("app_content").innerHTML = await res.text();

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
        template: await (await fetch('static/html/player_pattern.html')).text(),

        methods: {
            openCustomsMenu() {
                this.active = true;
                app.$refs.CustomMenu.open(this);
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
            deleteFromLobby() {
                sendPOST("/api/lobby/deleteFromLobby", { 'id': this.player.CustomID })
                app.updateLobby();
            },
            toggleRole(ARGrole) {
                let newRoleStr = "";
                for (roleIndex in this.player.RolesPriority) {
                    let role = this.player.RolesPriority[roleIndex]
                    let tempActive = role.active;
                    if (role.role == ARGrole) tempActive = !tempActive;
                    if (tempActive) newRoleStr += role.role;
                }
                sendPOST("/api/players/setRoles", { "id": this.player.CustomID, "roles": newRoleStr })
                app.updateLobby()
            },
            swapRoles(index) {
                let newRoleStr = "";
                for (roleIndex in this.player.RolesPriority) {
                    let role = this.player.RolesPriority[roleIndex]
                    if (role.active) newRoleStr += role.role;
                }
                let tempMass = newRoleStr.split("");
                let tempChar = tempMass[index]
                tempMass[index] = tempMass[index + 1]
                tempMass[index + 1] = tempChar
                sendPOST("/api/players/setRoles", { "id": this.player.CustomID, "roles": tempMass.join("") })
                app.updateLobby()
            },
            toggleFlex() {
                sendPOST("/api/players/setFlex", { "id": this.player.CustomID, "status": !this.player.isFlex })
                app.updateLobby();
            }
        },
        created() {
            this.menuOpened = this.opened;
        },
        computed: {
            styleObj: function() {
                return {
                    display: this.menuOpened ? "block" : "none"
                }
            }
        },
        template: await (await fetch('static/html/lobby_pattern.html')).text()
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
                const res = await fetch('/api/customs/getCustoms/' + target.player.id);
                const resData = await res.json();
                if (resData.type == 'custom') {
                    this.close();
                    sendPOST('/api/lobby/addToLobby', { 'id': resData.data.CustomID });
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

            createCustom() {
                sendPOST("/api/customs/createCustom", { "id": this.target.player.id });
                this.close();
                app.updateLobby();
            }
        },
        computed: {
            styleObj: function() {
                if (!this.customMenuVisible) return { "display": "none" }
                let lineRect = this.target.$el.getBoundingClientRect();
                let customerRect = this.$el.getBoundingClientRect();
                let totalHeight = lineRect.y;
                if (lineRect.y + customerRect.height > document.documentElement.clientHeight - 20) {
                    totalHeight -= lineRect.y + customerRect.height - document.documentElement.clientHeight + 20;
                }
                return {
                    top: totalHeight + 'px',
                    left: (lineRect.x + lineRect.width + 10) + 'px',
                    display: "block"
                }
            }
        },
        template: await (await fetch('static/html/custom_select_pattern.html')).text()
    });

    Vue.component("custom-pattern", {
        props: ["custom"],
        methods: {
            addToLobby() {
                app.$refs.CustomMenu.close();
                sendPOST('/api/lobby/addToLobby', { 'id': this.custom.CustomID })
                app.updateLobby();
            }
        },
        template: await (await fetch('static/html/custom_pattern.html')).text()
    });

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

            createPlayer() {
                sendPOST("/api/players/createPlayer", { "Username": this.createPlayerNickname });
                this.createPlayerNickname = "";
                this.updatePlayers();
            },

            createPlayerEnter(e) {
                if (e.code === "Enter") this.createPlayer();
            },

            updatePlayers() {
                fetch('/api/players/getPlayers/')
                    .then(response => response.json())
                    .then(data => (this.playerList = data));
            },

            updateLobby() {
                fetch('/api/lobby/getLobby')
                    .then(response => response.json())
                    .then(data => (this.lobbyPlayerList = data));
            },

            getPermissions() {
                fetch('/api/profile/getPermissions')
                    .then(response => response.json())
                    .then(data => (this.perms = data));
            },

            clearLobby() {
                sendPOST("/api/lobby/clearLobby", {})
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
                let res = await fetch('/api/profile/getBalances');
                let balance = await res.json();
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
                let image = await (await fetch('/api/profile/balanceImage', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8'
                    },
                    body: JSON.stringify(current_balance)
                })).blob()
                imageBlob = image
                let urlCreator = window.URL || window.webkitURL;
                let imageUrl = urlCreator.createObjectURL(image);
                this.imageSrc = imageUrl
            }
        },

        computed: {
            filteredPlayerList() {
                let player = this.playersNicknameFilter.toLowerCase();
                let players = this.playerList;
                let filteredPlayers = players.filter(function(elem) {
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

    function sendPOST(url, params) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, false);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.send(JSON.stringify(params));
    }

})