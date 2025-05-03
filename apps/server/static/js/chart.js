document.addEventListener("DOMContentLoaded", function() {
    // 서버에서 데이터 가져오기
    fetch('/get_product_data')
        .then(response => response.json())
        .then(data => {
            // 서버에서 받아온 데이터 (샘플 데이터로 대체 가능)

            const price = data.price; // 가격 데이터 (배열 형태)
            const discountRate = data.discountRate; // 할인율 데이터 (배열 형태)

            // 가격과 할인율 HTML 업데이트
            // document.getElementById('price').innerText = price.join(", ") + '원';  // 가격 배열을 쉼표로 구분하여 표시
            // document.getElementById('discount-rate').innerText = discountRate.join(", ") + '%';  // 할인율 배열을 쉼표로 구분하여 표시

            // 차트 그리기
            const ctx = document.getElementById('scoreChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: price.map((_, i) => `항목 ${i + 1}`),   // 항목별 라벨 생성
                    datasets: [
                        {
                            label: '가격',
                            data: price,
                            borderColor: 'rgba(54, 162, 235, 1)',  // 가격 라인 색
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',  // 가격 배경 색
                            tension: 0.3,
                            fill: false
                        },
                        {
                            label: '할인율',
                            data: discountRate,
                            borderColor: 'rgba(255, 99, 132, 1)',  // 할인율 라인 색
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',  // 할인율 배경 색
                            tension: 0.3,
                            fill: false,
                            yAxisID: 'y1'  // 할인율을 오른쪽 축에 표시
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: '가격 (원)' }
                        },
                        y1: {
                            position: 'right',
                            beginAtZero: true,
                            title: { display: true, text: '할인율 (%)' },
                            grid: { drawOnChartArea: false }  // 할인율 축은 그리드 표시 안함
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
