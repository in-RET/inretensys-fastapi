<script setup>
import TheWelcome from "./components/TheWelcome.vue";
import Footer from "./components/Footer.vue";
import Header from "./components/Header.vue";
import MenuComponents from "./components/menus/MenuComponents.vue"
import MenuMain from "./components/menus/MenuMain.vue"
import WorkingArea from "./components/WorkingArea.vue";
</script>

<template>
    <div class="row row-sm">
      <div class="col">
        <Header />    
      </div>
    </div>
    <div class="row">
      <div class="col col-sm-1">
        <MenuMain />
      </div>
      <div class="col">
        <WorkingArea />
      </div>
      <div class="col col-sm-2">
        <MenuComponents />
      </div>
      <!-- <div class="row">
        <div class="col"></div> for extra content
      </div> -->
      <div class="row">
        <div class="col">
          <Footer />
        </div>
      </div>

    </div>
</template>

<style>

</style>
