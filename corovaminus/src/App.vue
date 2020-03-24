<template>
  <section>
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">COVID-19 spread in Russia</h1>
        </div>
      </div>
    </section>
    <div id="app" class="container">
      <div class="columns">
        <div class="column">
          <Menu v-bind:fittingParams="fittingParams" @change="fittingParams = $event" />
        </div>
        <div class="column is-half">
          <Chart
            v-bind:charts="charts"
            v-bind:fittingParams="fittingParams"
            v-bind:fittingResults="fittingResults"
          />
        </div>
        <div class="column">
          <Table v-bind:dates="dates" v-bind:infected="infected" @submit="statistics.push($event)" />
        </div>
      </div>
    </div>
    <footer class="footer">
      <div class="content has-text-centered">
        <p>
          <a href="https://bulma.io">
            <img
              src="https://bulma.io/images/made-with-bulma.png"
              alt="Made with Bulma"
              width="128"
              height="24"
            />
          </a>
        </p>
      </div>
    </footer>
  </section>
</template>

<script>
import Vue from "vue";
import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "@mdi/font/css/materialdesignicons.css";

import Menu from "./components/Menu";
import Chart from "./components/Chart.vue";
import Table from "./components/Table.vue";
import fit from "./components/fit";
import erf from "./components/erf";

Vue.use(Buefy);

export default {
  name: "App",
  components: {
    Chart,
    Menu,
    Table
  },
  data() {
    return {
      statistics: [
        { date: "2020-03-06", infected: 7 },
        { date: "2020-03-07", infected: 11 },
        { date: "2020-03-08", infected: 14 },
        { date: "2020-03-09", infected: 17 },
        { date: "2020-03-10", infected: 20 },
        { date: "2020-03-11", infected: 28 },
        { date: "2020-03-12", infected: 34 },
        { date: "2020-03-13", infected: 45 },
        { date: "2020-03-14", infected: 59 },
        { date: "2020-03-15", infected: 69 },
        { date: "2020-03-16", infected: 93 },
        { date: "2020-03-17", infected: 114 },
        { date: "2020-03-18", infected: 147 },
        { date: "2020-03-19", infected: 199 },
        { date: "2020-03-20", infected: 253 },
        { date: "2020-03-21", infected: 306 },
        { date: "2020-03-22", infected: 367 },
        { date: "2020-03-23", infected: 438 }
      ],
      fittingParams: {
        initialValues: [1000, new Date("2020-04-01").getTime(), 30],
        minValues: [1000, new Date("2020-03-06").getTime(), 20],
        maxValues: [140000000, new Date("2020-12-31").getTime(), 70],
        damping: 0.01,
        gradientDifference: 50,
        maxIterations: 100,
        errorTolerance: 80
      },
      newEntry: {}
    };
  },
  computed: {
    dates() {
      return this.statistics.map(it => new Date(it.date));
    },

    infected() {
      return this.statistics.map(it => it.infected);
    },

    fittingResults() {
      console.log("Aloha");
      return fit(this.dates, this.infected, erf, this.fittingParams);
    },
    charts() {
      let minDate = Math.min(...this.dates);
      let sigma = this.fittingResults.parameterValues[2];
      let range = this.dateRange(minDate, sigma * 1.5);
      let colors = {
        red: "rgb(255, 99, 132)",
        orange: "rgb(255, 159, 64)",
        yellow: "rgb(255, 205, 86)",
        green: "rgb(75, 192, 192)",
        blue: "rgb(54, 162, 235)",
        purple: "rgb(153, 102, 255)",
        grey: "rgb(201, 203, 207)"
      };
      return {
        datasets: [
          {
            label: "Data",
            backgroundColor: colors.blue,
            borderColor: colors.blue,
            data: this.dates.map((date, i) => ({
              x: date,
              y: this.infected[i]
            })),
            fill: false,
            showLine: false
          },
          {
            label: "Predicted",
            backgroundColor: colors.red,
            borderColor: colors.red,
            data: range.map(x => ({
              x,
              y: erf(this.fittingResults.parameterValues)(x)
            })),
            // fill: false,
            pointRadius: false,
            showLine: true
          }
          // {
          //   label: "Initial",
          //   backgroundColor: colors[2],
          //   borderColor: colors[2],
          //   data: range.map(x => ({
          //     x,
          //     y: erf(this.fittingParams.initialValues)(x)
          //   })),
          //   fill: false,
          //   pointRadius: false,
          //   showLine: true
          // }
        ]
      };
    }
  },
  methods: {
    handle(event) {
      console.log(event);
    },
    dateRange(start, span) {
      let range = [];
      for (let days = 0; days < span; days += 1) {
        let date = new Date(start.valueOf());
        date.setDate(date.getDate() + days);
        range.push(date);
      }
      return range;
    }
  }
};
</script>

<style>
.title {
  font-size: 4.5rem;
  text-align: center;
}
</style>
