
import json
import random
from pathlib import Path
from datetime import datetime

import streamlit as st


# ============================================================
# LUNARIA TAROT
# 설치: python -m pip install --upgrade streamlit
# 실행: python -m streamlit run app.py
# ============================================================

st.set_page_config(
    page_title="LUNARIA TAROT",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HISTORY_FILE = Path(__file__).with_name("tarot_history.json")


# ============================================================
# 디자인
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top, #30234c 0%, #171324 42%, #0b0a13 100%);
    color: #eee7ff;
    font-family: 'Noto Sans KR', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Gowun Batang', serif !important;
    color: #f2eaff !important;
}

p, label, .stMarkdown {
    color: #e1d9f0;
}

div.stButton > button {
    width: 100%;
    min-height: 44px;
    border: 1px solid #6c578f;
    border-radius: 12px;
    background: linear-gradient(135deg, #35264e, #20182f);
    color: #f4edff;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #d5b7ff;
    background: linear-gradient(135deg, #4b356c, #302043);
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #171321;
    color: #f4edff;
    border: 1px solid #695483;
    border-radius: 10px;
}

div[data-testid="stSelectbox"] > div {
    background-color: #211a30;
}

.tarot-title {
    font-family: 'Gowun Batang', serif;
    text-align: center;
    font-size: clamp(36px, 6vw, 64px);
    letter-spacing: 7px;
    color: #e6d1ff;
    text-shadow: 0 0 25px #a67bdb80;
    margin-bottom: 0;
}

.tarot-subtitle {
    text-align: center;
    letter-spacing: 3px;
    color: #b8a5d4;
    font-size: 12px;
    margin-bottom: 30px;
}

.panel {
    background: #211a30bb;
    border: 1px solid #55416d;
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
}

.card-back {
    min-height: 160px;
    border: 1px solid #9478b5;
    border-radius: 12px;
    background:
        radial-gradient(circle at center, #493361 0%, #241832 60%, #171020 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #e8d7ff;
    text-align: center;
    font-size: 28px;
}

.card-name {
    font-family: 'Gowun Batang', serif;
    color: #f0ddff;
    font-size: 25px;
    margin-bottom: 5px;
}

.muted {
    color: #b6a6ca;
    font-size: 13px;
}

hr {
    border-color: #4b395e;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 카드 데이터
# ============================================================

MAJOR_NAMES = [
    "바보", "마법사", "여사제", "여황제", "황제",
    "교황", "연인", "전차", "힘", "은둔자",
    "운명의 수레바퀴", "정의", "매달린 사람", "죽음",
    "절제", "악마", "탑", "별", "달", "태양",
    "심판", "세계"
]

MAJOR_SYMBOLS = [
    "🃏", "🪄", "🌙", "🌿", "👑", "📿", "💞", "🏇",
    "🦁", "🏮", "☸️", "⚖️", "⏳", "🦋", "🕊️", "⛓️",
    "⚡", "⭐", "🌕", "☀️", "🔔", "🌍"
]

MAJOR_MEANINGS = [
    ("새 출발 · 가능성",
     "새로운 가능성이 열릴 수 있어요. 완벽한 확신을 기다리기보다 준비한 뒤 작은 첫걸음을 내딛어 보세요.",
     "충동적으로 행동하거나 실패가 두려워 기회를 미루고 있을 수 있어요. 설렘과 현실적인 준비를 함께 챙기세요."),
    ("실행력 · 표현",
     "이미 가진 능력과 자원을 활용할 때예요. 생각만 하던 일을 구체적인 행동으로 옮겨 보세요.",
     "계획에 비해 실행이 부족하거나 자신감을 잃었을 수 있어요. 작은 일 하나부터 끝내 보세요."),
    ("직관 · 관찰",
     "아직 드러나지 않은 정보가 있을 수 있어요. 서둘러 판단하기보다 관찰하고 사실을 확인하세요.",
     "불안과 추측을 직감으로 받아들이고 있지는 않은지 살펴보세요. 모르는 것은 직접 확인하는 편이 좋아요."),
    ("성장 · 돌봄",
     "정성을 들인 관계나 계획이 성장할 수 있어요. 자신과 주변을 돌보는 시간을 확보해 보세요.",
     "다른 사람을 챙기느라 자신을 소진하고 있을 수 있어요. 자신의 필요도 중요하게 다뤄 주세요."),
    ("안정 · 책임",
     "기준과 계획을 세우면 상황이 안정될 수 있어요. 장기적인 목표를 현실적인 단계로 나누세요.",
     "통제하려는 마음이 강해졌거나 계획이 흐트러졌을 수 있어요. 유연하게 조정할 부분을 찾아보세요."),
    ("배움 · 조언",
     "검증된 방법과 믿을 만한 조언이 도움이 될 수 있어요. 필요한 지식과 절차를 차근차근 익혀 보세요.",
     "주변의 기준을 무조건 따르거나 필요한 조언까지 거부하고 있지는 않은지 살펴보세요."),
    ("관계 · 선택",
     "관계에서 솔직한 대화와 상호 존중이 중요해요. 자신에게 중요한 가치와 상대의 기대를 확인하세요.",
     "기대가 서로 다르거나 중요한 대화를 미루고 있을 수 있어요. 추측보다 직접적인 소통이 필요해요."),
    ("집중 · 추진력",
     "목표를 분명히 하면 앞으로 나아갈 수 있어요. 흩어진 에너지를 한 방향에 집중해 보세요.",
     "조급함이나 여러 목표 때문에 집중이 흐트러질 수 있어요. 우선순위를 하나씩 정하세요."),
    ("용기 · 인내",
     "부드러운 태도와 꾸준함이 힘을 발휘할 수 있어요. 작은 진전도 인정하면서 계속해 보세요.",
     "자신감을 잃거나 감정을 억누르느라 지쳤을 수 있어요. 필요한 도움을 요청해도 괜찮아요."),
    ("성찰 · 탐색",
     "혼자 생각을 정리하며 자신에게 중요한 것이 무엇인지 살펴볼 때예요.",
     "혼자 고민하느라 도움을 받지 못하고 있을 수 있어요. 생각을 정리한 뒤 신뢰하는 사람과 이야기해 보세요."),
    ("변화 · 전환점",
     "상황이 바뀌거나 새로운 기회가 나타날 수 있어요. 변화에 대응할 수 있는 행동에 집중하세요.",
     "같은 문제를 반복하고 있다면 원인을 다시 살펴보세요. 바꿀 수 있는 조건부터 조정해 보세요."),
    ("공정함 · 사실",
     "감정과 사실을 구분하고 균형 있게 판단하는 것이 중요해요. 근거와 기준을 확인하세요.",
     "불공정함을 느끼거나 한쪽의 이야기만 보고 있을 수 있어요. 사실을 차분히 확인해 보세요."),
    ("멈춤 · 관점 전환",
     "잠시 속도를 늦추고 다른 관점에서 상황을 바라보세요. 기다리는 동안 배울 점을 찾아보세요.",
     "결정이 두려워 멈춰 있거나 일방적으로 희생하고 있을 수 있어요. 기다림의 이유를 점검하세요."),
    ("마무리 · 변화",
     "하나의 단계가 끝나고 새로운 방식이 필요할 수 있어요. 오래된 습관을 정리할 기회로 삼아 보세요.",
     "변화가 필요하다는 걸 알면서도 익숙함 때문에 미루고 있을 수 있어요. 작은 마무리부터 시작하세요."),
    ("조화 · 회복",
     "서로 다른 요소를 조율하고 지속 가능한 속도를 찾는 것이 중요해요.",
     "일정이나 감정이 한쪽으로 치우쳐 있을 수 있어요. 한꺼번에 해결하기보다 하나씩 조정하세요."),
    ("집착 · 유혹",
     "반복되는 습관이나 두려움이 선택을 좌우하고 있는지 돌아보세요. 알아차림이 변화의 시작이에요.",
     "오래된 패턴에서 벗어나려는 흐름일 수 있어요. 마음뿐 아니라 실제 행동도 조금씩 바꿔 보세요."),
    ("흔들림 · 재정비",
     "기존 계획을 다시 점검할 필요가 있을 수 있어요. 확인된 사실을 바탕으로 우선순위를 정하세요.",
     "문제를 미루거나 혼자 감당하고 있을 수 있어요. 가장 시급한 부분부터 안정시키세요."),
    ("희망 · 회복",
     "마음을 회복하고 장기적인 방향을 다시 찾는 흐름이에요. 작은 희망과 꾸준한 행동을 소중히 하세요.",
     "실망이 쌓여 가능성을 믿기 어려울 수 있어요. 억지로 괜찮은 척하기보다 필요한 지원을 찾아보세요."),
    ("불확실성 · 감정",
     "상황이 분명하지 않아 불안과 상상이 커질 수 있어요. 결론을 서두르지 말고 사실을 확인하세요.",
     "혼란이 걷히기 시작하거나 불안을 없애려 지나치게 확실한 답을 찾고 있을 수 있어요."),
    ("명료함 · 활력",
     "상황을 분명하게 바라보고 자신감을 회복할 수 있는 흐름이에요. 작은 성과도 인정해 보세요.",
     "좋은 점이 있어도 스스로 인정하지 못하거나 기대가 너무 높을 수 있어요. 현실적인 목표를 세우세요."),
    ("재평가 · 결단",
     "과거 경험에서 교훈을 얻고 미뤄 온 결정을 다시 살펴볼 때예요.",
     "과거의 후회나 타인의 평가 때문에 결정을 미루고 있을 수 있어요. 배운 점을 다음 선택에 활용하세요."),
    ("완성 · 다음 단계",
     "한 단계의 마무리와 성장을 상징해요. 지금까지의 노력을 확인하고 다음 단계로 나아가세요.",
     "완벽하지 않다는 이유로 마무리를 미루고 있을 수 있어요. 완료 기준을 정하고 끝낼 시점을 정하세요."),
]

SUITS = {
    "완드": ("🔥", "열정 · 행동 · 목표"),
    "컵": ("💧", "감정 · 사랑 · 관계"),
    "소드": ("⚔️", "생각 · 갈등 · 판단"),
    "펜타클": ("🪙", "현실 · 돈 · 노력"),
}

RANKS = [
    ("에이스", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5),
    ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10),
    ("페이지", 11), ("나이트", 12), ("퀸", 13), ("킹", 14),
]

MINOR_GUIDE = {
    1: ("시작", "새로운 기회나 가능성이 생길 수 있어요. 작은 시도를 시작해 보세요."),
    2: ("선택", "두 가지 방향 사이에서 균형을 찾고 결정을 준비할 때예요."),
    3: ("성장", "협력과 연습을 통해 경험이 쌓이는 흐름이에요."),
    4: ("안정", "기반을 다지고 현재 가진 것을 지키는 일이 중요해요."),
    5: ("어려움", "불편함이나 의견 차이가 생길 수 있어요. 문제를 구체적으로 나눠 보세요."),
    6: ("회복", "도움과 배려를 주고받으며 상황을 개선할 수 있어요."),
    7: ("점검", "지금까지의 노력을 평가하고 다음 행동을 정할 때예요."),
    8: ("연습", "반복적인 노력과 집중이 실력을 키워 줄 수 있어요."),
    9: ("성취", "개인적인 성과와 자신감을 돌아볼 수 있는 흐름이에요."),
    10: ("책임", "성과와 함께 부담도 커질 수 있어요. 역할과 우선순위를 조정하세요."),
    11: ("호기심", "새로운 것을 배우고 경험하는 단계예요."),
    12: ("추진력", "빠른 움직임이 도움이 될 수 있지만 방향도 확인하세요."),
    13: ("성숙", "자신의 감정과 능력을 이해하고 균형 있게 활용할 때예요."),
    14: ("주도력", "큰 그림을 보고 책임 있게 행동하는 것이 중요해요."),
}


def build_deck():
    deck = []

    for i, name in enumerate(MAJOR_NAMES):
        up_title, up_text, rev_text = MAJOR_MEANINGS[i]
        deck.append({
            "name": name,
            "symbol": MAJOR_SYMBOLS[i],
            "suit": "메이저 아르카나",
            "core": up_title,
            "up": up_text,
            "rev": rev_text,
            "advice": "지금 상황에서 실천할 수 있는 작은 행동 하나를 정해 보세요. 확인된 사실과 자신의 감정을 함께 살펴보는 것이 도움이 됩니다.",
        })

    for suit, (symbol, theme) in SUITS.items():
        for rank_name, rank_value in RANKS:
            title, meaning = MINOR_GUIDE[rank_value]

            deck.append({
                "name": f"{suit} {rank_name}",
                "symbol": symbol,
                "suit": suit,
                "core": f"{theme} · {title}",
                "up": meaning,
                "rev": (
                    f"{theme}와 관련해 균형이 흐트러졌을 수 있어요. "
                    "지나치게 서두르거나 미루고 있는 부분이 없는지 확인하고, "
                    "지금 바꿀 수 있는 작은 행동부터 시작해 보세요."
                ),
                "advice": (
                    f"{theme}와 관련된 목표를 구체적으로 정하고, "
                    "오늘 실천할 수 있는 행동 하나를 선택하세요."
                ),
            })

    return deck


DECK = build_deck()


# ============================================================
# 고민 분석 및 맞춤 조언
# ============================================================

TOPICS = {
    "연애": [
        "연애", "사랑", "남친", "남자친구", "여친", "여자친구",
        "짝사랑", "고백", "재회", "이별", "썸", "전남친", "전여친",
        "연락", "결혼", "애인", "호감"
    ],
    "학업": [
        "공부", "시험", "성적", "대학", "합격", "면접",
        "입시", "수능", "학교", "졸업", "과제", "자격증"
    ],
    "진로": [
        "취업", "직장", "진로", "회사", "이직", "직업",
        "꿈", "미래", "사업", "창업", "진학"
    ],
    "금전": [
        "돈", "금전", "월급", "알바", "아르바이트", "저축",
        "소비", "지출", "투자", "재산", "경제"
    ],
    "인간관계": [
        "친구", "가족", "부모", "엄마", "아빠", "인간관계",
        "싸움", "갈등", "손절", "배신", "화해", "사람"
    ],
    "건강": [
        "건강", "몸", "피곤", "피로", "잠", "수면",
        "운동", "생활습관", "스트레스", "컨디션"
    ],
}


TOPIC_ADVICE = {
    "연애": (
        "상대의 마음을 추측하는 것만으로 결론을 내리지 마세요. "
        "내가 원하는 관계와 받아들일 수 있는 기준을 먼저 정하고, "
        "필요한 이야기는 차분하게 직접 나누는 것이 좋아요."
    ),
    "학업": (
        "막연하게 잘해야 한다고 생각하기보다 시험 범위와 남은 시간을 나눠 보세요. "
        "중요한 부분부터 공부하고, 모르는 문제는 질문하거나 다시 풀어 보세요."
    ),
    "진로": (
        "관심 있는 분야의 실제 업무와 필요한 자격·경험을 조사해 보세요. "
        "가능성을 비교할 때는 흥미뿐 아니라 비용, 조건, 장기적인 목표도 함께 고려하세요."
    ),
    "금전": (
        "예상 수입과 고정 지출을 먼저 정리해 보세요. "
        "큰 결정을 내리기 전에는 조건과 위험을 확인하고, 감정적인 충동구매는 잠시 미뤄 보세요."
    ),
    "인간관계": (
        "상대의 의도를 단정하기보다 실제로 있었던 말과 행동을 살펴보세요. "
        "불편한 점은 구체적으로 설명하고, 서로 지켜야 할 경계도 존중하세요."
    ),
    "건강": (
        "수면, 식사, 수분 섭취, 활동량 등 일상적인 컨디션을 점검해 보세요. "
        "증상이 지속되거나 심해진다면 타로 해석 대신 의료 전문가의 도움을 받으세요."
    ),
    "일반": (
        "지금 가장 신경 쓰이는 문제를 한 문장으로 정리하고, "
        "내가 바꿀 수 있는 것과 당장 바꾸기 어려운 것을 구분해 보세요. "
        "작은 행동 하나를 실천하는 것이 다음 방향을 찾는 데 도움이 됩니다."
    ),
}


def detect_topic(question, selected_topic):
    if selected_topic != "자동 분석":
        return selected_topic

    text = question.lower()
    scores = {}

    for topic, words in TOPICS.items():
        scores[topic] = sum(1 for word in words if word in text)

    if not scores or max(scores.values()) == 0:
        return "일반"

    return max(scores, key=scores.get)


def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
    except (OSError, json.JSONDecodeError):
        return []

    return []


def save_history(record):
    history = load_history()
    history.insert(0, record)
    history = history[:100]

    try:
        HISTORY_FILE.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        st.warning("리딩 기록을 파일에 저장하지 못했어요.")


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# ============================================================
# 세션 초기화
# ============================================================

defaults = {
    "page": "home",
    "question": "",
    "topic": "자동 분석",
    "spread": "3장 리딩",
    "picked": [],
    "reading": None,
    "saved": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# 공통 화면
# ============================================================

st.markdown(
    '<div class="tarot-title">LUNARIA</div>'
    '<div class="tarot-subtitle">T A R O T · FIND YOUR INNER LIGHT</div>',
    unsafe_allow_html=True,
)


def go_home():
    st.session_state.page = "home"
    st.session_state.picked = []
    st.session_state.reading = None
    st.session_state.saved = False


def make_reading(question, topic, cards):
    result = []

    for card in cards:
        reversed_card = random.choice([True, False])
        meaning = card["rev"] if reversed_card else card["up"]

        result.append({
            **card,
            "reversed": reversed_card,
            "meaning": meaning,
        })

    return {
        "question": question,
        "topic": topic,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "cards": result,
    }


# ============================================================
# 홈 화면
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="panel">'
        '<h2 style="text-align:center;">달빛 아래, 마음을 펼쳐 보세요</h2>'
        '<p style="text-align:center;">'
        '고민을 적고 카드를 선택해 지금의 상황을 새로운 관점에서 바라보세요.'
        '</p></div>',
        unsafe_allow_html=True,
    )

    with st.form("question_form"):
        question = st.text_area(
            "지금 가장 궁금한 것은 무엇인가요?",
            value=st.session_state.question,
            placeholder="예: 지금 만나는 사람과 좋은 관계를 이어갈 수 있을까?",
            height=110,
        )

        topic = st.selectbox(
            "리딩 주제",
            [
                "자동 분석", "연애", "학업", "진로",
                "금전", "인간관계", "건강", "일반"
            ],
            index=[
                "자동 분석", "연애", "학업", "진로",
                "금전", "인간관계", "건강", "일반"
            ].index(st.session_state.topic),
        )

        spread = st.selectbox(
            "카드 배열",
            [
                "1장 리딩",
                "3장 리딩",
                "5장 리딩",
                "양자택일 리딩",
                "켈틱 크로스 10장",
            ],
            index=[
                "1장 리딩",
                "3장 리딩",
                "5장 리딩",
                "양자택일 리딩",
                "켈틱 크로스 10장",
            ].index(st.session_state.spread),
        )

        submitted = st.form_submit_button(
            "달빛 리딩 시작하기 ✦",
            use_container_width=True,
        )

    if submitted:
        if not question.strip():
            st.warning("고민이나 질문을 한 문장이라도 적어 주세요.")
        else:
            st.session_state.question = question.strip()
            st.session_state.topic = topic
            st.session_state.spread = spread
            st.session_state.topic_detected = detect_topic(question, topic)
            st.session_state.picked = []
            st.session_state.page = "pick"
            rerun_app()

    st.divider()

    left, right = st.columns(2)

    with left:
        if st.button("🌌 카드 도감 보기", use_container_width=True):
            st.session_state.page = "glossary"
            rerun_app()

    with right:
        if st.button("📜 지난 리딩 보기", use_container_width=True):
            st.session_state.page = "history"
            rerun_app()

    st.markdown(
        '<p class="muted" style="text-align:center;">'
        '타로는 자기 성찰을 위한 참고 도구이며 미래를 확정적으로 예측하지 않습니다.'
        '</p>',
        unsafe_allow_html=True,
    )


# ============================================================
# 카드 선택 화면
# ============================================================

elif st.session_state.page == "pick":

    spread = st.session_state.spread

    spread_counts = {
        "1장 리딩": 1,
        "3장 리딩": 3,
        "5장 리딩": 5,
        "양자택일 리딩": 2,
        "켈틱 크로스 10장": 10,
    }

    count = spread_counts[spread]
    topic = st.session_state.get("topic_detected", "일반")

    st.subheader("✦ 마음이 끌리는 카드를 선택하세요")
    st.write(f"**질문:** {st.session_state.question}")
    st.write(f"**주제:** {topic}  ·  **배열:** {spread}")
    st.caption(
        f"총 {count}장을 선택하면 해석을 확인할 수 있어요. "
        "카드는 선택한 순서대로 배치됩니다."
    )

    picked = st.session_state.picked

    st.markdown(
        f'<div class="panel" style="text-align:center;">'
        f'선택한 카드: {len(picked)} / {count}'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    for index, card in enumerate(DECK):
        with cols[index % 4]:
            already = any(item["name"] == card["name"] for item in picked)

            if already:
                st.button(
                    f"✓ {card['name']}",
                    key=f"picked_{index}",
                    disabled=True,
                    use_container_width=True,
                )
            elif len(picked) >= count:
                st.button(
                    "✦ 선택 완료",
                    key=f"disabled_{index}",
                    disabled=True,
                    use_container_width=True,
                )
            else:
                if st.button(
                    f"🌙  카드 {index + 1:02d}",
                    key=f"card_{index}",
                    use_container_width=True,
                ):
                    st.session_state.picked.append(card)
                    rerun_app()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("선택 초기화", use_container_width=True):
            st.session_state.picked = []
            rerun_app()

    with col2:
        if st.button(
            "선택한 카드 해석하기 ✦",
            disabled=len(picked) != count,
            use_container_width=True,
        ):
            st.session_state.reading = make_reading(
                st.session_state.question,
                topic,
                picked,
            )
            st.session_state.page = "result"
            st.session_state.saved = False
            rerun_app()

    if st.button("← 처음으로 돌아가기"):
        go_home()
        rerun_app()


# ============================================================
# 해석 결과
# ============================================================

elif st.session_state.page == "result":

    reading = st.session_state.reading

    if not reading:
        st.warning("아직 리딩 결과가 없어요.")
        if st.button("홈으로"):
            go_home()
            rerun_app()

    else:
        topic = reading["topic"]

        st.subheader("🌙 당신을 위한 리딩")
        st.markdown(
            f'<div class="panel"><b>질문</b><br>{reading["question"]}'
            f'<br><br><b>주제</b><br>{topic}</div>',
            unsafe_allow_html=True,
        )

        cards = reading["cards"]

        positions = {
            1: ["지금의 핵심"],
            2: ["선택 A", "선택 B"],
            3: ["과거", "현재", "앞으로의 방향"],
            5: ["현재 상황", "장애물", "숨은 영향", "조언", "가능한 흐름"],
            10: [
                "현재", "장애물", "먼 과거", "가까운 과거",
                "가능한 목표", "가까운 미래", "나의 태도",
                "주변 환경", "희망과 두려움", "종합 흐름"
            ],
        }

        labels = positions.get(len(cards), [f"{i + 1}번째 카드" for i in range(len(cards))])

        for i, card in enumerate(cards):
            label = labels[i] if i < len(labels) else f"{i + 1}번째 카드"
            orientation = "역방향" if card["reversed"] else "정방향"

            st.markdown(
                f'<div class="panel">'
                f'<div class="muted">{i + 1}. {label}</div>'
                f'<div class="card-name">{card["symbol"]} {card["name"]}</div>'
                f'<div class="muted">{orientation} · {card["core"]}</div>'
                f'<hr>'
                f'<p>{card["meaning"]}</p>'
                f'<b>실천 조언</b><br>{card["advice"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.subheader("✦ 질문에 맞춘 종합 조언")
        st.markdown(
            f'<div class="panel">{TOPIC_ADVICE.get(topic, TOPIC_ADVICE["일반"])}</div>',
            unsafe_allow_html=True,
        )

        if topic == "건강":
            st.info(
                "건강운은 생활 습관을 돌아보기 위한 참고용 해석이에요. "
                "질병을 진단하거나 건강 상태 및 치료 결과를 예측하지 않습니다. "
                "증상이 있다면 의료 전문가에게 상담하세요."
            )

        if not st.session_state.saved:
            if st.button("📜 이 리딩 기록 저장하기", use_container_width=True):
                save_history(reading)
                st.session_state.saved = True
                st.success("리딩 기록을 저장했어요.")
                rerun_app()
        else:
            st.success("이 리딩은 저장되었어요.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("새로운 리딩 시작", use_container_width=True):
                go_home()
                rerun_app()

        with col2:
            if st.button("카드 도감 보기", use_container_width=True):
                st.session_state.page = "glossary"
                rerun_app()


# ============================================================
# 카드 도감
# ============================================================

elif st.session_state.page == "glossary":

    st.subheader("📚 타로 카드 도감")

    selected_suit = st.selectbox(
        "카드 종류",
        ["전체", "메이저 아르카나", "완드", "컵", "소드", "펜타클"],
    )

    search = st.text_input("카드 이름 검색", placeholder="예: 연인, 컵 2")

    filtered = DECK

    if selected_suit != "전체":
        filtered = [c for c in filtered if c["suit"] == selected_suit]

    if search.strip():
        filtered = [
            c for c in filtered
            if search.strip().lower() in c["name"].lower()
        ]

    st.caption(f"검색 결과: {len(filtered)}장")

    for card in filtered:
        with st.expander(f'{card["symbol"]}  {card["name"]} · {card["core"]}'):
            st.write("**정방향**")
            st.write(card["up"])
            st.write("**역방향**")
            st.write(card["rev"])
            st.write("**실천 조언**")
            st.write(card["advice"])

    if st.button("← 홈으로"):
        go_home()
        rerun_app()


# ============================================================
# 이전 리딩 기록
# ============================================================

elif st.session_state.page == "history":

    st.subheader("📜 지난 리딩 기록")

    history = load_history()

    if not history:
        st.info("아직 저장된 리딩이 없어요.")
    else:
        st.caption(f"저장된 리딩: {len(history)}개")

        for index, item in enumerate(history):
            question = str(item.get("question", "질문 없음"))
            created = str(item.get("created", "날짜 미상"))
            topic = str(item.get("topic", "일반"))

            with st.expander(f"{created} · {topic} · {question[:45]}"):
                st.write(f"**질문:** {question}")

                for card in item.get("cards", []):
                    if not isinstance(card, dict):
                        continue

                    orientation = (
                        "역방향" if card.get("reversed") else "정방향"
                    )

                    st.markdown(
                        f'**{card.get("symbol", "🌙")} '
                        f'{card.get("name", "카드")} · {orientation}**'
                    )
                    st.write(card.get("meaning", card.get("up", "")))

                if st.button("이 기록 삭제", key=f"delete_{index}"):
                    history.pop(index)
                    try:
                        HISTORY_FILE.write_text(
                            json.dumps(history, ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )
                        st.success("기록을 삭제했어요.")
                        rerun_app()
                    except OSError:
                        st.error("기록 파일을 수정하지 못했어요.")

    if st.button("← 홈으로"):
        go_home()
        rerun_app()


# ============================================================
# 푸터
# ============================================================

st.divider()

st.markdown(
    '<p class="muted" style="text-align:center;">'
    'LUNARIA TAROT · 78 CARDS · FIND YOUR INNER LIGHT'
    '</p>',
    unsafe_allow_html=True,
)
