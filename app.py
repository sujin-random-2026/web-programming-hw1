import streamlit as st
import anthropic
import base64
import json

# 글씨체 바꾸기 (구글 폰트 - 주아)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
html, body, [class*="css"], h1, h2, h3, p, label, button, div {
    font-family: 'Jua', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

st.title("사진으로 수학 변형 문제 만들기")

# 리스트 - 변형 방식
modes = ["숫자만 바꾸기", "조건까지 바꾸기", "난이도 올리기", "난이도 낮추기"]
mode_text = [
    "숫자만 바꾸고 문제 구조와 난이도는 그대로",
    "숫자와 조건을 바꾸되 같은 개념을 쓰도록",
    "같은 개념을 쓰되 한 단계 더 어렵게",
    "같은 개념을 쓰되 계산이 쉽게",
]

# API 키는 .streamlit/secrets.toml 파일에 ANTHROPIC_API_KEY = "..." 로 저장
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


def make_problems(image_bytes, image_type, count, mode):
    # 선택한 변형 방식 설명 찾기
    how = ""
    for i in range(len(modes)):
        if modes[i] == mode:
            how = mode_text[i]

    image_data = base64.b64encode(image_bytes).decode("utf-8")

    prompt = ("사진 속 수학 문제를 읽고 변형 문제를 " + str(count) + "개 만들어줘. "
              "변형 방식: " + how + ". "
              "정답은 직접 풀어서 확인하고, 수식은 $ $로 감싸줘. "
              "다른 말 없이 아래 JSON 형식으로만 답해줘.\n"
              '{"original": "원래 문제", "problems": [{"problem": "문제", "answer": "정답", "solution": "풀이"}]}')

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": image_type, "data": image_data}},
                {"type": "text", "text": prompt},
            ],
        }],
    )

    text = response.content[0].text
    # 앞뒤에 ```json 같은게 붙어있으면 빼기
    start = text.find("{")
    end = text.rfind("}")
    return json.loads(text[start:end + 1])


# 입력 받기
how_input = st.radio("사진 넣는 방법", ["카메라로 찍기", "파일 올리기"])
if how_input == "카메라로 찍기":
    photo = st.camera_input("문제를 찍어주세요")
else:
    photo = st.file_uploader("문제 사진 올리기", type=["png", "jpg", "jpeg"])

count = st.slider("만들 문제 수", 1, 10, 3)
mode = st.selectbox("변형 방식", modes)

if st.button("변형 문제 만들기"):
    if photo is None:
        st.write("먼저 문제 사진을 넣어주세요!")
    else:
        with st.spinner("문제 만드는 중..."):
            try:
                result = make_problems(photo.getvalue(), photo.type, count, mode)
            except Exception as e:
                result = None
                st.write("오류가 났어요. 다시 시도해 주세요.")
                st.write(e)

        if result is not None:
            st.subheader("원래 문제")
            st.write(result["original"])

            st.subheader("변형 문제")
            num = 1
            for p in result["problems"]:
                st.markdown("**" + str(num) + "번.** " + p["problem"])
                with st.expander("정답 / 풀이 보기"):
                    st.write("정답: " + p["answer"])
                    st.write(p["solution"])
                num = num + 1

            st.caption("※ AI가 만든 문제라서 정답이 틀릴 수도 있으니 꼭 확인하기")
