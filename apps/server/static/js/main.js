
function goToProductPage(event) {
    if(event) event.preventDefault();
    // event.preventDefault(); // 폼 기본 동작 막기
    const input = document.getElementById('productInput').value.trim();

    console.log("입력값:",input); // 콘솔에서 값 확인용

    if (input === "") {
        alert("상품번호를 입력해주세요.");
    } else {
        // 상품번호가 CSV에 있는지 확인하는 AJAX 요청
        fetch(`/validate_product?product=${input}`)
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

// 공지사항 pop up 
function openPopup() {
    // 만약 로컬 스토리지에 'dontShowNotice'가 true면 열지 않음
    if (localStorage.getItem('dontShowNotice') === 'true') {
        return; // 팝업 안 띄움
    }
    fetch('./static/notice/notice.txt')
        .then(response => {
            if (!response.ok) throw new Error('공지사항을 불러올 수 없습니다.');
            return response.text();
        })
        .then(text => {
            const p = document.getElementById('noticeContent');
            p.innerText = text;
            document.getElementById('noticePopup').style.display = 'flex';
        })
        .catch(error => {
            console.error(error);
            // 실패 시 기본 안내 문구 표시 후 팝업 열기
            const p = document.getElementById('noticeContent');
            p.innerText = "공지사항을 불러오는데 실패했습니다.";
            document.getElementById('noticePopup').style.display = 'flex';
        });
}

// 팝업 닫기
function closePopup() {
    const checkbox = document.getElementById('dontShowAgain');
    if (checkbox.checked) {
        // 체크되어 있으면 로컬 스토리지에 기록
        localStorage.setItem('dontShowNotice', 'true');
    }
    document.getElementById('noticePopup').style.display = 'none';
}

// 페이지 로드 시 자동으로 팝업 열기 시도
window.onload = function() {
    openPopup();
};


function resetNotice() {
    localStorage.removeItem('dontShowNotice');
    openPopup();
}



document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("productInput");
    const resultsList = document.createElement("ul");
    resultsList.id = "searchResults";
    resultsList.className = "search-results";
    input.parentNode.insertBefore(resultsList, input.nextSibling);

    input.addEventListener("input", async () => {
        const query = input.value.trim();
        if (query === "") {
            resultsList.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
    
            resultsList.innerHTML = "";
            if (data.results.length === 0) {
                resultsList.style.display = 'none';
                return;
            } else {
                resultsList.style.display = 'block';
            }
    
            data.results.forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                li.className = "search-result-item";
                li.onclick = () => {
                    input.value = item;
                    resultsList.innerHTML = "";
                    resultsList.style.display = 'none';
                    goToProductPage();
                };
                resultsList.appendChild(li);
            });
        } catch (err) {
            console.error("검색 실패:", err);
            resultsList.style.display = 'none';
        }
    });

    // // 입력창 외부 클릭 시 결과 숨김
    // document.addEventListener("click", (e) => {
    //     if (!resultsList.contains(e.target) && e.target !== input) {
    //         resultsList.innerHTML = "";
    //     }
    // });
});


