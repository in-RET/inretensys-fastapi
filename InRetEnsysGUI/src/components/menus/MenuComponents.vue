<script setup>

function getComponentSchema(componentName) {
    fetch("/api/getComponentSchema/" + componentName)
    .then(response => {
        return response.json()
    })
    .then(data => {
        let workingarea = document.getElementById("workingarea")

        workingarea.innerText = data
    })

}

function getElementList() {
    fetch("/api/getComponentsList")
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log(data.components)

        let elements = data.components

        for (let id in elements) {
            let listGroup = document.getElementById("componentslist")

            var newBtn = document.createElement("button")
            newBtn.classList.add("list-group-item")
            newBtn.classList.add("list-group-item-action")
            newBtn.innerText = elements[id]

            newBtn.onclick = function() { getComponentSchema(elements[id]) }

            listGroup.appendChild(newBtn)
        }
    })
    .catch(response => {
        console.error(response)
    });

} 

getElementList()

</script>

<template>
    <p>Komponenten:</p>
    <div class="list-group me-2" id="componentslist"></div>
</template>

<style>

</style>