let app = null;
document.addEventListener("DOMContentLoaded", async () => {
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
                Team2NameSet: "",
                themeID: 0
            }
        },

        computed: {
            ExtendedLobby: {
                async set(v) {
                    await sendPOST("/api/profile/settings/setExtendedLobby", { "setting": v })
                    this.updateSettings()
                },
                get() {
                    return this.ExtendedLobbySet;
                }
            },
            CustomAutoChoice: {
                async set(v) {
                    await sendPOST("/api/profile/settings/setAutoCustom", { "setting": v })
                    this.updateSettings()
                },
                get() {
                    return this.CustomAutoChoiceSet;
                }
            },
            TeamTCount: {
                async set(v) {
                    if (parseInt(v) < 0) return
                    await sendPOST("/api/profile/settings/setTanksCount", { "setting": parseInt(v) })
                    this.updateSettings()
                },
                get() {
                    return this.TeamTCountSet;
                }
            },
            TeamDCount: {
                async set(v) {
                    if (parseInt(v) < 0) return
                    await sendPOST("/api/profile/settings/setDamageCount", { "setting": parseInt(v) })
                    this.updateSettings()
                },
                get() {
                    return this.TeamDCountSet;
                }
            },
            TeamHCount: {
                async set(v) {
                    if (parseInt(v) < 0) return
                    await sendPOST("/api/profile/settings/setHealsCount", { "setting": parseInt(v) })
                    this.updateSettings()
                },
                get() {
                    return this.TeamHCountSet;
                }
            },
            Team1Name: {
                async set(v) {
                    await sendPOST("/api/profile/settings/setTeamName1", { "setting": v })
                    this.updateSettings()
                },
                get() {
                    return this.Team1NameSet;
                }
            },
            Team2Name: {
                async set(v) {
                    await sendPOST("/api/profile/settings/setTeamName2", { "setting": v })
                    this.updateSettings()
                },
                get() {
                    return this.Team2NameSet;
                }
            },
            theme: {
                set(v) {
                    localStorage.setItem("theme", v)
                    this.themeID = v
                },
                get() {
                    return this.themeID
                }
            },
            themeImgSrc: {
                get() {
                    return '/static/img/theme' + this.themeID + '.jpg'
                }
            }
        },
        methods: {
            updateSettings() {
                axios.get('/api/profile/settings/getSettings')
                    .then(response => {
                        let data = response.data
                        this.ExtendedLobbySet = data.ExtendedLobby
                        this.CustomAutoChoiceSet = data.AutoCustom
                        this.TeamTCountSet = data.Amount.T
                        this.TeamDCountSet = data.Amount.D
                        this.TeamHCountSet = data.Amount.H
                        this.Team1NameSet = data.TeamNames["1"]
                        this.Team2NameSet = data.TeamNames["2"]
                    });
            },
            getTheme() {
                return localStorage.getItem("theme") != null ? parseInt(localStorage.getItem("theme")) : 0
            }

        },
        async created() {
            this.updateSettings()
            this.themeID = this.getTheme()
        }
    });

    async function sendPOST(url, params) {
        await axios.post(url, params)
    }
});