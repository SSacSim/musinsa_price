document.addEventListener("DOMContentLoaded", function() {
    // 서버에서 데이터 가져오기
    fetch('/get_product_data')
        .then(response => response.json())
        .then(data => {
            const date = data.date;  // 날짜 데이터 (예: ["2024-05-01", "2024-05-02", ...])
            const price = data.price;
            const discountRate = data.discountRate;

            const ctx = document.getElementById('scoreChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: date,  // ❗ x축을 날짜로 설정
                    datasets: [
                        {
                            label: '가격',
                            data: price,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            tension: 0.3,
                            fill: false
                        },
                        {
                            label: '할인율',
                            data: discountRate,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            tension: 0.3,
                            fill: false,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: { display: true, text: '날짜' }
                        },
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: '가격 (원)' }
                        },
                        y1: {
                            position: 'right',
                            beginAtZero: true,
                            title: { display: true, text: '할인율 (%)' },
                            grid: { drawOnChartArea: false }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
