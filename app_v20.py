
import random
import html
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="달빛 아래 타로",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG_COLOR = "#100c1d"
PANEL_COLOR = "#1d1630"
GOLD = "#e4c27a"
LIGHT_TEXT = "#f4edff"
MUTED_TEXT = "#b9abcF"

# 타로 이미지 저장소
IMAGE_BASE = (
    "https://raw.githubusercontent.com/"
    "seven102161/elaine-tarot-cards/main/cards/"
)

# BGM
BGM_URL = (
    "https://orangefreesounds.com/wp-content/uploads/"
    "2024/01/Free-meditative-music.mp3"
)
BGM_PAGE = "https://orangefreesounds.com/free-meditative-music/"

# =========================================================
# 카테고리
# =========================================================

TOPICS = [
    "종합 운세",
    "연애운",
    "상대방 속마음",
    "재회운",
    "직업·진로",
    "금전운",
    "인간관계",
    "건강·자기성찰",
    "학업운",
    "직접 입력",
]

TOPIC_DESCRIPTIONS = {
    "종합 운세": "현재의 흐름과 앞으로의 변화, 지금 필요한 선택을 살펴봅니다.",
    "연애운": "연애의 흐름과 관계의 가능성, 감정 표현과 현실적인 선택을 살펴봅니다.",
    "상대방 속마음": "상대의 태도와 관계에서 읽을 수 있는 신호를 상징적으로 살펴봅니다.",
    "재회운": "과거 관계의 원인과 현재의 거리, 다시 연락하기 전 고려할 점을 살펴봅니다.",
    "직업·진로": "현재의 업무 상황과 기회, 앞으로 취할 수 있는 현실적인 행동을 살펴봅니다.",
    "금전운": "소비 습관과 재정적인 기회, 주의해야 할 위험 요소를 살펴봅니다.",
    "인간관계": "관계의 균형과 소통 방식, 필요한 경계와 개선 방향을 살펴봅니다.",
    "건강·자기성찰": "마음의 부담과 생활의 균형, 자신을 돌보기 위해 필요한 변화를 살펴봅니다.",
    "학업운": "집중력과 학습 습관, 성과를 높이기 위한 구체적인 방법을 살펴봅니다.",
    "직접 입력": "궁금한 주제를 직접 작성하면 그 질문에 맞춰 해석합니다.",
}

# =========================================================
# 카드 데이터
# =========================================================

MAJOR_NAMES = [
    "바보", "마법사", "여사제", "여황제", "황제", "교황",
    "연인", "전차", "힘", "은둔자", "운명의 수레바퀴",
    "정의", "매달린 사람", "죽음", "절제", "악마",
    "탑", "별", "달", "태양", "심판", "세계",
]

MAJOR_CODES = [f"ar{i:02d}" for i in range(22)]

SUITS = {
    "완드": {
        "prefix": "wa",
        "theme": "열정, 추진력, 창조성, 행동",
        "cards": [
            ("에이스", "waac"),
            ("2", "wa02"),
            ("3", "wa03"),
            ("4", "wa04"),
            ("5", "wa05"),
            ("6", "wa06"),
            ("7", "wa07"),
            ("8", "wa08"),
            ("9", "wa09"),
            ("10", "wa10"),
            ("페이지", "wapa"),
            ("나이트", "wakn"),
            ("퀸", "waqu"),
            ("킹", "waki"),
        ],
    },
    "컵": {
        "prefix": "cu",
        "theme": "감정, 애정, 관계, 직관",
        "cards": [
            ("에이스", "cuac"),
            ("2", "cu02"),
            ("3", "cu03"),
            ("4", "cu04"),
            ("5", "cu05"),
            ("6", "cu06"),
            ("7", "cu07"),
            ("8", "cu08"),
            ("9", "cu09"),
            ("10", "cu10"),
            ("페이지", "cupa"),
            ("나이트", "cukn"),
            ("퀸", "cuqu"),
            ("킹", "cuki"),
        ],
    },
    "소드": {
        "prefix": "sw",
        "theme": "생각, 판단, 갈등, 의사소통",
        "cards": [
            ("에이스", "swac"),
            ("2", "sw02"),
            ("3", "sw03"),
            ("4", "sw04"),
            ("5", "sw05"),
            ("6", "sw06"),
            ("7", "sw07"),
            ("8", "sw08"),
            ("9", "sw09"),
            ("10", "sw10"),
            ("페이지", "swpa"),
            ("나이트", "swkn"),
            ("퀸", "swqu"),
            ("킹", "swki"),
        ],
    },
    "펜타클": {
        "prefix": "pe",
        "theme": "돈, 현실, 생활, 안정과 성과",
        "cards": [
            ("에이스", "peac"),
            ("2", "pe02"),
            ("3", "pe03"),
            ("4", "pe04"),
            ("5", "pe05"),
            ("6", "pe06"),
            ("7", "pe07"),
            ("8", "pe08"),
            ("9", "pe09"),
            ("10", "pe10"),
            ("페이지", "pepa"),
            ("나이트", "pekn"),
            ("퀸", "pequ"),
            ("킹", "peki"),
        ],
    },
}

MAJOR_MEANINGS = [
    ("새로운 시작", "미지의 가능성, 가벼운 출발, 경험을 통한 배움",
     "준비 부족, 충동적인 선택, 현실적인 조건을 놓치는 태도"),
    ("능력과 실행", "자원을 활용하는 능력, 계획의 실행, 주도권",
     "말과 행동의 불일치, 준비 부족, 능력을 제대로 활용하지 못함"),
    ("직관과 관찰", "내면의 목소리, 관찰, 드러나지 않은 정보",
     "혼란, 중요한 사실의 외면, 추측에 지나치게 의존함"),
    ("풍요와 성장", "돌봄, 창조성, 관계와 환경의 성장",
     "지나친 보살핌, 의존, 자신을 돌보지 못하는 상황"),
    ("질서와 책임", "구조, 경계, 책임감, 현실적인 통제",
     "경직된 태도, 과도한 통제, 타인의 의견을 배제함"),
    ("기준과 배움", "조언, 전통, 배움, 공통의 기준",
     "기존 방식에 대한 의문, 형식에 얽매임, 자기 기준의 부재"),
    ("관계와 선택", "상호 존중, 중요한 선택, 가치관의 조화",
     "엇갈린 기대, 선택의 회피, 가치관의 충돌"),
    ("추진과 돌파", "목표 집중, 실행력, 장애물 극복",
     "방향 상실, 조급함, 힘으로 상황을 밀어붙임"),
    ("내면의 힘", "인내, 감정 조절, 부드러운 용기",
     "자신감 저하, 감정 억압, 무리하게 버팀"),
    ("혼자만의 성찰", "거리 두기, 자기 점검, 신중한 탐색",
     "고립, 지나친 고민, 도움을 거절함"),
    ("변화의 흐름", "전환점, 새로운 기회, 흐름의 변화",
     "변화에 대한 저항, 불안정, 통제할 수 없는 요소에 집착함"),
    ("균형과 판단", "공정한 판단, 책임, 사실에 근거한 결정",
     "편향된 판단, 책임 회피, 결과를 충분히 살피지 않음"),
    ("관점의 전환", "잠시 멈춤, 다른 시각, 우선순위 재정비",
     "불필요한 희생, 정체, 결정을 미루는 습관"),
    ("끝과 전환", "한 단계의 마무리, 정리, 변화의 시작",
     "끝을 받아들이지 못함, 과거에 매달림, 변화에 대한 두려움"),
    ("조화와 회복", "속도 조절, 타협, 균형 회복",
     "극단적인 선택, 과도함, 생활 리듬의 불균형"),
    ("집착과 유혹", "의존, 욕구, 반복되는 패턴을 인식함",
     "구속에서 벗어남, 나쁜 습관의 인식, 선택권 회복"),
    ("기존 구조의 붕괴", "잘못된 기반을 재검토함, 갑작스러운 깨달음",
     "변화를 부정함, 불안정한 구조를 억지로 유지함"),
    ("희망과 회복", "회복 가능성, 장기적인 희망, 영감",
     "낙담, 자신에 대한 불신, 희망을 놓침"),
    ("불확실성과 감정", "직관, 숨겨진 불안, 불분명한 상황",
     "혼란이 걷힘, 두려움을 직면함, 사실을 구분함"),
    ("활력과 명료함", "자신감, 솔직함, 활력, 성과를 확인함",
     "기대가 지나침, 피로, 좋은 점을 충분히 누리지 못함"),
    ("돌아봄과 결단", "과거를 돌아봄, 평가, 중요한 결론",
     "자책, 평가에 대한 두려움, 결론을 피함"),
    ("완성과 통합", "목표의 마무리, 성취, 경험의 통합",
     "마무리의 지연, 미완성의 과제, 다음 단계에 대한 망설임"),
]

SUIT_MEANINGS = {
    "완드": [
        ("새로운 열정", "새로운 의욕과 시작할 만한 기회", "흥미가 식거나 시작을 망설임"),
        ("선택과 계획", "가능성을 비교하고 방향을 정함", "결정을 미루거나 시야가 좁아짐"),
        ("확장과 기다림", "준비한 일의 확장과 미래를 위한 탐색", "계획의 지연과 예상보다 느린 진행"),
        ("안정과 축하", "기반의 안정, 작은 성과, 편안한 관계", "안정이 흔들리거나 관계의 불편함"),
        ("경쟁과 마찰", "의견 차이를 조율하고 실력을 겨룸", "갈등을 피하거나 경쟁에 지침"),
        ("인정과 진전", "노력의 인정, 성과, 자신감 회복", "인정받지 못한다는 느낌, 성과의 지연"),
        ("입장 지키기", "압박 속에서도 원칙과 경계를 지킴", "방어적인 태도, 자신감 저하"),
        ("빠른 변화", "빠른 소식, 속도감 있는 진행, 행동", "지연, 엇갈린 일정, 성급함"),
        ("마지막 버팀", "경험을 바탕으로 끝까지 점검함", "지친 상태에서 무리하거나 경계심이 지나침"),
        ("과부하와 책임", "책임이 많아도 마무리를 향해 감", "짐을 혼자 짊어지고 부담을 나누지 못함"),
        ("새로운 탐색", "호기심, 학습, 가벼운 시도", "산만함, 준비 부족, 시작만 반복함"),
        ("속도와 결단", "빠른 실행, 열정적인 추진", "성급한 행동, 충동, 주변을 고려하지 않음"),
        ("자신감과 독립", "따뜻한 리더십, 자신감, 독립적인 매력", "감정적인 반응, 질투, 자기 돌봄의 부족"),
        ("성숙한 추진력", "목표를 현실로 만드는 리더십과 열정", "독단, 조급함, 타인의 속도를 무시함"),
    ],
    "컵": [
        ("감정의 시작", "호감, 마음의 열림, 정서적인 기회", "감정을 표현하기 어렵거나 마음이 닫힘"),
        ("상호 교감", "서로의 호응, 대화, 관계의 균형", "감정의 불균형, 오해, 기대의 차이"),
        ("즐거운 교류", "만남, 지지, 함께 나누는 기쁨", "관계의 피로, 소외감, 지나친 분위기 의존"),
        ("권태와 재검토", "감정을 살피며 진짜 원하는 것을 확인함", "기회를 놓치거나 불만을 외면함"),
        ("상실과 아쉬움", "실망을 인정하고 남아 있는 가능성을 살핌", "상실에서 회복하거나 과거를 놓아줌"),
        ("추억과 익숙함", "과거의 기억, 편안함, 순수한 마음", "과거를 이상화하거나 현재를 보지 못함"),
        ("환상과 선택지", "여러 가능성과 욕구를 탐색함", "혼란에서 벗어나 현실을 구분함"),
        ("떠남과 탐색", "충분하지 않은 것을 인정하고 방향을 바꿈", "미련, 떠나야 할 상황에 머무름"),
        ("만족과 자기 존중", "개인적인 만족, 독립성, 원하는 것을 누림", "겉보기 만족, 과도한 욕심, 공허함"),
        ("정서적 안정", "정서적 만족, 공동체, 오래가는 행복", "가족이나 관계의 기대가 어긋남"),
        ("섬세한 감정", "다정한 제안, 감수성, 마음을 표현함", "감정 기복, 소극적인 표현, 비현실적인 기대"),
        ("감정의 접근", "로맨틱한 접근, 초대, 감정 표현", "말뿐인 약속, 변덕, 현실성이 부족함"),
        ("공감과 직관", "감정을 이해하고 배려하는 태도", "감정에 휩쓸림, 경계가 약해짐"),
        ("감정의 성숙", "안정적인 공감, 감정 조절, 배려", "감정 조종, 회피, 속마음을 숨김"),
    ],
    "소드": [
        ("명확한 판단", "사실을 직시하고 결론을 내릴 기회", "판단이 흐려지거나 결정을 미룸"),
        ("결정 보류", "정보를 더 모으고 균형 있게 판단함", "회피, 불편한 사실을 보지 않음"),
        ("마음의 상처", "아픔을 인정하고 문제를 분명히 바라봄", "회복의 시작 또는 상처를 반복해서 되새김"),
        ("휴식과 회복", "생각을 쉬게 하고 체력을 회복함", "쉬지 못하거나 고립이 길어짐"),
        ("갈등과 승패", "갈등의 비용을 살피고 실질적인 해결을 찾음", "분쟁을 멈추거나 갈등의 여파를 정리함"),
        ("이동과 전환", "복잡한 상황에서 더 나은 환경으로 이동함", "변화를 미루거나 과거의 문제를 끌고 감"),
        ("전략과 경계", "신중한 계획, 정보 보호, 상황 판단", "숨김이 드러나거나 정직함을 요구받음"),
        ("제약과 불안", "스스로 제한하는 생각을 알아차림", "제약을 벗어날 실마리를 찾음"),
        ("걱정과 불면", "걱정의 원인을 구체적으로 나누어 살핌", "불안이 줄거나 문제를 혼자 감당함"),
        ("한계와 마무리", "더 이상 지속하기 어려운 패턴을 끝냄", "회복의 시작 또는 끝을 받아들이기 어려움"),
        ("질문과 관찰", "정보 수집, 솔직한 질문, 분석", "성급한 판단, 과도한 의심, 말실수"),
        ("빠른 주장", "신속한 대응, 직설적인 소통", "공격적인 말투, 서두르는 결정"),
        ("분명한 경계", "독립적인 판단, 사실에 근거한 대화", "차가운 태도, 비판, 감정을 배제함"),
        ("논리와 책임", "전략적인 판단, 원칙, 명확한 의사결정", "지나친 냉정함, 독단적인 판단"),
    ],
    "펜타클": [
        ("현실적인 기회", "돈이나 일의 새로운 기회, 실질적인 시작", "기회를 놓치거나 준비가 부족함"),
        ("자원 관리", "일정과 돈, 여러 책임을 균형 있게 관리함", "우선순위가 흐트러지거나 부담이 커짐"),
        ("협업과 숙련", "협력, 기술 향상, 성실한 작업", "협업 부족, 평가의 불일치, 숙련의 정체"),
        ("안정과 소유", "자산 보호, 절약, 안정적인 기반", "지나친 절약, 소유에 대한 집착"),
        ("부족함과 지원", "어려움을 인정하고 필요한 도움을 구함", "지원의 회복 또는 부족함에 대한 불안"),
        ("주고받는 균형", "공정한 보상, 도움, 자원의 배분", "불공정한 부담, 일방적인 지원"),
        ("장기적인 노력", "꾸준한 투자, 기다림, 중간 점검", "성과가 늦어져 조급해지거나 방향을 재검토함"),
        ("기술과 반복", "연습, 성실함, 기술 향상", "집중력 부족, 반복 작업의 지루함"),
        ("독립과 성과", "자립, 노력의 결실, 안정적인 생활", "비용 부담, 성과에 대한 불안"),
        ("장기적인 기반", "가족과 공동체의 안정, 지속 가능한 성과", "가족의 재정 문제, 불안정한 기반"),
        ("학습과 실무", "현실적인 학습, 새로운 기술, 성실한 시작", "계획만 세움, 실천 부족, 미숙함"),
        ("꾸준함과 신뢰", "느리지만 지속적인 실행, 책임감", "고집, 지나친 반복, 변화에 둔감함"),
        ("생활의 안정", "실용적인 돌봄, 현실 감각, 안정적인 관리", "돈이나 생활 문제에 대한 과도한 걱정"),
        ("물질적 성취", "장기적인 계획, 재정 감각, 책임 있는 운영", "물질에 대한 집착, 권위적인 운영"),
    ],
}

COURT_LABELS = {"페이지": "페이지", "나이트": "나이트", "퀸": "퀸", "킹": "킹"}

def make_deck():
    deck = []

    for i, name in enumerate(MAJOR_NAMES):
        upright, reversed_meaning = MAJOR_MEANINGS[i][1], MAJOR_MEANINGS[i][2]
        deck.append({
            "name": name,
            "code": MAJOR_CODES[i],
            "suit": "메이저 아르카나",
            "theme": MAJOR_MEANINGS[i][0],
            "upright": upright,
            "reversed": reversed_meaning,
        })

    for suit, info in SUITS.items():
        for index, (rank, code) in enumerate(info["cards"]):
            theme, upright, reversed_meaning = SUIT_MEANINGS[suit][index]

            if rank in COURT_LABELS:
                name = f"{suit} {rank}"
            elif rank == "에이스":
                name = f"{suit} 에이스"
            else:
                name = f"{suit} {rank}"

            deck.append({
                "name": name,
                "code": code,
                "suit": suit,
                "theme": theme,
                "upright": upright,
                "reversed": reversed_meaning,
            })

    return deck

DECK = make_deck()

# =========================================================
# 주제별 해석 방향
# =========================================================

TOPIC_GUIDANCE = {
    "종합 타로": {
        "focus": "현재 삶의 전체적인 흐름과 가장 중요한 과제",
        "action": "지금 당장 바꿀 수 있는 일 한 가지를 정하고 작은 행동부터 시작하세요.",
        "caution": "좋은 결과만 기대하거나 불편한 신호를 무시하지 마세요.",
    },
    "종합 운세": {
        "focus": "생활 전반의 흐름, 변화의 기회와 현실적인 과제",
        "action": "일정, 관계, 체력 중 지금 가장 부담이 큰 영역부터 정리하세요.",
        "caution": "한 번의 사건만으로 앞으로의 모든 일을 단정하지 마세요.",
    },
    "연애운": {
        "focus": "감정 표현, 상호성, 관계의 속도와 기대",
        "action": "상대의 반응을 추측하기보다 자신의 바람과 경계를 차분하게 표현하세요.",
        "caution": "호감과 실제로 관계를 유지하려는 행동은 구분해서 보세요.",
    },
    "상대방 속마음": {
        "focus": "상대의 태도에서 관찰할 수 있는 신호와 관계의 불확실성",
        "action": "상대의 마음을 단정하기보다 연락의 일관성, 약속, 행동을 살펴보세요.",
        "caution": "타로만으로 상대의 실제 생각이나 감정을 확정할 수는 없습니다.",
    },
    "재회운": {
        "focus": "이별의 원인, 현재의 거리, 다시 연락하기 전 확인할 점",
        "action": "연락하기 전에 과거에 반복된 문제와 이번에는 달라질 수 있는 부분을 정리하세요.",
        "caution": "그리움만으로 재회가 건강한 선택이라고 판단하지 마세요.",
    },
    "직업·진로": {
        "focus": "업무 환경, 역량, 기회, 지속 가능한 진로 선택",
        "action": "관심 있는 선택지를 실제 조건과 필요한 준비로 나눠 비교하세요.",
        "caution": "충동적인 퇴사나 큰 결정은 비용과 대안을 확인한 뒤 판단하세요.",
    },
    "금전운": {
        "focus": "소비 습관, 자원 관리, 현실적인 재정 계획",
        "action": "고정 지출과 변동 지출을 확인하고 이번 주의 지출 기준을 정하세요.",
        "caution": "카드 해석을 투자 수익이나 금전적 결과를 보장하는 예측으로 받아들이지 마세요.",
    },
    "인간관계": {
        "focus": "서로의 기대, 대화 방식, 관계의 경계와 균형",
        "action": "상대가 알아서 이해하길 기다리기보다 필요한 것을 구체적으로 전달하세요.",
        "caution": "한쪽만 노력해야 유지되는 관계인지도 살펴보세요.",
    },
    "건강·자기성찰": {
        "focus": "감정적 부담, 휴식, 일상 습관과 자기 돌봄",
        "action": "수면, 휴식, 식사, 감정 기록 등 일상에서 조정할 수 있는 한 가지를 시작하세요.",
        "caution": "타로는 의학적 진단이나 치료를 대신할 수 없습니다.",
    },
    "학업운": {
        "focus": "집중력, 학습 방식, 꾸준함과 성과",
        "action": "막연히 오래 공부하기보다 오늘 끝낼 수 있는 작은 목표를 정하세요.",
        "caution": "성적이나 합격 여부를 카드만으로 확정하지 마세요.",
    },
    "직접 입력": {
        "focus": "질문에 담긴 고민과 선택의 핵심",
        "action": "질문에서 내가 통제할 수 있는 요소를 골라 구체적인 행동으로 옮기세요.",
        "caution": "확인되지 않은 추측과 실제로 관찰된 사실을 구분하세요.",
    },
}

# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(ellipse at top, #302044 0%, {BG_COLOR} 55%);
        color: {LIGHT_TEXT};
    }}

    [data-testid="stSidebar"] {{
        background: #171123;
        border-right: 1px solid #40304e;
    }}

    h1, h2, h3, h4 {{
        color: {LIGHT_TEXT} !important;
    }}

    p, li, label, span {{
        color: inherit;
    }}

    .hero {{
        text-align: center;
        padding: 22px 12px 18px;
    }}

    .hero-title {{
        font-size: clamp(30px, 5vw, 48px);
        font-weight: 800;
        letter-spacing: 3px;
        color: {GOLD};
        text-shadow: 0 0 24px #c59a5a55;
    }}

    .hero-sub {{
        color: #c7b8df;
        font-size: 15px;
        margin-top: 10px;
        line-height: 1.8;
    }}

    .section-heading {{
        color: {GOLD};
        font-size: 22px;
        font-weight: 750;
        margin: 20px 0 8px;
    }}

    .topic-card {{
        border: 1px solid #574269;
        border-radius: 13px;
        background: linear-gradient(145deg, #281d39, #191325);
        padding: 14px 16px;
        min-height: 104px;
        margin-bottom: 8px;
    }}

    .topic-title {{
        color: {GOLD};
        font-size: 16px;
        font-weight: 750;
        margin-bottom: 7px;
    }}

    .topic-desc {{
        color: #c9bddb;
        font-size: 13px;
        line-height: 1.65;
    }}

    .selected-topic {{
        background: #2d2141;
        border: 1px solid {GOLD};
        border-radius: 13px;
        padding: 14px 16px;
        margin: 8px 0 15px;
    }}

    .selected-topic strong {{
        color: {GOLD};
        font-size: 18px;
    }}

    .selected-topic p {{
        color: #d4c8e5;
        margin: 5px 0 0;
    }}

    .moon-note {{
        color: #b9a8d1;
        font-size: 13px;
        text-align: center;
        line-height: 1.8;
        margin: 8px 0 16px;
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, #39284e, #241a35);
        border: 1px solid #695080;
        color: #f7edff;
        border-radius: 10px;
        min-height: 42px;
        transition: 0.2s ease;
    }}

    div.stButton > button:hover {{
        border-color: {GOLD};
        color: {GOLD};
        background: #332441;
    }}

    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #b28b51, #73502e);
        color: #fff9e9;
        border-color: #e4c27a;
    }}

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {{
        background: #21182f;
        color: #fff8ff;
        border-color: #58446c;
    }}

    .result-panel {{
        background: linear-gradient(145deg, #21182f, #171121);
        border: 1px solid #514064;
        border-radius: 14px;
        padding: 18px;
        margin: 8px 0 14px;
    }}

    .result-panel h3 {{
        color: {GOLD} !important;
    }}

    .small-muted {{
        color: #b7a7cc;
        font-size: 12px;
    }}

    [data-testid="stImage"] img {{
        border-radius: 10px;
    }}

    hr {{
        border-color: #493653;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 세션 상태
# =========================================================

def init_state():
    defaults = {
        "reading_mode": "종합 타로",
        "detail_topic": "연애운",
        "custom_topic": "",
        "question": "",
        "selected_cards": [],
        "reading_done": False,
        "reading_history": [],
        "bgm_enabled": False,
        "last_result": None,
        "draw_seed": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

def reset_reading():
    st.session_state.selected_cards = []
    st.session_state.reading_done = False
    st.session_state.last_result = None
    st.session_state.draw_seed = None

def select_card(card_index):
    if st.session_state.reading_done:
        return

    already_selected = [
        c["code"] for c in st.session_state.selected_cards
    ]

    card = DECK[card_index]

    if card["code"] in already_selected:
        return

    if len(st.session_state.selected_cards) >= 3:
        return

    st.session_state.selected_cards.append(card.copy())

    if len(st.session_state.selected_cards) == 3:
        st.session_state.reading_done = True
        st.session_state.draw_seed = random.randint(1, 10**9)

def choose_topic(topic):
    st.session_state.reading_mode = topic
    reset_reading()

def get_active_topic():
    if st.session_state.reading_mode == "종합 타로":
        return "종합 타로"

    topic = st.session_state.detail_topic

    if topic == "직접 입력":
        custom = st.session_state.custom_topic.strip()
        if custom:
            return custom

    return topic

# =========================================================
# 해석 도우미
# =========================================================

def get_orientation(card, position, seed):
    rng = random.Random(f"{seed}-{card['code']}-{position}")
    return "역방향" if rng.random() < 0.32 else "정방향"

def card_meaning(card, orientation):
    if orientation == "역방향":
        return card["reversed"]
    return card["upright"]

def question_keywords(question):
    q = question.lower()
    groups = {
        "연락": ["연락", "카톡", "문자", "전화", "답장", "디엠", "dm"],
        "감정": ["좋아", "사랑", "마음", "속마음", "호감", "감정"],
        "재회": ["재회", "다시 만나", "헤어", "이별", "전 애인", "전애인"],
        "일": ["직장", "회사", "일", "취업", "이직", "진로", "면접"],
        "돈": ["돈", "금전", "재정", "수입", "지출", "투자"],
        "공부": ["공부", "시험", "성적", "합격", "학업"],
        "관계": ["친구", "인간관계", "가족", "갈등", "싸움", "사이"],
        "결정": ["선택", "결정", "할까", "말까", "어떻게 해야", "어떡해"],
    }

    found = []
    for label, words in groups.items():
        if any(word in q for word in words):
            found.append(label)
    return found

def topic_context(topic, question, card, orientation):
    if topic in TOPIC_GUIDANCE:
        guide = TOPIC_GUIDANCE[topic]
    else:
        guide = TOPIC_GUIDANCE["직접 입력"]

    keywords = question_keywords(question)
    theme = card["theme"]
    meaning = card_meaning(card, orientation)

    if topic == "연애운":
        context = (
            f"이 카드는 연애에서 특히 **{theme}**의 문제가 중요해질 수 있음을 보여줍니다. "
            f"{meaning}이라는 상징을 바탕으로, 감정이 있는지만 생각하기보다 "
            "두 사람이 실제로 시간을 내고 대화를 이어가며 관계를 함께 만들어 가는지도 살펴보세요."
        )
    elif topic == "상대방 속마음":
        context = (
            f"이 카드의 핵심 상징은 **{theme}**입니다. {meaning}이라는 흐름은 "
            "상대의 행동을 해석할 때 참고할 관점을 제공합니다. 다만 상대가 실제로 무엇을 생각하는지는 "
            "카드만으로 알 수 없습니다. 연락의 일관성, 약속을 지키는 태도, 직접적인 표현을 "
            "함께 살펴보는 것이 중요합니다."
        )
    elif topic == "재회운":
        context = (
            f"이 카드는 **{theme}**라는 주제를 강조합니다. {meaning}이라는 관점에서 보면, "
            "재회 가능성만 기다리기보다 이별을 만든 문제가 무엇이었는지, 그 문제가 지금은 "
            "달라졌는지 확인하는 과정이 중요합니다. 다시 연락하더라도 상대의 경계와 의사를 존중해야 합니다."
        )
    elif topic == "직업·진로":
        context = (
            f"일과 진로에서는 **{theme}**가 중요한 키워드입니다. {meaning}이라는 의미를 "
            "현실에 적용하면, 현재의 역량과 환경을 점검하고 필요한 준비를 구체적인 행동으로 "
            "바꾸는 것이 도움이 됩니다. 기회가 있더라도 조건과 비용을 함께 비교해 보세요."
        )
    elif topic == "금전운":
        context = (
            f"금전 문제에서 이 카드는 **{theme}**를 강조합니다. {meaning}이라는 상징을 "
            "재정 습관에 적용해 보세요. 기대 수익보다 실제 지출과 감당할 수 있는 위험을 "
            "먼저 확인하고, 중요한 재정 결정은 검증된 정보에 근거해 판단하는 편이 안전합니다."
        )
    elif topic == "학업운":
        context = (
            f"학업에서는 **{theme}**가 중요한 흐름입니다. {meaning}이라는 의미는 "
            "공부 시간을 늘리는 것뿐 아니라 공부 방식과 집중 환경을 살펴볼 필요가 있음을 시사합니다. "
            "해야 할 일을 작게 나누고, 결과를 확인하면서 방법을 조정해 보세요."
        )
    elif topic == "건강·자기성찰":
        context = (
            f"자기성찰의 관점에서 **{theme}**가 눈에 띕니다. {meaning}이라는 상징은 "
            "지금의 감정과 생활 리듬을 돌아보는 계기로 활용할 수 있습니다. "
            "스스로를 몰아붙이기보다 휴식과 일상적인 돌봄을 확인해 보세요. "
            "건강 문제는 타로가 아니라 의료 전문가의 조언을 기준으로 판단해야 합니다."
        )
    elif topic == "인간관계":
        context = (
            f"관계에서 이 카드가 강조하는 것은 **{theme}**입니다. {meaning}이라는 관점에서 "
            "상대의 입장만 추측하기보다 실제로 어떤 대화와 행동이 오갔는지 살펴보세요. "
            "서로의 요구를 구체적으로 이야기하고, 한쪽에만 부담이 쏠리지 않는지도 확인할 필요가 있습니다."
        )
    else:
        context = (
            f"이 카드의 핵심은 **{theme}**입니다. {meaning}이라는 상징은 "
            f"현재 고민에서 {guide['focus']}를 살펴보도록 안내합니다. "
            "당장 모든 결론을 내리기보다 확인된 사실과 예상, 자신의 바람을 나누어 생각해 보세요."
        )

    if "연락" in keywords:
        context += (
            " 특히 연락이 질문의 핵심이라면, 연락이 올 것이라고 단정하기보다 "
            "현재 연락이 오가는 방식과 서로의 의사 표현을 기준으로 판단하는 것이 좋습니다."
        )
    if "재회" in keywords and topic != "재회운":
        context += (
            " 질문에 과거 관계가 포함되어 있다면, 그리움과 실제 관계를 다시 이어갈 준비가 되어 있는지는 "
            "별개의 문제라는 점도 기억해 주세요."
        )
    if "일" in keywords and topic not in ("직업·진로", "금전운"):
        context += (
            " 업무나 진로와 관련된 질문이라면, 감정적인 만족뿐 아니라 일정, 조건, 준비 정도도 함께 확인하세요."
        )
    if "돈" in keywords and topic != "금전운":
        context += (
            " 금전과 관련된 부분은 기대만으로 판단하지 말고 실제 수입과 지출, 감당할 수 있는 위험을 확인하세요."
        )

    return context

def position_text(position):
    return [
        ("첫 번째 카드 · 원인과 배경",
         "현재 고민이 시작된 배경, 반복되어 온 패턴, 지금의 상황에 영향을 주는 요소를 살펴봅니다."),
        ("두 번째 카드 · 현재 상황",
         "지금 눈앞에 놓인 문제와 감정, 관계나 환경에서 확인할 수 있는 현실적인 신호를 살펴봅니다."),
        ("세 번째 카드 · 앞으로의 흐름",
         "현재 방식이 이어질 때 고려할 수 있는 방향과, 흐름을 바꾸기 위해 취할 수 있는 선택을 살펴봅니다."),
    ][position]

def make_interpretation(card, orientation, topic, question, position, seed):
    title, position_description = position_text(position)
    meaning = card_meaning(card, orientation)
    context = topic_context(topic, question, card, orientation)

    if position == 0:
        detail = (
            f"이 카드는 지금의 고민을 단순히 최근에 발생한 일 하나로만 보지 말고, "
            f"그 이전부터 이어진 조건도 살펴보라고 말합니다. **{card['theme']}**라는 키워드를 "
            f"바탕으로 보면, {meaning}이 현재 상황에 영향을 주고 있을 가능성이 있습니다. "
            "이것이 반드시 과거에 실제로 일어났다는 뜻은 아닙니다. 본인의 경험과 맞는 부분만 "
            "취하고, 맞지 않는 해석은 억지로 끼워 맞추지 않아도 됩니다."
        )
    elif position == 1:
        detail = (
            f"현재 가장 중요하게 살펴볼 부분은 **{card['theme']}**입니다. "
            f"{meaning}이라는 상징은 지금 상황에서 무엇이 충분하고 무엇이 부족한지 "
            "구분하는 데 도움을 줄 수 있습니다. 감정이 강할수록 상대의 의도나 미래를 "
            "확정해서 생각하기 쉽습니다. 실제로 확인한 사실과 아직 확인하지 못한 추측을 "
            "나누어 보면, 지금 할 수 있는 선택이 더 선명해질 수 있습니다."
        )
    else:
        detail = (
            f"앞으로의 흐름은 이미 정해진 운명이라기보다 현재의 선택과 환경에 따라 달라질 수 있습니다. "
            f"이 카드의 **{card['theme']}**라는 상징과 {meaning}이라는 의미를 고려하면, "
            "서두르기보다는 지금의 행동이 어떤 결과를 만들 수 있는지 확인하면서 움직이는 것이 좋습니다. "
            "작은 변화를 먼저 시도하고, 상대나 환경의 실제 반응을 확인한 뒤 다음 결정을 내리세요."
        )

    if orientation == "역방향":
        orientation_note = (
            "역방향은 무조건 나쁜 결과를 뜻하지 않습니다. 이 카드의 주제가 막혀 있거나, "
            "과도하게 나타나거나, 다시 점검할 필요가 있다는 관점으로 해석할 수 있습니다."
        )
    else:
        orientation_note = (
            "정방향은 이 카드의 주제가 비교적 직접적으로 드러나는 모습으로 해석합니다. "
            "다만 좋은 의미의 카드라도 행동과 현실적인 조건을 대신해 주지는 않습니다."
        )

    if question.strip():
        question_note = (
            f"**질문과 연결해서 생각해 보면:** “{question.strip()}”라는 고민에서 "
            f"이 카드는 {card['theme']}라는 측면을 확인하도록 안내합니다. "
            "질문에 대한 답을 하나의 예언처럼 확정하기보다, 지금까지의 경험과 실제 상황에 "
            "대조해 보는 것이 이 해석을 가장 유용하게 활용하는 방법입니다."
        )
    else:
        question_note = (
            f"질문이 구체적으로 정해지지 않았다면, 최근 생활에서 **{card['theme']}**와 "
            "연결되는 일이 있었는지 떠올려 보세요. 현재 자신에게 가장 와닿는 부분부터 "
            "차분하게 살펴보면 됩니다."
        )

    return {
        "title": title,
        "position_description": position_description,
        "meaning": meaning,
        "detail": detail,
        "context": context,
        "orientation_note": orientation_note,
        "question_note": question_note,
    }

def make_synthesis(cards, orientations, topic, question):
    meanings = [
        card_meaning(card, orientation)
        for card, orientation in zip(cards, orientations)
    ]
    themes = [card["theme"] for card in cards]

    first, second, third = cards

    return f"""
### 세 장의 카드가 함께 전하는 이야기

첫 번째 카드인 **{first['name']}**는 `{themes[0]}`라는 배경을,
두 번째 카드인 **{second['name']}**는 `{themes[1]}`라는 현재의 핵심을,
세 번째 카드인 **{third['name']}**는 `{themes[2]}`라는 앞으로의 과제를 보여줍니다.

이 세 장을 하나의 이야기로 연결하면, 과거의 배경을 이해하는 데서 멈추지 않고
현재의 상황을 구체적으로 살핀 다음, 자신이 바꿀 수 있는 행동으로 이어가는 것이 중요합니다.

첫 번째 카드의 의미인 **{meanings[0]}**가 현재 상황의 배경과 연결되는 부분이 있는지 돌아보세요.
두 번째 카드의 의미인 **{meanings[1]}**는 지금 가장 주의 깊게 관찰해야 할 지점을 보여주는 상징입니다.
세 번째 카드의 의미인 **{meanings[2]}**는 미래가 확정되었다는 뜻이 아니라,
현재와 다른 선택을 할 때 무엇을 고려해야 하는지 생각할 실마리를 제공합니다.

**{topic} 관점에서의 핵심:** {TOPIC_GUIDANCE.get(topic, TOPIC_GUIDANCE['직접 입력'])['focus']}.

세 장의 카드가 모두 같은 말을 한다고 단정할 필요는 없습니다.
오히려 카드 사이의 차이를 살펴보면, 마음으로 바라는 방향과 현실적으로 필요한 행동 사이의
간격을 발견할 수도 있습니다. 가장 마음에 걸리는 카드 한 장을 골라,
그 카드가 떠올리게 하는 실제 상황이 무엇인지 적어 보는 것도 좋은 방법입니다.

타로는 미래를 확정하거나 다른 사람의 생각을 증명하는 도구가 아닙니다.
이 결과는 자신이 처한 상황을 여러 각도에서 돌아보기 위한 참고 자료로 활용하세요.
"""

# =========================================================
# 사이드바: BGM과 기록
# =========================================================

with st.sidebar:
    st.markdown("## 🌙 달빛 아래 타로")
    st.caption("카드와 함께 마음을 돌아보는 시간")

    st.divider()

    st.markdown("### 🎵 배경 음악")
    st.markdown(
        "<div style='color:#c6b6d9;font-size:13px;line-height:1.7;'>"
        "잔잔한 분위기의 음악을 원할 때 켜 주세요."
        "</div>",
        unsafe_allow_html=True,
    )

    st.session_state.bgm_enabled = st.toggle(
        "명상 분위기 BGM",
        value=st.session_state.bgm_enabled,
        key="bgm_toggle",
    )

    if st.session_state.bgm_enabled:
        st.audio(BGM_URL, format="audio/mp3")
        st.caption("음악이 재생되지 않으면 브라우저에서 오디오 재생을 확인해 주세요.")
        st.markdown(f"[음악 출처 페이지]({BGM_PAGE})")

    st.divider()

    st.markdown("### 📜 최근 리딩 기록")

    history = st.session_state.reading_history

    if history:
        for item in reversed(history[-5:]):
            with st.expander(
                f"{item['topic']} · {item['date']}",
                expanded=False,
            ):
                st.write(f"**질문:** {item['question'] or '질문 없음'}")
                st.write(f"**카드:** {' · '.join(item['cards'])}")
                st.write(item["summary"])
    else:
        st.caption("아직 저장된 리딩이 없습니다.")

    if st.button("리딩 기록 모두 지우기", use_container_width=True):
        st.session_state.reading_history = []
        st.rerun()

# =========================================================
# 헤더
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div style="font-size:35px;">☾ ✦ ☽</div>
        <div class="hero-title">달빛 아래 타로</div>
        <div class="hero-sub">
            마음속 질문을 떠올리고, 세 장의 카드로 지금의 흐름을 살펴보세요.<br>
            정답을 단정하기보다 자신에게 필요한 단서를 찾는 시간입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 카드 선택 전: 모든 카테고리를 이 화면에 배치
# =========================================================

if not st.session_state.reading_done:
    st.markdown(
        '<div class="section-heading">✧ 1. 리딩 종류 선택</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="moon-note">'
        '원하는 카테고리를 먼저 선택해 주세요. '
        '종합 타로는 특정 주제를 정하지 않고 세 장의 카드로 전체 흐름을 살펴봅니다.'
        '</div>',
        unsafe_allow_html=True,
    )

    # 종합 타로는 별도의 카드로 제공
    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(
            """
            <div class="topic-card" style="border-color:#d5b16b;">
                <div class="topic-title">🌙 종합 타로</div>
                <div class="topic-desc">
                    특정 주제에 한정하지 않고 현재의 흐름과 중요한 과제를 살펴봅니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "종합 타로 선택",
            type="primary" if st.session_state.reading_mode == "종합 타로" else "secondary",
            use_container_width=True,
            key="choose_general",
        ):
            choose_topic("종합 타로")
            st.rerun()

    with c2:
        st.markdown(
            """
            <div class="topic-card">
                <div class="topic-title">🔮 주제별 타로</div>
                <div class="topic-desc">
                    연애, 상대방의 속마음, 재회, 진로, 금전, 인간관계 등
                    궁금한 한 가지 주제에 집중해 해석합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "주제별 타로 선택",
            type="primary" if st.session_state.reading_mode != "종합 타로" else "secondary",
            use_container_width=True,
            key="choose_specific",
        ):
            choose_topic("연애운")
            st.rerun()

    if st.session_state.reading_mode != "종합 타로":
        st.markdown(
            '<div class="section-heading">✧ 2. 세부 카테고리 선택</div>',
            unsafe_allow_html=True,
        )

        topic_cols = st.columns(3)

        for i, topic in enumerate(TOPICS):
            col = topic_cols[i % 3]

            with col:
                is_selected = st.session_state.detail_topic == topic

                st.markdown(
                    f"""
                    <div class="topic-card"
                         style="{'border-color:#e4c27a;' if is_selected else ''}">
                        <div class="topic-title">{html.escape(topic)}</div>
                        <div class="topic-desc">
                            {html.escape(TOPIC_DESCRIPTIONS[topic])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "선택됨 ✓" if is_selected else "이 주제 선택",
                    type="primary" if is_selected else "secondary",
                    key=f"topic_{i}",
                    use_container_width=True,
                ):
                    st.session_state.detail_topic = topic
                    reset_reading()
                    st.rerun()

        if st.session_state.detail_topic == "직접 입력":
            st.markdown("#### 궁금한 주제 직접 작성")

            st.text_input(
                "어떤 문제를 살펴보고 싶나요?",
                placeholder="예: 지금 준비하는 일을 계속하는 게 좋을까?",
                key="custom_topic",
            )

    active_topic = get_active_topic()

    st.markdown(
        f"""
        <div class="selected-topic">
            <strong>현재 선택한 리딩: {html.escape(active_topic)}</strong>
            <p>{html.escape(TOPIC_GUIDANCE.get(active_topic, TOPIC_GUIDANCE['직접 입력'])['focus'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">✧ 3. 질문 작성</div>',
        unsafe_allow_html=True,
    )

    st.text_area(
        "카드를 뽑기 전에 마음속 질문을 적어 보세요.",
        placeholder="예: 지금 내가 가장 신경 써야 할 것은 무엇일까?",
        key="question",
        height=100,
        help="질문을 비워 두어도 카드 해석을 진행할 수 있습니다.",
    )

    st.markdown(
        '<div class="section-heading">✧ 4. 카드 세 장 선택</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="moon-note">
            아래 카드들은 모두 뒷면으로 표시됩니다.<br>
            마음이 가는 카드를 세 장 골라 주세요. 세 장을 모두 선택하면 앞면과 해석이 공개됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_codes = [card["code"] for card in st.session_state.selected_cards]

    st.markdown(
        f"**선택한 카드: {len(st.session_state.selected_cards)} / 3**"
    )

    progress_value = len(st.session_state.selected_cards) / 3
    st.progress(progress_value)

    if len(st.session_state.selected_cards) > 0:
        selected_labels = [
            f"{i + 1}. {card['name']}"
            for i, card in enumerate(st.session_state.selected_cards)
        ]
        st.caption(" · ".join(selected_labels))

    # 카드 뒷면 디자인
    CARD_BACK = """
    <div style="
        width:100%;
        aspect-ratio:2/3;
        border:2px solid #c8a96b;
        border-radius:11px;
        background:
          radial-gradient(circle at center, #45305e 0%, #251a3a 55%, #171123 100%);
        display:flex;
        align-items:center;
        justify-content:center;
        box-shadow:0 5px 16px #00000035;
        ">
        <div style="
            width:78%;
            height:88%;
            border:1px solid #b99b66;
            border-radius:7px;
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            color:#e5ca91;
            background:repeating-linear-gradient(
                45deg,
                #ffffff04,
                #ffffff04 3px,
                transparent 3px,
                transparent 7px
            );
            ">
            <div style="font-size:clamp(22px,3vw,36px);">☾</div>
            <div style="font-size:clamp(30px,4vw,52px);">✧</div>
            <div style="font-size:clamp(22px,3vw,36px);">☽</div>
        </div>
    </div>
    """

    card_cols = st.columns(7)

    for i, card in enumerate(DECK):
        col = card_cols[i % 7]

        with col:
            is_selected = card["code"] in selected_codes

            if is_selected:
                st.markdown(
                    f"""
                    <div style="position:relative;">
                        {CARD_BACK}
                        <div style="
                            text-align:center;
                            color:#e4c27a;
                            font-size:12px;
                            padding-top:5px;
                            font-weight:700;
                        ">선택 완료 ✓</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption(card["name"])
            else:
                st.markdown(CARD_BACK, unsafe_allow_html=True)

                if len(st.session_state.selected_cards) < 3:
                    st.button(
                        "이 카드 선택",
                        key=f"card_{i}",
                        use_container_width=True,
                        on_click=select_card,
                        args=(i,),
                    )
                else:
                    st.button(
                        "선택 완료",
                        key=f"card_disabled_{i}",
                        use_container_width=True,
                        disabled=True,
                    )

    if st.session_state.selected_cards:
        st.markdown("---")

        if st.button("선택한 카드 초기화", use_container_width=True):
            reset_reading()
            st.rerun()

# =========================================================
# 카드 선택 완료: 앞면 공개와 해석
# =========================================================

if st.session_state.reading_done and len(st.session_state.selected_cards) == 3:
    cards = st.session_state.selected_cards
    topic = get_active_topic()
    question = st.session_state.question
    seed = st.session_state.draw_seed or 12345

    orientations = [
        get_orientation(card, i, seed)
        for i, card in enumerate(cards)
    ]

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">✧ 선택한 세 장의 카드</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="selected-topic">
            <strong>리딩 종류: {html.escape(topic)}</strong>
            <p>질문: {html.escape(question if question.strip() else '별도의 질문 없음')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result_cols = st.columns(3)

    for i, (col, card, orientation) in enumerate(
        zip(result_cols, cards, orientations)
    ):
        with col:
            image_url = f"{IMAGE_BASE}{card['code']}.jpg"

            st.image(
                image_url,
                caption=f"{card['name']} · {orientation}",
                use_container_width=True,
            )

            st.markdown(f"### {position_text(i)[0]}")
            st.caption(position_text(i)[1])

            st.markdown(f"**핵심 키워드:** {card['theme']}")
            st.markdown(f"**카드 의미:** {card_meaning(card, orientation)}")

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">✧ 카드별 상세 해석</div>',
        unsafe_allow_html=True,
    )

    interpretations = []

    for i, (card, orientation) in enumerate(zip(cards, orientations)):
        interpretation = make_interpretation(
            card=card,
            orientation=orientation,
            topic=topic,
            question=question,
            position=i,
            seed=seed,
        )
        interpretations.append(interpretation)

        with st.container(border=True):
            st.markdown(f"### {interpretation['title']}")
            st.markdown(
                f"**{card['name']} · {orientation} · {card['theme']}**"
            )
            st.caption(interpretation["position_description"])

            st.markdown("#### 이 카드가 말하는 것")
            st.markdown(interpretation["detail"])

            st.markdown("#### 질문과 연결한 해석")
            st.markdown(interpretation["context"])
            st.markdown(interpretation["question_note"])

            st.info(interpretation["orientation_note"])

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">✧ 세 장을 연결한 종합 해석</div>',
        unsafe_allow_html=True,
    )

    synthesis = make_synthesis(cards, orientations, topic, question)

    with st.container(border=True):
        st.markdown(synthesis)

        st.markdown("### 지금 실천해 볼 것")
        active_guide = TOPIC_GUIDANCE.get(
            topic,
            TOPIC_GUIDANCE["직접 입력"],
        )

        st.markdown(f"- {active_guide['action']}")

        st.markdown("### 조심해서 살펴볼 것")
        st.markdown(f"- {active_guide['caution']}")

        st.markdown("### 스스로에게 던져 볼 질문")
        reflection_questions = [
            "이 해석 중 실제 경험과 가장 잘 맞는 부분은 무엇인가요?",
            "지금 상황에서 내가 직접 바꿀 수 있는 것은 무엇인가요?",
            "결정을 내리기 전에 더 확인해야 할 사실은 무엇인가요?",
        ]

        for q in reflection_questions:
            st.markdown(f"- {q}")

    # 기록은 같은 리딩이 반복 저장되지 않도록 마지막 결과와 비교
    current_result_key = (
        topic,
        question,
        tuple(card["code"] for card in cards),
        seed,
    )

    if st.session_state.last_result != current_result_key:
        from datetime import datetime

        st.session_state.reading_history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": topic,
            "question": question,
            "cards": [
                f"{card['name']} ({orientation})"
                for card, orientation in zip(cards, orientations)
            ],
            "summary": (
                f"{cards[0]['name']} → {cards[1]['name']} → {cards[2]['name']}"
            ),
        })

        st.session_state.last_result = current_result_key

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        if st.button("다시 카드 뽑기", type="primary", use_container_width=True):
            reset_reading()
            st.rerun()

    with right:
        if st.button("다른 카테고리로 보기", use_container_width=True):
            reset_reading()
            st.session_state.reading_mode = "종합 타로"
            st.rerun()

# =========================================================
# 하단 안내
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#a99ac6;
        line-height:2;
        padding:12px;
        ">
        ☾ 달빛 아래 타로 ☽<br>
        타로 해석은 자기성찰과 재미를 위한 참고 자료입니다.<br>
        미래나 다른 사람의 마음을 확정하는 사실로 받아들이기보다,
        현실의 정보와 자신의 판단을 함께 활용해 주세요.
    </div>
    """,
    unsafe_allow_html=True,
)
