import { Scatter, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
    extends: Scatter,
    mixins: [reactiveProp],
    props: ['options'],
    mounted() {
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        let options = {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                }],
                // yAxes: [{
                //     type: 'logarithmic',
                // }]
            },
            maintainAspectRatio: false
        }
        this.renderChart(this.chartData, options)
    }
}
