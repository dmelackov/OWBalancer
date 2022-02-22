<template>
    <div class="contacts">
            <p>Developers</p>
            <a href="https://discord.com/users/337577546168401920"
                >Demon_Dimon#0347</a
            >
            <a href="https://discord.com/users/254608220880896010"
                >Ivarys#2177</a
            >
        </div>
</template>

<script>
export default {
    data(){
        return {}
    }
}
</script>

<style scoped>

.contacts > a {
    color: #42556d;
    font-size: 14px;
}

.contacts>a:hover {
    color: #4e6785;
}

.contacts > p {
    color: #555555;
    font-size: 14px;
}


.contacts {
    width: max-content;
    display: flex;
    align-content: center;
    align-items: center;
    flex-wrap: nowrap;
}
</style>