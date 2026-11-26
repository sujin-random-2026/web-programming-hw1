import streamlit as st
import pandas as pd

st.set_page_config(page_title="물주기 예측기", page_icon="🌱")

# 글씨체 바꾸기
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');
* {font-family: 'Gowun Dodum', sans-serif;}
h1, h2, h3 {font-family: 'Jua', sans-serif; color: green;}
</style>
""", unsafe_allow_html=True)

# 1) 시작
st.title("🌱 식물 물주기 시기 예측기")
st.write("식물 종류랑 주변 온도, 습도를 넣으면 언제 물 주면 되는지 알려줌!")

# 2) 리스트 선언
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]

# 추가) 식물별 관리 팁
tips = ["선인장은 물 너무 자주 주면 뿌리가 썩음. 흙이 바싹 마르면 주기",
        "다육식물은 잎에 물을 저장함. 잎이 쭈글쭈글해지면 물 주기",
        "몬스테라는 겉흙이 2~3cm 마르면 물 듬뿍 주기",
        "스파티필름은 물 부족하면 잎이 축 처짐. 흙이 너무 마르지 않게 하기"]

# 사이드바에 식물 정보
st.sidebar.title("식물별 기본 물주기")
for i in range(len(plants)):
    st.sidebar.write(plants[i], ":", watering_days[i], "일")
st.sidebar.write("")
st.sidebar.write("덥고 건조하면 증산 작용이 활발해져서 물이 더 빨리 마름!")


def check_watering(plant, temperature, humidity, last_days):
    # 6) for문으로 선택한 식물 기준 찾기
    watering_interval = 0
    for i in range(len(plants)):
        if plants[i] == plant:
            watering_interval = watering_days[i]

    # 5) 온도 습도에 따라 간격 바꾸기
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

    # 마지막 물준 날이랑 비교
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

    return status, msg, left, watering_interval, temp_state, hum_state


# 3) 입력 받기
plant = st.selectbox("식물 종류 선택", plants)
temperature = st.slider("주변 온도 (도)", 0, 40, 25)
humidity = st.slider("주변 습도 (%)", 0, 100, 50)
last_days = st.number_input("마지막 물주기 (며칠 전)", 0, 60, 0)

# 4) 버튼 누르면 실행
if st.button("물주기 시기 분석"):
    status, msg, left, interval, temp_state, hum_state = check_watering(plant, temperature, humidity, last_days)

    st.header("분석 결과")

    # 상태마다 색 다르게
    if status == "시기 됨":
        st.error(msg)
        st.balloons()
    elif status == "곧":
        st.warning(msg)
    else:
        st.success(msg)

    # 7) 표로 출력
    df = pd.DataFrame({
        "항목": ["식물 종류", "온도", "습도"],
        "입력값": [plant, str(temperature) + " 도", str(humidity) + "%"],
        "상태": ["확인", temp_state, hum_state]
    })
    st.table(df)

    # 강조 수치
    st.metric("예상 물주기까지 남은 날짜", str(left) + " 일")

    st.write("식물 관리 안내: 흙이 충분히 말랐는지 확인한 후 물을 주세요.")

    # 추가) 선택한 식물 팁 보여주기
    for i in range(len(plants)):
        if plants[i] == plant:
            st.info("💡 " + plant + " 팁 : " + tips[i])

    # 추가) 온도 습도 반영해서 원래 간격이랑 비교
    st.write("원래 간격이랑 지금 환경에서 간격 비교")
    for i in range(len(plants)):
        if plants[i] == plant:
            compare = pd.DataFrame({"일": [watering_days[i], interval]}, index=["기본 간격", "지금 환경"])
            st.bar_chart(compare)

    st.caption("※ 실제 물주기 시기는 흙의 건조 상태와 식물의 생육 환경에 따라 달라질 수 있음")
