import streamlit as st
import pandas as pd

# 글씨체 바꾸기 (구글 폰트 - 고운돋움)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
html, body, [class*="css"], h1, h2, h3, p, label, button, div, td, th {
    font-family: 'Gowun Dodum', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# 1) 사용자가 앱에 접속함
st.title("식물 물주기 시기 예측기")

# 2) 리스트 선언 - 식물 종류별 기본 물주기 간격
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]


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

    # 마지막 물준 날짜랑 비교해서 메시지 정하기
    if last_days >= interval:
        msg = "물을 줄 시기가 되었습니다. 흙이 말랐는지 확인하고 물을 주세요."
    elif last_days >= interval - 2:
        msg = "곧 물을 줄 시기입니다. 흙 상태를 자주 확인해 주세요."
    else:
        msg = "아직 물을 줄 시기가 아닙니다. 흙의 상태를 확인해 주세요."

    left = interval - last_days
    if left < 0:
        left = 0

    return msg, left, temp_state, hum_state


# 3) 입력 받기
plant = st.selectbox("식물 종류", plants)
temperature = st.slider("주변 온도 (도)", 0, 40, 25)
humidity = st.slider("주변 습도 (%)", 0, 100, 50)
last_days = st.number_input("마지막으로 물 준 날 (며칠 전)", 0, 60, 0)

# 4) 버튼 누르면 함수 실행
if st.button("물주기 시기 분석"):
    msg, left, temp_state, hum_state = check_watering(plant, temperature, humidity, last_days)

    st.write(msg)

    # 7) 결과 출력 - 남은 날짜는 강조 수치, 분석 결과는 표로
    st.metric("물주기까지 남은 날짜", str(left) + "일")

    df = pd.DataFrame({
        "항목": ["식물 종류", "온도", "습도"],
        "입력값": [plant, str(temperature) + "도", str(humidity) + "%"],
        "상태": ["확인", temp_state, hum_state]
    })
    st.table(df)

    st.write("식물 관리 안내: 흙이 충분히 말랐는지 확인한 후 물을 주세요.")
    st.caption("※ 실제 물주기 시기는 흙의 건조 상태와 생육 환경에 따라 달라질 수 있음")
