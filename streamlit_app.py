import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="France EV Charging Infrastructure",
    page_icon="⚡",
    layout="wide"
)

# Custom css for dark mode
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0;
    }
    .subtitle {
        font-size: 1.3rem;
        color: #999;
        text-align: center;
        margin-bottom: 3rem;
    }
    .section-title {
        font-size: 2.2rem;
        font-weight: bold;
        color: #667eea;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-bottom: 4px solid #667eea;
        padding-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }
    .insight-box {
        background: rgba(102, 126, 234, 0.05);
        border-left: 6px solid #667eea;
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        color: #ccc;
    }
    .insight-box h3 {
        color: #667eea;
        margin-top: 0;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    .insight-box p {
        color: #ccc;
        line-height: 1.8;
        font-size: 1.05rem;
        margin: 0.8rem 0;
    }
    .insight-box strong {
        color: #667eea;
        font-weight: 700;
    }
    .insight-box ul {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    .insight-box li {
        color: #ccc;
        margin: 0.8rem 0;
        line-height: 1.7;
    }
    .metric-card {
        background: rgba(102, 126, 234, 0.08);
        padding: 2.5rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        color: #667eea;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #999;
        margin-top: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .conclusion-box {
        background: rgba(76, 175, 80, 0.05);
        border-left: 6px solid #4caf50;
        padding: 2.5rem;
        margin: 2rem 0;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        color: #ccc;
    }
    .conclusion-box h3 {
        color: #4caf50;
        margin-top: 0;
        font-size: 1.4rem;
        margin-bottom: 1.2rem;
    }
    .conclusion-box p {
        color: #ccc;
        line-height: 1.8;
        font-size: 1.05rem;
        margin: 1rem 0;
    }
    .conclusion-box ul {
        margin: 1.2rem 0;
        padding-left: 1.5rem;
    }
    .conclusion-box li {
        color: #ccc;
        margin: 0.9rem 0;
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    /* Navigation header styling */
    [data-testid="stSidebar"] h1 {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 600;
        padding-bottom: 0.5rem;
    }
    
    /* Enhanced button styling with hover effects */
    [data-testid="stSidebar"] button {
        width: 100%;
        text-align: left;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 500;
        color: #e0e0e0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Hover effect */
    [data-testid="stSidebar"] button:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(102, 126, 234, 0.1) 100%);
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
        color: #ffffff;
    }
    
    /* Active/clicked state */
    [data-testid="stSidebar"] button:active {
        transform: translateX(3px) scale(0.98);
        box-shadow: 0 2px 4px rgba(255, 75, 75, 0.3);
    }
    
    /* About section styling */
    [data-testid="stSidebar"] h3 {
        color: #667eea;
        font-size: 1.1rem;
        margin-top: 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #667eea;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    /* Divider styling */
    [data-testid="stSidebar"] hr {
        margin: 1rem 0;
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load EV charging infrastructure data from local CSV"""
    try:
        df = pd.read_csv('consolidation-etalab-schema-irve-statique-v-2.3.1-20251024.csv')
        return df
    except FileNotFoundError:
        st.error("File not found: consolidation-etalab-schema-irve-statique-v-2.3.1-20251024.csv")
        st.info("Make sure the CSV file is in the same directory as this script.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def prepare_data(df):
    """Clean and prepare data"""
    if df is None:
        return None
    
    if 'date_mise_en_service' in df.columns:
        df['date_mise_en_service'] = pd.to_datetime(df['date_mise_en_service'], errors='coerce')
        df['year_installed'] = df['date_mise_en_service'].dt.year
    
    if 'puissance_nominale' in df.columns:
        df['puissance_nominale'] = pd.to_numeric(df['puissance_nominale'], errors='coerce')
    
    if 'nbre_pdc' in df.columns:
        df['nbre_pdc'] = pd.to_numeric(df['nbre_pdc'], errors='coerce')
    
    bool_cols = ['prise_type_ef', 'prise_type_2', 'prise_type_combo_ccs', 
                 'prise_type_chademo', 'gratuit', 'paiement_acte', 'paiement_cb', 
                 'reservation']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().isin(['true', '1', 'yes']).astype(int)
    
    if 'consolidated_commune' in df.columns:
        df['commune'] = df['consolidated_commune']
    
    return df


# ============================================================================
# NAVIGATION SETUP
# ============================================================================
# Initialize session state for navigation
if 'current_section' not in st.session_state:
    st.session_state.current_section = "I"

# Define sections with descriptions
SECTIONS = {
    "I": {"title": "The State of French EV Today"},
    "II": {"title": "Year-by-Year Growth Acceleration"},
    "III": {"title": "Regional Concentration & Disparities"},
    "IV": {"title": "The Critical Role of Fast Charging"},
    "V": {"title": "Technical Standardization: Connector Types"},
    "VI": {"title": "Payment Methods & Reservations"},
    "VII": {"title": "Closing the Infrastructure Gap"},
    "VIII": {"title": "Conclusion"},
    "IX": {"title": "Data Sources & Methodology"},
}

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("# Navigation")
    st.markdown("---")
    
    for section_key, section_info in SECTIONS.items():
        button_label = f"{section_key} / {section_info['title']}"
        if st.button(button_label, key=f"nav_{section_key}", use_container_width=True):
            st.session_state.current_section = section_key
            st.rerun()
    
    st.markdown("---")
    st.markdown("### About")
    st.caption("**Data Analysis and Visualization** : Final Project")
    st.caption("by AININE Nassim, 20220610")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

st.markdown('<h1 class="main-title">⚡ France\'s Electric Future </h1>', unsafe_allow_html=True)

with st.spinner("Loading charging station data..."):
    df_raw = load_data()

if df_raw is None:
    st.stop()

df = prepare_data(df_raw)

if df is None or len(df) == 0:
    st.error("No valid data available after preprocessing.")
    st.stop()

current_section = st.session_state.current_section

# ============================================================================
# I / The State of French EV Infrastructure Today
# ============================================================================

if current_section == "I":
    st.markdown("""
    Electric vehicles are the future of transportation. But they need one very critical thing : charging infrastructure. 
    This document is about how France is racing to build a nationwide network of charging stations, and whether 
    it is able to keep pace with the electric revolution. As such, the main question that we will need to tackle is the following : Is France ready for an all-electric future ?
    """)

    st.markdown('<h2 class="section-title">I / The State of French EV Infrastructure Today</h2>', unsafe_allow_html=True)

    total_stations = len(df)
    total_charge_points = df['nbre_pdc'].sum() if 'nbre_pdc' in df.columns else 0
    total_power = df['puissance_nominale'].sum() if 'puissance_nominale' in df.columns else 0
    total_operators = df['nom_operateur'].nunique() if 'nom_operateur' in df.columns else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_stations:,}</div>
            <div class="metric-label">Charging Stations</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(total_charge_points):,}</div>
            <div class="metric-label">Charge Points</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(total_power/1000):.0f} MW</div>
            <div class="metric-label">Total Power Capacity</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_operators}</div>
            <div class="metric-label">Network Operators</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
    <h3>The current state of things :</h3>
    <p>
    Right now, all across France, there are 176,286 charging stations standing ready for electric vehicles. That's 2,345,294 charge points. 
    This is enough electricity to simultaneously charge <strong>hundreds of thousands of cars</strong>. 
    Together, they pack 12430 megawatts of raw capacity, scattered from coastal towns to Alpine villages.
    </p>
    <p>
    But there is however a twist: all this infrastructure isn't controlled by one company. <strong>321 different operators are fighting for dominance</strong>. 
    Energy corporations, EV specialists, and startup are all fighting for position. 
    Competition does help create innovation, but it also means chaos, 
    such as issues with incompatible payment apps, different pricing schemes and a fragmented networks that feel less like one system
    </p>
    <p>
    Finally there is one last and main issue : is 2,345,294 charge points enough ? France wants 15 million EVs on the road by 2030. 
    The industry standard is one public charger per 10 vehicles. If we do the math for this, <strong>France will need 1.5 million charge points</strong>. 
    That number is approximately 10 times what exists today.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# II / The Build-Out: Year-by-Year Growth Acceleration
# ============================================================================
elif current_section == "II":
    st.markdown('<h2 class="section-title">II / Year-by-Year Growth Acceleration</h2>', unsafe_allow_html=True)

    if 'year_installed' in df.columns:
        df_years = df[df['year_installed'].notna()]
        df_years = df_years[(df_years['year_installed'] >= 2010) & (df_years['year_installed'] <= 2025)]
        
        if len(df_years) > 0:
            yearly_installs = df_years.groupby('year_installed').size().reset_index()
            yearly_installs.columns = ['Year', 'New_Stations']
            yearly_installs['Cumulative_Stations'] = yearly_installs['New_Stations'].cumsum()
            
            fig_growth = go.Figure()
            
            fig_growth.add_trace(go.Bar(
                x=yearly_installs['Year'],
                y=yearly_installs['New_Stations'],
                name='New Stations',
                marker_color='#667eea',
                yaxis='y'
            ))
            
            fig_growth.add_trace(go.Scatter(
                x=yearly_installs['Year'],
                y=yearly_installs['Cumulative_Stations'],
                name='Cumulative Total',
                line=dict(color='#d32f2f', width=4),
                yaxis='y2',
                marker=dict(size=8)
            ))
            
            fig_growth.update_layout(
                title_text='<b style="color: #ccc;">EV Charging Station Growth: The Exponential Curve</b>',
                title_font_size=18,
                xaxis=dict(title_text='<b style="color: #ccc;">Year</b>', title_font_size=14, tickfont=dict(color='#999')),
                yaxis=dict(title_text='<b style="color: #ccc;">New Stations per Year</b>', side='left', title_font_size=13, tickfont=dict(color='#999')),
                yaxis2=dict(title_text='<b style="color: #ccc;">Cumulative Total</b>', overlaying='y', side='right', title_font_size=13, tickfont=dict(color='#999')),
                hovermode='x unified',
                height=600,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, color='#ccc')
            )
            
            st.plotly_chart(fig_growth, use_container_width=True)
            
            recent_years = yearly_installs[yearly_installs['Year'] >= 2020]
            if len(recent_years) >= 2:
                avg_growth = recent_years['New_Stations'].mean()
                peak_year = yearly_installs.loc[yearly_installs['New_Stations'].idxmax(), 'Year']
                peak_installs = yearly_installs['New_Stations'].max()
                
                st.markdown(f"""
                <div class="insight-box">
                <h3>The Acceleration Phase (2020-2025)</h3>
                <p>
                Let's take a look at this graph. The red line curving upward is no accident. We can see that France has had a huge growth spurt. 
                <strong>Since 2020, the country has been deploying an average of 15,544 charging stations per year</strong>. 
                Not incrementally, nor cautiously, but in a very aggressive manner.
                </p>
                <p>
                The main shift happened around 2019/2020. That's the moment when the growth stopped being linear and instead became exponential. The reason ? 
                Because the urgency finally sank in. 
                Climate change isn't abstract anymore, and they finally noticed that EVs aren't a luxury, but that they are necessary. The Governments started setting mandates, 
                and private companies smelled opportunity. 
                </p>
                <p>
                <strong>2024 was the peak year: 25,210 new stations installed in a single year</strong>. It wasn't because it became easy to install thanks to technology getting easier. 
                It was money flowing. Highway rest stops were mandated to install chargers. Commercial parking lots followed. 
                Employers realized their EV-driving employees needed places to charge during the workday. Everything was falling into place.
                </p>
                <p>
                But again, one very important question comes to mind : can France keep this up ? For the next six years ? And without slowing down ? The easy part was done. 
                The hard part comes next: rural areas, faster deployment timelines and scaling supply chains across the country. 
                The acceleration has to continue, or the 2030 target just becomes wishful thinking.
                </p>
                </div>
                """, unsafe_allow_html=True)


# ============================================================================
# III / Geography Matters: Regional Concentration & Disparities</h2>
# ============================================================================
elif current_section == "III":
    st.markdown('<h2 class="section-title">III / Regional Concentration & Disparities</h2>', unsafe_allow_html=True)


    st.markdown("### Top 15 Communes")
    if 'commune' in df.columns:
        commune_counts = df['commune'].value_counts().head(15).reset_index()
        commune_counts.columns = ['Commune', 'Stations']
        
        fig_communes = px.bar(
            commune_counts,
            x='Stations',
            y='Commune',
            orientation='h',
            color='Stations',
            color_continuous_scale='Blues',
            title='Charging Stations by City'
        )
        fig_communes.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            title_font_color='#ccc',
            font=dict(size=11, color='#ccc'),
            xaxis=dict(tickfont=dict(color='#999')),
            yaxis=dict(tickfont=dict(color='#999'))
        )
        st.plotly_chart(fig_communes, use_container_width=True)
        
        top_commune = commune_counts.iloc[0]['Commune']
        top_commune_count = commune_counts.iloc[0]['Stations']

    st.markdown(f"""
    <div class="insight-box">
    <h3>The Urban vs Rural Divide</h3>
    <p>
    If you're living in Paris, it is a paradise for EVs. There are 394 charging stations in your city. Around any corner you'll be able to find a charger. 
    But, outside the cities, the rural side of France looks completely different. <strong>Small towns and villages ? Charging deserts</strong>. 
    One charging point serving thousands of people, for kilometers around.
    </p>
    <p>
    The reasons are economics. Cities have density, lots of people, money and demand. Rural areas are sparse, which means chargers sit unused. 
    Private operators cannot justify the investment, so they don't build. <strong>Rural EVs drivers are at an impasse</strong>. They're stuck relying on home charging 
    or taking long detours to the nearest city. The EV revolution has an urban bias, and it is getting worse, not better.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Top 10 Operators")
    if 'nom_operateur' in df.columns:
        operator_counts = df['nom_operateur'].value_counts().head(10).reset_index()
        operator_counts.columns = ['Operator', 'Stations']
        
        fig_ops = px.bar(
            operator_counts,
            x='Stations',
            y='Operator',
            orientation='h',
            color='Stations',
            color_continuous_scale='Purples',
            title='Stations by Network Operator'
        )
        fig_ops.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            title_font_color='#ccc',
            font=dict(size=11, color='#ccc'),
            xaxis=dict(tickfont=dict(color='#999')),
            yaxis=dict(tickfont=dict(color='#999'))
        )
        st.plotly_chart(fig_ops, use_container_width=True)
        
        top_operator = operator_counts.iloc[0]['Operator']
        top_operator_count = operator_counts.iloc[0]['Stations']     

    
    st.markdown(f"""
    <div class="insight-box">
    <h3>Fragmentation and Useless issues</h3>
    <p>
    Then there is the operator question. Power Dot France controls 13,069 stations, with only Bouygues Energies and & Services right behind. 
    That's a huge margin of power in a market with 321 operators total. On paper it would look fragmented, but in reality a few giants dominate. 
    Which means different apps for charging, different payment systems, different customer service and many others annoying side-effects. 
    <strong>Unsurprisingly, drivers hate this fragmentation. They want one app, one payment method, one seamless experience</strong>. 
    Instead they get a random looking patchwork of a system that feels like it was assembled from spare parts.
    </p>
    </div>
    """, unsafe_allow_html=True)
   

# ============================================================================
# IV / The Critical Role of Fast Charging
# ============================================================================
elif current_section == "IV":
    st.markdown('<h2 class="section-title">IV / The Critical Role of Fast Charging</h2>', unsafe_allow_html=True)

    if 'puissance_nominale' in df.columns:
        df_power = df[df['puissance_nominale'].notna()]
        
        df_power['charging_speed'] = pd.cut(
            df_power['puissance_nominale'],
            bins=[0, 22, 50, 150, 10000],
            labels=['Slow (≤22kW)', 'Medium (22-50kW)', 'Fast (50-150kW)', 'Ultra-Fast (>150kW)']
        )
        
        power_dist = df_power['charging_speed'].value_counts().reset_index()
        power_dist.columns = ['Charging_Speed', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_power_pie = px.pie(
                power_dist,
                values='Count',
                names='Charging_Speed',
                title='Charging Infrastructure Mix',
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig_power_pie.update_layout(
                height=550,
                title_font_size=16,
                title_font_color='#ccc',
                font=dict(size=12, color='#ccc'),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig_power_pie.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
            st.plotly_chart(fig_power_pie, use_container_width=True)
        
        with col2:
            fig_power_bar = px.bar(
                power_dist.sort_values('Count', ascending=True),
                x='Count',
                y='Charging_Speed',
                orientation='h',
                title='Number of Stations per Speed Tier',
                color='Count',
                color_continuous_scale='Viridis'
            )
            fig_power_bar.update_layout(
                height=550,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=16,
                title_font_color='#ccc',
                font=dict(size=12, color='#ccc'),
                xaxis=dict(tickfont=dict(color='#999')),
                yaxis=dict(tickfont=dict(color='#999'))
            )
            st.plotly_chart(fig_power_bar, use_container_width=True)
            
        st.markdown(f"""
        <div class="insight-box">
        <h3> The Speed Trap</h3>
        <p>
        This is where France's infrastructure reveals its weakness. 58.8% of chargers are slow (≤22kW). 
        It is not all bad, they are great for overnight charging at home. You can park your car at 8pm, and wake up with 150-200km of range.
        But for everyone else ? For families planning road trips ? For people who need a charge in 30 minutes ? <strong>These slow chargers are useless</strong>.
        </p>
        <p>
        Now the real issue: <strong>only 27.9% of stations offer fast or ultra-fast charging (>50kW)</strong>. These are the chargers that matter for long-distance travel.
        They can give an EV 200km in 20-30 minutes, making them able to to compete with gas cars. But they are very rare and scattered. Mostly on highways, occasionally in cities.
        Not enough.
        </p>
        <p>
        This is the paradox of this infrastructure : France has a network optimized for daily commuting (slow home charging). 
        What it didn't build was the nervous system for road trips, something very important for France.  
        The solution ? France needs a highway revolution. DC fast chargers every 150km along major routes. Chargers in commercial areas and at rest stops. Not someday now. 
        Because without them, mass EV adoption <strong>will stay just out of reach</strong>.
        </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# V / Technical Standardization: Connector Types
# ============================================================================
elif current_section == "V":
    st.markdown('<h2 class="section-title">V / Technical Standardization: Connector Types</h2>', unsafe_allow_html=True)

    plug_types = {}

    if 'prise_type_2' in df.columns:
        plug_types['Type 2 (AC standard)'] = int(df['prise_type_2'].astype(int).sum())

    if 'prise_type_combo_ccs' in df.columns:
        plug_types['CCS Combo (DC fast)'] = int(df['prise_type_combo_ccs'].astype(int).sum())

    if 'prise_type_chademo' in df.columns:
        plug_types['CHAdeMO (DC)'] = int(df['prise_type_chademo'].astype(int).sum())

    if 'prise_type_ef' in df.columns:
        plug_types['Type EF (AC)'] = int(df['prise_type_ef'].astype(int).sum())

    plug_df = pd.DataFrame(list(plug_types.items()), columns=['Plug_Type', 'Count'])
    plug_df = plug_df[plug_df['Count'] > 0].sort_values('Count', ascending=False)

    if len(plug_df) > 0:
        fig_plugs = px.bar(
            plug_df,
            x='Plug_Type',
            y='Count',
            title='Available Connector Types Across France',
            color='Count',
            color_continuous_scale='Teal',
            labels={'Count': 'Number of Stations', 'Plug_Type': 'Connector Type'}
        )
        fig_plugs.update_layout(
            height=550,
            showlegend=False,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            title_font_color='#ccc',
            font=dict(size=12, color='#ccc'),
            xaxis=dict(tickfont=dict(color='#999')),
            yaxis=dict(tickfont=dict(color='#999'))
        )
        st.plotly_chart(fig_plugs, use_container_width=True)
        
    st.markdown(f"""
    <div class="insight-box">
    <h3>The Standardization Miracle and its downsides</h3>
    <p>
    In early 2010s EV charging was a nightmare. Tesla had its own connector. Japan used CHAdeMO. Europe ? <strong>Multiple competing standards fighting for dominance.</strong>
    Drivers needed adapters for adapters. It was chaos. Then Europe got smart and mandated standardization. 
    Type 2 became the EU standard for AC charging, and it's everywhere now, in 110,073 stations. That's progress.
    Nissan, a Tesla, a Renault : now they all use the same connector. <strong>One cable fits all.</strong>
    </p>
    <p>
    For fast charging, CCS Combo is winning (59,433 stations worldwide). It's becoming the global standard. Even Tesla caved and adopted it in Europe. 
    This is good, because convergence means compatibility, which means fewer headaches for drivers.
    But there are still issues however. CHAdeMO (10,357 stations) is slowly dying. Nissan owners will <strong>soon find their cars to be obsolete.</strong>
    Japanese EV drivers are also feeling the pressure as their charger network dies too. This is standardization's dark side: winners and losers, created overnight.
    </p>
    <p>
    There is still a remaining problem. While the plugs are standardized, <strong>everything else is fragmented</strong>. Payment systems -> Dozens of apps. 
    Pricing -> Wildly inconsistent. Availability -> Unpredictable. You can plug in anywhere, but actually using the charger is where the headaches starts.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VI / Accessibility: Payment Methods & Reservations
# ============================================================================
elif current_section == "VI":
    st.markdown('<h2 class="section-title">VI / Accessibility: Payment Methods & Reservations</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Payment Landscape")
        
        payment_methods = {}
        
        if 'paiement_cb' in df.columns:
            payment_methods['Credit Card'] = int(df['paiement_cb'].astype(int).sum())
        
        if 'paiement_acte' in df.columns:
            payment_methods['Pay-as-you-go'] = int(df['paiement_acte'].astype(int).sum())
        
        if 'gratuit' in df.columns:
            payment_methods['Free'] = int(df['gratuit'].astype(int).sum())
        
        payment_df = pd.DataFrame(list(payment_methods.items()), columns=['Payment_Type', 'Count'])
        payment_df = payment_df[payment_df['Count'] > 0].sort_values('Count', ascending=False)
        
        if len(payment_df) > 0:
            fig_payment = px.pie(
                payment_df,
                values='Count',
                names='Payment_Type',
                title='Payment Options at Stations',
                color_discrete_sequence=['#2563eb', '#fbbf24', '#a855f7']
            )
            fig_payment.update_layout(
                height=550,
                title_font_size=16,
                title_font_color='#ccc',
                font=dict(size=12, color='#ccc'),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig_payment.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
            st.plotly_chart(fig_payment, use_container_width=True)

    with col2:
        st.markdown("### Reservation Capability")
        
        if 'reservation' in df.columns:
            has_reservation = int(df['reservation'].astype(int).sum())
            total_with_booking = len(df[df['reservation'].notna()])
            reservation_pct = (has_reservation / total_with_booking * 100) if total_with_booking > 0 else 0
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{reservation_pct:.1f}%</div>
                <div class="metric-label">Stations Support Reservations</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="insight-box">
            <p>
            Here's a problem that'll make any future EV driver anxious: <strong>only 23.0%</strong> of charging stations let you reserve ahead. 
            You arrive, needing a charge, and… someone else is already there. Now you have to wait. Maybe 20 minutes, maybe an hour. Or you drive to the next 
            station, hoping it's free. Gas cars have gas stations on every corner. 
            </p>
            <p> 
            But EVs ? <strong>You're gambling.</strong> 
            </p>
            <p>
            Payment-wise, credit card is king. Most stations accept it. But some don't. Some need subscriptions. And some only work with specific apps. 
            Like said in previous sections, it's a fragmented mess of systems. What if gas stations worked like this, with each pump accepting different payment methods, 
            each requiring its own membership card ? Drivers would riot. But EV drivers ? They just sigh and have to download yet another app. 
            <strong>It's the EV tax: hassle, friction, and frustration.</strong>
            </p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# VII / The 2030 Challenge: Closing the Infrastructure Gap
# ============================================================================
elif current_section == "VII":
    st.markdown('<h2 class="section-title">VII / The 2030 Challenge: Closing the Infrastructure Gap</h2>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
    <p>
    France has set an ambitious target: <strong>15 million electric vehicles on roads by 2030</strong>. Industry experts recommend 
    maintaining at least 1 public charging point per 10 vehicles. This means France needs 1.5 million charge points 
    by 2030. The question is: <strong>can we get there from where we are today ?</strong>
    </p>
    </div>
    """, unsafe_allow_html=True)

    total_stations = len(df)
    total_charge_points = df['nbre_pdc'].sum() if 'nbre_pdc' in df.columns else 0
    total_power = df['puissance_nominale'].sum() if 'puissance_nominale' in df.columns else 0
    total_operators = df['nom_operateur'].nunique() if 'nom_operateur' in df.columns else 0

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Scenario Analysis")
        
        # Use actual current charge points
        current_points = int(total_charge_points)
        target_2030 = 1_500_000
        years_remaining = 2030 - 2025
        
        growth_rate = st.slider(
            "Annual growth rate (%)",
            min_value=10,
            max_value=60,
            value=30,
            step=5,
            help="Adjust the slider to see different growth scenarios. Historical growth has been around 25-40%."
        )
        
        projected_2030 = current_points * ((1 + growth_rate/100) ** years_remaining)
        gap = target_2030 - projected_2030
        gap_percent = (gap / target_2030 * 100)
        
        st.metric("Current Charge Points (2025)", f"{current_points:,}")
        st.metric(f"Projected 2030 (at {growth_rate}% growth)", f"{int(projected_2030):,}")
        
        if gap > 0:
            st.metric("Shortfall", f"{int(gap):,}", 
                    delta=f"{gap_percent:.1f}% below target", delta_color="inverse")
        else:
            st.metric("Surplus", f"{int(abs(gap)):,}", 
                    delta=f"{abs(gap_percent):.1f}% above target", delta_color="normal")

    with col2:
        st.markdown("### Projection Trajectory")
        
        years = list(range(2025, 2031))
        projected = [current_points * ((1 + growth_rate/100) ** (y - 2025)) for y in years]
        
        fig_projection = go.Figure()
        
        fig_projection.add_trace(go.Scatter(
            x=years,
            y=projected,
            mode='lines+markers',
            name='Projected Growth',
            line=dict(color='#667eea', width=4),
            marker=dict(size=10)
        ))
        
        fig_projection.add_hline(
            y=target_2030,
            line_dash="dash",
            line_color="red",
            line_width=3,
            annotation_text="2030 Target: 1.5M",
            annotation_position="right"
        )
        
        fig_projection.update_layout(
            title_text='<b style="color: #ccc;">Path to 2030: Can France Close the Gap ?</b>',
            yaxis_title='<b style="color: #ccc;">Total Charge Points</b>',
            xaxis_title='<b style="color: #ccc;">Year</b>',
            hovermode='x unified',
            height=550,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            font=dict(size=12, color='#ccc'),
            xaxis=dict(tickfont=dict(color='#999')),
            yaxis=dict(tickfont=dict(color='#999'))
        )
        
        st.plotly_chart(fig_projection, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <h3>The Result</h3>
    <p>
    At {growth_rate}% annual growth, France reaches {int(projected_2030):,} charge points by 2030.
    </p>
    <p>
    That actually exceeds the target by {int(abs(gap)):,} charge points. At this growth rate, France would 
    be well-positioned to support 15 million EVs by 2030. <strong>But there's a catch: maintaining {growth_rate}% growth 
    for five straight years requires everything to go right</strong>.
    </p>
    <p>
    No supply chain disruptions. No economic downturns that freeze investment. No regulatory 
    slowdowns. No political shifts (Probably the hardest thing for France). This pace requires sustained momentum across government policy, private investment, and infrastructure 
    deployment. One major hiccup and the trajectory could drastically change.
    </p>
    <p>
    If France can pull it off, they'll become Europe's EV infrastructure leader. However, if they stumble, they'll join 
    the long list of ambitious targets that sounded great but never materialized.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# VIII / Conclusion
# ============================================================================
elif current_section == "VIII":

    st.markdown('<h2 class="section-title">VIII / What Does This All Mean ?</h2>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
    <h3>Connecting the Dots</h3>

    <p>
    By going through France's EV charging infrastructure, the numbers tell a story. 176,286 stations, 2,345,294 charge points, exponential growth since 2020. On paper ? Impressive. 
    In reality ? It's more complicated.
    </p>

    <p>The Good News: <strong>the Momentum is Real !</strong></p>
    <p>
    France isn't sitting still. The acceleration from 2020-2025 proves it. Exponential growth, not linear. 321 operators competing means innovation is happening. 
    The infrastructure foundation is solid. Not perfect, not complete, but <strong>real</strong>.
    </p>

    <p>But the <strong>Bad News</strong> Outweighs It</p>
    <p>
    Here's what the data actually shows when you stop looking at charts and start thinking about what it means to drive an EV in France:
    </p>

    <ul>
    <li><strong>Scale</strong> is a nightmare. We need 10x what we have in 6 years. That's not ambitious, it's more like madness. </li>
    <li>The urban-rural <strong>split</strong> is getting worse, not better. Cities like Paris are swimming in chargers. But small towns ? Forgotten. This builds resentment. 
        It builds inequality. It's unsustainable politically.</li>
    <li>Road trips are still a <strong>gamble.</strong> 27.9% fast chargers means highway EV travel remains uncertain. Families hesitate.</li>
    <li>Every station requires a <strong>different app.</strong> 23.0% let you reserve. Different payment systems. Different pricing. It's a mess. 
        And a mess means friction, which in turn means dead adoption.</li>
    <li><strong>One supply chain hiccup, and everything falls apart.</strong> There's no buffer. We're running at max capacity to hit targets. Any disruption cascades.</li>
    </ul>

    <p>
    This isn't about chargers. It's about whether Europe can decarbonize fast enough. The EU committed to <strong>climate neutrality</strong> by 2050. 
    That's mostly glitter for the eyes without transport transformation. And transport transformation is impossible without charging infrastructure. 
    France's infrastructure determines whether France's EV adoption succeeds. France's success determines whether Europe gets there.
    </p>

    <p>
    And there's geopolitics here too. China is already dominating EV manufacturing AND charging. America is throwing billions at it. 
    If France, Europe's largest economy by many measures, fails this, China will win the infrastructure race. And whoever owns the charging ecosystem 
    for the next 50 years owns a piece of every vehicle's daily life.
    </p>

    <p>
    <strong>The Uncomfortable Truth</strong> is that while France is building infrastructure at a pace that looks good on a PowerPoint, 
    it probably won't cut it for the real world. 
    It's moving faster than it did 5 years ago, but not fast enough for what comes next.
    Which means delayed EV adoption. Which means delayed decarbonization. Which means climate timelines get tighter.
    </p>

    <p style="font-size: 1.1rem; font-weight: bold; margin-top: 2rem; color: #fbbf24; border-top: 2px solid #4caf50; padding-top: 1.5rem;">
    France has achieved measurable progress. Infrastructure development is accelerating.
    However, quantitative growth alone does not equate to an operationally coherent system.

    True success will come when drivers can charge their vehicles seamlessly, anywhere, at any time, through a unified application and payment interface. 
    France is establishing the necessary foundation.
    The next and more complex phase lies ahead : ensuring functional integration and reliability across the entire network.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA SOURCES
# ============================================================================
elif current_section == "IX":
    st.markdown("---")
    st.markdown("## Raw Data")

    with st.expander("View Data Sample (First 100 Records)"):
        st.dataframe(df.head(100), use_container_width=True, height=400)
        st.markdown(f"**Total records in dataset:** {len(df):,}")

    st.markdown("---")
    st.markdown("""
    **Data Source:** Consolidation ETALAB - Base Nationale des IRVE  
    **Coverage:** France (metropolitan and overseas), all public charging stations  
    **Last Updated:** October 24, 2025  
    **Format:** CSV (consolidation-etalab-schema-irve-statique-v-2.3.1-20251024.csv)   
    **Link:** https://www.data.gouv.fr/datasets/base-nationale-des-irve-infrastructures-de-recharge-pour-vehicules-electriques/#/resources/eb76d20a-8501-400e-b336-d85724de5435

    **Key Variables:**
    - `date_mise_en_service`: Installation date
    - `nom_station`: Station name
    - `nom_operateur`: Network operator
    - `puissance_nominale`: Power rating (kW)
    - `nbre_pdc`: Number of charge points
    - `consolidated_commune`: Location (city)
    - `prise_type_*`: Available connector types
    """, unsafe_allow_html=True)

st.markdown("""---""")
st.markdown("""Data Analysis & Visualization | AININE Nassim | 20220610
""")
