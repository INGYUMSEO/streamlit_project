
import streamlit as st
import pandas as pd
import requests
import time

# 기본 설정
st.set_page_config(page_title="사업자등록 상태 조회", layout="centered")
st.title("📄 국세청 사업자등록 상태 조회 서비스")

# 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드 (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=1)
    df['사업자등록번호'] = df['사업자번호'].astype(str).str.zfill(10)

    SERVICE_KEY = "qI0GOBGZY/ErxFs2+tOzlj7RGmsMsUgAf+wxKrCJooMIa/+wRxxr696f6Ka9kWaHmzZD6Ttvhc0iNCHoyEY9vw=="
    API_URL = "https://api.odcloud.kr/api/nts-businessman/v1/status"
    headers = {'Content-Type': 'application/json'}

    biz_nums = df['사업자등록번호'].tolist()
    results = []
    chunk_size = 100

    with st.spinner("🔍 사업자 상태 조회 중..."):
        for i in range(0, len(biz_nums), chunk_size):
            chunk = biz_nums[i:i+chunk_size]
            payload = {"b_no": chunk}

            try:
                response = requests.post(API_URL, headers=headers, params={"serviceKey": SERVICE_KEY}, json=payload)
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    results.extend(data)
                else:
                    st.error(f"❌ 요청 실패: {response.status_code}")
            except Exception as e:
                st.error(f"❌ 예외 발생: {e}")
            time.sleep(1)

    result_df = pd.DataFrame(results)
    merged_df = df.merge(result_df, left_on="사업자등록번호", right_on="b_no", how="left")

    st.success("✅ 조회 완료!")
    st.dataframe(merged_df[['업체명', '사업자등록번호', 'b_stt', 'tax_type', 'end_dt']])

    # 다운로드 버튼
    st.download_button(
        label="💾 결과 엑셀 다운로드",
        data=merged_df.to_excel(index=False, engine='openpyxl'),
        file_name="사업자등록상태_조회결과.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    result_df = pd.DataFrame(results)
    merged_df = df.merge(result_df, left_on="사업자등록번호", right_on="b_no", how="left")

    st.success("✅ 조회 완료!")
    st.dataframe(merged_df[['업체명', '사업자등록번호', 'b_stt', 'tax_type', 'end_dt']])

    # 다운로드 버튼
    st.download_button(
        label="💾 결과 엑셀 다운로드",
        data=merged_df.to_excel(index=False, engine='openpyxl'),
        file_name="사업자등록상태_조회결과.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

