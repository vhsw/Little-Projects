<template>
  <section class="section">
    <div id="app" class="container">
      <Chart chartData />
    </div>
  </section>
</template>

<script>
import Chart from "./components/Chart.vue";

import Vue from "vue";
import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "@mdi/font/css/materialdesignicons.css";

Vue.use(Buefy);

Vue.config.productionTip = false;

export default {
  name: "App",
  components: {
    Chart
  }
};
</script>

<style>
</style>
