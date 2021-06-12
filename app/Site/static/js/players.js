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
    if (!target) return;
    console.log(target.dataset.playerId)
})

playersTable.addEventListener("click", async(e) => {
    let target = e.target.closest("nav");
    if (!target) return;
    const res = await fetch('/api/getCustoms/' + target.dataset.playerId)
    var data = await res.json()
    if (data.type == 'custom') {
        sendPOST('/api/addToLobby', { 'id': data.data.CustomID })
        updateLobby()
        return;
    }
    if (data.type == "none") {
        var none_custom_select = await (await fetch('static/html/custom_select_none_pattern.html')).text()
        openCustomMenu(target, Mustache.render(none_custom_select, data))
        return
    }
    var custom_select = await (await fetch('static/html/custom_select_pattern.html')).text()
    openCustomMenu(target, Mustache.render(custom_select, data))
    var CustomTableSelect = document.getElementById("CustomTableSelect")
    CustomTableSelect.onclick = function(e) {
        var target = e.target.closest("td")
        if (lastActive) lastActive.classList.remove("active")
        customSelect.style.display = 'none'
        sendPOST('/api/addToLobby', { 'id': target.dataset.playerId })
        updateLobby()
    }

})

searchField.addEventListener('input', updatePlayers)
updatePlayers()
updateLobby()

var lastActive = null;

async function updatePlayers() {
    const res = await fetch('/api/getPlayers/' + searchField.value)
    var data = await res.json()
    playersTable.innerHTML = "";
    var pattern = await fetch('static/html/player_pattern.html')
    var pattern_data = await pattern.text()
    data.forEach(element => {
        var tr = document.createElement("tr")
        tr.innerHTML = Mustache.render(pattern_data, element)
        playersTable.appendChild(tr)
    });

}

async function updateLobby() {
    const res = await fetch('/api/getLobby')
    var data = await res.json()
    lobbyTable.innerHTML = "";
    var pattern = await fetch('static/html/lobby_pattern.html')
    var pattern_data = await pattern.text()
    data.forEach(element => {
        var tr = document.createElement("tr")
        tr.innerHTML = Mustache.render(pattern_data, element)
        lobbyTable.appendChild(tr)
    });
}


async function deleteFromLobby(id) {
    console.log("Delete " + id)
    sendPOST('/api/deleteFromLobby', { 'id': id })
    updateLobby()
}

function sendPOST(url, params) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(params))
}

function openCustomMenu(target, content) {
    if (lastActive) lastActive.classList.remove("active")
    customSelect.innerHTML = content
    customSelect.style.display = 'block'
    var lineRect = target.getBoundingClientRect()
    var customerRect = customSelect.getBoundingClientRect()
    var totalHeight = lineRect.y;
    if (lineRect.y + customerRect.height > document.documentElement.clientHeight - 20) totalHeight -= lineRect.y + customerRect.height - document.documentElement.clientHeight + 20
    customSelect.style.top = totalHeight + "px"
    customSelect.style.left = lineRect.x + lineRect.width + 10 + "px"
    lastActive = target
    target.classList.add("active")
}