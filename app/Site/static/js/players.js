(() => {
    const searchField = document.getElementById("PlayersSearch")
    const playersTable = document.getElementById("players_list")
    const lobbyTable = document.getElementById("lobby_list")
    const customSelect = document.getElementById("customSelect")
    const body = document.getElementById("body")
    const lobby_count = document.getElementById("lobby_count")
    const balance_button = document.getElementById("balance_button")
    const balance_img = document.getElementById("balance_image")
    const balance_count = document.getElementById("balance_count")
    const balance_controlls_left = document.getElementById("balance_button_left")
    const balance_controlls_right = document.getElementById("balance_button_right")
        //const copy_button = document.getElementById("copy_button")
    const UserNickname = document.getElementById("UserNickname")
    const UserCreateButton = document.getElementById("UserCreateButton")
    const clear_button = document.getElementById("clear_button")

    body.addEventListener("mousedown", (e) => {
        if (!e.target.closest(".customSelect")) {
            if (lastActive) lastActive.classList.remove("active")
            customSelect.style.display = 'none'
        }
        if (!e.target.closest(".lobby_container ")) {
            if (currentLobbyElem) {
                currentLobbyElem.style.display = "none"
                currentLobbyElem = null
            }
        }
    })

    customSelect.style.display = 'none'
    if (localStorage.getItem("balance_index")) {
        updateimage()
    }

    let currentElem = null;
    let currentLobbyElem = null;
    let imageBlob = null;

    lobbyTable.addEventListener("mouseover", (e) => { //X
        var target = e.target.closest(".player_container")
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

    lobbyTable.addEventListener("mouseout", (e) => { //X
        var target = e.target.closest(".player_container")
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

    lobbyTable.addEventListener("click", (e) => { // Delete from lobby event or open menu
        let target = e.target.closest("p");
        if (target && target.classList.contains("X")) {
            target = target.closest(".player_container")
            sendPOST("/api/deleteFromLobby", { 'id': target.dataset.playerId })
            updateLobby()
            return
        }
        target = e.target.closest(".player_container")
        if (!target) return;
        if (!e.target.closest(".player_inner_container")) return;
        let menu = target.getElementsByClassName("lobby_menu")[0]
        if (currentLobbyElem && currentLobbyElem != menu) currentLobbyElem.style.display = "none"
        if (menu.style.display == "block") {
            menu.style.display = "none"
            currentLobbyElem = null
        } else {
            menu.style.display = "block"
            currentLobbyElem = menu
        }
    })

    lobbyTable.addEventListener("click", (e) => { // Role swap
        let target = e.target.closest("img");

        if (!target) return;
        if (!target.closest(".role")) return;
        if (!target.closest(".lobby_sr").getElementsByClassName("flex")[0].classList.contains("innactive")) return
        var roles = target.closest(".lobby_sr").children
        rolesStr = ""
        for (let i = 0; i < roles.length; i++) {
            element = roles[i];
            if (element.tagName == "P") continue;
            if (!element.getElementsByTagName("img")[0]) continue;
            if (!element.getElementsByTagName("img")[0].classList.contains("innactive")) rolesStr += element.dataset.roleId
        }
        roleTarget = target.closest("div")
        if (rolesStr.includes(roleTarget.dataset.roleId)) {
            rolesStr = rolesStr.replace(roleTarget.dataset.roleId, "")
        } else {
            rolesStr += roleTarget.dataset.roleId
        }

        sendPOST("/api/setRoles", { "id": target.closest(".player_container").dataset.playerId, "roles": rolesStr })
        updateLobby()
    })

    lobbyTable.addEventListener("click", (e) => { // Flex change
        let target = e.target.closest("img")
        if (!target) return;
        if (!target.classList.contains("flex")) return;
        sendPOST("/api/setFlex", { "id": target.closest(".player_container").dataset.playerId, "status": target.classList.contains("innactive") })
        updateLobby()
    })

    lobbyTable.addEventListener('click', (e) => { // Role activate/deactivate
        let target = e.target.closest("p");
        if (!target || !target.classList.contains("switch_button")) return;
        var roles = target.closest(".lobby_sr").children
        rolesStr = ""
        for (let i = 0; i < roles.length; i++) {
            element = roles[i];
            if (element.tagName == "P") continue;
            if (!element.getElementsByTagName("img")[0]) continue;
            if (!element.getElementsByTagName("img")[0].classList.contains("innactive")) rolesStr += element.dataset.roleId
        }
        if (target.dataset.buttonId == 0) {
            newRoles = rolesStr.charAt(1) + rolesStr.charAt(0) + rolesStr.charAt(2)
        } else {
            newRoles = rolesStr.charAt(0) + rolesStr.charAt(2) + rolesStr.charAt(1)
        }
        sendPOST("/api/setRoles", { "id": target.closest(".player_container").dataset.playerId, "roles": newRoles })
        updateLobby()
    })

    playersTable.addEventListener("click", async(e) => { // Add to lobby
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

    balance_button.addEventListener("click", async(e) => { // Balance
        var balance = await (await fetch('/api/getBalances')).json()
        if (balance["ok"]) {
            localStorage.setItem("balance", JSON.stringify(balance))
            localStorage.setItem("balance_index", 0)

            updateimage()
        } else {
            console.log("It's not ok")
        }
    })

    balance_controlls_right.addEventListener('click', (e) => {
        index = parseInt(localStorage.getItem("balance_index"))
        balance = JSON.parse(localStorage.getItem("balance"))


        if (index + 1 < balance["Balances"].length) {
            localStorage.setItem("balance_index", index + 1)
            updateimage()
        }


    })

    balance_controlls_left.addEventListener('click', (e) => {
        index = parseInt(localStorage.getItem("balance_index"))
        balance = JSON.parse(localStorage.getItem("balance"))

        if (index - 1 >= 0) {
            localStorage.setItem("balance_index", index - 1)
            updateimage()
        }

    })

    lobbyTable.addEventListener("input", (e) => { // Role sr inputs control
        var target = e.target.closest("input")
        if (!target) return;
        if (target.value > 5000) {
            target.value = 5000
        }
        if (target.value < 0) {
            target.value = 0
        }
    })

    lobbyTable.addEventListener("change", (e) => { // Sr change 
        var target = e.target.closest("input")
        if (!target) return;
        if (target.value == "") target.value = "0"
        dataSend = {}
        dataSend["role"] = target.closest(".role").dataset.roleId
        dataSend["rating"] = target.value
        dataSend["customId"] = target.closest(".player_container").dataset.playerId
        sendPOST("/api/changeRoleSr", dataSend)
        updateLobby()
    })

    lobbyTable.addEventListener("keydown", (e) => { // Inputs enter blur
        var target = e.target.closest("input")
        if (!target) return;
        if (e.keyCode === 13) {
            target.blur()
        }
    })

    UserNickname.addEventListener("keydown", (e) => { // User enter create
        if (e.keyCode === 13) {
            UserCreateButton.click()
        }
    })

    customSelect.addEventListener("click", (e) => { // Create custom button
        let target = e.target.closest(".create_container")
        if (!target) return;
        if (lastActive) lastActive.classList.remove("active")
        customSelect.style.display = 'none'
        sendPOST("/api/createCustom", { "id": lastActive.dataset.playerId })
        updateLobby()
    })

    UserCreateButton.addEventListener("click", (e) => { //User create
        value = UserNickname.value.replace(/^\s+|\s+$/g, '')
        if (value != "") {
            UserNickname.value = ""
            sendPOST("/api/createPlayer", { "Username": value })
            updatePlayers()
        }
    })

    clear_button.addEventListener("click", (e) => { // Clear lobby
        sendPOST("/api/clearLobby", {})
        updateLobby()
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
            openID = currentLobbyElem.closest(".player_container").dataset.playerId
        }
        var scroll = lobbyTable.closest("div").scrollTop;
        const res = await fetch('/api/getLobby')
        var data = await res.json()
        lobbyTable.innerHTML = "";
        var pattern = await fetch('static/html/lobby_pattern.html')
        var pattern_data = await pattern.text()
        data.forEach(element => {
            for (let i = 0; i < 3; i++) {
                element.RolesPriority[i].btn = (i != 2)
                if (i != 2) element.RolesPriority[i].btn_id = i
            }
        });

        lobbyTable.innerHTML = Mustache.render(pattern_data, { 'data': data })
        lobby_count.innerText = "Players in lobby: " + data.length
        if (openID != null) {
            for (let i = 0; i < lobbyTable.children.length; i++) {
                let elem = lobbyTable.children[i];
                if (elem.dataset.playerId == openID) {
                    let menu = elem.getElementsByClassName("lobby_menu")[0]
                    menu.style.display = "block"
                    currentLobbyElem = menu
                }
            }
        }
        lobbyTable.closest("div").scrollTop = scroll
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

    async function updateimage() {
        index = parseInt(localStorage.getItem("balance_index"))
        balance = JSON.parse(localStorage.getItem("balance"))
        if (balance["Balances"].length == 0) {
            balance_img.src = "/static/img/balance_404.png"
            balance_count.innerText = "0/0"
            return
        }
        current_balance = balance["Balances"][index]
        var image = await (await fetch('/api/balanceImage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(current_balance)
        })).blob()
        imageBlob = image
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL(image);
        balance_img.src = imageUrl
        balance_count.innerText = (index + 1) + "/" + balance["Balances"].length
    }
})();