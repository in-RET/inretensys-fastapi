<script setup>
  import Footer from "@/components/Footer.vue";
  import Header from "@/components/Header.vue";
  import MenuComponents from "@/components/menus/MenuComponents.vue"
  import MenuMain from "@/components/menus/MenuMain.vue"
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
        <router-view />   
      </div>
      <div class="col col-sm-2">
        <KeepAlive>
          <Suspense>
            <MenuComponents />
            <template #fallback>
              <p>Loading...</p>
            </template>
          </Suspense>
        </KeepAlive>
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
