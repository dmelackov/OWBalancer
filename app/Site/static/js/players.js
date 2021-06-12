var searchField = document.getElementById("PlayersSearch")
var playersTable = document.getElementById("players_list")
var lobbyTable = document.getElementById("lobby_list")
var customSelect = document.getElementById("customSelect")
var body = document.getElementById("body")

body.addEventListener("click", (e) => {
    var element = document.elementFromPoint(e.clientX, e.clientY)
    if (element.id == "body") {
        if (lastActive) lastActive.classList.remove("active")
        customSelect.style.display = 'none'
    }
})

customSelect.style.display = 'none'

lobbyTable.addEventListener("click", (e) => {
    let target = e.target.closest("td");
    console.log(target.dataset.playerId)
})

playersTable.addEventListener("click", (e) => {
    let target = e.target.closest("nav");
    if (lastActive) lastActive.classList.remove("active")
    console.log(target.dataset.playerId)
    customSelect.style.display = 'block'
    var lineRect = target.getBoundingClientRect()
    var customerRect = customSelect.getBoundingClientRect()
    var totalHeight = lineRect.y;
    if (lineRect.y + customerRect.height > document.documentElement.clientHeight - 20) totalHeight -= lineRect.y + customerRect.height - document.documentElement.clientHeight + 20
    customSelect.style.top = totalHeight + "px"
    customSelect.style.left = lineRect.x + lineRect.width + 10 + "px"
    lastActive = target
    target.classList.add("active")
    console.log(lineRect)
})

searchField.addEventListener('input', updatePlayers)
updatePlayers()
updateLobby()

var lastActive = null;

async function updatePlayers() {
    const res = await fetch('/api/getPlayers/' + searchField.value)
    var data = await res.json()
    console.log(data)
    playersTable.innerHTML = "";
    var pattern = await fetch('static/html/player_pattern.html')
    var pattern_data = await pattern.text()
    data.forEach(element => {
        var tr = document.createElement("tr")
        tr.innerHTML = Mustache.render(pattern_data, { "id": element.id, "Username": element.Username })
        playersTable.appendChild(tr)
    });

}

async function updateLobby() {
    const res = await fetch('/api/getLobby')
    var data = await res.json()
    console.log(data)
    lobbyTable.innerHTML = "";
    var pattern = await fetch('static/html/lobby_pattern.html')
    var pattern_data = await pattern.text()
    data.forEach(element => {
        var tr = document.createElement("tr")
        tr.innerHTML = Mustache.render(pattern_data, { "id": element.id, "Username": element.Username })
        lobbyTable.appendChild(tr)
    });
}


async function deleteFromLobby(id) {
    console.log("Delete " + id)
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/deleteFromLobby', false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    var data = {}
    data.id = id
    xhr.send(JSON.stringify(data));
    updateLobby()
}