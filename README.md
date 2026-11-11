# 지폭 구성 계산기 v4

Streamlit 기반 지폭 구성 시뮬레이터입니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Streamlit Community Cloud 배포 설정

- Repository: GitHub 저장소
- Branch: `main`
- Main file path: `streamlit_app.py`

## v4 주요 변경사항

- TEST 지폭을 1~5개까지 개별 설정
- TEST 1~TEST 5 각각의 제품 폭과 배치 위치 선택
- 지정한 TEST 배치 순서에 따라 롤 시각화, 상세 표, 요약 순서 동기화
- SVG의 `preserveAspectRatio`를 사용해 글자가 늘어나거나 찌그러지는 문제 방지
- 롤 위의 좌측/우측 여폭 안내 문구 제거
- 여폭은 모든 지폭의 제품 폭에 각각 적용
