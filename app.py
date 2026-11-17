"""FindIt — AI-assisted lost & found administration console.

Run with:  streamlit run app.py
Expects CSV files in ./outputs (matches, no_match, unclaimed, lost, found)
and optionally ./data (lost.csv, found.csv) as fallback sources.
"""

from datetime import datetime
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
APP_NAME = "FindIt"
BASE = Path(__file__).parent
OUT = BASE / "outputs"
DATA = BASE / "data"
OUT.mkdir(exist_ok=True)

PENDING, APPROVED, REJECTED = "Pending", "Approved", "Rejected"
DECISIONS = [PENDING, APPROVED, REJECTED]

# Palette: ink navy, warm paper, teal for action, muted status colours.
INK = "#14213D"
PAPER = "#F7F5F0"
SURFACE = "#FFFFFF"
LINE = "#E4E0D6"
MUTED = "#6B6F7B"
TEAL = "#0F766E"
AMBER = "#B45309"
GREEN = "#2F6B4F"
RED = "#A23B3B"

st.set_page_config(
    page_title=f"{APP_NAME} · Lost & Found",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
}}
.stApp {{ background: {PAPER}; color: {INK}; }}
.block-container {{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1240px; }}
#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stHeader"] {{ background: transparent; }}

h1, h2, h3 {{
    font-family: 'Newsreader', Georgia, serif !important;
    color: {INK} !important;
    letter-spacing: -0.01em;
}}
h1 {{ font-weight: 600; font-size: 2.3rem !important; }}
h2 {{ font-weight: 600; font-size: 1.6rem !important; }}
h3 {{ font-weight: 600; font-size: 1.2rem !important; }}

/* Sidebar */
[data-testid="stSidebar"] {{ background: {INK}; border-right: none; }}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stCaption {{ color: #E7EBF3 !important; }}
[data-testid="stSidebar"] .stCaption p {{ color: #9AA6BF !important; }}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.12); }}
.brand-name {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 1.8rem; font-weight: 600; color: #FFFFFF !important; margin: 0;
}}
.brand-tag {{ font-size: .85rem; color: #9AA6BF !important; margin-top: .15rem; }}

/* Hero */
.fi-hero {{
    background: {INK};
    color: {PAPER};
    border-radius: 14px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 1.6rem;
}}
.fi-hero h1 {{ color: {PAPER} !important; margin: 0 0 .5rem 0; }}
.fi-hero p {{ color: #C9D2E3; margin: 0; max-width: 620px; line-height: 1.6; }}

/* Metrics */
.fi-metric {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-left: 3px solid var(--accent, {TEAL});
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    height: 100%;
}}
.fi-metric-label {{ font-size: .8rem; color: {MUTED}; font-weight: 500; }}
.fi-metric-value {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 2.1rem; font-weight: 600; color: {INK}; line-height: 1.15; margin: .2rem 0;
}}
.fi-metric-note {{ font-size: .8rem; color: {MUTED}; }}

/* Panels */
.fi-panel {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-radius: 12px;
    padding: 1.25rem 1.35rem;
}}

/* Status badges */
.fi-badge {{
    display: inline-block; font-size: .75rem; font-weight: 600;
    padding: .2rem .6rem; border-radius: 999px; border: 1px solid;
}}
.fi-badge-pending  {{ color: {AMBER}; background: #FDF6EC; border-color: #F1D9B5; }}
.fi-badge-approved {{ color: {GREEN}; background: #EEF6F1; border-color: #C5E0CF; }}
.fi-badge-rejected {{ color: {RED};   background: #FBEFEF; border-color: #EBC7C7; }}

/* Empty state */
.fi-empty {{
    background: {SURFACE}; border: 1px dashed #CFC9BA; border-radius: 12px;
    padding: 2rem; text-align: left;
}}
.fi-empty strong {{ font-family: 'Newsreader', Georgia, serif; font-size: 1.15rem; }}
.fi-empty p {{ color: {MUTED}; margin: .35rem 0 0 0; }}

/* Buttons and widgets */
div.stButton > button {{
    border-radius: 8px; font-weight: 500; padding: .45rem 1rem;
    border: 1px solid {LINE};
}}
div.stButton > button[kind="primary"] {{
    background: {TEAL}; border-color: {TEAL}; color: #FFFFFF;
}}
div.stButton > button:focus-visible, .stTextInput input:focus-visible {{
    outline: 2px solid {TEAL}; outline-offset: 2px;
}}
[data-testid="stDataFrame"] {{ border-radius: 10px; overflow: hidden; border: 1px solid {LINE}; }}
[data-testid="stExpander"] {{
    background: {SURFACE}; border: 1px solid {LINE}; border-radius: 12px; margin-bottom: .6rem;
}}
.fi-footer {{ color: {MUTED}; font-size: .8rem; margin-top: 2.5rem; }}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Data access
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _read_csv(path_str: str, mtime: float) -> pd.DataFrame:
    """Cached on (path, mtime) so edits to the files are picked up automatically."""
    try:
        df = pd.read_csv(path_str)
    except Exception:
        return pd.DataFrame()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(str(path), path.stat().st_mtime)


def load_records() -> dict:
    lost = load_csv(OUT / "lost.csv")
    if lost.empty:
        lost = load_csv(DATA / "lost.csv")

    found = load_csv(OUT / "found.csv")
    if found.empty:
        found = load_csv(DATA / "found.csv")
    matches = load_csv(OUT / "matches.csv")
    if "score" in matches.columns:
        matches = matches.copy()
        matches["score"] = pd.to_numeric(matches["score"], errors="coerce")
    return {
        "lost": lost,
        "found": found,
        "matches": matches,
        "no_match": load_csv(OUT / "no_match.csv"),
        "unclaimed": load_csv(OUT / "unclaimed.csv"),
    }


def match_key(row: pd.Series) -> str:
    return f"{row.get('lost_id', '?')}::{row.get('found_id', '?')}"


def init_decisions() -> None:
    """Restore previously saved review decisions the first time the app loads."""
    if "decisions" in st.session_state:
        return
    st.session_state.decisions = {}
    prior = load_csv(OUT / "review_decisions.csv")
    for _, row in prior.iterrows():
        decision = row.get("decision", PENDING)
        if decision in DECISIONS:
            st.session_state.decisions[match_key(row)] = decision


def decision_for(key: str) -> str:
    return st.session_state.decisions.get(key, PENDING)


def set_decision(key: str, value: str) -> None:
    st.session_state.decisions[key] = value


def save_decisions(matches: pd.DataFrame) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = [
        {
            "lost_id": row.get("lost_id"),
            "found_id": row.get("found_id"),
            "decision": decision_for(match_key(row)),
            "reviewed_at": timestamp,
        }
        for _, row in matches.iterrows()
    ]
    pd.DataFrame(rows).to_csv(OUT / "review_decisions.csv", index=False)
    st.toast("Review decisions saved.", icon="✅")


# ----------------------------------------------------------------------------
# UI helpers
# ----------------------------------------------------------------------------
def metric_card(label: str, value, note: str, accent: str = TEAL) -> None:
    st.markdown(
        f'<div class="fi-metric" style="--accent:{accent}">'
        f'<div class="fi-metric-label">{label}</div>'
        f'<div class="fi-metric-value">{value}</div>'
        f'<div class="fi-metric-note">{note}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def badge(decision: str) -> str:
    css = decision.lower()
    return f'<span class="fi-badge fi-badge-{css}">{decision}</span>'


def empty_state(title: str, body: str) -> None:
    st.markdown(
        f'<div class="fi-empty"><strong>{title}</strong><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


def filter_frame(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if df.empty or not query.strip():
        return df
    needle = query.strip().lower()
    mask = (
        df.astype(str)
        .apply(lambda col: col.str.lower().str.contains(needle, regex=False, na=False))
        .any(axis=1)
    )
    return df[mask]


def show_table(df: pd.DataFrame, empty_title: str = "Nothing to show yet",
               empty_body: str = "Records will appear here once the data files are added.") -> None:
    if df.empty:
        empty_state(empty_title, empty_body)
        return
    st.dataframe(df, use_container_width=True, hide_index=True)


def download_button(df: pd.DataFrame, label: str, file_name: str) -> None:
    if not df.empty:
        st.download_button(
            label,
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=file_name,
            mime="text/csv",
        )


def score_histogram(scores: pd.Series) -> None:
    scores = scores.dropna()
    if scores.empty:
        empty_state("No scores yet", "Match scores will be plotted once they are available.")
        return
    chart = (
        alt.Chart(pd.DataFrame({"score": scores}))
        .mark_bar(color=TEAL, cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("score:Q", bin=alt.Bin(maxbins=12), title="Match score"),
            y=alt.Y("count()", title="Matches"),
            tooltip=[alt.Tooltip("count()", title="Matches")],
        )
        .properties(height=280)
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor=MUTED, titleColor=MUTED, gridColor=LINE, domainColor=LINE)
    )
    st.altair_chart(chart, use_container_width=True)


# ----------------------------------------------------------------------------
# Load state
# ----------------------------------------------------------------------------
data = load_records()
lost, found = data["lost"], data["found"]
matches, no_match, unclaimed = data["matches"], data["no_match"], data["unclaimed"]
init_decisions()

total_lost = len(lost) if not lost.empty else len(no_match)
total_found = len(found) if not found.empty else len(unclaimed)
total_matches = len(matches)

decision_counts = {d: 0 for d in DECISIONS}
for _, row in matches.iterrows():
    decision_counts[decision_for(match_key(row))] += 1

reviewed = total_matches - decision_counts[PENDING]
decided = decision_counts[APPROVED] + decision_counts[REJECTED]
approval_rate = (decision_counts[APPROVED] / decided * 100) if decided else 0.0
has_data = any(not frame.empty for frame in (lost, found, matches))

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
PAGES = ["Overview", "Lost items", "Found items", "AI matches", "Admin review", "Analytics"]

with st.sidebar:
    st.markdown(f'<p class="brand-name">🔎 {APP_NAME}</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-tag">Lost & found, reconciled by AI</p>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.divider()
    if has_data:
        st.success("Data loaded")
    else:
        st.warning("No data files found")
    st.caption(f"Version 1.1 · {datetime.now():%d %b %Y}")

# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def render_overview() -> None:
    st.markdown(
        '<div class="fi-hero">'
        "<h1>Every lost item deserves a way home.</h1>"
        "<p>Review AI-suggested matches, verify ownership claims, and track "
        "what has been returned to its owner.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Lost reports", total_lost, "Items reported missing")
    with c2:
        metric_card("Found reports", total_found, "Items handed in", accent=INK)
    with c3:
        metric_card("AI matches", total_matches, "Suggested pairings", accent=TEAL)
    with c4:
        metric_card("Awaiting review", decision_counts[PENDING], "Need an admin decision", accent=AMBER)

    st.write("")
    left, right = st.columns([1.6, 1], gap="large")

    with left:
        st.subheader("Recent AI matches")
        show_table(matches.head(8), "No matches yet",
                   "Run the matching pipeline to generate suggested pairings.")

    with right:
        st.subheader("Review progress")
        st.markdown('<div class="fi-panel">', unsafe_allow_html=True)
        progress = reviewed / total_matches if total_matches else 0.0
        st.write(f"**{reviewed} of {total_matches}** matches reviewed")
        st.progress(progress)
        st.write("")
        st.write(f"Approved: **{decision_counts[APPROVED]}**")
        st.write(f"Rejected: **{decision_counts[REJECTED]}**")
        st.write(f"Lost items without a match: **{len(no_match)}**")
        st.write(f"Unclaimed found items: **{len(unclaimed)}**")
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("AI matches are suggestions. Every ownership claim requires human verification.")


def render_item_list(title: str, subtitle: str, df: pd.DataFrame, key: str, file_name: str) -> None:
    st.title(title)
    st.caption(subtitle)

    col_search, col_export = st.columns([3, 1], vertical_alignment="bottom")
    with col_search:
        query = st.text_input("Search", placeholder="Search by any field, such as an ID, colour or location",
                              key=f"search_{key}", label_visibility="collapsed")
    filtered = filter_frame(df, query)
    with col_export:
        download_button(filtered, "Export CSV", file_name)

    st.caption(f"Showing {len(filtered):,} of {len(df):,} records")
    show_table(filtered, "No records", "Add a CSV file to outputs/ or data/ to populate this view.")


def render_ai_matches() -> None:
    st.title("AI matches")
    st.caption("Potential pairings between lost and found reports, ranked by the matching model.")

    if matches.empty:
        empty_state("No AI matches available", "Run the matching pipeline to generate suggestions.")
        return

    col_status, col_score, col_search = st.columns([1, 1, 2], vertical_alignment="bottom")
    with col_status:
        if "status" in matches.columns:
            options = ["All"] + sorted(matches["status"].dropna().astype(str).unique().tolist())
        else:
            options = ["All"]
        status = st.selectbox("Status", options)
    with col_score:
        if "score" in matches.columns and matches["score"].notna().any():
            lo, hi = float(matches["score"].min()), float(matches["score"].max())
            threshold = st.slider("Minimum score", lo, hi, lo) if lo < hi else lo
        else:
            threshold = None
    with col_search:
        query = st.text_input("Search matches", placeholder="Search matches",
                              key="search_matches", label_visibility="collapsed")

    view = matches
    if status != "All" and "status" in view.columns:
        view = view[view["status"].astype(str) == status]
    if threshold is not None:
        view = view[view["score"] >= threshold]
    view = filter_frame(view, query)

    st.caption(f"Showing {len(view):,} of {total_matches:,} matches")
    show_table(view, "No matches fit these filters", "Try widening the score range or clearing the search.")
    download_button(view, "Export matches", "matches_filtered.csv")

    if "score" in matches.columns:
        st.subheader("Score distribution")
        score_histogram(matches["score"])


def render_admin_review() -> None:
    st.title("Admin review")
    st.caption("Verify each AI suggestion against the physical item and the claimant before approving.")

    if matches.empty:
        empty_state("No matches to review", "Matches appear here once the pipeline has run.")
        return

    summary_cols = st.columns(4)
    with summary_cols[0]:
        metric_card("Pending", decision_counts[PENDING], "To review", accent=AMBER)
    with summary_cols[1]:
        metric_card("Approved", decision_counts[APPROVED], "Ownership confirmed", accent=GREEN)
    with summary_cols[2]:
        metric_card("Rejected", decision_counts[REJECTED], "Not a match", accent=RED)
    with summary_cols[3]:
        metric_card("Approval rate", f"{approval_rate:.0f}%", "Of decided matches", accent=INK)

    st.write("")
    view = st.radio("Show", ["All"] + DECISIONS, horizontal=True, key="admin_filter")

    shown = 0
    for _, row in matches.iterrows():
        key = match_key(row)
        decision = decision_for(key)
        if view != "All" and decision != view:
            continue
        shown += 1

        title = (
            f"Lost #{row.get('lost_id', '—')}  ↔  Found #{row.get('found_id', '—')}"
            f"   ·   Score {row.get('score', '—')}   ·   {decision}"
        )
        with st.expander(title):
            details = row.astype(str).to_frame("Value")
            st.dataframe(details, use_container_width=True)

            b1, b2, b3, _ = st.columns([1, 1, 1, 3])
            with b1:
                st.button(
                    "Approve claim", key=f"approve_{key}", type="primary",
                    disabled=decision == APPROVED,
                    on_click=set_decision, args=(key, APPROVED),
                    use_container_width=True,
                )
            with b2:
                st.button(
                    "Reject claim", key=f"reject_{key}",
                    disabled=decision == REJECTED,
                    on_click=set_decision, args=(key, REJECTED),
                    use_container_width=True,
                )
            with b3:
                st.button(
                    "Reset to pending", key=f"reset_{key}",
                    disabled=decision == PENDING,
                    on_click=set_decision, args=(key, PENDING),
                    use_container_width=True,
                )
            st.markdown(f"Current decision: {badge(decision)}", unsafe_allow_html=True)

    if shown == 0:
        empty_state("Nothing in this view", "Change the filter above to see other matches.")

    st.divider()
    save_col, note_col = st.columns([1, 3], vertical_alignment="center")
    with save_col:
        st.button("Save decisions", type="primary", on_click=save_decisions, args=(matches,))
    with note_col:
        st.caption("Decisions are written to outputs/review_decisions.csv and restored on next launch.")


def render_analytics() -> None:
    st.title("Analytics")
    st.caption("How the recovery system is performing.")

    a, b, c, d = st.columns(4)
    with a:
        metric_card("Total matches", total_matches, "AI suggestions", accent=TEAL)
    with b:
        metric_card("Approval rate", f"{approval_rate:.0f}%", "Of decided matches", accent=GREEN)
    with c:
        metric_card("Unmatched lost", len(no_match), "Lost reports, no match", accent=AMBER)
    with d:
        metric_card("Unclaimed found", len(unclaimed), "Found items, no owner", accent=RED)

    st.write("")
    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Match score distribution")
        if "score" in matches.columns:
            score_histogram(matches["score"])
        else:
            empty_state("No scores available", "The matches file needs a score column.")
    with right:
        st.subheader("Decision breakdown")
        if total_matches:
            breakdown = pd.DataFrame(
                {"decision": DECISIONS, "count": [decision_counts[d] for d in DECISIONS]}
            )
            pie = (
                alt.Chart(breakdown)
                .mark_arc(innerRadius=60)
                .encode(
                    theta="count:Q",
                    color=alt.Color(
                        "decision:N",
                        scale=alt.Scale(domain=DECISIONS, range=[AMBER, GREEN, RED]),
                        legend=alt.Legend(orient="bottom", title=None),
                    ),
                    tooltip=["decision", "count"],
                )
                .properties(height=280)
                .configure_view(strokeWidth=0)
            )
            st.altair_chart(pie, use_container_width=True)
        else:
            empty_state("No decisions yet", "Decisions will be summarised here once reviews begin.")

    st.subheader("Lost items without matches")
    show_table(no_match, "No unmatched lost items", "Every lost report has a suggested match.")

    st.subheader("Unclaimed found items")
    show_table(unclaimed, "No unclaimed items", "All found items have an owner.")


ROUTES = {
    "Overview": render_overview,
    "Lost items": lambda: render_item_list(
        "Lost items", "Every reported missing item, searchable and exportable.",
        lost, "lost", "lost_items.csv"),
    "Found items": lambda: render_item_list(
        "Found items", "Every item handed in, searchable and exportable.",
        found, "found", "found_items.csv"),
    "AI matches": render_ai_matches,
    "Admin review": render_admin_review,
    "Analytics": render_analytics,
}

ROUTES[page]()

st.markdown(
    f'<div class="fi-footer">{APP_NAME} · Intelligent lost & found management</div>',
    unsafe_allow_html=True,
)