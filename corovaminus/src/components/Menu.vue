<template>
  <b-menu>
    <b-menu-list icon="settings" label="Settings">
      <b-menu-item label="Initial Values">
        <parameter-form
          v-bind:params="fittingParams.initialValues"
          @change="send('initialValues', $event)"
        />
      </b-menu-item>
      <b-menu-item label="Min Values">
        <parameter-form
          v-bind:params="fittingParams.minValues"
          @change="send('minValues', $event)"
        />
      </b-menu-item>
      <b-menu-item label="Max Values">
        <parameter-form
          v-bind:params="fittingParams.maxValues"
          @change="send('maxValues', $event)"
        />
      </b-menu-item>
      <b-menu-item label="Algotithm Params">
        <b-field label="Damping">
          <b-input
            min="0"
            v-bind:value="fittingParams.damping"
            @input="send('damping', parseFloat($event))"
          />
        </b-field>
        <b-field label="Gradient Difference">
          <b-input
            v-bind:value="fittingParams.gradientDifference"
            @input="send('gradientDifference', parseFloat($event))"
          />
        </b-field>
        <b-field label="Max Iterations">
          <b-input
            type="number"
            min="10"
            v-bind:value="fittingParams.maxIterations"
            @input="send('maxIterations', parseFloat($event))"
          />
        </b-field>
        <b-field label="Error Tolerance">
          <b-input
            v-bind:value="fittingParams.errorTolerance"
            @input="send('errorTolerance', parseFloat($event))"
          />
        </b-field>
      </b-menu-item>
    </b-menu-list>
  </b-menu>
</template>

<script>
import ParameterForm from "./ParameterForm";

export default {
  components: {
    ParameterForm
  },
  props: ["fittingParams"],
  data() {
    return {
      isActive: true
    };
  },
  methods: {
    send(key, value) {
      if (typeof value === "number" && (value <= 0 || isNaN(value))) return;
      let localParams = this.fittingParams;
      localParams[key] = value;
      this.$emit("change", localParams);
    }
  }
};
</script>
