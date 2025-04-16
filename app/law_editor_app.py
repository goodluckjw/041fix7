import streamlit as st
from utils.xml_parser import parse_law_xml
from utils.api_request import fetch_law_list, fetch_law_detail

st.set_page_config(page_title="부칙 개정 도우미", layout="wide")

st.title("📘 부칙 개정 도우미")
st.caption("법령 본문 중 검색어를 포함하는 조문을 찾아줍니다.")

search_word = st.text_input("🔍 찾을 단어", placeholder="예: 건조물")

if "result" not in st.session_state:
    st.session_state.result = {}

if st.button("🔎 법률 검색"):
    st.session_state.result = fetch_law_list(search_word)

if st.session_state.get("result"):
    st.success(f"✅ 총 {len(st.session_state.result)}개의 법령을 찾았습니다.")
    for law_name, law_url in st.session_state.result.items():
        with st.expander(law_name):
            st.markdown(f"🔗 [원문 보기]({law_url})")
            xml_content = fetch_law_detail(law_url)
            if xml_content:
                matches = parse_law_xml(xml_content, search_word)
                if matches:
                    for match in matches:
                        st.markdown(match, unsafe_allow_html=True)
                else:
                    st.info("🔎 해당 검색어를 포함한 조문이 없습니다.")