<template>
  <div class="columns">
    <div class="column">
      <section>
        <line-chart :chart-data="datacollection"></line-chart>
      </section>
    </div>
    <div class="column">
      <section>
        <b-field grouped>
          <b-datepicker
            placeholder="Select date..."
            icon="calendar"
            editable
            expanded
            v-model="newEntry.date"
          ></b-datepicker>
          <b-input
            placeholder="Infected"
            controls-position="compact"
            type="number"
            min="0"
            expanded
            v-model="newEntry.infected"
          ></b-input>
          <p class="control">
            <button class="button is-primary" @click="submitEntry">Add</button>
          </p>
        </b-field>
      </section>
      <section>
        <b-table
          :data="stats"
          :checked-rows.sync="checkedRows"
          :mobile-cards="false"
          checkable
          narrowed
        >
          <template slot-scope="props">
            <b-table-column
              field="date"
              label="Date"
              sortable
            >{{ format(new Date(props.row.date ), "dd.MM.yyyy")}}</b-table-column>
            <b-table-column field="infected" label="Infected" sortable>{{props.row.infected}}</b-table-column>
          </template>
        </b-table>
      </section>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Amplitude</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control">
              <input class="input" type="text" v-model.number="lm_params.init.ampl" />
            </p>
          </div>
        </div>
      </div>
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Offset</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control">
              <input class="input" type="text" v-model.number="lm_params.init.offset" />
            </p>
          </div>
        </div>
      </div>
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Sigma</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control">
              <input class="input" type="text" v-model.number="lm_params.init.sigma" />
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { format } from "date-fns";
import LineChart from "./LineChart";
// import Table from "./Table";
import fit from "./fit";
import erf from "./erf";
import normalize_dates from "./normalize_dates";

export default {
  components: {
    LineChart
    // Table
  },
  data: function() {
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
        { date: "2020-03-22", infected: 367 }
      ],
      lm_params: {
        init: {
          ampl: 1000,
          offset: 30,
          sigma: 30
        }
      },
      newEntry: {},
      checkedRowsStorage: []
    };
  },
  computed: {
    stats: function() {
      return this.statistics.map((it, index) => ({
        ...it,
        index,
        date: new Date(it.date)
      }));
    },
    checkedRows: {
      get: function() {
        if (this.checkedRowsStorage.length >= 2) return this.checkedRowsStorage;
        return this.stats;
      },
      set: function(value) {
        this.checkedRowsStorage = value;
      }
    },
    datacollection: function() {
      console.log(this.stats);
      console.log(this.checkedRows);
      let min = Math.min(...this.checkedRows.map(it => new Date(it.date)));
      let ticks = [];
      for (let days = 1; days < 60; days += 1) {
        let date = new Date(min.valueOf());
        date.setDate(date.getDate() + days);
        ticks.push(date);
      }
      // let labels = ticks.map(it => format(it, "dd MM yyyy"));
      let fitted_params = this.fitData();
      console.log("parameterValues ", fitted_params.parameterValues);
      console.log("fitted_params ", fitted_params);
      // let { ampl, offset, sigma } = this.lm_params.init;

      // let func = erf([ampl, offset, sigma]);
      let func = erf(fitted_params.parameterValues);
      let normalized_ticks = normalize_dates(ticks);
      let fitted = normalized_ticks.map(func);
      // let fitted = this.normalize_dates(ticks).map(x => func(x));
      return {
        // labels: labels,/
        datasets: [
          {
            label: "Data",
            backgroundColor: "rgb(54, 162, 235)",
            borderColor: "rgb(54, 162, 235)",
            data: this.checkedRows.map(it => ({
              x: new Date(it.date),
              y: it.infected
            })),
            fill: false,
            showLine: false
          },
          {
            label: "Predicted",
            backgroundColor: "rgb(255, 99, 132)",
            borderColor: "rgb(255, 99, 132)",
            data: [...ticks.keys()].map(i => ({
              x: ticks[i],
              y: fitted[i]
            })),
            fill: false,
            pointRadius: false,
            showLine: true
          }
        ]
      };
    }
  },
  methods: {
    format: format,
    fitData() {
      let dates = this.checkedRows.map(it => new Date(it.date).getTime());
      let x = normalize_dates(dates);
      let y = this.checkedRows.map(it => it.infected);
      let { ampl, offset, sigma } = this.lm_params.init;
      // let min_timestamp = Math.min(...x);
      // let day_ms = 1000 * 60 * 60 * 24;/
      let init = [ampl, offset, sigma];
      console.log("init params", init);
      let minValues = [360, 20, 20];
      let maxValues = [140000000, 70, 70];
      return fit(x, y, erf, init, minValues, maxValues);
    },
    submitEntry() {
      console.log(this.newEntry);
      let { date, infected } = this.newEntry;
      // let date_str = date;
      this.statistics.push({ date: format(date, "yyyy-MM-dd"), infected });
    }
  }
};
</script>
