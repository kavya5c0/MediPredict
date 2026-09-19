import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import 'highcharts/highcharts-more'

Highcharts.setOptions({
  colors: ['#3B82F6', '#EF4444', '#10B981', '#F59E0B']
})

const HealthOverviewChart = ({ stats }) => {
  const options = {
    chart: {
      type: 'bar',
      height: 300
    },
    title: {
      text: null
    },
    xAxis: {
      categories: ['Reports', 'Predictions', 'Chat', 'Recommendations'],
      labels: {
        style: {
          fontSize: '12px'
        }
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Count'
      }
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      bar: {
        borderRadius: 5,
        dataLabels: {
          enabled: true
        }
      },
      series: {
        borderWidth: 0,
        colorByPoint: true
      }
    },
    series: [{
      name: 'Health Data',
      data: [stats.reports, stats.predictions, stats.chatMessages, stats.recommendations],
      colors: ['#3B82F6', '#EF4444', '#10B981', '#F59E0B']
    }]
  }

  return <HighchartsReact highcharts={Highcharts} options={options} />
}

export default HealthOverviewChart