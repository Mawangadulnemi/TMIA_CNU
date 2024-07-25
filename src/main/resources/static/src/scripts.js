document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.getElementById('loginButton');

    // 로그인 상태 체크 함수
    function checkLoginStatus() {
        if (sessionStorage.getItem('access_token')) {
            loginButton.textContent = 'LOGOUT';
        } else {
            loginButton.textContent = 'LOGIN';
        }
    }

    // 로그인 상태 확인용 GET 요청
    function verifyLoginStatus() {
        fetch('/api/auth/', {
            method: 'GET',
        })
        .then((response) => {
            if (response.status === 200) {
                sessionStorage.setItem('access_token', 'some_dummy_token');
                loginButton.textContent = 'LOGOUT';
            } else if (response.status === 401) {
                sessionStorage.removeItem('access_token');
                loginButton.textContent = 'LOGIN';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            sessionStorage.removeItem('access_token');
            loginButton.textContent = 'LOGIN';
        });
    }

    verifyLoginStatus();
// 쿠키 삭제 함수
    function deleteCookie(name) {
        document.cookie = name + '=; Max-Age=-99999999;';
    }

    // 로그인 버튼 클릭 이벤트
    loginButton.addEventListener('click', function () {
        fetch('/api/auth/logout', {
            method: 'GET',
        })
        .then((response) => {
            return response.status === 200
        })
        .catch((error) => {
            console.error('Error:', error);
            return false
        });
        if (sessionStorage.getItem('access_token')) {
            // 로그아웃 로직
            sessionStorage.removeItem('access_token');
            deleteCookie('access_token'); // 쿠키 삭제
            loginButton.textContent = 'LOGIN';
            alert('로그아웃 되었습니다.');
            window.location.href = 'index.html'; // 로그아웃 후 index.html로 이동
        } else {
            // 로그인 페이지로 이동
            window.location.href = 'login.html';
        }
    });

    // 기타 이벤트 리스너들
    const ctaButton = document.getElementById('ctaButton');
    if (ctaButton) {
        ctaButton.addEventListener('click', function () {
            if (sessionStorage.getItem('access_token')) {
                window.location.href = 'select.html';
            } else {
                window.location.href = 'login.html';
            }
        });
    }

    const languageButton = document.getElementById('languageButton');
    if (languageButton) {
        languageButton.addEventListener('click', function () {
            if (sessionStorage.getItem('access_token')) {
                window.location.href = 'select.html';
            } else {
                window.location.href = 'login.html';
            }
        });
    }

    // 로그인 폼 제출 이벤트
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(loginForm);

            fetch('/api/auth/login', {
                method: 'POST',
                body: formData,
            })
            .then((response) => {
                if (response.status === 200) {
                    loginButton.textContent = 'LOGOUT'; // 로그인 성공 후 버튼 텍스트 변경
                    window.location.href = 'index.html'; // 로그인 성공 후 이동할 페이지
                } else {
                    throw new Error('로그인 실패. 이메일과 비밀번호를 확인하세요.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert(error.message);
            });
        });
    }
    checkLoginStatus();
});

document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.introduce__tab');
    const stepTitle = document.querySelector('.introduce__step-title');
    const stepDescription = document.querySelector('.introduce__step-description');
    const stepImage = document.querySelector('.introduce__step-image');
    const guideButtons = document.querySelectorAll('.introduce__guide-button');
    const guideModal = document.getElementById('guideModal');
    const guideContent = document.querySelector('.guide-modal-content ul');
    const guideModalClose = document.querySelector('.guide-modal-close');

    const steps = {
        1: {
            title: '01. 로그인',
            description: '로그인 버튼을 클릭해주세요.<br>ID와 PW를 입력해주세요.',
            image: 'assets/videos/step1.png',
            guide: `
                    <li>
                        <strong>📹 Tmia 서비스 회원가입 할 때</strong>
                            <ul>
                                <li>로그인 페이지에서 회원가입 버튼을 클릭합니다.</li>
                                <li>사용하고싶은 ID를 입력합니다.</li>
                                <li>사용자 계정의 비밀번호를 설정합니다.</li>
                            </ul>
                    </li>
                    <hr />
                    <li>
                        <strong>📁 Tmia 서비스 로그인 할 때</strong>
                            <ul>
                                <li>로그인 페이지를 클릭하여 이동합니다.</li>
                                <li>사용자 ID를 입력합니다.</li>
                                <li>사용자 PassWord를 입력합니다.</li>
                            </ul>
                    </li>
                `,
        },
        2: {
            title: '02. 상대방 선택',
            description: '상대방을 추가해주세요.<br>상대방 선택해주세요.',
            image: 'assets/videos/step2.png',
            guide: `
                    <li>
                        <strong>📁 영상 통화 상대를 추가하고 싶을 때</strong>
                        <ul>
                            <li>로그인 후 이용하기 버튼을 클릭한다.</li>
                            <li>+ 모양의 버튼을 클릭한다.</li>
                            <li>상대방의 정보를 입력 후 생성한다.</li>
                        </ul>
                    </li>
                    <hr />
                    <li>
                        <strong>📁 영상 통화를 시작하고 싶을 때</strong>
                        <ul>
                            <li>로그인 후 이용하기 버튼을 클릭한다.</li>
                            <li>생성되어 있는 통화 상대방을 클릭한다.</li>
                            <li>연결음이 들린 후 성공하면 영상통화가 시작된다.</li>
                        </ul>
                    </li>
                `,
        },
        3: {
            title: '03. 영상 통화',
            description: '스페이스바를 꾹 누르고 말을 한 뒤 뗍니다.<br>상대방을 위해 또박또박 말해주세요.',
            image: 'assets/videos/step1.png',
            guide: `
                    <li>
                        <strong>📹 버튼을 통해 상대방에게 질문하고 싶을 때</strong>
                        <ul>
                            <li>영상 통화 시작 후 화면 좌측의 원하는 질문을 클릭한다.</li>
                            <li>질문 클릭 시 상대방에게 해당 질문에 맞는 대답이 돌아온다.</li>
                            <li>같은 방식으로 원하는 질문을 클릭한다.</li>
                        </ul>
                    </li>
                    <hr />
                    <li>
                        <strong>📁 음성을 통해 상대방에게 질문하고 싶을 때</strong>
                        <ul>
                            <li>영상 통화 시작 후 스페이스 바 버튼을 누른다.</li>
                            <li>스페이스 바를 누른 상태에서 원하는 질문을 한다.</li>
                            <li>질문을 한 뒤 스페이스 바를 떼면 상대방이 대답을 한다.</li>
                        </ul>
                    </li>
                `,
        },
    };

    tabs.forEach((tab) => {
        tab.addEventListener('click', function () {
            const step = this.getAttribute('data-step');

            // Update active tab
            document.querySelector('.introduce__tab--active').classList.remove('introduce__tab--active');
            this.classList.add('introduce__tab--active');

            // Update step content
            stepTitle.innerHTML = steps[step].title;
            stepDescription.innerHTML = steps[step].description;
            stepImage.src = steps[step].image;
            guideButtons.forEach((button) => {
                button.setAttribute('data-step', step);
            });
        });
    });

    guideButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const step = this.getAttribute('data-step');
            guideContent.innerHTML = steps[step].guide;
            guideModal.style.display = 'flex';
        });
    });

    guideModalClose.addEventListener('click', function () {
        guideModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === guideModal) {
            guideModal.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const sinhaechulProfile = document.getElementById('sinhaechulProfile');
    const connectingScreen = document.getElementById('connectingScreen');
    const loadingSound = document.getElementById('loadingSound');

    sinhaechulProfile.addEventListener('click', function () {
        connectingScreen.style.display = 'flex'; // 로딩 화면 표시
        loadingSound.play(); // 로딩 사운드 재생
        setTimeout(function () {
            window.location.href = 'conversation.html'; // 3초 후에 conversation.html로 이동
        }, 6400);
    });

    const addProfileButton = document.getElementById('addProfileButton');
    const modal = document.getElementById('modal');
    const modalClose = document.getElementById('modalClose');
    const modalForm = modal.querySelector('form');
    const profilesContainer = document.querySelector('.profiles');

    modal.style.display = 'none';
    // 모달을 열기 위한 버튼 클릭 이벤트 리스너
    addProfileButton.addEventListener('click', function () {
        modal.style.display = 'flex';
    });

    // 모달을 닫기 위한 닫기 버튼 클릭 이벤트 리스너
    modalClose.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // 모달 외부를 클릭했을 때 모달을 닫는 이벤트 리스너
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // 폼 제출 이벤트 리스너
    modalForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const photoFile = document.getElementById('photo').files[0];
        const relation = document.getElementById('relation').value;

        // 사진 파일이 있는 경우에만 프로필 추가
        if (photoFile) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const profileImage = e.target.result;
                const newProfile = document.createElement('div');
                newProfile.classList.add('profile');
                newProfile.innerHTML = `
                        <img src="${profileImage}" alt="${name}" />
                        <div class="profile__name">${name}</div>
                    `;
                profilesContainer.insertBefore(newProfile, addProfileButton.parentElement);
            };
            reader.readAsDataURL(photoFile);

            modal.style.display = 'none';
            modalForm.reset();
        }
    });
});

// 회원 가입 관련
document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signupForm');
    const signupModal = document.getElementById('signupModal');
    const modalCloseButton = document.getElementById('modalCloseButton');

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault(); // 기본 폼 제출 동작 막기

        const formData = new FormData(signupForm);
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');

        // 비밀번호 확인
        if (password !== confirmPassword) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
        }

        fetch('/api/auth/signup', {
            method: 'POST',
            body: formData,
        }).then((response) => {
            console.log('응답 상태:', response.status); // 응답 상태 코드 로그
            if (response.status === 201) {
                signupModal.style.display = 'flex';
                return response.json();
            } else {
                throw new Error('회원가입 실패');
            }
        });
    });

    modalCloseButton.addEventListener('click', function () {
        signupModal.style.display = 'none';
        // 로그인 페이지로 이동
        window.location.href = 'login.html';
    });
});
