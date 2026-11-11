# 지폭 구성 계산기 (v2)

Streamlit 기반 지폭 구성 계산기입니다.

## 파일
- `streamlit_app.py`: Streamlit 앱 본체
- `requirements.txt`: Python 패키지
- `packages.txt`: Streamlit Cloud 시스템 패키지

## Streamlit Community Cloud 배포
1. 이 폴더의 파일 4개를 GitHub 저장소 루트에 업로드합니다.
2. Streamlit Community Cloud에서 저장소와 브랜치를 선택합니다.
3. Main file path는 `streamlit_app.py`로 지정합니다.
4. Deploy를 누릅니다.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 주요 기능
- 전체 지폭 및 지폭 개수 설정
- TEST 폭 설정
- 지폭별 좌·우 여폭 설정
- 균등 분할, 직접 입력, 폭 조합 검색
- 원통형 롤 분할 SVG 시각화
- 지폭별 상세표, 구성 요약, 확인 항목
- CSV 내보내기
