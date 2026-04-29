import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="운영 대시보드", layout="wide")

# ── 샘플 데이터 ──────────────────────────────────────────
chart_data = pd.DataFrame({
    "Month": ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"],
    "Sales": [4300,4500,2800,3600,3750,2700,1800,2650,1850,1300,4900,2050]
})

table_data = pd.DataFrame({
    "거래내역": ["INV001","INV002","INV003","INV004","INV005"],
    "결제":     ["수금","미수금","수금","미수금","수금"],
    "총액":     [500, 200, 150, 350, 400],
    "지불방법": ["신용카드","현금","체크카드","신용카드","무통장입금"]
})

videos = {
    "멜로":    "https://www.youtube.com/watch?v=0pdqf4P9MB8",
    "미스터리": "https://www.youtube.com/watch?v=YoHD9XEInc0",
    "스릴러":  "https://www.youtube.com/watch?v=6hB3S9bIaco",
    "액션":    "https://www.youtube.com/watch?v=TcMBFSGVi1c",
}

# ── 1. 운영현황 ──────────────────────────────────────────
st.header("운영 현황")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.container(border=True).metric(label="매출 합계", value="45,231", delta="+20.1%")
    with col2:
        st.container(border=True).metric(label="회원 가입",  value="+235",   delta="-1.21%")
    with col3:
        st.container(border=True).metric(label="판매 수익",  value="+12,234", delta="+19%")

st.write("")

# ── 2. 매출 현황 ─────────────────────────────────────────
with st.container(border=True):
    st.header("매출 현황")
    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "📈 Line Chart", "🏔 Area Chart"])

    base = alt.Chart(chart_data).encode(
        x=alt.X("Month:O", sort=None, title="Month",
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Sales:Q", title="Sales",
                axis=alt.Axis(titleAngle=0, titleAlign="right", titleY=-10))
    ).properties(width="container").configure_view(
        strokeWidth=0
    )

    with tab1:
        chart = base.mark_bar()
        st.altair_chart(chart, use_container_width=True, theme="streamlit")
    with tab2:
        chart = base.mark_line(point=True)
        st.altair_chart(chart, use_container_width=True, theme="streamlit")
    with tab3:
        chart = base.mark_area(opacity=0.5)
        st.altair_chart(chart, use_container_width=True, theme="streamlit")

st.write("")

# ── 3. 거래내역 (Read Only) ──────────────────────────────
with st.container(border=True):
    st.subheader("📋 거래내역 (Read Only)")
    st.dataframe(table_data, use_container_width=True)

st.write("")

# ── 4. 거래내역 (Editable) ───────────────────────────────
with st.container(border=True):
    st.subheader("✏️ 거래내역 (Editable)")
    edited_df = st.data_editor(
        table_data,
        use_container_width=True,
        column_config={
            "거래내역": st.column_config.TextColumn(disabled=True),
            "결제": st.column_config.SelectboxColumn(
                options=["수금", "미수금"]
            ),
            "총액": st.column_config.NumberColumn(
                min_value=0, max_value=1000
            ),
            "지불방법": st.column_config.SelectboxColumn(
                options=["신용카드", "현금", "체크카드", "무통장입금"]
            ),
        }
    )

st.write("")

# ── 5. 지불 방법 선택 + 6. 찬/반 투표 ──────────────────────

# 투표 session_state 초기화
if "vote_submitted" not in st.session_state:
    st.session_state.vote_submitted = False
if "vote_type" not in st.session_state:
    st.session_state.vote_type = None
if "vote_reason" not in st.session_state:
    st.session_state.vote_reason = ""

@st.dialog("의견을 말씀해주세요.")
def show_opinion(vote_type):
    label = "찬성 하는 이유는 무엇입니까?" if vote_type == "찬성" else "반대 하는 이유는 무엇입니까?"
    st.markdown(label)
    reason = st.text_area("그 이유는...", label_visibility="collapsed")
    if st.button("제출"):
        st.session_state.vote_submitted = True
        st.session_state.vote_type = vote_type
        st.session_state.vote_reason = reason
        st.rerun()

with st.container(border=True):
    st.subheader("지불 방법 선택")
    col_pay, col_vote = st.columns(2)

    with col_pay:
        with st.container(border=True):
            st.markdown("**지불 방법을 선택하세요**")
            payment = st.radio(
                label="지불 방법",
                options=["신용카드", "현금", "체크카드"],
                captions=["국민/신한/우리", "현금영수증", "KB/신한"],
                label_visibility="collapsed"
            )
            if payment == "신용카드":
                st.info("💳 신용카드 결제 시 수수료 면제 혜택이 적용됩니다.")
            elif payment == "현금":
                st.success("💵 현금 결제 시 10% 할인 혜택이 적용됩니다.")
            elif payment == "체크카드":
                st.warning("💳 체크카드 결제 시 3% 할인 혜택이 적용됩니다.")

    with col_vote:
        with st.container(border=True):
            st.markdown("**찬/반 투표**")
            if st.session_state.vote_submitted:
                # 제출 후 결과 표시
                reason = st.session_state.vote_reason
                if st.session_state.vote_type == "찬성":
                    st.success(f"찬성 하시는 이유는 '{reason}' 입니다" if reason else "찬성에 투표하셨습니다.")
                else:
                    st.warning(f"반대 하시는 이유는 '{reason}' 입니다" if reason else "반대에 투표하셨습니다.")
                if st.button("다시 투표하기", use_container_width=True):
                    st.session_state.vote_submitted = False
                    st.session_state.vote_type = None
                    st.session_state.vote_reason = ""
                    st.rerun()
            else:
                # 투표 전 버튼 표시
                st.write("찬/반 투표에 참여해주세요.")
                v_col1, v_col2 = st.columns(2)
                with v_col1:
                    if st.button("찬성", use_container_width=True):
                        show_opinion("찬성")
                with v_col2:
                    if st.button("반대", use_container_width=True):
                        show_opinion("반대")

st.write("")

# ── 7. 서두르세요 (CTA) + 비디오 ────────────────────────
with st.container(border=True):
    cta_col1, cta_col2 = st.columns([1, 3])
    with cta_col1:
        st.markdown("## ⚠️")
    with cta_col2:
        st.markdown("### **서두르세요!**")
        st.markdown("주말 넷플릭스 주도권을 룸메에게 뺏겨서야 되겠습니까?")

    st.write("")

    # 장르 버튼 (session_state로 선택 유지)
    if "selected_genre" not in st.session_state:
        st.session_state.selected_genre = "멜로"

    genre_cols = st.columns(4)
    for i, genre in enumerate(["멜로", "미스터리", "스릴러", "액션"]):
        with genre_cols[i]:
            if st.button(genre, use_container_width=True):
                st.session_state.selected_genre = genre

    st.markdown(f"현재 선택된 장르: **{st.session_state.selected_genre}**")
    st.video(videos[st.session_state.selected_genre])

st.write("")

# ── 8. 익스팬더 ──────────────────────────────────────────
with st.container(border=True):
    st.subheader("익스팬더")
 
    expander_content = {
        "멜로":    "주말엔 무조건 멜로 정주행이지",
        "미스터리": "한번 미스터리에 빠지면 못 헤어나와요",
        "스릴러":  "어제 다 못 본 그장면에서 다시 봐야지",
        "액션":    "스트레스를 시원하게 날려버려요!",
    }
 
    for genre, content in expander_content.items():
        with st.expander(genre):
            st.write(content)