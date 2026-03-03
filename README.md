# 🐾 Pooweep Pet Store Automation

> **pooweep.co.kr** - 한국 반려동물 이커머스 자동화 시스템
>
> ## 📌 프로젝트 개요
>
> Cafe24 기반 펫케어 쇼핑몰(pooweep.co.kr)의 상품 소싱, 판매, 마케팅, 관리를 자동화하는 스크립트 및 가이드 모음입니다.
>
> ## 🏪 스토어 현황
>
> | 항목 | 내용 |
> |------|------|
> | 도메인 | pooweep.co.kr |
> | 플랫폼 | Cafe24 |
> | 상품수 | 47개 |
> | 소싱방식 | Cafe24 드랍쉬핑 |
> | 카테고리 | 사료/간식, 용품, 외출/이동, 패션, 건강/위생 |
>
> ## 📂 프로젝트 구조
>
> ```
> pooweep-pet-automation/
> ├── cafe24_api_manager.py    # Cafe24 Open API 자동화 (상품/주문/고객)
> ├── requirements.txt         # Python 패키지 의존성
> ├── .env.example            # 환경변수 템플릿
> ├── docs/
> │   └── PLATFORM_SETUP_GUIDE.md  # 플랫폼별 가입/설정 가이드
> └── README.md
> ```
>
> ## 🚀 빠른 시작
>
> ```bash
> # 1. 레포지토리 클론
> git clone https://github.com/jasonjkkim-netizen/pooweep-pet-automation.git
> cd pooweep-pet-automation
>
> # 2. 가상환경 생성 및 활성화
> python -m venv venv
> source venv/bin/activate  # Windows: venv\Scripts\activate
>
> # 3. 패키지 설치
> pip install -r requirements.txt
>
> # 4. 환경변수 설정
> cp .env.example .env
> # .env 파일을 편집하여 API 키 입력
>
> # 5. 자동화 실행
> python cafe24_api_manager.py
> ```
>
> ## 🔧 주요 기능
>
> ### cafe24_api_manager.py
> - **상품 관리**: 목록 조회, 상세 조회, 정보 수정
> - - **주문 관리**: 주문 조회, 상태 변경 자동화
>   - - **고객 관리**: 회원 목록 조회
>     - - **재고 관리**: 재고 부족 상품 자동 알림
>       - - **일일 리포트**: 매일 자동 생성
>         - - **스케줄러**: 30분마다 주문 처리, 매일 리포트 생성
>          
>           - ## 📋 플랫폼별 가입 가이드
>          
>           - 자세한 가입 순서는 [docs/PLATFORM_SETUP_GUIDE.md](docs/PLATFORM_SETUP_GUIDE.md) 참고
>          
>           - | 플랫폼 | 목적 | 우선순위 |
> |--------|------|---------|
> | Cafe24 마켓플러스 | 멀티채널 판매 (네이버/쿠팡/11번가) | ⭐⭐⭐ |
> | 네이버 스마트스토어 | 판매채널 확장 | ⭐⭐⭐ |
> | 채널톡 | CRM/고객응대 자동화 | ⭐⭐ |
> | 네이버 광고 | 검색광고 유입 | ⭐⭐ |
> | 쿠팡 | 판매채널 확장 | ⭐⭐ |
> | 카카오모먼트 | 디스플레이 마케팅 | ⭐ |
> | 사방넷 | 고급 통합관리 | ⭐ |
>
> ## ⚡ Cafe24 내장 자동화 (마켓플러스)
>
> Cafe24 마켓플러스를 통해 별도 외부 솔루션 없이도 멀티채널 판매가 가능합니다:
> - 네이버 쇼핑, 쿠팡, 11번가, G마켓/옥션 등 일괄 연동
> - - 상품 일괄 등록/수정
>   - - 주문 통합 관리 및 재고 자동 동기화
>    
>     - 설정 경로: **Cafe24 관리자 > 마켓플러스**
>    
>     - ## 🛠 커스터마이징
>    
>     - 이 프로젝트는 다른 방향에서 수정할 수 있도록 모듈화되어 있습니다:
>
> - `cafe24_api_manager.py`의 `Cafe24APIManager` 클래스를 상속하여 커스텀 기능 추가
> - - `.env` 파일로 설정값 관리 (코드 수정 없이 환경변수만 변경)
>   - - 스케줄러 시간/주기는 `run_scheduler()` 함수에서 자유롭게 수정
>    
>     - ## 📞 스토어 정보
>    
>     - - **상호**: 베리스
>       - - **대표**: 김종국
>         - - **주소**: 서울특별시 용산구 이촌동 412
>           - - **연락처**: 010-9169-9335
>             - 
