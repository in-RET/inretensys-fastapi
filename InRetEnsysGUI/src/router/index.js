import { createWebHistory, createRouter } from "vue-router"

import ViewPageNotFound from "@/views/ViewPageNotFound.vue"
import ViewEnergySystem from "@/views/ViewEnergySystem.vue"
import ViewAbout from "@/views/ViewAbout.vue"

const routes = [
    {
        path: "/",
        name: "Empty",
        component: ViewEnergySystem
    },
    {
        path: "/about",
        name: "About",
        component: ViewAbout
    },
    {
        path: "/:catchAll(.*)*",
        name: "PageNotFound",
        component: ViewPageNotFound
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router