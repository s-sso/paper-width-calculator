# 지폭 구성 계산기 v6

## GitHub 교체 파일
- `streamlit_app.py`
- `roll_component/index.html` (필수: 롤 내부 입력 컨트롤을 위한 로컬 Streamlit 컴포넌트)

기존 `requirements.txt`, `packages.txt`는 그대로 사용할 수 있습니다. 추가 Python 패키지는 없습니다.

Streamlit Cloud Main file path: `streamlit_app.py`

롤 이미지 안의 각 지폭 폭 숫자를 직접 클릭해 수정할 수 있습니다. 일반 지폭을 수정하면 폭 직접 입력 모드로 전환됩니다. TEST 지폭은 왼쪽 TEST 입력값과 동기화됩니다. 왼쪽 사이드바 접기 버튼은 숨김 처리되어 항상 펼쳐진 상태로 유지됩니다.
