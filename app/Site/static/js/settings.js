let app = null;
document.addEventListener("DOMContentLoaded", async() => {
    let res = await fetch("/static/html/settings_page_content.html");
    document.getElementById("app_content").innerHTML = await res.text();

    app = new Vue({
        el: "#app_content",
        data() {
            return {
                ExtendedLobbySet: false,
                CustomAutoChoiceSet: false,
                TeamTCountSet: 0,
                TeamDCountSet: 0,
                TeamHCountSet: 0,
                Team1NameSet: "",
                Team2NameSet: ""
            }
        },
        computed: {
            ExtendedLobby: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.ExtendedLobbySet;
                }
            },
            CustomAutoChoice: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.CustomAutoChoiceSet;
                }
            },
            TeamTCount: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.TeamTCountSet;
                }
            },
            TeamDCount: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.TeamDCountSet;
                }
            },
            TeamHCount: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.TeamHCountSet;
                }
            },
            Team1Name: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.Team1NameSet;
                }
            },
            Team2Name: {
                set(v) {
                    console.log(v)
                },
                get() {
                    return this.Team2NameSet;
                }
            },
        },
        methods: {
            updateSettings() {
                fetch('/api/getPlayers/')
                    .then(response => response.json())
                    .then(data => (this.playerList = data));
            }
        }
    });
});