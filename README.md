# 지폭 구성 계산기 v5

Streamlit 기반 지폭 구성 시뮬레이터입니다.

## 실행

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Streamlit Community Cloud

- Branch: `main`
- Main file path: `streamlit_app.py`

## v5 변경사항

- 롤 시각화 바로 아래에 각 지폭과 정렬된 제품 폭 입력란 추가
- TEST 폭 입력은 사이드바와 롤 아래 입력란이 양방향 동기화
- 일반 지폭을 롤 아래에서 수정하면 폭 직접 입력 모드로 자동 전환
- 폭 합계가 일시적으로 맞지 않아도 입력란과 롤 미리보기가 유지되어 나머지 폭을 계속 수정 가능
- 실제 합계가 맞지 않을 때는 확인 패널이 경고 상태로 전환
- 왼쪽 계산기와 오른쪽 메인 화면의 상단 여백 축소
- 계산·표·요약·CSV는 변경된 지폭과 순서를 반영
