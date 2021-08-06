let app = null;
document.addEventListener("DOMContentLoaded", async() => {
    let res = await fetch("/static/html/main_page_content.html");
    document.getElementById("app_content").innerHTML = await res.text();

    document.body.addEventListener("mousedown", (e) => {
        if (!e.target.closest(".customSelect")) {
            //if (lastActive) lastActive.classList.remove("active")
            app.$refs.CustomMenu.customMenuVisible = false;
        }
        //if (!e.target.closest(".lobby_container ")) {
        //    if (currentLobbyElem) {
        //        currentLobbyElem.style.display = "none"
        //        currentLobbyElem = null
        //    }
        //}
    })

    Vue.component('player-container', {
        props: ["player", "index"],

        template: await (await fetch('static/html/player_pattern.html')).text(),

        methods: {
            openCustomsMenu() {
                app.$refs.CustomMenu.open(this);
            }
        }
    });

    Vue.component('lobby-player-container', {
        props: ["player"],
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
                this.target = target
                const res = await fetch('/api/getCustoms/' + target.player.id)
                const resData = await res.json()
                if (resData.type == 'custom') {
                    this.customMenuVisible = false
                    sendPOST('/api/addToLobby', { 'id': resData.data.CustomID })
                    app.updateLobby()
                    return;
                }
                if (resData.data) {
                    this.customList = resData.data
                } else {
                    this.customList = []
                }
                this.customMenuVisible = true
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
                app.$refs.CustomMenu.customMenuVisible = false;
                sendPOST('/api/addToLobby', { 'id': this.custom.id })
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
                lobbyPlayerList: []
            }
        },

        methods: {

            createPlayer() {
                sendPOST("/api/createPlayer", { "Username": this.createPlayerNickname });
                this.createPlayerNickname = "";
                this.updatePlayers();
            },

            createPlayerEnter(e) {
                if (e.code === "Enter") this.createPlayer();
            },

            updatePlayers() {
                fetch('/api/getPlayers/')
                    .then(response => response.json())
                    .then(data => (this.playerList = data));
            },

            updateLobby() {
                fetch('/api/getLobby')
                    .then(response => response.json())
                    .then(data => (this.lobbyPlayerList = data));
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
        }
    });

    function sendPOST(url, params) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, false);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.send(JSON.stringify(params));
    }

})