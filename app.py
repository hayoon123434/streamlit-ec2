import streamlit as st
import json
import time

# -------------------------------------------------------
# 페이지 설정 (소개 및 기본 세팅 자료 참고)
# -------------------------------------------------------
st.set_page_config(
    page_title="🎬 영화/드라마 퀴즈",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------
# 사용자 계정 (미리 정의)
# -------------------------------------------------------
USERS = {
    "하윤": "movie123",
    "admin": "admin1234",
    "guest": "1234",
}

# -------------------------------------------------------
# 캐싱 적용 (성능 최적화 및 캐싱 자료 참고)
# Streamlit은 위젯 상호작용마다 스크립트 전체를 재실행하기 때문에
# JSON 파일을 매번 다시 읽는 비효율이 발생합니다.
# @st.cache_data를 사용하면 최초 1회만 파일을 읽고 이후엔 캐시된 결과를 반환합니다.
# -------------------------------------------------------
@st.cache_data
def load_quiz_data():
    with open("quiz_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# -------------------------------------------------------
# session_state 초기화 (세션 상태 관리 자료 참고)
# -------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ''

if 'quiz_started' not in st.session_state:
    st.session_state['quiz_started'] = False

if 'current_q' not in st.session_state:
    st.session_state['current_q'] = 0

if 'score' not in st.session_state:
    st.session_state['score'] = 0

if 'answers' not in st.session_state:
    st.session_state['answers'] = []

if 'quiz_done' not in st.session_state:
    st.session_state['quiz_done'] = False


# -------------------------------------------------------
# 화면 1: 로그인 페이지
# -------------------------------------------------------
def show_login():
    # 학번 / 이름 표시 (과제 필수 조건)
    st.caption("학번: 2025404021　|　이름: 양하윤")
    st.markdown("---")

    st.title("🎬 영화/드라마 상식 퀴즈")
    st.write("로그인 후 퀴즈를 시작할 수 있습니다.")

    st.markdown("---")
    st.subheader("로그인")

    # 입력 위젯 (기본 컴포넌트 자료 참고)
    username = st.text_input("아이디", placeholder="아이디를 입력하세요")
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")

    if st.button("로그인", type="primary", use_container_width=True):
        if not username or not password:
            st.warning("아이디와 비밀번호를 모두 입력해 주세요.")
        elif username in USERS and USERS[username] == password:
            # 로그인 성공 → session_state 업데이트 (세션 상태 관리 자료 참고)
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"환영합니다, {username}님! 🎉")
            time.sleep(0.7)
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    st.caption("테스트 계정: 하윤 / movie123")


# -------------------------------------------------------
# 화면 2: 홈 (퀴즈 시작 전 안내)
# -------------------------------------------------------
def show_home():
    # 학번 / 이름 표시 (과제 필수 조건)
    st.caption("학번: 2025404021　|　이름: 양하윤")
    st.markdown("---")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🎬 영화/드라마 상식 퀴즈")
    with col2:
        st.write("")
        if st.button("로그아웃"):
            # 세션 전체 초기화 (세션 상태 관리 자료 참고)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.write(f"👤 **{st.session_state['username']}** 님, 반갑습니다!")
    st.markdown("---")

    st.write(
        "한국 영화/드라마와 할리우드 명작까지! "
        "당신의 영화 지식을 테스트해 보세요 🍿"
    )

    st.info(
        "📌 **퀴즈 안내**\n\n"
        "- 총 10문제, 문제당 10점 (만점 100점)\n"
        "- 4지 선다형 객관식\n"
        "- 문제를 선택한 뒤 **정답 확인** 버튼을 눌러 진행하세요\n"
        "- 모든 문제를 마치면 점수와 해설을 확인할 수 있습니다"
    )

    st.markdown("---")

    if st.button("퀴즈 시작하기 🎬", type="primary", use_container_width=True):
        st.session_state['quiz_started'] = True
        st.session_state['current_q'] = 0
        st.session_state['score'] = 0
        st.session_state['answers'] = []
        st.session_state['quiz_done'] = False
        st.rerun()


# -------------------------------------------------------
# 화면 3: 퀴즈 진행
# -------------------------------------------------------
def show_quiz():
    quiz_data = load_quiz_data()
    total = len(quiz_data)
    idx = st.session_state['current_q']

    # 학번 / 이름 표시
    st.caption("학번: 2025404021　|　이름: 양하윤")
    st.markdown("---")

    # 진행도 표시 (상태 표시 자료 참고)
    st.progress(idx / total, text=f"진행도: {idx} / {total} 문제")

    q = quiz_data[idx]

    st.subheader(f"Q{idx + 1}. {q['question']}")
    st.write("")

    already_answered = len(st.session_state['answers']) > idx

    if not already_answered:
        # 라디오 버튼으로 선택 (기본 컴포넌트 자료 참고)
        selected = st.radio(
            "답을 골라주세요:",
            options=q["options"],
            key=f"q_{idx}",
            index=None
        )

        st.write("")

        if st.button("정답 확인", type="primary", use_container_width=True):
            if selected is None:
                st.warning("보기를 선택해 주세요!")
            else:
                st.session_state['answers'].append(selected)
                if selected == q["answer"]:
                    st.session_state['score'] += 10
                st.rerun()

    else:
        user_ans = st.session_state['answers'][idx]
        correct_ans = q["answer"]

        if user_ans == correct_ans:
            st.success(f"✅ 정답! **{correct_ans}**")
        else:
            st.error(f"❌ 오답입니다. 내가 고른 답: **{user_ans}**")
            st.info(f"💡 정답은 **{correct_ans}** 입니다.")

        # 해설 (기본 컴포넌트 자료 참고 - expander 활용)
        with st.expander("해설 보기"):
            st.write(q["explanation"])

        st.write("")

        if idx + 1 < total:
            if st.button("다음 문제 →", type="primary", use_container_width=True):
                st.session_state['current_q'] += 1
                st.rerun()
        else:
            if st.button("최종 결과 보기 🏆", type="primary", use_container_width=True):
                st.session_state['quiz_done'] = True
                st.rerun()


# -------------------------------------------------------
# 화면 4: 결과 페이지
# -------------------------------------------------------
def show_result():
    quiz_data = load_quiz_data()
    score = st.session_state['score']
    total = len(quiz_data)
    answers = st.session_state['answers']

    # 학번 / 이름 표시
    st.caption("학번: 2025404021　|　이름: 양하윤")
    st.markdown("---")

    st.title("🏆 퀴즈 결과")
    st.markdown("---")

    # 점수 표시 (metric - 실전 응용 자료 참고)
    col1, col2, col3 = st.columns(3)
    col1.metric("내 점수", f"{score}점")
    col2.metric("맞힌 문제", f"{score // 10} / {total}개")
    col3.metric("정답률", f"{score}%")

    st.write("")

    # 등급 메시지
    if score == 100:
        st.success("🥇 완벽해요! 진짜 영화/드라마 마니아시네요!")
        st.balloons()
    elif score >= 80:
        st.success("🥈 훌륭해요! 꽤 많이 알고 계시네요 😄")
    elif score >= 60:
        st.info("🥉 나쁘지 않아요! 조금만 더 보면 완벽할 것 같아요 🎬")
    elif score >= 40:
        st.warning("😅 더 많은 영화/드라마를 즐겨보세요!")
    else:
        st.error("😢 아직 갈 길이 멀었어요... 넷플릭스를 켜세요!")

    st.markdown("---")

    # 문제별 결과 정리
    st.subheader("📋 문제별 결과")
    for i, q in enumerate(quiz_data):
        user_ans = answers[i] if i < len(answers) else "(미응답)"
        correct_ans = q["answer"]
        is_correct = user_ans == correct_ans
        icon = "✅" if is_correct else "❌"

        with st.expander(f"{icon} Q{i + 1}. {q['question']}"):
            if is_correct:
                st.success(f"정답: **{correct_ans}**")
            else:
                st.error(f"내 답: **{user_ans}**")
                st.info(f"정답: **{correct_ans}**")
            st.write(f"📖 {q['explanation']}")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("다시 풀기 🔄", type="primary", use_container_width=True):
            st.session_state['quiz_started'] = True
            st.session_state['current_q'] = 0
            st.session_state['score'] = 0
            st.session_state['answers'] = []
            st.session_state['quiz_done'] = False
            st.rerun()
    with col_b:
        if st.button("홈으로 🏠", use_container_width=True):
            st.session_state['quiz_started'] = False
            st.session_state['current_q'] = 0
            st.session_state['score'] = 0
            st.session_state['answers'] = []
            st.session_state['quiz_done'] = False
            st.rerun()


# -------------------------------------------------------
# 라우팅: session_state 값에 따라 화면 전환
# (세션 상태 관리 자료 참고)
# -------------------------------------------------------
if not st.session_state['logged_in']:
    show_login()
elif st.session_state['quiz_done']:
    show_result()
elif st.session_state['quiz_started']:
    show_quiz()
else:
    show_home()
