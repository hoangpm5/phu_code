import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard công việc", layout="wide")
st.title("Dashboard quản lý công việc")
st.markdown("Theo dõi các công việc cần làm trong ngày.")

#session state
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=[
        "Công việc",
        "ưu tiên",
        "Hạn",
        "Trạng thái"
    ])
# form thêm việc
with st.form("task_form"):
    task = st.text_input("tên công việc")
    priority = st.selectbox(
        "Mức ưu tiên",
        [" Cao", "Trung bình", "Thấp"]
    )
    deadline = st.date_input("Hạn hoàn thành")
    submit = st.form_submit_button("Thêm")
    if submit:
        if task != "":
            new_row = pd.DataFrame([{
                "Công việc": task,
                "Ưu tiên": priority,
                "Hạn": deadline,
                "Trạng thái": "Chưa xong"
            }])

            st.session_state.tasks = pd.concat(
                [st.session_state.tasks, new_row],
                ignore_index=True
            )
            st.success("Đã thêm công việc !")
        else:
            st.warning("Vui lòng nhập tên công việc. ")
#danh sách
st.subheader("Danh sách công việc ")
if len(st.session_state.tasks) > 0:
    tasks = st.session_state.tasks.copy()
    for i in range(len(tasks)):
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.write(
                f"{tasks.loc[i, 'Công việc']} |"
                f"{tasks.loc[i, 'Ưu tiên']} |"
                f"{tasks.loc[i, 'Hạn']} |"
                f"{tasks.loc[i, 'Trạng thái']}"
            )
        with col2:
            if tasks.loc[i, "Trạng thái"] == "Chưa xong":
                if st.button("✅ Done", key = f"done{i}"):
                    st.session_state.tasks.loc[i, "Trạng thái"] = " Hoàn thành"
                    st.rerun()
        with col3:
            if st.button("Xóa", key=f"delete{i}"):
                st.session_state.tasks = st.session_state.tasks.drop(i).reset_index(drop=True)
                st.rerun()
        st.divider()
        st.dataframe(
            st.session_state.tasks,
            use_container_width=True
        )
else:
    st.info("chưa có công việc nào. ")
st.subheader("Thống kê")
total = len(st.session_state.tasks)

done = len(
    st.session_state.tasks[
        st.session_state.tasks["Trạng thái"] == "Hoàn thành"
    ]
)
pending = total - done

c1, c2, c3 = st.columns(3)

c1.metric("Tổng", total)
c1.metric("Đã hoàn thành ", done)
c1.metric("Còn lại ", pending)

#biểu đồ
st.subheader("Tiến độ công việc")
chart = pd.DataFrame({
    "Trạng thái":[
        "Hoàn thành",
        "Chưa xong"
    ],
    "Số lượng":[
        done,
        pending
    ]
})
st.bar_chart(chart.set_index("Trạng thái"))

#xuất Excel
st.subheader("xuất excel")
def convert_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Tasks"
        )

    return output.getvalue()

excel = convert_excel(st.session_state.tasks)
st.download_button(
    " Tải excel",
    data= excel,
    file_name = "todo_list.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

#ty le hoan thanh
if total > 0:
    percent =  done/total
    st.subheader("Tiến độ hoàn thành ")
    st.progress(percent)
    st.write(f"đã hoàn thành {percent*100: .1f}% công việc.")