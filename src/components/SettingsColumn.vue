<template>
    <div class="column_widget lobby">
        <p class="column_title">Settings</p>
        <hr>
        <div class="players_count">
            <slot> </slot>
        </div>
    </div>
</template>

<style scoped>
@import "../assets/css/global.css";

.column_widget {
    display: flex;
    flex-direction: column;
    border-radius: 6px;
    margin: 8px;
    margin-top: 10px;
    padding: 16px 16px;
    min-width: 15%;
    max-width: 15%;
    background-color: #11161d;
}

.column_title {
    margin: 0;
    margin-bottom: 5px;
    text-align: center;
}
</style>