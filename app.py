import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 全局大屏现代视觉配置
st.set_page_config(page_title="POPMART 招聘多维分析大屏", layout="wide", initial_sidebar_state="expanded")

# 注入自定义高端视觉CSS样式
st.markdown("""
    <style>
        .reportview-container { background: #F8F9FA; }
        .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        h1 { font-weight: 800 !important; color: #0F172A !important; font-family: 'PingFang SC', sans-serif; }
        h2 { font-weight: 700 !important; color: #1E293B !important; border-bottom: 3px solid #636EFA; padding-bottom: 0.4rem; margin-top: 1.5rem; }
        h3 { font-weight: 600 !important; color: #334155 !important; }
        div[data-testid="stMetricValue"] { font-size: 2.3rem !important; font-weight: 800 !important; color: #4F46E5 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. 严格定义院校类别库
LIST_985 = [
    '清华大学', '北京大学', '中国人民大学', '北京航空航天大学', '北京理工大学', '中国农业大学', 
    '北京师范大学', '中央民族大学', '南开大学', '天津大学', '大连理工大学', '东北大学', 
    '吉林大学', '哈尔滨工业大学', '复旦大学', '同济大学', '上海交通大学', '华东师范大学', 
    '南京大学', '东南大学', '浙江大学', '中国科学技术大学', '厦门大学', '山东大学', 
    '中国海洋大学', '武汉大学', '华中科技大学', '湖南大学', '中南大学', '中山大学', 
    '华南理工大学', '四川大学', '重庆大学', '电子科技大学', '西安交通大学', '西北工业大学', 
    '西北农林科技大学', '兰州大学', '国防科技大学'
]
LIST_ART_8 = ['中央美术学院', '中国美术学院', '西安美术学院', '四川美术学院', '鲁迅美术学院', '广州美术学院', '天津美术学院', '湖北美术学院']
LIST_LANG_8 = ['北京外国语大学', '上海外国语大学', '西安外国语大学', '四川外国语大学', '天津外国语大学', '大连外国语大学', '广东外语外贸大学', '北京第二外国语学院']
LIST_211_ONLY = [
    '中国传媒大学', '上海大学', '暨南大学', '对外经济贸易大学', '中南财经政法大学', '上海财经大学', 
    '郑州大学', '海南大学', '西南财经大学', '东华大学', '苏州大学', '北京林业大学', '南京师范大学', 
    '安徽大学', '北京交通大学', '华中师范大学', '华中农业大学', '武汉理工大学', '中国地质大学（武汉）',
    '中国地质大学（北京）', '中国石油大学（北京）', '中国石油大学（华东）', '中国矿业大学（北京）',
    '中国矿业大学', '华北电力大学', '北京化工大学', '北京科技大学', '北京工业大学', '北京邮电大学',
    '北京中医药大学', '北京体育大学', '中央音乐学院', '中国政法大学', '中央财经大学', '天津医科大学',
    '河北工业大学', '太原理工大学', '内蒙古大学', '辽宁大学', '大连海事大学', '东北师范大学', 
    '延边大学', '哈尔滨工程大学', '东北农业大学', '东北林业大学', '华东理工大学', '第二军医大学', 
    '南京航空航天大学', '南京理工大学', '河海大学', '江南大学', '南京农业大学', '中国药科大学', 
    '合肥工业大学', '福州大学', '南昌大学', '河南大学', '湖南师范大学', '陕西师范大学', 
    '西北大学', '西安电子科技大学', '长安大学', '青海大学', '宁夏大学', '新疆大学', 
    '石河子大学', '华南师范大学', '广西大学', '四川农业大学', '西南交通大学', '西南大学', '贵州大学', '云南大学', '西藏大学'
]
LIST_QS200 = [
    '香港大学', '悉尼大学', '新南威尔士大学', '香港城市大学', '伦敦大学学院', '曼彻斯特大学', 
    '格拉斯哥大学', '墨尔本大学', '爱丁堡大学', '哥伦比亚大学', '莫纳什大学', '香港中文大学', 
    '利兹大学', '新加坡国立大学', '南洋理工大学', '香港理工大学', '南安普顿大学', '伦敦国王学院', 
    '昆士兰大学', '布里斯托大学', '约翰霍普金斯大学', '伦敦艺术大学', '马来亚大学', '伯明翰大学', 
    '华威大学', '澳大利亚国立大学', '纽约大学', '谢菲尔德大学', '香港科技大学', '诺丁汉大学', 
    '杜伦大学', '南加利福尼亚大学', '波士顿大学', '芝加哥大学', '西北大学', '加州大学伯克利分校',
    '加州大学洛杉矶分校', '多伦多大学', '麦吉尔大学', '英属哥伦比亚大学', '早稻田大学', '东京大学', 
    '首尔大学', '延世大学', '高丽大学', '南加州大学', '宾夕法尼亚大学', '康奈尔大学'
]

def classify_university(name):
    if not isinstance(name, str): return '普通院校'
    name = name.strip()
    if name in LIST_985: return '985'
    if name in LIST_ART_8: return '八大美院'
    if name in LIST_LANG_8: return '八大外国语'
    if name in LIST_211_ONLY: return '211'
    if name in LIST_QS200: return 'QS200'
    overseas_keywords = ['大学（英国）', '学院（英国）', '大学（美国）', '香港', '澳门', '新加坡', '马来西亚', '悉尼', '墨尔本', '伦敦', '纽约', '加州', '巴黎', '东京', '首尔', '伯明翰', '曼彻斯特', '昆士兰', '莫纳什', '波士顿', '奥克兰', '多伦多', '温哥华']
    if any(kw in name for kw in overseas_keywords) or name.endswith(('University', 'College', 'School')): return '海外院校'
    if any(c.isalpha() for c in name) and not any('\u4e00' <= c <= '\u9fff' for c in name): return '海外院校'
    return '普通院校'

COLOR_PALETTE = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#374151', '#6B7280', '#9CA3AF']

# 3. 侧边栏控制台
st.sidebar.header("📁 数据与页面配置")
uploaded_files = st.sidebar.file_uploader("请上传您转换好的标准 CSV 文件", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    data_list = []
    for file in uploaded_files:
        for encoding_type in ['utf-8', 'gbk', 'utf-16', 'ansi']:
            try:
                file.seek(0)
                tmp_df = pd.read_csv(file, encoding=encoding_type)
                if len(tmp_df.columns) > 1:
                    data_list.append(tmp_df)
                    break
            except Exception: continue
            
    if data_list:
        df = pd.concat(data_list, ignore_index=True)
        
        # 智能匹配列名
        columns = df.columns.tolist()
        def auto_match(targets):
            for t in targets:
                if t in columns: return columns.index(t)
            return 0

        date_col = columns[auto_match(['最初投递时间', '最后投递时间', '投递日期', '最初投遞時間', '最後投遞時間'])]
        pos_col = columns[auto_match(['应聘职位', '职位名称', '岗位', '應聘職位', '職位名稱'])]
        edu_col = columns[auto_match(['最高学历', '学历', '最高學歷', '學歷'])]
        uni_col = columns[auto_match(['最高学历学校', '毕业学校', '学校', '最高學歷學校', '畢業學校'])]
        type_col = columns[auto_match(['面试类型', '面試類型'])]
        result_col = columns[auto_match(['全部面试结果', '全部面試結果'])]

        # 数据清洗与预处理
        df['clean_date'] = pd.to_datetime(df[date_col], errors='coerce').dt.date
        df = df.dropna(subset=['clean_date'])  
        df['院校类别'] = df[uni_col].apply(classify_university)

        # 🚀 导航栏单开页面
        st.sidebar.markdown("---")
        st.sidebar.subheader("🖥️ 切换视图页面")
        page_mode = st.sidebar.radio("请选择要查看的分析板块：", ["🏠 核心投递大屏 (单页全景)", "🎯 招聘漏斗分析专项页"])

        # ==================== 页面一：核心投递大屏 ====================
        if page_mode == "🏠 核心投递大屏 (单页全景)":
            st.title("🏠 POPMART 核心投递全景大屏")
            
            # KPI核心数据展示区
            kpi1, kpi2, kpi3 = st.columns(3)
            # 智能兼容简体和繁体字，精准提取管培生项目数据
            mt_df = df[df[pos_col].astype(str).str.contains('管培生|Trainee|国际管培生|國際管培生')]
            kpi1.metric(label="📥 简历总接收量", value=f"{len(df):,} 份")
            kpi2.metric(label="🎓 覆盖独立高校数", value=f"{df[uni_col].nunique():,} 所")
            kpi3.metric(label="🌟 国际管培生投递量", value=f"{len(mt_df):,} 份")
            st.markdown("---")
            
            # 每日投递趋势与学历占比
            col_trend_l, col_edu_r = st.columns([12, 8])
            with col_trend_l:
                daily_df = df.groupby('clean_date').size().reset_index(name='投递量').sort_values(by='clean_date')
                fig_daily = px.line(daily_df, x='clean_date', y='投递量', title="📈 每日简历收递时序趋势图", markers=True)
                fig_daily.update_traces(line=dict(width=3, color='#4A90E2'), marker=dict(size=6))
                fig_daily.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False))
                st.plotly_chart(fig_daily, use_container_width=True)
            with col_edu_r:
                edu_df = df.groupby(edu_col).size().reset_index(name='人数')
                fig_edu = px.pie(edu_df, values='人数', names=edu_col, title="🎓 候选人最高学历占比", hole=0.4, color_discrete_sequence=COLOR_PALETTE)
                fig_edu.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_edu, use_container_width=True)
            
            st.markdown("---")
            
            # 1. 院校类型可视化 & 2. 校招整体投递院校前10可视化
            st.write("## 🏛️ 院校背景与供给分析")
            col1, col2 = st.columns(2)
            
            with col1:
                cate_df = df.groupby('院校类别').size().reset_index(name='人数')
                fig_cate = px.pie(cate_df, values='人数', names='院校类别', title="🏫 1. 院校类型分布比例（独立互不包含）", hole=0.4, color_discrete_sequence=COLOR_PALETTE)
                fig_cate.update_traces(textposition='outside', textinfo='percent+label')
                st.plotly_chart(fig_cate, use_container_width=True)
                
            with col2:
                top10_df = df[uni_col].value_counts().head(10).reset_index()
                top10_df.columns = ['学校名称', '投递量']
                fig_top10 = px.bar(top10_df.sort_values(by='投递量', ascending=True), x='投递量', y='学校名称', orientation='h', title="🏆 2. 校招整体投递院校前 10 排行榜", text='投递量')
                fig_top10.update_traces(marker_color='#3B82F6', textposition='outside')
                fig_top10.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False))
                st.plotly_chart(fig_top10, use_container_width=True)
                
            st.markdown("---")
            
            # 3. 各岗位投递量可视化图表（纯视觉，无明细表）
            st.write("## 💼 3. 各岗位投递量可视化分布")
            pos_df = df.groupby(pos_col).size().reset_index(name='投递人数').sort_values(by='投递人数', ascending=True)
            fig_pos = px.bar(pos_df, x='投递人数', y=pos_col, orientation='h', title="各岗位收到简历总量横向对比（纯图表视觉呈现）", text='投递人数')
            fig_pos.update_traces(marker_color='#10B981', textposition='outside')
            fig_pos.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False))
            st.plotly_chart(fig_pos, use_container_width=True)
            
            st.markdown("---")
            
            # 🌟 4. 国际管培生项目投递院校分析可视化图表
            st.write("## 🌍 4. 国际管培生项目投递院校分析")
            if len(mt_df) > 0:
                mt_uni_df = mt_df[uni_col].value_counts().head(10).reset_index()
                mt_uni_df.columns = ['学校名称', '管培生投递量']
                fig_mt = px.bar(mt_uni_df.sort_values(by='管培生投递量', ascending=True), 
                                x='管培生投递量', y='学校名称', orientation='h', title="🎯 国际管培生专项：投递量前 10 名的高校分布图", text='管培生投递量')
                fig_mt.update_traces(marker_color='#8B5CF6', textposition='outside')
                fig_mt.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False))
                st.plotly_chart(fig_mt, use_container_width=True)
            else:
                st.warning("数据表中未检测到职位名称包含‘管培生’或‘Trainee’的记录。")

        # ==================== 页面二：招聘漏斗专项页 ====================
        elif page_mode == "🎯 招聘漏斗分析专项页":
            st.title("🎯 招聘转化漏斗与环节高校分布分析")
            st.markdown("💡 *本页面为单开专项页：专注于全链路转化效率，以及每个环节前10名的高校分布可视化。*")
            
            m_types = df[type_col].fillna('')
            m_res = df[result_col].fillna('')
            
            f_投简历 = df
            f_筛选通过 = df[df[type_col].notna() | m_res.str.contains('通过|未评价|待定|通過|未評價|待定')]
            f_进入初面 = df[m_types.str.contains('初试|初試')]
            f_初面通过 = df[m_res.str.contains('通过\(1\)|通过\(2\)|通過\(1\)|通過\(2\)') | m_types.str.contains('复试|终试|複試|終試')]
            f_复试通过 = df[m_res.str.contains('通过\(2\)|通過\(2\)') | m_types.str.contains('终试|終試')]
            f_终面通过 = df[m_types.str.contains('终试|終試') & m_res.str.contains('通过|通過')]
            f_offer = df[m_res.str.contains('录取|offer|录用|錄取|錄用', case=False)]
            f_入职 = df[m_res.str.contains('入职|到岗|入職|到崗', case=False)]
            
            # 🌟 简繁英数据多重兼容匹配，消除空白Bug
            stages = ['投简历人数', '筛选通过人数', '进入初面人数', '初面通过人数', '复试通过人数', '终面通过人数', 'offer人数', '入职人数']
            dfs = [f_投简历, f_筛选通过, f_进入初面, f_初面通过, f_复试通过, f_终面通过, f_offer, f_入职]
            counts = [len(x) for x in dfs]
            
            col_funnel_left, col_drill_right = st.columns([11, 9])
            with col_funnel_left:
                fig_funnel = go.Figure(go.Funnel(
                    y=stages, x=counts, textposition="inside", textinfo="value+percent previous+percent initial",
                    marker={"color": ['#1E3A8A', '#2563EB', '#3B82F6', '#10B981', '#059669', '#D97706', '#DC2626', '#9D174D']}
                ))
                fig_funnel.update_layout(title_text="⏳ 标准校招全流程流转漏斗模型", margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_funnel, use_container_width=True)
                
            with col_drill_right:
                st.subheader("🔍 各环节通过候选人：前10名高校分布")
                selected_stage = st.selectbox("请切换选择要分析的招聘流转环节：", stages, index=0)
                target_df = dfs[stages.index(selected_stage)]
                
                if len(target_df) > 0:
                    top10_uni = target_df[uni_col].value_counts().head(10).reset_index()
                    top10_uni.columns = ['学校名称', '该环节通过人数']
                    fig_stage_uni = px.bar(top10_uni.sort_values(by='该环节通过人数', ascending=True), 
                                    x='该环节通过人数', y='学校名称', orientation='h', title=f"🏫 {selected_stage}：通过人数最高的前 10 所高校", text='该环节通过人数')
                    fig_stage_uni.update_traces(marker_color='#EC4899', textposition='outside')
                    fig_stage_uni.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False))
                    st.plotly_chart(fig_stage_uni, use_container_width=True)
                    st.dataframe(top10_uni, use_container_width=True)
                else:
                    st.warning(f"当前选定环节【{selected_stage}】暂无候选人数据。")
else:
    st.info("👋 纯视觉多页面矩阵大屏已全线修复！请上传您转换好的标准 CSV 文件。")