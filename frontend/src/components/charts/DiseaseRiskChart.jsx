import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import 'highcharts/highcharts-more'

const DiseaseRiskChart = () => {
  const options = {
    chart: {
      type: 'pie',
      height: 300
    },
    title: {
      text: null
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b>: {point.percentage:.1f} %'
        },
        showInLegend: true
      }
    },
    series: [{
      name: 'Disease Risk',
      colorByPoint: true,
      data: [
        { name: 'Diabetes', y: 35, color: '#EF4444' },
        { name: 'Cardiovascular', y: 25, color: '#F59E0B' },
        { name: 'Hypertension', y: 20, color: '#3B82F6' },
        { name: 'Low Risk', y: 20, color: '#10B981' }
      ]
    }]
  }

  return <HighchartsReact highcharts={Highcharts} options={options} />
}

export default DiseaseRiskChart