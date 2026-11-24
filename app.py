import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="맞춤형 식물 물주기 시기 분석기", layout="centered")

# ---------------------------------------------------------
# 1. 리스트(list) 선언: 식물 종류별 기본 물주기 간격 및 원리 데이터
# ---------------------------------------------------------
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]
plant_principles = [
    (
        "낮에 기공을 닫고 밤에 여는 CAM 광합성을 통해 증산 작용을 극도로"
        " 억제하므로 수분 소모가 매우 느립니다. 흙이 완전히 말랐을 때 흠뻑"
        " 주세요."
    ),
    (
        "잎과 줄기의 저수 조직에 수분을 저장하고 두꺼운 큐티클층을 가져 증산"
        " 속도가 느린 편입니다. 아래쪽 잎이 살짝 말랑해질 때 흙 위로 급수하세요."
    ),
    (
        "잎 면적이 넓고 기공이 많아 증산 작용이 활발하며, 증산 인력으로 뿌리의"
        " 삼투압 수분 흡수가 빠르게 일어납니다. 겉흙이 마르면 충분히 주세요."
    ),
    (
        "잎이 얇고 증산량이 많아 팽압 유지에 많은 수분이 필요합니다. 수분이"
        " 부족하면 잎이 처지므로 겉흙이 마르기 시작할 때 바로 급수하세요."
    ),
]


# ---------------------------------------------------------
# 2. 함수(def) 정의: 물주기 상태 및 예상 남은 날짜 판별
# ---------------------------------------------------------
def check_watering(plant, temperature, humidity, last_days):
    # [반복구조 for] 리스트를 순회하며 선택한 식물의 기본 물주기 기준과 원리 찾기
    watering_interval = 7
    selected_principle = ""

    for i in range(len(plants)):
        if plants[i] == plant:
            watering_interval = watering_days[i]
            selected_principle = plant_principles[i]
            break

    # [선택구조 if-elif-else] 주변 온도와 습도에 따른 증산 작용 속도 반영
    if temperature >= 28:
        watering_interval = watering_interval - 1
    elif temperature <= 15:
        watering_interval = watering_interval + 1

    if humidity <= 35:
        watering_interval = watering_interval - 1
    elif humidity >= 70:
        watering_interval = watering_interval + 1

    # 최소 급수 간격 1일 유지
    if watering_interval < 1:
        watering_interval = 1

    # 예상 물주기까지 남은 날짜 계산
    remaining_days = watering_interval - last_days
    if remaining_days < 0:
        remaining_days = 0

    # [선택구조 if-elif-else] 물주기 상태 판별 및 안내 메시지 생성
    if last_days >= watering_interval:
        water_status = "시기됨"
        guide_message = (
            "물주기 시기가 되었으니 흙을 확인하고 충분한 물을 주세요! (증산"
            " 작용으로 토양 수분 고갈)"
        )
    elif last_days >= watering_interval - 2:
        water_status = "곧"
        guide_message = (
            f"곧 물을 줄 시기입니다. 약 {remaining_days}일 뒤에 흙의 건조"
            " 상태를 확인하세요."
        )
    else:
        water_status = "아직"
        guide_message = (
            "아직 물을 줄 시기가 아닙니다. 토양 내 수분과 뿌리의 삼투 흡수가"
            " 안정적으로 유지되고 있습니다."
        )

    return (
        water_status,
        remaining_days,
        guide_message,
        watering_interval,
        selected_principle,
    )


# ---------------------------------------------------------
# 3. Streamlit 웹 UI 구성 및 사용자 입력 받기
# ---------------------------------------------------------
st.title("🌱 맞춤형 식물 물주기 시기 분석기")
st.write(
    "식물 종류와 주변 환경(온도·습도)에 따른 **증산 작용 및 수분 흡수"
    " 원리**를 분석합니다."
)

st.divider()

# 사용자 입력 위젯 (모든 변수명 snake_case 적용)
selected_plant = st.selectbox("식물 종류 선택", plants)
temperature = st.slider("주변 온도 (°C)", min_value=0, max_value=40, value=25)
humidity = st.slider("주변 습도 (%)", min_value=0, max_value=100, value=50)
last_days = st.number_input(
    "마지막 물주기 (며칠 전)", min_value=0, max_value=100, value=11, step=1
)

# ---------------------------------------------------------
# 4. 버튼 클릭 시 함수 호출 및 분석 결과 출력
# ---------------------------------------------------------
if st.button("물주기 시기 분석", type="primary", use_container_width=True):
    (
        water_status,
        remaining_days,
        guide_message,
        adjusted_interval,
        principle_text,
    ) = check_watering(selected_plant, temperature, humidity, last_days)

    st.divider()

    # 강조 수치 표시 (예상 물주기까지 남은 시간)
    st.metric(
        label="예상 물주기까지 남은 시간",
        value=f"[{remaining_days}일]",
        delta=f"상태: {water_status} (환경 반영 주기: {adjusted_interval}일)",
    )

    # 물주기 상태별 안내 메시지 출력
    if water_status == "시기됨":
        st.error(f"🚨 {guide_message}")
    elif water_status == "곧":
        st.warning(f"⚠️ {guide_message}")
    else:
        st.success(f"✅ {guide_message}")

    # 온도 및 습도 상태 판별 (결과표 표시용)
    if temperature > 27:
        temp_status = "높음 (증산 촉진)"
    elif temperature < 18:
        temp_status = "낮음 (증산 둔화)"
    else:
        temp_status = "보통"

    if humidity > 65:
        hum_status = "다습 (증산 억제)"
    elif humidity < 40:
        hum_status = "건조 (증산 촉진)"
    else:
        hum_status = "보통"

    # 환경 분석 결과표 (DataFrame) 출력
    st.subheader("📊 환경 분석 결과표")
    result_df = pd.DataFrame({
        "항목": ["식물종류", "온도", "습도", "마지막 물주기", "물주기 상태"],
        "입력 값": [
            selected_plant,
            f"{temperature}도",
            f"{humidity}%",
            f"{last_days}일 전",
            water_status,
        ],
        "상태": [
            "확인",
            temp_status,
            hum_status,
            f"권장 주기 {adjusted_interval}일",
            f"남은 시간 [{remaining_days}일]",
        ],
    })
    st.dataframe(result_df, use_container_width=True, hide_index=True)

    # 증산 작용 및 흡수 원리 연계 해설
    st.info(
        f"**🔬 {selected_plant}의 증산 작용 및 관리 원리**\n\n{principle_text}"
    )
