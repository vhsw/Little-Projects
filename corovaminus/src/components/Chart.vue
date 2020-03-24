<template>
  <div class="columns">
    <div class="column">
      <section>
        <b-notification
          title="Bad fittnes"
          type="is-danger"
          has-icon
          :active.sync="fittingResults.parameterError > fittingParams.errorTolerance"
          role="alert"
        >Algorithm failed to converge. Error level is {{fittingResults.parameterError.toFixed(2)}}</b-notification>
      </section>
      <section>
        <line-chart :chart-data="charts"></line-chart>
      </section>
      <section>
        <b-message>
          <p>Total cases expected: {{fittingResults.parameterValues[0].toFixed(0)}}</p>
          <p>Peak expected: {{new Date(fittingResults.parameterValues[1]) | formatDistanceToNow}}</p>
          <p>Expected duration: {{fittingResults.parameterValues[2].toFixed(0)}}</p>
        </b-message>
      </section>
    </div>
  </div>
</template>

<script>
import LineChart from "./LineChart";

import { formatDistanceToNow } from "date-fns";

export default {
  components: {
    LineChart
  },
  props: ["charts", "fittingParams", "fittingResults"],
  filters: {
    formatDistanceToNow: value =>
      formatDistanceToNow(value, { addSuffix: true })
  }
};
</script>
