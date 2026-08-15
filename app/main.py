from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from app.db.queries import (
    get_all_packages,
    get_node_counts,
    get_relationship_count,
    get_repository_impacts
)

st.set_page_config(
    page_title="Dependency Impact Explorer",
    layout="wide",
)

# Sidebar
st.sidebar.title("Graph Information")
st.sidebar.write("### Nodes")

counts = get_node_counts()
for label, count in counts.items():
    st.sidebar.markdown(f"- {label}: {count}")

st.sidebar.markdown(f"### Relationships: {get_relationship_count()}")

# Main Page
st.title("🔍 Dependency Impact Explorer")
st.info(
    """
    This application explores package dependencies using a graph database.

    Select a package to identify affected repositories and visualize
    the dependency chain between repositories and packages.
    """
)

packages = get_all_packages()
selected_package = st.selectbox("📦 Select a package",packages,)

if st.button("Analyze"):
    try:
        with st.spinner("Analyzing..."):
            impacts = get_repository_impacts(selected_package)

        st.markdown(f"### Affected repositories: {len(impacts)}")

        if not impacts:
            st.info("""
                No repositories depend on this package.
                Try selecting a different package.
                """
            )
        else:
            for index, impact in enumerate(impacts, start=1):
                st.markdown(f"**{index}. {impact['repository']}**")
                developers = ", ".join(impact["developers"])

                st.caption(f"Maintained by: {developers}")
                st.code(" → ".join(impact["path"]))
                
    except Exception as e:
        st.error("""
            Unable to analyze the dependency graph.

            Please verify that:
            • The database is running.
            • The `.env` configuration is correct.
            • The network connection is available.
            """
        )
