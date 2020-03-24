<template>
  <section>
    <section>
      <b-field>
        <b-datepicker placeholder="Date" icon="calendar" editable expanded v-model="newEntry.date"></b-datepicker>
        <b-input placeholder="Infected" type="number" min="0" expanded v-model="newEntry.infected"></b-input>
        <p class="control">
          <b-button class="button is-primary" @click="submitEntry" icon-right="plus" />
        </p>
      </b-field>
    </section>
    <section>
      <b-table
        :data="tableData"
        :columns="columns"
        :mobile-cards="false"
        :default-sort="['date', 'desc']"
        narrowed
      ></b-table>
    </section>
  </section>
</template>
<script>
import { format } from "date-fns";
export default {
  props: ["dates", "infected"],
  computed: {
    tableData() {
      return this.dates.map((date, i) => ({
        date: format(date, "dd.MM.yyyy"),
        infected: this.infected[i]
      }));
    }
  },
  data() {
    return {
      columns: [
        {
          field: "date",
          label: "Date",
          width: "40",
          sortable: true
        },
        {
          field: "infected",
          label: "Infected",
          numeric: true
        }
      ],
      newEntry: {}
    };
  },
  methods: {
    submitEntry() {
      console.log(this.newEntry);
      let { date, infected } = this.newEntry;
      this.$emit("submit", {
        date: format(date, "yyyy-MM-dd"),
        infected: parseInt(infected)
      });
    }
  }
};
</script>
