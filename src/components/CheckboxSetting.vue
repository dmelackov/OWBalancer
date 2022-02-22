<template>
    <div class="settings_checkbox">
        <input type="checkbox" name="checkbox" v-model="value">
        <p class="checkbox_title">{{ title }}</p>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    props: ["title", "setting"],
    data(){
        return {
            SettingValue: false
        }
    },
    computed: {
        value: {
            get(){
                return this.SettingValue
            },
            async set(v){
                await axios.post("/api/profile/settings/setSettings", {"setting": this.setting, "value": v})
                this.getValueFromServer()
            }
        }
    },
    methods: {
        async getValueFromServer(){
            this.SettingValue = (await axios.get('/api/profile/settings/getSettings')).data[this.setting]
        }
    },
    created(){
        this.getValueFromServer()
    }
}
</script>

<style scoped>
.settings_checkbox {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: max-content;
    margin-bottom: 5px;
    margin-top: 5px;
}

.checkbox_title {
    margin: 0;
}
</style>