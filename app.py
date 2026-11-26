import streamlit as st
import pandas as pd

# 글씨체, 배경색 바꾸기
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
.tip {
    background-color: #ffffff;
    border-left: 6px solid #6fbf73;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# 1) 사용자가 앱에 접속함
st.title("🌱 식물 물주기 시기 예측기")
st.write("식물 종류와 주변 환경을 입력하면 언제 물을 주면 좋을지 알려줘요!")

# 2) 리스트 선언 - 식물 종류별 기본 물주기 간격
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]
icons = ["🌵", "🪴", "🌿", "🌸"]
tips = [
    "선인장은 물을 너무 자주 주면 뿌리가 썩어요. 흙이 완전히 마르면 주세요.",
    "다육식물은 잎에 물을 저장해요. 잎이 쭈글해지면 물이 필요하다는 신호예요.",
    "몬스테라는 겉흙이 2~3cm 정도 마르면 물을 듬뿍 주세요.",
    "스파티필름은 물이 부족하면 잎이 축 처져요. 흙이 촉촉하게 유지되게 해주세요.",
]

# 사이드바 - 식물별 기본 정보
st.sidebar.header("📖 식물 도감")
for i in range(len(plants)):
    st.sidebar.write(icons[i] + " " + plants[i] + " : " + str(watering_days[i]) + "일마다")
st.sidebar.caption("※ 기본 간격이고 온도, 습도에 따라 달라져요")


def check_watering(plant, temperature, humidity, last_days):
    # 6) 반복 - 리스트를 돌면서 선택한 식물의 물주기 간격 찾기
    interval = 0
    for i in range(len(plants)):
        if plants[i] == plant:
            interval = watering_days[i]

    # 5) 조건 판단 - 온도, 습도 확인
    # 덥거나 건조하면 증산 작용이 많아져서 물이 빨리 마른다
    if temperature >= 30:
        temp_state = "높음"
        interval = interval - 2
    elif temperature <= 15:
        temp_state = "낮음"
        interval = interval + 2
    else:
        temp_state = "보통"

    if humidity <= 30:
        hum_state = "건조"
        interval = interval - 1
    elif humidity >= 70:
        hum_state = "습함"
        interval = interval + 1
    else:
        hum_state = "보통"

    if interval < 1:
        interval = 1

    # 마지막 물준 날짜랑 비교해서 상태 정하기
    if last_days >= interval:
        status = "시기 됨"
        msg = "물을 줄 시기가 되었습니다. 흙이 말랐는지 확인하고 물을 주세요."
    elif last_days >= interval - 2:
        status = "곧"
        msg = "곧 물을 줄 시기입니다. 흙 상태를 자주 확인해 주세요."
    else:
        status = "아직"
        msg = "아직 물을 줄 시기가 아닙니다. 흙의 상태를 확인해 주세요."

    left = interval - last_days
    if left < 0:
        left = 0

    return status, msg, left, interval, temp_state, hum_state


# 3) 입력 받기
plant = st.selectbox("식물 종류", plants)

col1, col2 = st.columns(2)
with col1:
    temperature = st.slider("🌡️ 주변 온도 (도)", 0, 40, 25)
with col2:
    humidity = st.slider("💧 주변 습도 (%)", 0, 100, 50)

last_days = st.number_input("마지막으로 물 준 날 (며칠 전)", 0, 60, 0)

# 4) 버튼 누르면 함수 실행
if st.button("물주기 시기 분석", use_container_width=True):
    status, msg, left, interval, temp_state, hum_state = check_watering(plant, temperature, humidity, last_days)

    # 선택한 식물 아이콘이랑 팁 찾기
    icon = ""
    tip = ""
    for i in range(len(plants)):
        if plants[i] == plant:
            icon = icons[i]
            tip = tips[i]

    st.subheader(icon + " " + plant + " 분석 결과")

    # 상태에 따라 메시지 색 다르게
    if status == "시기 됨":
        st.error(msg)
    elif status == "곧":
        st.warning(msg)
    else:
        st.success(msg)

    # 7) 결과 출력 - 강조 수치
    m1, m2, m3 = st.columns(3)
    m1.metric("물주기까지 남은 날짜", str(left) + "일")
    m2.metric("이번 물주기 간격", str(interval) + "일")
    m3.metric("마지막 물주기", str(last_days) + "일 전")

    # 흙 수분 게이지 (남은 날짜 비율로 대충 표시)
    water = int(left / interval * 100)
    st.write("흙 속 수분 (예상) : " + str(water) + "%")
    st.progress(water)

    # 환경 분석 결과 표
    df = pd.DataFrame({
        "항목": ["식물 종류", "온도", "습도"],
        "입력값": [plant, str(temperature) + "도", str(humidity) + "%"],
        "상태": ["확인", temp_state, hum_state]
    })
    st.table(df)

    # 식물별 관리 팁
    st.markdown('<div class="tip">💡 <b>' + plant + ' 관리 팁</b><br>' + tip + '</div>', unsafe_allow_html=True)

    # 다른 식물이랑 물주기 간격 비교 그래프
    st.subheader("📊 식물별 기본 물주기 간격 비교")
    chart = pd.DataFrame({"물주기 간격(일)": watering_days}, index=plants)
    st.bar_chart(chart)

    st.caption("※ 실제 물주기 시기는 흙의 건조 상태와 생육 환경에 따라 달라질 수 있음")
