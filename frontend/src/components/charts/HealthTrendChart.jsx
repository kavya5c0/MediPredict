import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import 'highcharts/highcharts-more'

const HealthTrendChart = () => {
  const options = {
    chart: {
      type: 'line',
      height: 300
    },
    title: {
      text: null
    },
    xAxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    },
    yAxis: {
      title: {
        text: 'Value'
      }
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      line: {
        dataLabels: {
          enabled: false
        },
        enableMouseTracking: true
      }
    },
    series: [
      {
        name: 'Blood Pressure',
        data: [120, 118, 122, 119, 121, 120],
        color: '#3B82F6'
      },
      {
        name: 'Heart Rate',
        data: [72, 74, 71, 73, 72, 72],
        color: '#EF4444'
      },
      {
        name: 'Glucose',
        data: [95, 98, 92, 96, 94, 95],
        color: '#10B981'
      }
    ]
  }

  return <HighchartsReact highcharts={Highcharts} options={options} />
}

export default HealthTrendChart