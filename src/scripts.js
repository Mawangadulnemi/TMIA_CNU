document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.header__menu__item');
    const sections = document.querySelectorAll('main section');
    const loginButton = document.getElementById('loginButton');
    const languageButton = document.getElementById('languageButton');
    let isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

    // 메뉴 항목 클릭 이벤트
    menuItems.forEach((item) => {
        item.addEventListener('click', function () {
            // 기존 활성화된 항목에서 active 클래스 제거
            document.querySelector('.header__menu__item.active').classList.remove('active');
            // 클릭된 항목에 active 클래스 추가
            this.classList.add('active');
        });
    });

    // 스크롤 이벤트를 통해 활성화된 메뉴 항목 업데이트
    window.addEventListener('scroll', function () {
        let currentSection = '';

        // 현재 스크롤 위치에 따라 현재 섹션을 찾음
        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 60) {
                currentSection = section.getAttribute('id');
            }
        });

        // 메뉴 항목에서 active 클래스 업데이트
        menuItems.forEach((item) => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${currentSection}`) {
                item.classList.add('active');
            }
        });
    });

    // 로그인 버튼 클릭 이벤트
    loginButton.addEventListener('click', function () {
        if (isLoggedIn) {
            // 로그아웃 로직
            isLoggedIn = false;
            localStorage.setItem('isLoggedIn', 'false');
            loginButton.textContent = 'LOGIN';
            alert('로그아웃 되었습니다.');
            window.location.href = 'index.html'; // 로그아웃 후 index.html로 이동
        } else {
            // 로그인 페이지로 이동
            window.location.href = 'login.html';
        }
    });

    // 로그인 상태 체크 (임시로 로컬 스토리지 사용)
    if (localStorage.getItem('isLoggedIn') === 'true') {
        isLoggedIn = true;
        loginButton.textContent = 'LOGOUT';
    }

    // Tmia 이용하기 버튼 클릭 이벤트
    const ctaButton = document.getElementById('ctaButton');
    if (ctaButton) {
        ctaButton.addEventListener('click', function () {
            if (isLoggedIn) {
                window.location.href = 'select.html';
            } else {
                window.location.href = 'login.html';
            }
        });
    }

    // 이용하기 (KOR) 버튼 클릭 이벤트
    if (languageButton) {
        languageButton.addEventListener('click', function () {
            if (isLoggedIn) {
                window.location.href = 'select.html';
            } else {
                window.location.href = 'login.html';
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.introduce__tab');
    const stepTitle = document.querySelector('.introduce__step-title');
    const stepDescription = document.querySelector('.introduce__step-description');
    const stepImage = document.querySelector('.introduce__step-image');

    const steps = {
        1: {
            title: '01. 로그인',
            description: '로그인 버튼을 클릭해주세요.<br>ID와 PW를 입력해주세요.',
            image: 'assets/videos/step1.png',
        },
        2: {
            title: '02. 상대방 선택',
            description: '상대방을 추가해주세요.<br>상대방 선택해주세요.',
            image: 'assets/videos/step2.png',
        },
        3: {
            title: '03. 영상 통화',
            description: '스페이스바를 꾹 누르고 말을 한 뒤 뗍니다.<br>상대방을 위해 또박또박 말해주세요.',
            image: 'assets/videos/step1.png',
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
        });
    });

    // 로그인 폼 제출 시 메인 페이지로 이동
    const loginForm = document.querySelector('.login__form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            // 로그인 성공 처리
            localStorage.setItem('isLoggedIn', 'true');
            window.location.href = 'index.html';
        });
    }
});

// Select 관련
document.addEventListener('DOMContentLoaded', function () {
    const sinhaechulProfile = document.querySelector('.profiles .profile');
    sinhaechulProfile.addEventListener('click', function () {
        window.location.href = 'conversation.html';
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
