import streamlit as st
import pandas as pd

# 1. 데이터 구조 (리스트): 식물 종류별 기본 물주기 간격(일)
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]


# 2. 함수 (def): 물주기 상태와 남은 날짜를 계산해 돌려줌
def check_watering(plant, temperature, humidity, last_days):
    # 4. 반복문 (for): 리스트를 돌며 선택한 식물의 기본 간격 찾기
    watering_interval = 0
    for i in range(len(plants)):
        if plants[i] == plant:
            watering_interval = watering_days[i]

    # 온도에 따른 조정 (더우면 증산 작용이 활발 → 물이 빨리 마름)
    if temperature >= 30:
        temp_state = "높음"
        watering_interval = watering_interval - 2
    elif temperature <= 15:
        temp_state = "낮음"
        watering_interval = watering_interval + 2
    else:
        temp_state = "보통"

    # 습도에 따른 조정 (건조하면 증산 작용이 활발 → 물이 빨리 마름)
    if humidity <= 30:
        humid_state = "건조"
        watering_interval = watering_interval - 1
    elif humidity >= 70:
        humid_state = "습함"
        watering_interval = watering_interval + 1
    else:
        humid_state = "보통"

    # 간격이 1일보다 짧아지지 않도록
    if watering_interval < 1:
        watering_interval = 1

    # 3. 조건문 (if-elif-else): 물주기 상태 판단
    if last_days >= watering_interval:
        message = "물을 줄 시기가 되었습니다! 흙이 말랐는지 확인한 뒤 물을 주세요."
    elif last_days >= watering_interval - 2:
        message = "곧 물을 줄 시기입니다. 흙의 상태를 자주 확인해 주세요."
    else:
        message = "아직 물을 줄 시기가 아닙니다. 흙의 상태를 확인해 주세요."

    remaining = watering_interval - last_days
    if remaining < 0:
        remaining = 0

    return message, remaining, watering_interval, temp_state, humid_state


# ---------------- 화면 구성 ----------------
st.title("🌱 식물 물주기 시기 예측기")

plant = st.selectbox("식물 종류 선택", plants)
temperature = st.slider("주변 온도 (도)", 0, 40, 25)
humidity = st.slider("주변 습도 (%)", 0, 100, 50)
last_days = st.number_input("마지막 물주기 (며칠 전)", min_value=0, max_value=60, value=0, step=1)

if st.button("물주기 시기 분석"):
    message, remaining, interval, temp_state, humid_state = check_watering(
        plant, temperature, humidity, last_days
    )

    # 텍스트 메시지
    if remaining == 0:
        st.warning(message)
    else:
        st.info(message)

    # 테이블(표)
    st.subheader("환경 및 식물 관리 분석 결과")
    result = pd.DataFrame({
        "항목": ["식물 종류", "온도", "습도", "조정된 물주기 간격"],
        "입력값": [plant, f"{temperature} 도", f"{humidity}%", f"{interval} 일"],
        "상태": ["확인", temp_state, humid_state, "계산됨"],
    })
    st.table(result)

    # 강조 수치(Metric)
    st.metric("예상 물주기까지 남은 날짜", f"{remaining} 일")

    st.write("💧 식물 관리 안내: 흙이 충분히 말랐는지 확인한 후 물을 주세요.")
    st.caption("※ 이 결과는 프로그램의 예시이며, 실제 물주기 시기는 흙의 건조 상태와 "
               "식물의 생육 환경에 따라 달라질 수 있습니다.")
