import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import math

# ----------------- PAGE CONFIGURATION & THEME -----------------
st.set_page_config(
    page_title="AuraFin - AI-Driven Risk Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #161a24 100%);
        color: #e2e8f0;
    }
    
    /* Premium Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0c0e14;
        border-right: 1px solid #2d3748;
    }
    
    /* Glassmorphism Card Style */
    .metric-card {
        background: rgba(22, 28, 45, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .metric-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 10px 40px 0 rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .metric-sub {
        font-size: 0.75rem;
        color: #475569;
    }
    
    .metric-sub.positive {
        color: #34d399;
    }
    
    .metric-sub.negative {
        color: #f87171;
    }
    
    /* Glowing Headers */
    .glow-header {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #6366f1, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .glow-subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 8px;
    }
    
    /* Badges */
    .badge-anomaly {
        background-color: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_data():
    tx_file = "transactions.csv"
    hr_file = "high_risk_transactions.csv"
    
    if not os.path.exists(tx_file):
        st.error(f"Could not find `{tx_file}`. Please generate the data first.")
        return None, None
        
    df_tx = pd.read_csv(tx_file)
    df_tx['Timestamp'] = pd.to_datetime(df_tx['Timestamp'])
    df_tx['Amount'] = df_tx['Amount'].astype(float)
    
    if os.path.exists(hr_file):
        df_hr = pd.read_csv(hr_file)
        df_hr['Timestamp'] = pd.to_datetime(df_hr['Timestamp'])
        df_hr['Amount'] = df_hr['Amount'].astype(float)
    else:
        df_hr = pd.DataFrame()
        
    return df_tx, df_hr

df_tx, df_hr = load_data()

if df_tx is not None:
    # ----------------- SIDEBAR FILTERING -----------------
    st.sidebar.markdown("<h2 style='color:#818cf8;margin-top:0;'>⚡ AuraFin Filters</h2>", unsafe_allow_html=True)
    st.sidebar.write("Refine your analytics view below:")
    
    # Sidebar Category Filter
    all_categories = sorted(df_tx['Category'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Filter by Categories",
        options=all_categories,
        default=all_categories
    )
    
    # Sidebar Amount Filter
    min_amt = float(df_tx['Amount'].min())
    max_amt = float(df_tx['Amount'].max())
    
    amount_range = st.sidebar.slider(
        "Transaction Amount Range ($)",
        min_value=0.0,
        max_value=max_amt,
        value=(0.0, max_amt)
    )
    
    # Apply filters
    filtered_tx = df_tx[
        (df_tx['Category'].isin(selected_categories)) &
        (df_tx['Amount'] >= amount_range[0]) &
        (df_tx['Amount'] <= amount_range[1])
    ]
    
    # Calculate stats
    mean_val = df_tx['Amount'].mean()
    std_val = df_tx['Amount'].std()
    
    # ----------------- MAIN LAYOUT -----------------
    st.markdown("<h1 class='glow-header'>AuraFin // Risk Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;margin-top:-10px;margin-bottom:30px;'>AI-powered statistical anomaly engine & Fintech data analytics dashboard.</p>", unsafe_allow_html=True)
    
    # Key Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_volume = filtered_tx['Amount'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Volume</div>
            <div class="metric-value">${total_volume:,.2f}</div>
            <div class="metric-sub">{len(filtered_tx):,} transactions filtered</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        avg_amount = filtered_tx['Amount'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Spending</div>
            <div class="metric-value">${avg_amount:,.2f}</div>
            <div class="metric-sub">Across all selected items</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        # Standard deviation for filtered set
        std_dev_calc = filtered_tx['Amount'].std()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Standard Deviation</div>
            <div class="metric-value">${std_dev_calc:,.2f}</div>
            <div class="metric-sub">Volatility standard metric</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        # Flagged anomalies count in filtered set
        anomalies_filtered = df_hr[
            (df_hr['Category'].isin(selected_categories)) & 
            (df_hr['Amount'] >= amount_range[0]) & 
            (df_hr['Amount'] <= amount_range[1])
        ]
        anomaly_count = len(anomalies_filtered)
        st.markdown(f"""
        <div class="metric-card" style="border-color: rgba(239, 68, 68, 0.2);">
            <div class="metric-label" style="color: #fca5a5;">Flagged Anomalies</div>
            <div class="metric-value" style="background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); -webkit-background-clip: text;">{anomaly_count}</div>
            <div class="metric-sub negative">{anomaly_count / len(filtered_tx) * 100:.2f}% anomaly rate</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts Section
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.markdown("<div class='glow-subheader'>Spending by Category</div>", unsafe_allow_html=True)
        
        # Aggregate category data
        cat_data = filtered_tx.groupby('Category')['Amount'].sum().reset_index()
        cat_data = cat_data.sort_values(by='Amount', ascending=False)
        
        # Interactive Plotly chart with custom sleek theme
        fig = px.bar(
            cat_data,
            x='Category',
            y='Amount',
            color='Amount',
            color_continuous_scale=['#818cf8', '#6366f1', '#4f46e5', '#4338ca'],
            text_auto='.2s'
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Inter',
            font_color='#cbd5e1',
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=11, color='#94a3b8')
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=11, color='#94a3b8'),
                title="Total Amount ($)"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with chart_col2:
        st.markdown("<div class='glow-subheader'>Category Composition</div>", unsafe_allow_html=True)
        
        # Custom sleek donut chart
        fig_donut = px.pie(
            cat_data,
            values='Amount',
            names='Category',
            hole=0.45,
            color_discrete_sequence=['#6366f1', '#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#06b6d4']
        )
        
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Inter',
            font_color='#cbd5e1',
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(
                font=dict(size=10, color='#94a3b8'),
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            )
        )
        
        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent',
            marker=dict(line=dict(color='#0e1117', width=2))
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)

    # Anomalies Section
    st.markdown("<div class='glow-subheader'>⚠️ Flagged Anomalies & High-Risk Activities</div>", unsafe_allow_html=True)
    st.write("These transactions represent transaction amounts deviating by more than **3 standard deviations** from the population mean. Immediate review is advised.")
    
    if len(anomalies_filtered) > 0:
        # Show anomalies with beautiful styling
        # Round columns for visual neatness
        anom_display = anomalies_filtered.copy()
        anom_display['Amount'] = anom_display['Amount'].map(lambda x: f"${x:,.2f}")
        anom_display['Deviation_StdDev'] = anom_display['Deviation_StdDev'].map(lambda x: f"+{x:.1f} σ")
        anom_display = anom_display.rename(columns={
            "Transaction_ID": "Transaction ID",
            "User_ID": "User ID",
            "Timestamp": "Timestamp",
            "Category": "Category",
            "Location": "Location",
            "Deviation_StdDev": "Risk Deviation"
        })
        
        # Display as a dataframe with highlighting
        st.dataframe(
            anom_display,
            use_container_width=True,
            column_config={
                "Risk Deviation": st.column_config.TextColumn(
                    "Risk Deviation",
                    help="How many standard deviations this transaction deviates from the mean amount.",
                )
            }
        )
        
        # Interactive details drawer
        st.markdown("### 🔍 Outlier Analysis Detail")
        selected_txn = st.selectbox(
            "Select a transaction ID for deeper investigation:",
            options=anomalies_filtered['Transaction_ID'].unique()
        )
        
        if selected_txn:
            details = anomalies_filtered[anomalies_filtered['Transaction_ID'] == selected_txn].iloc[0]
            
            d_col1, d_col2, d_col3 = st.columns(3)
            
            with d_col1:
                st.info(f"**Transaction ID**: `{details['Transaction_ID']}`  \n**User ID**: `{details['User_ID']}`  \n**Timestamp**: `{details['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')}`")
            with d_col2:
                st.warning(f"**Amount**: `${details['Amount']:,.2f}`  \n**Category**: `{details['Category']}`  \n**Location**: `{details['Location']}`")
            with d_col3:
                dev = float(details['Deviation_StdDev'])
                st.error(f"**Risk Level**: `CRITICAL`  \n**Statistical Deviation**: `+{dev:.2f} σ`  \n**Anomaly Probability**: `> 99.999%`  \n*Note: Flagged because amount exceeded normal threshold of ${mean_val + 3*std_val:,.2f}*")
                
    else:
        st.success("No anomalies found matching current filters.")

    # Statistical distribution chart
    st.markdown("<div class='glow-subheader'>🔬 Transaction Amount Distribution</div>", unsafe_allow_html=True)
    st.write("A log-scale distribution displaying normal transactional bounds versus extreme outlier activities.")
    
    # Generate log scale bins for transaction amounts
    # Normal amounts are mostly < 1500, anomalies are up to 1.2M. Let's make an interactive plot using plotly.
    df_tx['Log_Amount'] = df_tx['Amount'].apply(lambda x: math.log10(x) if x > 0 else 0)
    
    fig_dist = px.histogram(
        df_tx,
        x='Amount',
        nbins=200,
        log_y=True,
        title="Transaction Volatility Curve (Log Scale Count)",
        color_discrete_sequence=['#6366f1']
    )
    
    fig_dist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Inter',
        font_color='#cbd5e1',
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.02)',
            title="Transaction Size ($)",
            tickprefix="$",
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            title="Frequency (Log Scale Count)",
            zeroline=False
        )
    )
    
    # Add anomaly boundary indicator line
    fig_dist.add_vline(
        x=mean_val + 3 * std_val,
        line_width=2,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="3σ Anomaly Threshold",
        annotation_position="top right"
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)

else:
    st.info("Loading dataset...")
