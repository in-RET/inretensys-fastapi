<script setup>
import { ref } from 'vue'

async function getComponentSchema(componentName) {
    let response =  await fetch("/api/getComponentSchema/" + componentName)
    let data = await response.json()

    // console.log(data)

    // let workingarea = document.getElementById("workingarea")
    // workingarea.innerHTML = data
}

function addGraphNode(name) {
    console.log("addGraphNode")    
}

let elements = null
let isFetching = true

try {
    let response = await fetch("/api/getComponentsList")
    let data = await response.json()

    elements = ref(data.components)
    isFetching = false
}
catch (exception) {
    console.error(exception)
}

</script>

<template>
    <div v-if="!isFetching">
        <p>Komponenten:</p>
        <div class="list-group me-2" >
            <button v-for="elem in elements" @click="getComponentSchema(elem)" class="list-group-item list-group-item-action">{{ elem }}</button>
        </div>
    </div>
</template>

<style>

</style>