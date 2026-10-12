import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import 'highcharts/highcharts-more'

const DiseaseRiskChart = ({ predictions = [] }) => {
  // Get the latest prediction's all_probabilities
  const latestPrediction = predictions.length > 0 ? predictions[0] : null
  const allProbabilities = latestPrediction?.all_probabilities || {}

  // Convert probabilities to chart data
  const chartData = Object.entries(allProbabilities).map(([name, value]) => ({
    name: name,
    y: (value || 0) * 100, // Convert to percentage
    color: getColorForDisease(name)
  }))

  // Fallback data if no predictions
  const fallbackData = [
    { name: 'Diabetes', y: 35, color: '#EF4444' },
    { name: 'Cardiovascular', y: 25, color: '#F59E0B' },
    { name: 'Hypertension', y: 20, color: '#3B82F6' },
    { name: 'Low Risk', y: 20, color: '#10B981' }
  ]

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
      data: chartData.length > 0 ? chartData : fallbackData
    }]
  }

  return <HighchartsReact highcharts={Highcharts} options={options} />
}

function getColorForDisease(disease) {
  const colors = {
    'Type 2 Diabetes': '#EF4444',
    'Heart Disease': '#F59E0B',
    'Hypertension': '#3B82F6',
    'Stroke': '#8B5CF6',
    'Kidney Disease': '#EC4899',
    'Liver Disease': '#06B6D4',
    'Respiratory Disease': '#10B981'
  }
  return colors[disease] || '#6B7280'
}

export default DiseaseRiskChart
