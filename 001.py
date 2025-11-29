import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser
#pip install scikit-learn feedparser
st.sidebar.title("🎶 Danh sách nghệ sĩ")
selected_artist = st.sidebar.radio("Chọn nghệ sĩ:", ["Đen Vâu", "Hà Anh Tuấn", "Sơn Tùng M-TP", "Những bản nhạc giúp tâm trạng vui vẻ hơn"])

videos = {
    "Đen Vâu": [
        ("Bữa ăn cho em", "https://www.youtube.com/watch?v=ukHK1GVyr0I"),
        ("Mang tiền về cho mẹ", "https://www.youtube.com/watch?v=UVbv-PJXm14"),
        ("Trời hôm nay nhiều mây cực!", "https://www.youtube.com/watch?v=MBaF0l-PcRY"),
        ("Hai triệu năm", "https://www.youtube.com/watch?v=LSMDNL4n0kM")
    ],
    "Hà Anh Tuấn": [
        ("Tuyết rơi mùa hè", "https://www.youtube.com/watch?v=pTh3KCD7Euc"),
        ("Nước ngoài", "https://www.youtube.com/watch?v=pU3O9Lnp-Z0"),
        ("Tháng tư là lời nói dối của em", "https://www.youtube.com/watch?v=UCXao7aTDQM"),
        ("Xuân thì", "https://www.youtube.com/watch?v=3s1r_g_jXNs")
    ],
    "Sơn Tùng M-TP": [
        ("Lạc trôi", "https://www.youtube.com/watch?v=Llw9Q6akRo4"),
        ("Chúng ta không thuộc về nhau", "https://www.youtube.com/watch?v=qGRU3sRbaYw"),
        ("Muộn rồi mà sao còn", "https://www.youtube.com/watch?v=xypzmu5mMPY"),
        ("Hãy trao cho anh", "https://www.youtube.com/watch?v=knW7-x7Y7RE")
    ],
    "Những bản nhạc giúp tâm trạng vui vẻ hơn":[
        ("Những bản nhạc giúp tâm trạng vui vẻ hơn", "https://www.youtube.com/watch?v=SlsH6PbDJZk&t=898s"),
        ("Lỡ Duyên", "https://www.youtube.com/watch?v=fq_H4A3HgD4&list=RDfq_H4A3HgD4&start_radio=1&rv=fq_H4A3HgD4"),
        ("Bài hat về tình yêu quê hương đất nước", "https://www.youtube.com/watch?v=GOMGeUetqlI&list=RDSlsH6PbDJZk&index=3"),
        ("Đi giữa trời rực rỡ", "https://www.youtube.com/watch?v=D1Uf9vREh6Q&list=RDSlsH6PbDJZk&index=3"),
        ("STAY HOME, STAY HAPPY, STAY HÀANHTUẤN", "https://www.youtube.com/watch?v=MMgPOQ9gJhM&list=RDEMrx5Xy48sg-WCr9qiaw1hhg&index=2"),
        ("Focus Time", "https://www.youtube.com/watch?v=Lcmlq9utGYk")
    ]
}

st.title("🎧 Ứng dụng giải trí và sức khỏe")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9= st.tabs(["🎤 MV yêu thích", "💤 Dự đoán giờ ngủ", "📰 Đọc báo", "Kiểm tra sức khỏe", "Lượng nước cần uống mỗi ngày", "Bước chân mỗi ngày", "Sports", "Thời gian ngủ", "The hinh"])

with tab1:
    st.header(f"Các bài hát của {selected_artist} 🎵")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)

with tab2:
    st.header("🔮 Dự đoán giờ ngủ mỗi đêm")
    #Tuoi, mức độ hoạt động thể chất, thời gian dùng máy tính 
    x = [
        [10, 1, 8],
        [20, 5, 6],
        [25, 8, 3],
        [30, 6, 5],
        [35, 2, 9],
        [40, 4, 3]
    ]
    y = [10, 8, 6, 7, 9.5, 9]
    model = LinearRegression()
    model.fit(x, y)
    st.write("Nhập thông tin cá nhân: ")
    age = st.number_input("Tuổi của bạn", min_value= 5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    screen_time = st.number_input("Thời gian dùng màn hình trong 1 ngày (giờ)", min_value=0, max_value=24, value=6)

    if st.button("Dự đoán ngay "):
        input_data = [[age, activity, screen_time]]
        result = model.predict(input_data)[0]
        st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")

        if result < 6.5:
            st.warning("có thể bạn cần nghỉ ngơi nhiều hơn để cải thiện sức khỏe. ")
        elif result > 9:
            st.info("có thể bạn đang vận động nhiều, bạn cần ngủ bù hợp lý nhé ")
        else:
            st.success("Lượng ngủ lý tưởng, hãy giữ thói quen tốt ")
with tab3:
    st.header("📰 Tin tức mới nhất")
    tabA, tabB = st.tabs(['📰 Tin tức mới nhất từ VnExpress', 'Cập nhật giá vàng từ Vietnamnet'])
    with tabA: 
        feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
        for entry in feed.entries[:5]:
            st.subheader(entry.title)
            st.write(entry.published)
            st.write(entry.link)
    with tabB:
        st.header("💰 Cập nhật giá vàng từ Vietnamnet")
        feed = feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")
        gold_news = [entry for entry in feed.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]
        if gold_news:
            for entry in gold_news[:5]:  # Hiện 5 bài gần nhất
                st.subheader(entry.title)
                st.write(entry.published)
                st.write(entry.link)
        else:
            st.warning("Không tìm thấy bản tin giá vàng gần đây.")
with tab4:
    st.header("📊 Kiểm tra chỉ số BMI của bạn")

    can_nang = st.number_input("Nhập cân nặng của bạn (kg)", min_value=10.0, max_value=200.0, value=60.0, step=0.1)
    chieu_cao = st.number_input("Nhập chiều cao của bạn (m)", min_value=1.0, max_value=2.5, value=1.7, step=0.01)

    if st.button("📏 Tính BMI"):
        bmi = can_nang / (chieu_cao ** 2)
        st.success(f"Chỉ số BMI của bạn là: {bmi:.2f}")

        if bmi < 18.5:
            st.warning("Bạn đang thiếu cân, nên ăn uống đầy đủ và dinh dưỡng hơn.")
        elif 18.5 <= bmi < 25:
            st.info("Bạn có cân nặng bình thường. Hãy tiếp tục duy trì lối sống lành mạnh.")
        elif 25 <= bmi < 30:
            st.warning("Bạn đang thừa cân. Nên cân đối chế độ ăn và tập thể dục.")
        else:
            st.error("Bạn đang béo phì. Nên gặp chuyên gia dinh dưỡng hoặc bác sĩ để được tư vấn.")
with tab5:
    st.title("Khuyến nghị lượng nước uống mỗi ngày")
    tuoi = st.number_input("Nhập tuổi của bạn:", min_value=1, max_value=100, value=18, step=1)
    if st.button("Kiểm tra lượng nước cần uống"):
        if tuoi < 4:
            st.info("Khuyến nghị: 1.3 lít/ngày")
        elif 4 <= tuoi <= 8:
            st.info("Khuyến nghị: 1.7 lít/ngày")
        elif 9 <= tuoi <= 13:
            st.info("Khuyến nghị: 2.1 đến 2.4 lít/ngày")
        elif 14 <= tuoi <= 18:
            st.info("Khuyến nghị: 2.3 đến 3.3 lít/ngày")
        elif 19 <= tuoi <= 50:
            st.info("Khuyến nghị: 2.7 lít/ngày đối với nữ, 3.7 lít/ngày đối với nam")
        elif tuoi > 50:
            st.info("Khuyến nghị: Khoảng 2.5 đến 3.0 lít/ngày (phụ thuộc vào sức khỏe và mức độ vận động)")
        else:
            st.warning("Vui lòng nhập độ tuổi hợp lệ.")
with tab6:
    st.header("Kiểm tra số bước đi phù hợp mỗi ngày")
    age2 = st.number_input("Nhập tuổi của bạn:", min_value=0.0, max_value=130.0, value=18.0, step=1.0)
    if st.button("Kiểm tra số bước"):
        st.success(f"Tuổi của bạn: {age2:.0f}")
        if age2 < 18:
            st.info("🔹 Bạn nên đi **12.000-15.000 bước** mỗi ngày.")
        elif 17 < age2 <= 39:
            st.info("🔹 Bạn nên đi **8.000-10.000 bước** mỗi ngày.")
        elif 39 < age2 <= 64:
            st.warning("🔸 Bạn nên đi **7.000-9.000 bước** mỗi ngày.")
        elif age2 > 64:
            st.warning("🔸 Bạn nên đi **6.000-8.000 bước** mỗi ngày.")
        else:
            st.error("⚠️ Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")

with tab7:
    st.header("The latest news from VnExpress")
    feed = feedparser.parse("https://vietnamnet.vn/rss/the-thao.rss")
    for entry in feed.entries[:10]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
with tab8:
    st.title('Kiem tra thoi gian ngu moi ngay')
    tabA, tabB = st.tabs(['Tre so sinh/Moi tap di', 'Tre nho/Nguoi lon'])
    with tabA:
        thang = st.number_input('Nhap so thang tuoi: ',min_value=0, max_value=12, value=1, step=1)
        if st.button('Tinh thoi gian can ngu theo thang tuoi'):
            if thang < 4:
                st.info('Can ngu 14 - 17 tieng moi ngay')
            else:
                st.info('Can ngu 12 - 15 tieng moi ngay')
    with tabB:
        tuoi = st.number_input('Nhap do tuoi cua ban: ',min_value=0, max_value=100, value=18, step=1)
        if st.button('Tinh thoi gian can ngu'):
            if tuoi < 3:
                st.info('Can ngu 11 - 14 tieng moi ngay')
            elif tuoi < 6:
                st.info('Can ngu 10 - 13 tieng moi ngay')
            elif tuoi < 14:
                st.info('Can ngu 9 - 11 tieng moi ngay')
            elif tuoi < 18:
                st.info('Can ngu 8 - 10 tieng moi ngay')
            elif tuoi < 65:
                st.info('Can ngu 7 - 9 tieng moi ngay')
            else:
                st.info('Can ngu 7 - 8 tieng moi ngay')
with tab9:
    st.header("🏋️‍♂️ Thể hình & Giảm cân thông minh")

    goal = st.selectbox(
        "🎯 Mục tiêu tập luyện của bạn:",
        ["Giảm cân", "Giữ cân", "Tăng cơ"]
    )

    workout_days = st.slider("Bạn muốn tập bao nhiêu ngày/tuần?", 1, 7, 4)
    st.write(f"Bạn dự định tập {workout_days} buổi/tuần để đạt mục tiêu {goal.lower()}.")

    # 🔹 Ước tính nhu cầu calo theo mục tiêu
    if 'tdee' in locals():
        if goal == "Giảm cân":
            target_calories = tdee - 400
        elif goal == "Giữ cân":
            target_calories = tdee
        else:
            target_calories = tdee + 300

        st.subheader("Nhu cầu năng lượng theo mục tiêu")
        st.write(f"- **TDEE:** {tdee:.0f} kcal/ngày")
        st.write(f"- **Lượng calo khuyến nghị để {goal.lower()}:** `{target_calories:.0f}` kcal/ngày")

        # 🔹 Gợi ý tỉ lệ dinh dưỡng
        st.markdown("### 🍗 Tỉ lệ dinh dưỡng gợi ý:")
        if goal == "Giảm cân":
            st.write("**Protein:** 40% | **Carb:** 35% | **Fat:** 25%")
        elif goal == "Giữ cân":
            st.write("**Protein:** 30% | **Carb:** 45% | **Fat:** 25%")
        else:
            st.write("**Protein:** 35% | **Carb:** 45% | **Fat:** 20%")

        # 🔹 Gợi ý thực đơn
        st.markdown("### Gợi ý bữa ăn hằng ngày:")
        if goal == "Giảm cân":
            st.markdown("""
            - **Sáng:** Yến mạch + sữa chua Hy Lạp + trái cây  
            - **Trưa:** Cơm gạo lứt, ức gà, rau luộc  
            - **Tối:** Salad cá hồi / đậu phụ + rau củ  
            - **Snack:** Hạnh nhân, sữa không đường  
            """)
        elif goal == "Tăng cơ":
            st.markdown("""
            - **Sáng:** Trứng + bánh mì nguyên cám + sữa  
            - **Trưa:** Cơm, thịt bò, rau xanh  
            - **Tối:** Cá hồi, khoai lang, rau củ  
            - **Sau tập:** Whey protein hoặc sữa chocolate ít béo  
            """)
        else:
            st.markdown("""
            - **Sáng:** Trứng + trái cây + bánh mì đen  
            - **Trưa:** Cơm + thịt gà + rau  
            - **Tối:** Cá + rau + trái cây  
            """)

        # 🔹 Bài tập theo mục tiêu
        st.markdown("### 🏃‍♂️ Gợi ý bài tập:")
        if goal == "Giảm cân":
            st.info("""
            - Cardio: chạy bộ, đạp xe, nhảy dây (4–5 buổi/tuần)  
            - Tập sức mạnh: Squat, Push-up, Plank (3 buổi/tuần)  
            - Nghỉ ngơi hợp lý, ngủ đủ 7–8 tiếng  
            """)
        elif goal == "Tăng cơ":
            st.info("""
            - Tập tạ 4–5 buổi/tuần (chia nhóm cơ: ngực, lưng, chân, tay)  
            - Ăn nhiều protein, đặc biệt sau tập  
            - Cardio nhẹ (2 buổi/tuần) để duy trì tim mạch  
            """)
        else:
            st.info("""
            - Kết hợp cả cardio và tập tạ  
            - Giữ thói quen vận động đều, duy trì năng lượng ổn định  
            """)
    else:
        st.warning("Hãy phân tích sức khỏe (phần đầu) để hệ thống tính TDEE trước khi tạo kế hoạch thể hình.")