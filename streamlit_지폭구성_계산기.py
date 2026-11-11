import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="지폭 구성 계산기", page_icon="📐", layout="wide")

# --- Style ---
st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1450px;}
.metric-card {background:#f4f7fb; border:1px solid #dce5ef; padding:18px 20px; border-radius:12px;}
h1, h2, h3 {letter-spacing:-.03em;}
.stButton>button {border-radius:8px; font-weight:600;}
</style>
""", unsafe_allow_html=True)

st.title("📐 지폭 구성 계산기")
st.caption("TEST 등급 기준 폭을 고정하고, 4,850 mm 지폭 내 나머지 폭을 조합합니다.")

# --- Sidebar settings ---
with st.sidebar:
    st.header("기본 조건")
    deckle = st.number_input("기준 지폭 (mm)", min_value=100, max_value=20000, value=4850, step=10)
    st.markdown("**지폭별 여폭 설정**")
    edge_left = st.number_input("좌측 여폭 (mm)", min_value=0, max_value=100, value=12, step=1)
    edge_right = st.number_input("우측 여폭 (mm)", min_value=0, max_value=100, value=12, step=1)
    edge_each = edge_left
    per_width_allowance = edge_left + edge_right
    st.caption(f"지폭 1개당 여폭: {per_width_allowance} mm · 전체 여폭: {per_width_allowance*int(n)} mm")
    st.divider()
    st.header("구성 조건")
    n = st.number_input("구성 지폭 개수 (n)", min_value=1, max_value=20, value=5, step=1)
    test_width = st.number_input("TEST 등급 지폭 (a, mm)", min_value=100, max_value=deckle, value=800, step=10)
    st.caption("※ 각 지폭의 제품 폭에 좌/우 여폭 12 mm씩 별도 적용합니다.")

# 여폭은 원롤 양끝이 아니라 각 지폭의 좌/우에 각각 적용
total_allowance = (edge_left + edge_right) * int(n)
usable = deckle - total_allowance
remaining = usable - test_width
others_n = int(n)-1

c1,c2,c3,c4 = st.columns(4)
c1.metric("전체 지폭", f"{deckle:,.0f} mm")
c2.metric("유효 지폭", f"{usable:,.0f} mm", f"지폭당 여폭 {edge_left+edge_right} mm")
c3.metric("TEST 지폭", f"{test_width:,.0f} mm")
c4.metric("나머지 폭 합계", f"{remaining:,.0f} mm")

st.divider()
st.subheader("나머지 지폭 구성")

if test_width > usable:
    st.error("TEST 지폭이 유효 지폭보다 큽니다. 입력값을 확인하세요.")
elif n == 1:
    st.info("구성 지폭이 1개이므로 TEST 지폭만 배치됩니다.")
    st.success(f"사용 폭 {test_width:,.0f} mm / 잔여 {remaining:,.0f} mm")
else:
    st.markdown(f"TEST {test_width:,.0f} mm를 고정하면, 나머지 **{others_n}개 지폭**의 합은 **{remaining:,.0f} mm**입니다.")
    st.markdown("아래에서 나머지 폭의 구성 방식을 선택하세요.")

    mode = st.radio("구성 방식", ["균등 분할", "직접 입력", "후보 폭 조합 찾기"], horizontal=True)

    widths = []
    if mode == "균등 분할":
        base = remaining // others_n
        rem = remaining - base*others_n
        widths = [base + (1 if i < rem else 0) for i in range(others_n)]
        st.caption("합계가 정확히 맞도록 mm 단위 정수 폭으로 분배합니다.")
    elif mode == "직접 입력":
        default_vals = [remaining // others_n]*others_n
        default_vals[-1] += remaining - sum(default_vals)
        cols = st.columns(min(others_n, 5))
        for i in range(others_n):
            with cols[i % len(cols)]:
                val = st.number_input(f"나머지 폭 {i+1} (mm)", min_value=0, max_value=usable, value=int(default_vals[i]), step=10, key=f"w{i}")
                widths.append(int(val))
        total_input = sum(widths)
        delta = remaining-total_input
        if delta == 0:
            st.success(f"입력 합계 {total_input:,} mm = 목표 {remaining:,} mm")
        else:
            st.warning(f"입력 합계 {total_input:,} mm / 목표 {remaining:,} mm · 차이 {delta:+,} mm")
    else:
        min_w = st.number_input("최소 폭 (mm)", min_value=100, max_value=usable, value=500, step=10)
        max_w = st.number_input("최대 폭 (mm)", min_value=min_w, max_value=usable, value=min(1200, usable), step=10)
        step_w = st.number_input("폭 간격 (mm)", min_value=1, max_value=100, value=10, step=1)
        candidates = list(range(int(min_w), int(max_w)+1, int(step_w)))
        # Search combinations (repetition allowed), capped to prevent huge computation.
        solutions = []
        def dfs(start, left, target, path):
            if len(path) == others_n:
                if left == 0:
                    solutions.append(path.copy())
                return
            slots = others_n-len(path)
            if left < slots*min_w or left > slots*max_w:
                return
            for j in range(start, len(candidates)):
                x = candidates[j]
                if x > left: break
                dfs(j, left-x, target, path+[x])
                if len(solutions) >= 1000: return
        if len(candidates) <= 150 and others_n <= 8:
            dfs(0, int(remaining), int(remaining), [])
        else:
            st.warning("검색 범위가 큽니다. 폭 범위/간격 또는 지폭 개수를 줄여주세요.")
        if solutions:
            st.success(f"조건에 맞는 조합 {len(solutions):,}개 (최대 1,000개까지 표시)")
            pick = st.selectbox("조합 선택", range(len(solutions)), format_func=lambda x: f"조합 {x+1}: " + " / ".join(map(str, solutions[x])) + " mm")
            widths = solutions[pick]
        else:
            st.warning("조건에 맞는 조합을 찾지 못했습니다.")

    if widths and (mode != "직접 입력" or sum(widths)==remaining):
        all_widths = [int(test_width)] + [int(x) for x in widths]
        total = sum(all_widths)
        st.divider()
        st.subheader("구성 결과")
        df = pd.DataFrame({
            "순번": range(1, len(all_widths)+1),
            "등급": ["TEST"] + ["일반"]*others_n,
            "제품 폭 (mm)": all_widths,
            "좌 여폭 (mm)": [edge_left]*len(all_widths),
            "우 여폭 (mm)": [edge_right]*len(all_widths),
            "필요 원폭 (mm)": [x+edge_left+edge_right for x in all_widths],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        m1,m2,m3 = st.columns(3)
        m1.metric("제품 폭 합계", f"{total:,} mm")
        m2.metric("여폭 포함 필요 폭", f"{total+(edge_left+edge_right)*len(all_widths):,} mm")
        m3.metric("유효폭 대비 잔여", f"{usable-total:,} mm")
        # Large roll visualization: each slice is proportional to its width.
        st.markdown("#### 원롤 분할 시각화")
        st.caption("원롤을 위에서 내려다본 형태입니다. 각 세그먼트 폭은 입력한 제품 폭에 비례합니다.")

        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, Circle
        from matplotlib import font_manager

        # Korean font fallback for Windows/Linux environments
        font_candidates = ["Malgun Gothic", "NanumGothic", "AppleGothic", "DejaVu Sans"]
        available_fonts = {f.name for f in font_manager.fontManager.ttflist}
        chosen_font = next((name for name in font_candidates if name in available_fonts), "DejaVu Sans")
        plt.rcParams["font.family"] = chosen_font
        plt.rcParams["axes.unicode_minus"] = False

        fig, ax = plt.subplots(figsize=(16, 5.5))
        colors = ["#F59E0B"] + ["#2563EB" if i % 2 else "#0EA5E9" for i in range(1, len(all_widths))]
        x = 0
        for i, w in enumerate(all_widths):
            ax.add_patch(Rectangle((x, 0), w, 1, facecolor=colors[i], edgecolor="white", linewidth=2))
            ax.text(x+w/2, 0.56, f"{'TEST' if i==0 else f'폭 {i+1}'}", ha="center", va="center",
                    color="white", fontsize=13, fontweight="bold")
            ax.text(x+w/2, 0.34, f"{w:,} mm", ha="center", va="center", color="white", fontsize=12)
            x += w

        # Each product width receives its own left/right trim allowance.
        # Render allowances as narrow hatched bands around every product segment.
        product_x = 0
        for i, w in enumerate(all_widths):
            ax.add_patch(Rectangle((product_x-edge_left, 0), edge_left, 1,
                                  facecolor="#9CA3AF", edgecolor="white", hatch="//", linewidth=1))
            ax.add_patch(Rectangle((product_x+w, 0), edge_right, 1,
                                  facecolor="#9CA3AF", edgecolor="white", hatch="//", linewidth=1))
            product_x += w
        ax.text(x/2, 1.12, f"각 지폭 좌 {edge_left} mm · 우 {edge_right} mm 여폭", ha="center", va="bottom",
                fontsize=11, color="#4B5563", fontweight="bold")

        ax.set_xlim(-edge_left-20, x+edge_right+20)
        ax.set_ylim(-0.25, 1.55)
        ax.set_aspect("auto")
        ax.axis("off")
        ax.set_title(f"원롤 폭 구성  |  제품 폭 합계 {sum(all_widths):,} mm  +  지폭별 여폭 {edge_each*2*len(all_widths):,} mm",
                     fontsize=16, fontweight="bold", pad=18)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.caption("주황색 = TEST 지폭 · 파란색 계열 = 일반 지폭 · 각 구획 양쪽 회색 사선 = 해당 지폭 여폭")
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 구성 결과 CSV 다운로드", csv, "지폭구성결과.csv", "text/csv")
