var searchField = document.getElementById("PlayersSearch")
var playersTable = document.getElementById("players_list")
searchField.addEventListener('input', updatePlayers)
updatePlayers()

function updatePlayers() {
    fetch('/api/getPlayers/' + searchField.value)
        .then(async(res) => {
            var data = await res.json()
            console.log(data)
            playersTable.innerHTML = "";
            var pattern = await fetch('static/html/player_pattern.html')
            var pattern_data = await pattern.text()
            data.forEach(async element => {
                var tr = document.createElement("tr")
                var local_pattern_data = pattern_data.replace("$id", element.id).replace("$Username", element.Username)
                tr.innerHTML = local_pattern_data
                playersTable.appendChild(tr)
            });
        })
}

function addToLobby(id) {
    console.log("Add " + id)
}