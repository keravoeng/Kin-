import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="Kin - Personal Voice AI", page_icon="🤖", layout="wide")

st.title("🤖 Kin (คิน) - ผู้ช่วย AI ส่วนตัว")
st.caption("พูดคำว่า 'คิน' ตามด้วยสิ่งที่คุณอยากรู้ได้เลย!")

# ช่องใส่ API Key สำหรับเชื่อมต่อสมอง AI
api_key = st.sidebar.text_input("ใส่ Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.8-flash")
    # โค้ด HTML/JavaScript สำหรับรับเสียงบน Android Chrome
    st.markdown("""
    <script>
    function startDictation() {
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "th-TH";
            recognition.start();

            recognition.onresult = function(e) {
                var transcript = e.results[0][0].transcript;
                recognition.stop();
                
                // ส่งค่าเสียงที่พูดเข้าช่องค้นหาใน Streamlit
                var inputArea = window.parent.document.querySelector('textarea[aria-label="ช่องพิมพ์สั่งงานน้อง Kin:"]');
                if (inputArea) {
                    inputArea.value = transcript;
                    inputArea.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };

            recognition.onerror = function(e) {
                recognition.stop();
            }
        }
    }
    </script>
    """, unsafe_allow_html=True)

    # ปุ่มกดฟังเสียง
    if st.button("🎙️ กดเพื่อพูดกับ Kin"):
        st.info("🎧 กำลังฟัง... พูดคำว่า 'คิน ...' ได้เลยครับ")
        st.components.v1.html("<script>startDictation()</script>", height=0)

    # ช่องรับคำสั่ง (จากการพูดหรือพิมพ์)
    query = st.text_input("ช่องพิมพ์สั่งงานน้อง Kin:", placeholder="เช่น คิน ช่วยหาความรู้เรื่องอวกาศหน่อย")

    if query:
        # ตรวจจับ Wake word "คิน"
        clean_query = query.replace("คิน", "").strip()
        
        with st.spinner(f"Kin กำลังหาข้อมูลเกี่ยวกับ '{clean_query}' ให้ครับ..."):
            try:
                # คำสั่งให้ AI ค้นหาและเตรียมลิงก์
                prompt = f"""คุณคือ Kin ผู้ช่วย AI 
                โปรดตอบคำถามต่อไปนี้เป็นภาษาไทยอย่างกระชับและเข้าใจง่าย: {clean_query}
                พร้อมกับให้ Keyword ภาษาอังกฤษสำหรับนำไปค้นหาเว็บเพิ่มเติมต่อด้วย
                """
                response = model.generate_content(prompt)
                
                st.subheader("💡 Kin สรุปให้ฟัง:")
                st.write(response.text)
                
                # สร้างลิงก์ค้นหาเปิดเว็บให้อัตโนมัติ
                search_url = f"https://www.google.com/search?q={clean_query}"
                st.markdown("---")
                st.subheader("🌐 เว็บไซต์ข้อมูลอ้างอิง:")
                st.markdown(f"👉 **[คลิกที่นี่เพื่อเปิดดูเว็บข้อมูลเกี่ยวกับ {clean_query}]({search_url})**")
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.warning("🔑 กรุณากรอก Gemini API Key ที่แถบด้านข้าง (Sidebar) เพื่อเปิดการทำงานของ Kin ครับ")
