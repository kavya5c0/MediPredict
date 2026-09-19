import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import 'highcharts/highcharts-more'
import 'highcharts/modules/solid-gauge'

const HealthGaugeChart = ({ value = 78, title = 'Score' }) => {
  const options = {
    chart: {
      type: 'solidgauge',
      height: 250
    },
    title: {
      text: null
    },
    pane: {
      center: ['50%', '50%'],
      size: '100%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },
    exporting: {
      enabled: false
    },
    credits: {
      enabled: false
    },
    tooltip: {
      enabled: false
    },
    yAxis: {
      min: 0,
      max: 100,
      lineWidth: 0,
      tickPositions: []
    },
    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    },
    series: [{
      name: title,
      data: [value],
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:28px;font-weight:bold">{y}</span><br/><span style="font-size:12px;color:#666">Health Score</span></div>'
      },
      tooltip: {
        valueSuffix: ' out of 100'
      }
    }]
  }

  return <HighchartsReact highcharts={Highcharts} options={options} />
}

export default HealthGaugeChart