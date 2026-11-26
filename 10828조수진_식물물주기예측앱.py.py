import streamlit as st
import pandas as pd

# 꾸미기 - 글씨체, 배경색, 상자
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');
html, body, [class*="css"], p, label, button, div, td, th {
    font-family: 'Gowun Dodum', sans-serif !important;
}
h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #2f6b3a;
}
.stApp {
    background-color: #f3faf1;
}
.guide {
    background-color: #ffffff;
    border-left: 6px solid #6fbf73;
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# 1) 시작: 사용자가 앱에 접속함
st.title("🌱 식물 물주기 시기 예측기")
st.write("식물 종류와 주변 온도, 습도를 입력하면 물을 줄 시기를 알려드려요.")
st.divider()

# 2) 리스트 선언: 식물 종류별 기본 물주기 간격
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]


def check_watering(plant, temperature, humidity, last_days):
    # 6) 반복: 리스트를 돌면서 선택한 식물의 물주기 기준 찾기
    watering_interval = 0
    for i in range(len(plants)):
        if plants[i] == plant:
            watering_interval = watering_days[i]

    # 5) 조건 판단: 온도, 습도 확인
    # 덥거나 건조하면 증산 작용이 많아져서 흙이 빨리 마른다
    if temperature >= 30:
        temp_state = "높음"
        watering_interval = watering_interval - 2
    elif temperature <= 15:
        temp_state = "낮음"
        watering_interval = watering_interval + 2
    else:
        temp_state = "보통"

    if humidity <= 30:
        hum_state = "건조"
        watering_interval = watering_interval - 1
    elif humidity >= 70:
        hum_state = "습함"
        watering_interval = watering_interval + 1
    else:
        hum_state = "보통"

    if watering_interval < 1:
        watering_interval = 1

    # 마지막 물주기 날짜랑 비교 (시기 됨 / 곧 / 아직)
    if last_days >= watering_interval:
        status = "시기 됨"
        msg = "물을 줄 시기가 되었습니다. 흙의 상태를 확인하고 물을 주세요."
    elif last_days >= watering_interval - 2:
        status = "곧"
        msg = "곧 물을 줄 시기입니다. 흙의 상태를 확인해 주세요."
    else:
        status = "아직"
        msg = "아직 물을 줄 시기가 아닙니다. 흙의 상태를 확인해 주세요."

    left = watering_interval - last_days
    if left < 0:
        left = 0

    return status, msg, left, temp_state, hum_state


# 3) 입력 받기
plant = st.selectbox("(1) 식물 종류 선택", plants)

col1, col2 = st.columns(2)
with col1:
    temperature = st.slider("(2) 주변 온도 (도)", 0, 40, 25)
with col2:
    humidity = st.slider("(3) 주변 습도 (%)", 0, 100, 50)

last_days = st.number_input("(4) 마지막 물주기 (며칠 전)", 0, 60, 0)

# 4) 버튼 클릭 시 함수 실행
if st.button("물주기 시기 분석", use_container_width=True):
    status, msg, left, temp_state, hum_state = check_watering(plant, temperature, humidity, last_days)

    st.divider()
    st.subheader("분석 결과")

    # 텍스트 메시지 (상태에 따라 색 다르게)
    if status == "시기 됨":
        st.error(msg)
    elif status == "곧":
        st.warning(msg)
    else:
        st.success(msg)

    # 7) 결과 출력: 환경 분석 결과 표
    st.write("**환경 및 식물 관리 분석 결과**")
    df = pd.DataFrame({
        "항목": ["식물 종류", "온도", "습도"],
        "입력값": [plant, str(temperature) + " 도", str(humidity) + "%"],
        "상태": ["확인", temp_state, hum_state]
    })
    st.table(df)

    # 강조 수치
    st.metric("예상 물주기까지 남은 날짜", str(left) + " 일")

    # 식물 관리 안내
    st.markdown('<div class="guide">💧 <b>식물 관리 안내</b><br>흙이 충분히 말랐는지 확인한 후 물을 주세요.</div>',
                unsafe_allow_html=True)

    st.caption("※ 위 결과는 프로그램의 예시이며, 실제 물주기 시기는 흙의 건조 상태와 식물의 생육 환경에 따라 달라질 수 있음.")
