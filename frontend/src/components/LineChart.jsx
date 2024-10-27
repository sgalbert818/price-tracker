import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, TimeScale, Tooltip, Legend } from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(LineElement, PointElement, LinearScale, TimeScale, Tooltip, Legend);

const LineChart = ({ data }) => {
    // Assuming data is an array of arrays like [['2024-10-12T00:00:00Z', '44'], ['2024-10-13T00:00:00Z', '56']]
    const labels = data.map(item => item[1]); // ISO date strings
    const values = data.map(item => Number(item[0])); // Corresponding values

    const chartData = {
        labels: labels,
        datasets: [
            {
                label: 'Price',
                data: values,
                fill: false,
                borderColor: 'black',
                tension: 0.1,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day', // Adjust this based on your data
                },
                title: {
                    display: false,
                    text: 'Date',
                },
            },
            y: {
                title: {
                    display: false,
                    text: 'Values',
                },
            },
        },
        plugins: {
            title: {
                display: false, // Hides the title
            },
            legend: {
                display: false, // Show the legend
            },
        },
    };

    return <Line data={chartData} options={options} />;
};

export default LineChart;
