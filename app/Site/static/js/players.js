(() => {
    const searchField = document.getElementById("PlayersSearch")
    const playersTable = document.getElementById("players_list")
    const lobbyTable = document.getElementById("lobby_list")
    const customSelect = document.getElementById("customSelect")
    const body = document.getElementById("body")
    const lobby_count = document.getElementById("lobby_count")

    body.addEventListener("click", (e) => {
        var element = document.elementFromPoint(e.clientX, e.clientY)
        if (element.id == "body") {
            if (lastActive) lastActive.classList.remove("active")
            customSelect.style.display = 'none'
        }
    })

    customSelect.style.display = 'none'


    let currentElem = null;
    let currentLobbyElem = null;

    lobbyTable.addEventListener("mouseover", (e) => { //mouseout
        var target = e.target.closest("td")
        if (!target) return;
        if (!lobbyTable.contains(target)) return;
        let relatedTarget = e.relatedTarget;
        while (relatedTarget) {
            if (relatedTarget == currentElem) return;
            relatedTarget = relatedTarget.parentNode;
        }
        currentElem = target;
        target.getElementsByClassName("sr_lobby")[0].style.display = "none"
        target.getElementsByClassName("author-right")[0].style.display = "none"
        target.getElementsByClassName("X")[0].style.display = "flex"
    })

    lobbyTable.addEventListener("mouseout", (e) => { //mouseover
        var target = e.target.closest("td")
        if (!target) return;
        let relatedTarget = e.relatedTarget;
        while (relatedTarget) {
            if (relatedTarget == currentElem) return;
            relatedTarget = relatedTarget.parentNode;
        }
        target.getElementsByClassName("X")[0].style.display = "none"
        target.getElementsByClassName("sr_lobby")[0].style.display = "block"
        target.getElementsByClassName("author-right")[0].style.display = "block"
    })

    lobbyTable.addEventListener("click", (e) => {
        let target = e.target.closest("p");
        if (target && target.classList.contains("X")) {
            target = target.closest("td")
            sendPOST("/api/deleteFromLobby", { 'id': target.dataset.playerId })
            updateLobby()
            return
        }
        target = e.target.closest("td")
        if (!target) return;
        if (!e.target.closest(".player_inner_container")) return;
        let menu = target.getElementsByClassName("lobby_menu")[0]
        if (currentLobbyElem && currentLobbyElem != menu) currentLobbyElem.style.display = "none"
        console.log(menu.style.display)
        if (menu.style.display == "block") {
            menu.style.display = "none"
        } else {
            menu.style.display = "block"
        }
        currentLobbyElem = menu
    })

    lobbyTable.addEventListener("click", (e) => {
        let target = e.target.closest("img");
        if (!target) return;
        var roles = target.closest(".lobby_sr").children
        rolesStr = ""
        for (let i = 0; i < roles.length; i++) {
            element = roles[i];
            if (!element.getElementsByTagName("img")[0].classList.contains("innactive")) rolesStr += element.dataset.roleId
        }
        roleTarget = target.closest("div")
        if (rolesStr.includes(roleTarget.dataset.roleId)) {
            rolesStr = rolesStr.replace(roleTarget.dataset.roleId, "")
        } else {
            rolesStr += roleTarget.dataset.roleId
        }

        console.log({ "id": target.closest("td").dataset.playerId, "roles": rolesStr })
        sendPOST("/api/setRoles", { "id": target.closest("td").dataset.playerId, "roles": rolesStr })
        updateLobby()
    })

    playersTable.addEventListener("click", async(e) => {
        let target = e.target.closest("nav");
        if (!target) return;
        const res = await fetch('/api/getCustoms/' + target.dataset.playerId)
        var data = await res.json()
        if (data.type == 'custom') {
            if (lastActive) lastActive.classList.remove("active")
            customSelect.style.display = 'none'
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
        playersTable.innerHTML = Mustache.render(pattern_data, { 'data': data })
    }

    async function updateLobby() {
        let openID = null;
        if (currentLobbyElem) {
            openID = currentLobbyElem.closest("td").dataset.playerId
        }
        const res = await fetch('/api/getLobby')
        var data = await res.json()
        lobbyTable.innerHTML = "";
        var pattern = await fetch('static/html/lobby_pattern.html')
        var pattern_data = await pattern.text()
        lobbyTable.innerHTML = Mustache.render(pattern_data, { 'data': data })
        lobby_count.innerText = "Игроков в лобби: " + data.length
        if (openID != null) {
            var tbody = lobbyTable.getElementsByTagName("tbody")[0]
            for (let i = 0; i < tbody.children.length; i++) {
                element = tbody.children[i];
                var elem = element.getElementsByTagName("td")[0];
                if (elem.dataset.playerId == openID) {
                    let menu = element.getElementsByClassName("lobby_menu")[0]
                    menu.style.display = "block"
                    currentLobbyElem = menu
                }
            }
        }
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
})();