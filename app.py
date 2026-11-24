import pandas as pd
import streamlit as st

# 식물 종류별 기본 물주기 간격과 특징 리스트
plants = ["선인장", "다육식물", "몬스테라", "스파티필름"]
watering_days = [14, 10, 7, 5]
plant_info = [
    (
        "낮에 기공을 닫고 밤에 여는 CAM 광합성을 해서 증산 작용이 매우 적습니다."
        " 흙이 완전히 말랐을 때 물을 주세요."
    ),
    (
        "잎과 줄기에 수분을 저장하고 큐티클층이 두꺼워 증산 속도가 느립니다."
        " 아래쪽 잎이 살짝 말랑해질 때 물을 주세요."
    ),
    (
        "잎이 넓고 기공이 많아 증산 작용이 활발합니다. 증산 인력으로 뿌리의"
        " 삼투압 흡수가 빠르니 겉흙이 마르면 물을 주세요."
    ),
    (
        "잎이 얇고 증산량이 많아 수분이 많이 필요합니다. 물이 부족하면 잎이"
        " 처지므로 겉흙이 마르기 시작할 때 바로 주세요."
    ),
]


# 물주기 시기와 상태를 계산하는 함수
def check_watering(plant, temperature, humidity, last_days):
  # for문으로 선택한 식물의 기본 물주기 일수와 설명 찾기
  watering_interval = 7
  info_text = ""

  for i in range(len(plants)):
    if plants[i] == plant:
      watering_interval = watering_days[i]
      info_text = plant_info[i]
      break

  # 온도와 습도에 따른 증산 작용 속도 반영
  if temperature >= 28:
    watering_interval = watering_interval - 1
  elif temperature <= 15:
    watering_interval = watering_interval + 1

  if humidity <= 35:
    watering_interval = watering_interval - 1
  elif humidity >= 70:
    watering_interval = watering_interval + 1

  if watering_interval < 1:
    watering_interval = 1

  # 남은 날짜 계산
  remain_days = watering_interval - last_days
  if remain_days < 0:
    remain_days = 0

  # 조건문으로 물주기 상태 판별
  if last_days >= watering_interval:
    status = "시기됨"
    message = (
        "물주기 시기가 되었습니다. 흙의 건조 상태를 확인하고 물을 주세요."
    )
  elif last_days >= watering_interval - 2:
    status = "곧"
    message = f"곧 물을 줄 시기입니다. 약 {remain_days}일 뒤에 물을 주세요."
  else:
    status = "아직"
    message = (
        "아직 물을 줄 시기가 아닙니다. 토양 수분과 뿌리의 삼투 흡수가"
        " 안정적입니다."
    )

  return status, remain_days, message, watering_interval, info_text


# 화면 제목 및 설명
st.title("맞춤형 식물 물주기 시기 확인 앱")
st.write(
    "식물 종류와 주변 온도, 습도에 따른 증산 작용 원리를 이용해 물주기 시기를"
    " 알려줍니다."
)

# 사용자 입력 받기
selected_plant = st.selectbox("식물 종류를 선택하세요", plants)
temperature = st.slider("주변 온도 (°C)", 0, 40, 25)
humidity = st.slider("주변 습도 (%)", 0, 100, 50)
last_days = st.number_input("마지막으로 물 준 날 (며칠 전)", 0, 100, 11)

# 버튼 클릭 시 결과 출력
if st.button("물주기 시기 분석"):
  status, remain_days, message, final_days, info_text = check_watering(
      selected_plant, temperature, humidity, last_days
  )

  st.subheader(f"예상 물주기까지 남은 시간: [{remain_days}일]")

  if status == "시기됨":
    st.error(message)
  elif status == "곧":
    st.warning(message)
  else:
    st.success(message)

  # 온도와 습도 상태 정리
  if temperature > 27:
    temp_state = "높음 (증산 활발)"
  elif temperature < 18:
    temp_state = "낮음 (증산 둔화)"
  else:
    temp_state = "보통"

  if humidity > 65:
    hum_state = "다습 (증산 억제)"
  elif humidity < 40:
    hum_state = "건조 (증산 촉진)"
  else:
    hum_state = "보통"

  # 결과표 출력
  st.write("### 환경 분석 결과표")
  result_table = pd.DataFrame({
      "항목": ["식물종류", "온도", "습도", "마지막 물주기"],
      "입력 값": [
          selected_plant,
          f"{temperature}도",
          f"{humidity}%",
          f"{last_days}일 전",
      ],
      "상태": ["확인", temp_state, hum_state, f"권장 주기 {final_days}일"],
  })
  st.dataframe(result_table, hide_index=True)

  # 식물별 원리 및 관리 방법 출력
  st.write(f"**[{selected_plant}의 증산 작용 및 관리 방법]**")
  st.info(info_text)
