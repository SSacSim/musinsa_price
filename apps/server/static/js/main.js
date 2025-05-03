// function goToProductPage(event) {
//     event.preventDefault(); // 폼 기본 동작 막기
//     const input = document.getElementById('productInput').value.trim();
//     console.log(input)
//     if (input) {
//         window.location.href = `/product/${input}`;
//     }
// }


function goToProductPage(event) {
    event.preventDefault(); // 폼 기본 동작 막기
    const input = document.getElementById('productInput').value.trim();

    console.log("입력값:", input); // 콘솔에서 값 확인용

    if (input === "") {
        alert("상품번호를 입력해주세요.");
    } else {
        // 상품번호가 CSV에 있는지 확인하는 AJAX 요청
        fetch(`/validate_product?product_id=${input}`)
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    // 유효한 상품번호라면 해당 페이지로 리디렉션
                    window.location.href = data.url;
                } else {
                    // 유효하지 않으면 오류 메시지 출력
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error("에러 발생:", error);
                alert("서버 오류가 발생했습니다. 다시 시도해주세요.");
            });
    }
}
