import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlalchemy

# -----------------------------
# 1. PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Marine Data Explorer",
        page_icon="🌊",
            layout="wide"
            )

            # -----------------------------
            # 2. LOAD DATA (Mock or Real)
            # -----------------------------
            @st.cache_data
            def load_mock_data():
                """Generate a fake dataset for demo purposes"""
                    np.random.seed(42)
                        species_list = ["Sardinella longiceps", "Thunnus albacares", "Lutjanus campechanus"]
                            n = 300
                                df = pd.DataFrame({
                                        "species": np.random.choice(species_list, n),
                                                "latitude": np.random.uniform(8.5, 12.0, n),
                                                        "longitude": np.random.uniform(74.5, 77.0, n),
                                                                "collection_date": pd.date_range("2022-01-01", periods=n, freq="D"),
                                                                        "abundance": np.random.randint(10, 500, n),
                                                                                "temperature": np.random.uniform(22, 30, n)
                                                                                    })
                                                                                        return df

                                                                                        @st.cache_data
                                                                                        def load_real_data():
                                                                                            """Fetch data from Postgres (replace with your DB details)"""
                                                                                                try:
                                                                                                        engine = sqlalchemy.create_engine(
                                                                                                                    "postgresql://user:password@host:5432/marine"
                                                                                                                            )
                                                                                                                                    query = """
                                                                                                                                            SELECT species, latitude, longitude, collection_date, abundance, temperature
                                                                                                                                                    FROM species_occurrence
                                                                                                                                                            LIMIT 5000;
                                                                                                                                                                    """
                                                                                                                                                                            df = pd.read_sql(query, engine)
                                                                                                                                                                                    return df
                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                st.warning(f"Could not connect to database. Using mock data. Error: {e}")
                                                                                                                                                                                                        return load_mock_data()

                                                                                                                                                                                                        # -----------------------------
                                                                                                                                                                                                        # 3. SELECT MODE
                                                                                                                                                                                                        # -----------------------------
                                                                                                                                                                                                        mode = st.sidebar.radio("📂 Data Source", ["Mock Dataset", "Postgres Database"])

                                                                                                                                                                                                        if mode == "Mock Dataset":
                                                                                                                                                                                                            df = load_mock_data()
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                df = load_real_data()

                                                                                                                                                                                                                # -----------------------------
                                                                                                                                                                                                                # 4. SIDEBAR FILTERS
                                                                                                                                                                                                                # -----------------------------
                                                                                                                                                                                                                st.sidebar.header("🔍 Filters")
                                                                                                                                                                                                                species = st.sidebar.selectbox(
                                                                                                                                                                                                                    "Select Species",
                                                                                                                                                                                                                        options=["All"] + sorted(df["species"].unique().tolist())
                                                                                                                                                                                                                        )
                                                                                                                                                                                                                        date_range = st.sidebar.date_input(
                                                                                                                                                                                                                            "Select Date Range",
                                                                                                                                                                                                                                [df["collection_date"].min(), df["collection_date"].max()]
                                                                                                                                                                                                                                )

                                                                                                                                                                                                                                filtered_df = df.copy()
                                                                                                                                                                                                                                if species != "All":
                                                                                                                                                                                                                                    filtered_df = filtered_df[filtered_df["species"] == species]

                                                                                                                                                                                                                                    filtered_df = filtered_df[
                                                                                                                                                                                                                                        (filtered_df["collection_date"] >= pd.to_datetime(date_range[0])) &
                                                                                                                                                                                                                                            (filtered_df["collection_date"] <= pd.to_datetime(date_range[1]))
                                                                                                                                                                                                                                            ]

                                                                                                                                                                                                                                            # -----------------------------
                                                                                                                                                                                                                                            # 5. DASHBOARD LAYOUT
                                                                                                                                                                                                                                            # -----------------------------
                                                                                                                                                                                                                                            st.title("🌊 Marine Data Explorer")
                                                                                                                                                                                                                                            st.markdown("Explore marine biodiversity, fisheries, and oceanographic data interactively.")

                                                                                                                                                                                                                                            col1, col2 = st.columns([2, 1])

                                                                                                                                                                                                                                            # Map
                                                                                                                                                                                                                                            with col1:
                                                                                                                                                                                                                                                st.subheader("📍 Species Occurrences Map")
                                                                                                                                                                                                                                                    fig_map = px.scatter_mapbox(
                                                                                                                                                                                                                                                            filtered_df,
                                                                                                                                                                                                                                                                    lat="latitude",
                                                                                                                                                                                                                                                                            lon="longitude",
                                                                                                                                                                                                                                                                                    color="species",
                                                                                                                                                                                                                                                                                            size="abundance",
                                                                                                                                                                                                                                                                                                    hover_name="species",
                                                                                                                                                                                                                                                                                                            hover_data={"temperature": True},
                                                                                                                                                                                                                                                                                                                    zoom=6,
                                                                                                                                                                                                                                                                                                                            height=500
                                                                                                                                                                                                                                                                                                                                )
                                                                                                                                                                                                                                                                                                                                    fig_map.update_layout(mapbox_style="open-street-map")
                                                                                                                                                                                                                                                                                                                                        st.plotly_chart(fig_map, use_container_width=True)

                                                                                                                                                                                                                                                                                                                                        # Stats
                                                                                                                                                                                                                                                                                                                                        with col2:
                                                                                                                                                                                                                                                                                                                                            st.subheader("📊 Summary Stats")
                                                                                                                                                                                                                                                                                                                                                st.metric("Records", len(filtered_df))
                                                                                                                                                                                                                                                                                                                                                    st.metric("Avg Abundance", f"{filtered_df['abundance'].mean():.1f}")
                                                                                                                                                                                                                                                                                                                                                        st.metric("Avg Temp (°C)", f"{filtered_df['temperature'].mean():.1f}")

                                                                                                                                                                                                                                                                                                                                                        # Time series
                                                                                                                                                                                                                                                                                                                                                        st.subheader("📈 Abundance Over Time")
                                                                                                                                                                                                                                                                                                                                                        fig_time = px.line(
                                                                                                                                                                                                                                                                                                                                                            filtered_df.groupby("collection_date")["abundance"].mean().reset_index(),
                                                                                                                                                                                                                                                                                                                                                                x="collection_date",
                                                                                                                                                                                                                                                                                                                                                                    y="abundance",
                                                                                                                                                                                                                                                                                                                                                                        title="Mean Abundance Over Time"
                                                                                                                                                                                                                                                                                                                                                                        )
                                                                                                                                                                                                                                                                                                                                                                        st.plotly_chart(fig_time, use_container_width=True)

                                                                                                                                                                                                                                                                                                                                                                        # Correlation
                                                                                                                                                                                                                                                                                                                                                                        st.subheader("🌡️ Abundance vs Temperature")
                                                                                                                                                                                                                                                                                                                                                                        fig_corr = px.scatter(
                                                                                                                                                                                                                                                                                                                                                                            filtered_df,
                                                                                                                                                                                                                                                                                                                                                                                x="temperature",
                                                                                                                                                                                                                                                                                                                                                                                