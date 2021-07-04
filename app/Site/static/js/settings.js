(() => {
    const searchField = document.getElementById("PlayersSearch")
    const playersTable = document.getElementById("players_list")



    searchField.addEventListener('input', updatePlayers)

    updatePlayers()
    async function updatePlayers() {
        const res = await fetch('/api/getPlayers/' + searchField.value)
        var data = await res.json()
        playersTable.innerHTML = "";
        var pattern = await fetch('static/html/player_pattern.html')
        var pattern_data = await pattern.text()
        playersTable.innerHTML = Mustache.render(pattern_data, { 'data': data })
    }

})()