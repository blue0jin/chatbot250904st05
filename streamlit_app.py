import openai
import streamlit as st
from openai import OpenAI
import os

# 페이지 설정
st.set_page_config(
    page_title="✈️ 여행 가이드 챗봇",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    /* 전체 배경 그라디언트 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 메인 컨테이너 */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin-top: 1rem;
    }
    
    /* 제목 스타일 */
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background: linear-gradient(180deg, #ff9a9e 0%, #fecfef 100%);
    }
    
    /* 채팅 메시지 스타일 */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 경고 메시지 스타일 */
    .stAlert {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 메인 제목
st.markdown('<h1 class="main-title">🌍 ✈️ 여행 가이드 챗봇 🏖️</h1>', unsafe_allow_html=True)

# 소개 메시지
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">🎒 당신의 여행 동반자입니다! 🎒</h3>
    <p style="color: #34495e; margin: 0; font-size: 1.1rem;">여행지 추천, 준비물, 문화, 음식 등 모든 여행 정보를 친절하게 안내해드립니다 ✨</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 설정
st.sidebar.markdown("### 🔧 설정")
st.sidebar.markdown("---")
openai_api_key = st.sidebar.text_input("🔑 OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.sidebar.warning("⚠️ OpenAI API 키를 입력해주세요.")
    st.sidebar.markdown("""
    ### 📝 사용 방법
    1. 🔑 왼쪽에 OpenAI API 키를 입력하세요
    2. 💬 여행 관련 질문을 입력하세요
    3. 🤖 AI가 친절하게 답변해드립니다!
    
    ### 🌟 추천 질문들
    - 🇯🇵 "일본 여행 추천 코스는?"
    - 🎒 "유럽 배낭여행 준비물은?"
    - 🍜 "태국 현지 음식 추천해줘"
    - 💰 "동남아 여행 예산은 얼마나?"
    - 🏨 "제주도 숙박 추천해줘"
    """)
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [  
        {"role": "system", 
         "content": "반드시 한국어, 영어, 일본어로 제공. "
          "당신은 여행에 관한 질문에 답하는 전문 여행 가이드 챗봇입니다. "
          "만약에 여행 외의 질문에 대해서는 정중하게 여행 관련 질문을 요청하세요. "
          "정확하지 않은 정보는 제공하지 말고, 모르는 내용은 솔직히 모른다고 하세요. "
          "여행지 추천, 준비물, 문화, 음식, 교통, 숙박 등 다양한 여행 주제에 대해 친절하고 상세하게 안내해주세요. "
          "답변에 관련 이모지를 적절히 사용하여 친근하게 대화하세요."
        }  
    ]

# 사용자 입력 영역
st.markdown("### 💬 여행에 대해 무엇이든 물어보세요!")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "질문을 입력하세요", 
        key="user_input", 
        placeholder="예: 제주도 3박 4일 여행 코스 추천해줘 🌺",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("🚀 전송", use_container_width=True)

if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI API 호출
    with st.spinner("🤔 여행 정보를 찾고 있습니다..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=0.7
        )

    # OpenAI 응답 추가
    response_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", 
                                      "content": response_message})

# 대화 내용 표시 영역
if len(st.session_state.messages) > 1:  # 시스템 메시지 외에 대화가 있을 때만 표시
    st.markdown("### 💭 대화 내용")
    st.markdown("---")

    for message in st.session_state.messages:
        if message["role"] != "system":  # 시스템 메시지는 표시하지 않음
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 나:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 여행 가이드:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 15px;">
    <p style="margin: 0; color: #1565c0; font-weight: bold;">🌟 즐거운 여행 되세요! 🌟</p>
    <p style="margin: 0; color: #1976d2; font-size: 0.9rem;">✈️ 언제든지 여행 관련 질문을 해주세요 🗺️</p>
</div>
""", unsafe_allow_html=True)
