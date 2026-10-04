import streamlit as st
from chatbot import UrClinicBot


# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="UrClinic | AI Healthcare Assistant",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BOT
# =========================================================
@st.cache_resource
def load_bot():
    return UrClinicBot()


bot = load_bot()


# =========================================================
# SESSION
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# THEME
# =========================================================
st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap'
);


/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background:
        linear-gradient(
            rgba(3, 38, 38, 0.91),
            rgba(4, 70, 63, 0.90)
        ),
        url("https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=2200&q=85");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


/* ---------- MAIN WIDTH ---------- */

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(3, 42, 42, 0.98),
            rgba(5, 63, 58, 0.98)
        );

    border-right: 1px solid rgba(218, 174, 79, 0.25);
}

[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] h3 {
    color: #E8C878 !important;
}


/* ---------- MAIN TITLE ---------- */

.main-title {
    font-family: 'Playfair Display', serif;
    text-align: center;
    font-size: 3rem;
    font-weight: 600;
    color: #F5F0E5;
    margin-bottom: 0;

    text-shadow:
        0 0 8px rgba(228,185,95,0.45),
        0 0 20px rgba(228,185,95,0.30),
        0 0 40px rgba(228,185,95,0.18);
}

.main-title span {
    color: #E4B95F;

    text-shadow:
        0 0 8px rgba(228,185,95,0.75),
        0 0 18px rgba(228,185,95,0.60),
        0 0 35px rgba(228,185,95,0.40),
        0 0 55px rgba(228,185,95,0.20);
}

.subtitle {
    text-align: center;
    color: #AFC5BE;
    font-family: 'DM Sans', sans-serif;
    margin-top: 3px;
    margin-bottom: 25px;
}


/* ---------- LOGO ---------- */

.logo {
    text-align: center;
    font-size: 42px;
    color: #E4B95F;

    text-shadow:
        0 0 12px rgba(228,185,95,0.55),
        0 0 30px rgba(228,185,95,0.25);

    margin-bottom: -5px;
}


/* ---------- DIRECT HEADINGS ---------- */

.section-heading {
    color: #E4B95F;
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 600;

    margin-top: 20px;
    margin-bottom: 8px;

    text-shadow:
        0 0 10px rgba(228,185,95,0.28);
}


/* ---------- CHAT MESSAGES ---------- */

/* =========================================
   SIDEBAR GOLD THEME
   ========================================= */

[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: #E4B95F !important;
}


/* UrClinic Sidebar Title */

[data-testid="stSidebar"] h3 {
    color: #F0C96A !important;

    text-shadow:
        0 0 8px rgba(240, 201, 106, 0.75),
        0 0 18px rgba(240, 201, 106, 0.50),
        0 0 35px rgba(240, 201, 106, 0.30) !important;
}


/* Sidebar description */

[data-testid="stSidebar"] p {
    color: #E4B95F !important;

    text-shadow:
        0 0 6px rgba(228, 185, 95, 0.25);
}


/* What can I ask? */

[data-testid="stSidebar"] h3 {
    color: #F0C96A !important;
}


/* Symptoms, Departments, Tests etc. */

[data-testid="stSidebar"] li,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] span {
    color: #E4B95F !important;
}


/* Sidebar divider */

[data-testid="stSidebar"] hr {
    border-color: rgba(228, 185, 95, 0.30) !important;
}


/* Clear Conversation button */

[data-testid="stSidebar"] button {
    color: #E4B95F !important;

    border-color: rgba(228, 185, 95, 0.35) !important;

    text-shadow:
        0 0 6px rgba(228, 185, 95, 0.20);
}


/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    border-left: 2px solid rgba(228,185,95,0.45) !important;
}


/* Assistant answer */

/* Assistant Answer — GOLD */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) p {
    color: #F0C96A !important;

    font-family: 'DM Sans', sans-serif;

    font-size: 0.98rem;

    line-height: 1.7;

    text-shadow:
        0 0 8px rgba(240,201,106,0.30),
        0 0 18px rgba(240,201,106,0.12);
}


/* User Question — GOLD */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) p {
    color: #E4B95F !important;

    font-family: 'DM Sans', sans-serif;

    line-height: 1.6;

    text-shadow:
        0 0 7px rgba(228,185,95,0.25);
}


/* ---------- ANSWER TEXT ---------- */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) p {

    color: #F0C96A !important;

    font-family: 'DM Sans', sans-serif;

    font-size: 0.98rem;

    line-height: 1.7;

    text-shadow:
        0 0 8px rgba(240,201,106,0.16);
}


/* ---------- USER TEXT ---------- */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) p {

    color: #E1EAE5 !important;

    font-family: 'DM Sans', sans-serif;

    line-height: 1.6;
}


/* ---------- INPUT ---------- */

[data-testid="stChatInput"] > div {

    background:
        rgba(3, 44, 43, 0.78) !important;

    border:
        1px solid rgba(228,185,95,0.38) !important;

    border-radius: 16px !important;

    box-shadow:
        0 0 20px rgba(228,185,95,0.08),
        inset 0 0 20px rgba(255,255,255,0.025) !important;

    backdrop-filter: blur(16px);
}


[data-testid="stChatInput"] textarea {

    color: #F5F2E9 !important;

    font-family: 'DM Sans', sans-serif !important;
}


[data-testid="stChatInput"] textarea::placeholder {
    color: #89A59E !important;
}


/* ---------- QUICK BUTTONS ---------- */

div.stButton > button {

    background:
        rgba(5, 66, 61, 0.58) !important;

    color: #DDB45D !important;

    border:
        1px solid rgba(228,185,95,0.28) !important;

    border-radius: 12px !important;

    font-family: 'DM Sans', sans-serif !important;

    transition: all 0.2s ease !important;
}


div.stButton > button:hover {

    background:
        rgba(8, 127, 108, 0.45) !important;

    color: #F5D889 !important;

    border-color:
        rgba(228,185,95,0.65) !important;

    box-shadow:
        0 0 18px rgba(228,185,95,0.12);
}


/* ---------- EXPANDER ---------- */

[data-testid="stExpander"] {

    background:
        rgba(3, 48, 47, 0.45) !important;

    border:
        1px solid rgba(228,185,95,0.16) !important;

    border-radius: 13px !important;
}


/* ---------- MOBILE ---------- */

@media (max-width: 700px) {

    .main-title {
        font-size: 2.3rem;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

}
/* =========================================
   FORCE CHAT QUESTION + ANSWER GOLD
   ========================================= */

/* User question */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) * {
    color: #E4B95F !important;
    text-shadow: 0 0 8px rgba(228, 185, 95, 0.25) !important;
}


/* UrClinic answer */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) * {
    color: #F0C96A !important;
    text-shadow:
        0 0 8px rgba(240, 201, 106, 0.30),
        0 0 18px rgba(240, 201, 106, 0.12) !important;
}


/* Paragraphs + text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: #F0C96A !important;
}


/* User question specifically */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) p,
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) span {
    color: #E4B95F !important;
}
/* =========================================
   TOP NAVIGATION BAR
   LIGHT CHAMPAGNE GOLD GLASS
   ========================================= */

header[data-testid="stHeader"] {
    background:
        linear-gradient(
            90deg,
            rgba(255, 248, 235, 0.82),
            rgba(250, 238, 215, 0.76),
            rgba(255, 246, 228, 0.82)
        ),
        url("https://static.wixstatic.com/media/f6c52c_2697e75a8d9244a6a4c9573963f35bbf~mv2.png/v1/fill/w_980%2Ch_549%2Cal_c%2Cq_90%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/f6c52c_2697e75a8d9244a6a4c9573963f35bbf~mv2.png");

    background-size: cover;
    background-position: center;

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    border-bottom:
        1px solid rgba(190, 145, 60, 0.30);

    box-shadow:
        0 4px 25px rgba(190, 145, 60, 0.18);
}


/* Navigation icons */

header[data-testid="stHeader"] button {
    color: #80612B !important;
}

header[data-testid="stHeader"] svg {
    color: #80612B !important;
    fill: #80612B !important;
}
/* =========================================
   FOOTER — GOLD IMAGE BACKGROUND
   ========================================= */

footer {
    background:
        linear-gradient(
            90deg,
            rgba(255, 248, 235, 0.82),
            rgba(250, 238, 215, 0.76),
            rgba(255, 246, 228, 0.82)
        ),
        url("https://static.wixstatic.com/media/f6c52c_2697e75a8d9244a6a4c9573963f35bbf~mv2.png/v1/fill/w_980%2Ch_549%2Cal_c%2Cq_90%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/f6c52c_2697e75a8d9244a6a4c9573963f35bbf~mv2.png") !important;

    background-size: cover !important;
    background-position: center !important;

    border-top: 1px solid rgba(190, 145, 60, 0.30) !important;

    box-shadow:
        0 -4px 25px rgba(190, 145, 60, 0.18) !important;

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}
/* =========================================
   OUTER-MOST FOOTER / CHAT INPUT AREA
   ========================================= */

[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer {

    background:
        linear-gradient(
            90deg,
            rgba(255, 248, 235, 0.82),
            rgba(250, 238, 215, 0.76),
            rgba(255, 246, 228, 0.82)
        ),
        url("https://static.wixstatic.com/media/f6c52c_2697e75a8d9244a6a4c9573963f35bbf~mv2.png/v1/fill/w_980%2Ch_549%2Cal_c%2Cq_90%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/f6c52c_2697e75a8d9244a6a4c9573963f35bbf~mv2.png") !important;

    background-size: cover !important;
    background-position: center !important;

    border-top: 1px solid rgba(190, 145, 60, 0.30) !important;

    box-shadow:
        0 -5px 30px rgba(190, 145, 60, 0.20) !important;

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}
/* =========================================
   SMALL LEFT MENU BUTTON
   ========================================= */

[data-testid="stSidebarCollapsedControl"] {
    left: 12px !important;
    right: auto !important;
    top: 12px !important;
    z-index: 999999 !important;
}

[data-testid="stSidebarCollapsedControl"] button {
    width: 78px !important;
    height: 34px !important;

    background:
        linear-gradient(
            90deg,
            rgba(255, 248, 235, 0.94),
            rgba(250, 238, 215, 0.90)
        ) !important;

    border: 1px solid rgba(190, 145, 60, 0.38) !important;
    border-radius: 9px !important;

    color: #80612B !important;

    box-shadow:
        0 3px 14px rgba(190, 145, 60, 0.16) !important;

    font-family: 'DM Sans', sans-serif !important;
}

/* Icon */
[data-testid="stSidebarCollapsedControl"] button svg {
    color: #80612B !important;
    fill: #80612B !important;
    width: 16px !important;
    height: 16px !important;
}

/* Add Menu text */
[data-testid="stSidebarCollapsedControl"] button::after {
    content: "Menu";

    margin-left: 5px;

    color: #80612B !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* Hover */
[data-testid="stSidebarCollapsedControl"] button:hover {
    background:
        linear-gradient(
            90deg,
            rgba(250, 238, 215, 0.98),
            rgba(255, 248, 235, 0.98)
        ) !important;

    border-color: rgba(190, 145, 60, 0.60) !important;

    box-shadow:
        0 4px 18px rgba(190, 145, 60, 0.22) !important;
}
/* =========================================
   CLEAN SIDEBAR TOGGLE
   ========================================= */

header[data-testid="stHeader"] button {
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;

    padding: 6px !important;

    border-radius: 9px !important;
}

/* Hide tooltip text */
header[data-testid="stHeader"] button span {
    display: none !important;
}

/* Clean icon */
header[data-testid="stHeader"] button svg {
    width: 17px !important;
    height: 17px !important;

    color: #80612B !important;
    fill: #80612B !important;
}

/* Hover */
header[data-testid="stHeader"] button:hover {
    background: rgba(250, 238, 215, 0.90) !important;
    border-color: rgba(190, 145, 60, 0.45) !important;

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown(
        "### ✚ UrClinic"
    )

    st.caption(
        "AI Healthcare Information Assistant"
    )

    st.divider()

    st.markdown("### What can I ask?")

    st.markdown("""
    🩺 Symptoms

    🏥 Hospital Departments

    🧪 Medical Tests

    💊 Medicines

    📅 Appointments

    🚨 Emergency Warning Signs
    """)

    st.divider()

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="logo">✚</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Ur<span>Clinic</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent hospital information assistant'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="section-heading">'
        'How can I help you today?'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask me about symptoms, hospital departments, "
        "medical tests, medicines, appointments, "
        "or general healthcare information."
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# =========================================================
# MESSAGE INPUT
# =========================================================

user_input = st.chat_input(
    "Ask UrClinic a healthcare question..."
)


if user_input:

    answer = bot.get_response(
        user_input
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# =========================================================
# QUICK QUESTIONS
# =========================================================

st.markdown(
    '<div class="section-heading">'
    'Quick Questions'
    '</div>',
    unsafe_allow_html=True
)


questions = [
    "I have a fever. What should I do?",
    "Which doctor should I see for a rash?",
    "What department handles cough?",
    "What is an MRI?",
    "How can I book an appointment?",
    "What are emergency warning signs?"
]


for i in range(0, len(questions), 2):

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            questions[i],
            key=f"q_{i}",
            use_container_width=True
        ):

            answer = bot.get_response(
                questions[i]
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": questions[i]
                }
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

    if i + 1 < len(questions):

        with col2:

            if st.button(
                questions[i + 1],
                key=f"q_{i+1}",
                use_container_width=True
            ):

                answer = bot.get_response(
                    questions[i + 1]
                )

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": questions[i + 1]
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                st.rerun()


# =========================================================
# DISCLAIMER
# =========================================================

st.caption(
    "UrClinic provides general healthcare information only. "
    "It does not diagnose conditions or replace professional "
    "medical advice. For serious symptoms, seek emergency care."
)