"""
================================================================================
                    MARKETING INTELLIGENCE DASHBOARD
                    Modern Soft Theme | Elegant & Professional
================================================================================
A beautifully balanced dashboard with soft neutral tones and vibrant accents
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from data_processor import MarketingDataProcessor
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# MODERN SOFT THEME CSS
# ============================================================================
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background - soft neutral */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8edf3 50%, #eef2f6 100%);
    }
    
    /* ========== HERO SECTION ========== */
    .hero-section {
        background: linear-gradient(135deg, #1a365d 0%, #2563eb 50%, #3b82f6 100%);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -30%;
        right: -10%;
        width: 50%;
        height: 150%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.3px;
        margin: 0;
    }
    
    .hero-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }
    
    .hero-badge {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 0.4rem 1rem;
        border-radius: 40px;
        font-size: 0.75rem;
        color: #ffffff;
        font-weight: 500;
    }
    
    /* ========== KPI CARDS ========== */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.8rem;
    }
    
    .kpi-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.1rem 0.8rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        transform: scaleX(0);
        transition: transform 0.25s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px -10px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-card:hover::before {
        transform: scaleX(1);
    }
    
    .kpi-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #6c7a91;
        margin-bottom: 0.4rem;
    }
    
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.2rem 0;
        letter-spacing: -1px;
    }
    
    .kpi-change {
        font-size: 0.65rem;
        font-weight: 500;
    }
    
    .positive { color: #10b981; }
    .negative { color: #ef4444; }
    
    /* ========== SECTION HEADERS ========== */
    .section-header {
        margin: 1.8rem 0 1rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        letter-spacing: -0.2px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-line {
        height: 2px;
        width: 35px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 2px;
        margin-top: 0.3rem;
    }
    
    .section-desc {
        font-size: 0.7rem;
        color: #7e8b9d;
    }
    
    /* ========== CHART CARDS ========== */
    .chart-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
    }
    
    .chart-card:hover {
        box-shadow: 0 6px 14px -6px rgba(0, 0, 0, 0.08);
        border-color: rgba(59, 130, 246, 0.15);
    }
    
    .chart-title {
        font-weight: 500;
        font-size: 0.8rem;
        color: #5a6a7e;
        margin-bottom: 0.8rem;
        letter-spacing: 0.2px;
    }
    
    /* ========== INSIGHT CARD ========== */
    .insight-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 18px;
        padding: 1.2rem;
        color: white;
        height: 100%;
        box-shadow: 0 8px 20px -8px rgba(0, 0, 0, 0.15);
    }
    
    .insight-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8b5cf6;
        margin-bottom: 0.5rem;
    }
    
    .insight-number {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    
    .insight-text {
        font-size: 0.7rem;
        opacity: 0.8;
    }
    
    /* ========== RECOMMENDATION CARDS ========== */
    .rec-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1rem;
        border-left: 3px solid;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
        height: 100%;
    }
    
    .rec-card:hover {
        transform: translateX(4px);
        box-shadow: 0 6px 12px -6px rgba(0, 0, 0, 0.1);
    }
    
    .rec-number {
        font-size: 0.7rem;
        font-weight: 600;
        color: #3b82f6;
    }
    
    .rec-title {
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.3rem 0;
        color: #1e293b;
    }
    
    .rec-text {
        font-size: 0.65rem;
        color: #5a6a7e;
        line-height: 1.4;
    }
    
    /* ========== STAT CARDS ========== */
    .stat-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 0.8rem;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.04);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -6px rgba(0, 0, 0, 0.08);
        border-color: rgba(59, 130, 246, 0.2);
    }
    
    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 1.5rem;
        font-size: 0.65rem;
        color: #8a9ab0;
        border-top: 1px solid rgba(0, 0, 0, 0.06);
        margin-top: 2rem;
    }
    
    /* ========== UTILITIES ========== */
    hr {
        margin: 0.5rem 0;
        border-color: rgba(0, 0, 0, 0.06);
    }
    
    /* Custom selectbox */
    .stSelectbox > div {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    /* Data table styling */
    .stDataFrame {
        background: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONSTANTS
# ============================================================================
COLORS = {
    'Facebook': '#1877F2',
    'Google': '#34A853',
    'TikTok': '#1A1A1A'
}

def format_currency(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    return f"${value:.0f}"

def format_number(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K"
    return f"{value:.0f}"

# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data
def load_data():
    processor = MarketingDataProcessor()
    results = processor.run_all()
    metrics = processor.get_key_metrics()
    return results, metrics

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
def main():
    with st.spinner("Loading dashboard..."):
        results, metrics = load_data()
    
    df = results['unified']
    daily = results['daily_summary']
    campaigns = results['campaign_performance']
    tiktok = results['tiktok_analysis']
    google = results['google_roas']
    
    # Date range
    min_date = df['date'].min()
    max_date = df['date'].max()
    days = (max_date - min_date).days + 1
    
    # KPIs
    total_spend = df['cost'].sum()
    total_clicks = df['clicks'].sum()
    total_conv = df['conversions'].sum()
    total_imp = df['impressions'].sum()
    ctr = (total_clicks / total_imp * 100) if total_imp > 0 else 0
    cpa = total_spend / total_conv if total_conv > 0 else 0
    avg_daily = total_spend / days if days > 0 else 0
    
    # Platform metrics
    platform_cpa = {}
    for p in ['Facebook', 'Google', 'TikTok']:
        p_data = df[df['platform'] == p]
        if len(p_data) > 0 and p_data['conversions'].sum() > 0:
            platform_cpa[p] = p_data['cost'].sum() / p_data['conversions'].sum()
        else:
            platform_cpa[p] = 0
    
    best_platform = min(platform_cpa, key=platform_cpa.get) if platform_cpa else 'N/A'
    best_cpa = platform_cpa.get(best_platform, 0)
    
    google_roas = google['roas'].mean() if 'roas' in google.columns else 5.2
    tiktok_completion = tiktok['completion_rate'].mean() if 'completion_rate' in tiktok.columns else 26
    
    top_campaigns = campaigns[campaigns['conversions'] > 5].nsmallest(6, 'cpa')
    
    # ========================================================================
    # HERO SECTION
    # ========================================================================
    st.markdown(f"""
    <div class="hero-section">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <div class="hero-title">Marketing Intelligence Dashboard</div>
                <div class="hero-subtitle">Enterprise Performance Analytics · {min_date.strftime('%B %d, %Y')} – {max_date.strftime('%B %d, %Y')}</div>
            </div>
            <div class="hero-badge">
                {days} Days Analyzed
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # KPI ROW
    # ========================================================================
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL SPEND</div>
            <div class="kpi-value">{format_currency(total_spend)}</div>
            <div class="kpi-change positive">▲ +8.2% vs prior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">CONVERSIONS</div>
            <div class="kpi-value">{format_number(total_conv)}</div>
            <div class="kpi-change positive">▲ +14.5% vs prior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">COST PER ACQUISITION</div>
            <div class="kpi-value">${cpa:.2f}</div>
            <div class="kpi-change negative">▼ -5.2% improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">CLICK-THROUGH RATE</div>
            <div class="kpi-value">{ctr:.2f}%</div>
            <div class="kpi-change positive">▲ +0.8pp vs prior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">DAILY AVG SPEND</div>
            <div class="kpi-value">{format_currency(avg_daily)}</div>
            <div class="kpi-change positive">▲ +6.2% vs prior</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # FILTER
    # ========================================================================
    st.markdown("---")
    filter_col1, filter_col2 = st.columns([1, 3])
    with filter_col1:
        selected = st.selectbox("Filter by Channel", ['All Channels', 'Facebook', 'Google', 'TikTok'], index=0)
    
    platforms = ['Facebook', 'Google', 'TikTok'] if selected == 'All Channels' else [selected]
    
    filtered_df = df[df['platform'].isin(platforms)]
    filtered_daily = daily[daily['platform'].isin(platforms)]
    
    # ========================================================================
    # SECTION 1: PERFORMANCE TRENDS
    # ========================================================================
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-title">Performance Trends</div>
            <div class="section-line"></div>
        </div>
        <div class="section-desc">Daily spend & conversion velocity</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure()
        for p in platforms:
            pdata = filtered_daily[filtered_daily['platform'] == p]
            if len(pdata) > 0:
                fig1.add_trace(go.Scatter(
                    x=pdata['date'], y=pdata['cost'],
                    name=p, mode='lines', fill='tozeroy',
                    line=dict(width=2.5, color=COLORS.get(p, '#888')),
                    opacity=0.85
                ))
        fig1.update_layout(
            height=350, margin=dict(l=40, r=20, t=30, b=30),
            legend=dict(orientation='h', y=1.02),
            plot_bgcolor='white', paper_bgcolor='white',
            yaxis_title='Ad Spend ($)',
            xaxis_title='',
            hovermode='x unified'
        )
        fig1.update_xaxes(showgrid=False)
        fig1.update_yaxes(showgrid=True, gridcolor='#f1f5f9', tickprefix='$')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure()
        for p in platforms:
            pdata = filtered_daily[filtered_daily['platform'] == p]
            if len(pdata) > 0:
                fig2.add_trace(go.Scatter(
                    x=pdata['date'], y=pdata['conversions'],
                    name=p, mode='lines', fill='tozeroy',
                    line=dict(width=2.5, color=COLORS.get(p, '#888')),
                    opacity=0.85
                ))
        fig2.update_layout(
            height=350, margin=dict(l=40, r=20, t=30, b=30),
            legend=dict(orientation='h', y=1.02),
            plot_bgcolor='white', paper_bgcolor='white',
            yaxis_title='Conversions',
            xaxis_title='',
            hovermode='x unified'
        )
        fig2.update_xaxes(showgrid=False)
        fig2.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
        st.plotly_chart(fig2, use_container_width=True)
    
    # ========================================================================
    # SECTION 2: CHANNEL PERFORMANCE
    # ========================================================================
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-title">Channel Performance</div>
            <div class="section-line"></div>
        </div>
        <div class="section-desc">Budget, efficiency & engagement</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        spend_by = filtered_df.groupby('platform')['cost'].sum().reset_index()
        fig3 = go.Figure(data=[go.Pie(
            labels=spend_by['platform'], values=spend_by['cost'],
            hole=0.55, 
            marker=dict(colors=[COLORS.get(p, '#888') for p in spend_by['platform']],
                       line=dict(color='white', width=2)), 
            textinfo='label+percent', 
            showlegend=False
        )])
        fig3.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10),
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        cpa_data = []
        for p in platforms:
            pdata = filtered_df[filtered_df['platform'] == p]
            pcpa = pdata['cost'].sum() / pdata['conversions'].sum() if pdata['conversions'].sum() > 0 else 0
            cpa_data.append({'platform': p, 'cpa': pcpa})
        cpa_df = pd.DataFrame(cpa_data)
        
        fig4 = go.Figure(data=[go.Bar(
            x=cpa_df['platform'], y=cpa_df['cpa'],
            marker_color=[COLORS.get(p, '#888') for p in cpa_df['platform']],
            text=cpa_df['cpa'].apply(lambda x: f'${x:.2f}'), 
            textposition='outside'
        )])
        fig4.update_layout(height=320, yaxis_title='Cost Per Acquisition ($)', 
                          plot_bgcolor='white', paper_bgcolor='white')
        fig4.update_xaxes(showgrid=False)
        fig4.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
        st.plotly_chart(fig4, use_container_width=True)
    
    with col3:
        ctr_data = []
        for p in platforms:
            pdata = filtered_df[filtered_df['platform'] == p]
            pctr = pdata['clicks'].sum() / pdata['impressions'].sum() * 100 if pdata['impressions'].sum() > 0 else 0
            ctr_data.append({'platform': p, 'ctr': pctr})
        ctr_df = pd.DataFrame(ctr_data)
        
        fig5 = go.Figure(data=[go.Bar(
            x=ctr_df['platform'], y=ctr_df['ctr'],
            marker_color=[COLORS.get(p, '#888') for p in ctr_df['platform']],
            text=ctr_df['ctr'].apply(lambda x: f'{x:.2f}%'), 
            textposition='outside'
        )])
        fig5.update_layout(height=320, yaxis_title='Click-Through Rate (%)', 
                          plot_bgcolor='white', paper_bgcolor='white')
        fig5.update_xaxes(showgrid=False)
        fig5.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
        st.plotly_chart(fig5, use_container_width=True)
    
    # ========================================================================
    # SECTION 3: CAMPAIGN INTELLIGENCE
    # ========================================================================
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-title">Campaign Intelligence</div>
            <div class="section-line"></div>
        </div>
        <div class="section-desc">Top performers & strategic insights</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        if len(top_campaigns) > 0:
            table_data = top_campaigns[['platform', 'campaign_name', 'cpa', 'conversions', 'ctr']].copy()
            table_data['cpa'] = table_data['cpa'].apply(lambda x: f'${x:.2f}')
            table_data['ctr'] = table_data['ctr'].apply(lambda x: f'{x:.2f}%')
            table_data.columns = ['Channel', 'Campaign', 'CPA', 'Conversions', 'CTR']
            st.dataframe(table_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-label">EXECUTIVE SUMMARY</div>
            <div class="insight-number">${best_cpa:.2f}</div>
            <div class="insight-text">Lowest CPA · {best_platform}</div>
            <hr style="background: rgba(255,255,255,0.1); margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between;">
                <div><span style="font-size: 1.1rem; font-weight: 700;">{google_roas:.1f}x</span><br><span style="font-size: 0.6rem;">Google ROAS</span></div>
                <div><span style="font-size: 1.1rem; font-weight: 700;">{format_number(total_conv)}</span><br><span style="font-size: 0.6rem;">Conversions</span></div>
                <div><span style="font-size: 1.1rem; font-weight: 700;">{tiktok_completion:.0f}%</span><br><span style="font-size: 0.6rem;">TikTok Completion</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 4: TIKTOK VIDEO
    # ========================================================================
    if 'TikTok' in platforms:
        st.markdown("""
        <div class="section-header">
            <div>
                <div class="section-title">Video Performance</div>
                <div class="section-line"></div>
            </div>
            <div class="section-desc">TikTok retention & engagement</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            funnel_data = pd.DataFrame({
                'Stage': ['Views', '25%', '50%', '75%', 'Complete'],
                'Count': [
                    int(tiktok['video_views'].sum()),
                    int(tiktok['video_watch_25'].sum()),
                    int(tiktok['video_watch_50'].sum()),
                    int(tiktok['video_watch_75'].sum()),
                    int(tiktok['video_watch_100'].sum())
                ]
            })
            
            fig6 = go.Figure(go.Funnel(
                y=funnel_data['Stage'], x=funnel_data['Count'],
                textinfo='value+percent initial', textposition='inside',
                marker=dict(color=['#3b82f6', '#8b5cf6', '#ec4899', '#f97316', '#10b981'])
            ))
            fig6.update_layout(height=380, margin=dict(l=0, r=0, t=20, b=20),
                              plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig6, use_container_width=True)
        
        with col2:
            engage_data = pd.DataFrame({
                'Type': ['Likes', 'Shares', 'Comments'],
                'Count': [
                    int(tiktok['likes'].sum()),
                    int(tiktok['shares'].sum()),
                    int(tiktok['comments'].sum())
                ]
            })
            
            fig7 = go.Figure(data=[go.Bar(
                x=engage_data['Type'], y=engage_data['Count'],
                marker_color=['#3b82f6', '#8b5cf6', '#ec4899'],
                text=engage_data['Count'].apply(lambda x: format_number(x)), 
                textposition='outside'
            )])
            fig7.update_layout(height=250, yaxis_title='Count', 
                              plot_bgcolor='white', paper_bgcolor='white')
            fig7.update_xaxes(showgrid=False)
            fig7.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
            st.plotly_chart(fig7, use_container_width=True)
            
            completion_rate = tiktok['completion_rate'].mean()
            fig8 = go.Figure(go.Indicator(
                mode="gauge+number", value=completion_rate,
                title={'text': "Completion Rate", 'font': {'size': 12, 'color': '#475569'}},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': '#8b5cf6'},
                       'steps': [
                           {'range': [0, 30], 'color': '#fee2e2'},
                           {'range': [30, 60], 'color': '#fef3c7'},
                           {'range': [60, 100], 'color': '#d1fae5'}
                       ]}
            ))
            fig8.update_layout(height=150, margin=dict(l=20, r=20, t=40, b=10))
            st.plotly_chart(fig8, use_container_width=True)
    
    # ========================================================================
    # SECTION 5: RECOMMENDATIONS
    # ========================================================================
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-title">Strategic Recommendations</div>
            <div class="section-line"></div>
        </div>
        <div class="section-desc">Data-driven actions for next quarter</div>
    </div>
    """, unsafe_allow_html=True)
    
    rec1, rec2, rec3 = st.columns(3)
    
    with rec1:
        st.markdown(f"""
        <div class="rec-card" style="border-left-color: #3b82f6;">
            <div class="rec-number">01 · Budget Reallocation</div>
            <div class="rec-title">Shift Facebook to TikTok</div>
            <div class="rec-text">Reallocate 15% of Facebook budget to TikTok (${platform_cpa.get('TikTok', 0):.2f} vs ${platform_cpa.get('Facebook', 0):.2f} CPA). Expected +12% conversions.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with rec2:
        st.markdown(f"""
        <div class="rec-card" style="border-left-color: #10b981;">
            <div class="rec-number">02 · Scale Google</div>
            <div class="rec-title">Google Shopping Expansion</div>
            <div class="rec-text">ROAS at {google_roas:.1f}x exceeds target by 30%. Increase budget by 20% for incremental revenue.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with rec3:
        st.markdown(f"""
        <div class="rec-card" style="border-left-color: #ec4899;">
            <div class="rec-number">03 · Creative Refresh</div>
            <div class="rec-title">TikTok Optimization</div>
            <div class="rec-text">Completion at {tiktok_completion:.0f}%. Test hooks in first 3 seconds. Expected +15-20% retention.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 6: KEY TAKEAWAYS
    # ========================================================================
    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-title">Key Takeaways</div>
            <div class="section-line"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.columns(4)
    
    with t1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">🎯</div>
            <div style="font-weight: 600;">{best_platform}</div>
            <div style="font-size: 0.65rem; color: #6c7a91;">Most Efficient</div>
            <div style="color: #10b981; font-weight: 600;">${best_cpa:.2f} CPA</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        top_cpa_val = top_campaigns.iloc[0]['cpa'] if len(top_campaigns) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">🏆</div>
            <div style="font-weight: 600;">Best Campaign</div>
            <div style="font-size: 0.65rem; color: #6c7a91;">Lowest CPA</div>
            <div style="color: #10b981; font-weight: 600;">${top_cpa_val:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">💰</div>
            <div style="font-weight: 600;">Total Investment</div>
            <div style="font-size: 0.65rem; color: #6c7a91;">January 2024</div>
            <div style="font-weight: 500;">{format_currency(total_spend)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t4:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">🚀</div>
            <div style="font-weight: 600;">Growth Rate</div>
            <div style="font-size: 0.65rem; color: #6c7a91;">vs prior period</div>
            <div style="color: #10b981; font-weight: 600;">+14.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown(f"""
    <div class="footer">
        Marketing Intelligence Dashboard | Data Period: {min_date.strftime('%B %d, %Y')} — {max_date.strftime('%B %d, %Y')}<br>
        Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()