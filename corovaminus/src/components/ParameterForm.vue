<template>
  <section>
    <b-field label="Amplitude">
      <b-input type="number" min="0" v-bind:value="amplitude" @input="send(0, parseFloat($event))" />
    </b-field>
    <b-field label="Offset">
      <b-input type="date" v-bind:value="offset" @input="send(1, new Date($event).getTime())" />
    </b-field>
    <b-field label="Sigma">
      <b-input v-bind:value="sigma" @input="send(2, parseFloat($event))" />
    </b-field>
  </section>
</template>
<script>
import { format } from "date-fns";
export default {
  props: ["params"],
  name: "parameter-form",
  computed: {
    amplitude() {
      return this.params[0];
    },
    offset() {
      return format(this.params[1], "yyyy-MM-dd");
    },
    sigma() {
      return this.params[2];
    }
  },
  methods: {
    send(key, value) {
      if (isNaN(value)) return;
      let localParams = this.params.slice();
      localParams[key] = value;
      this.$emit("change", localParams);
    }
  }
};
</script>
