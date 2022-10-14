<script setup>
defineProps({
  ModelData: {
    type: String,
    required: true,
  },
});

console.log(ModelData)

</script>

<template>
<p>
    {{ ModelData }}
</p>
</template>

<style>

</style>