import base64
from pathlib import Path

import streamlit as st

from recommender import recommend_restaurants


st.set_page_config(
    page_title="TableTwo",
    page_icon="🍽️",
    layout="centered"
)


def get_base64_image(image_path):
    image_file = Path(image_path)
    return base64.b64encode(image_file.read_bytes()).decode()


bg_image = get_base64_image("tabletwo-bg.png")


st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap');

    .stApp {{
        background:
            linear-gradient(
                rgba(5, 8, 20, 0.55),
                rgba(5, 8, 20, 0.55)
            ),
            url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    html, body, [class*="css"] {{
        text-transform: lowercase;
    }}

    h1, h2, h3, p, label, div {{
        color: white !important;
    }}

    .main-title {{
        text-transform: none !important;
        text-align: center;
        font-family: 'Fredoka', sans-serif !important;
        font-size: 4rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
        color: white !important;
    }}

    .subtitle {{
        text-align: center;
        font-size: 1.05rem;
        margin-bottom: 2rem;
        color: rgba(255,255,255,0.92) !important;
    }}

    .restaurant-name {{
        text-transform: none !important;
    }}

    .restaurant-name a {{
        text-transform: none !important;
        color: #70b7ff !important;
        text-decoration: none !important;
        font-family: 'Fredoka', sans-serif !important;
    }}

    .restaurant-name a:hover {{
        text-decoration: underline !important;
    }}

    input {{
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.20) !important;
        background-color: rgba(18, 20, 32, 0.78) !important;
        color: white !important;
    }}

    div[data-baseweb="select"] > div {{
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.20) !important;
        background-color: rgba(18, 20, 32, 0.78) !important;
        color: white !important;
    }}

    .stButton > button,
    .stLinkButton > a {{
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.26) !important;
        background-color: rgba(12, 16, 30, 0.88) !important;
        color: white !important;
        letter-spacing: 0.03em !important;
        text-transform: lowercase !important;
    }}

    .stButton > button:hover,
    .stLinkButton > a:hover {{
        border-color: white !important;
        background-color: rgba(28, 35, 58, 0.92) !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        background-color: rgba(10, 14, 28, 0.42) !important;
        backdrop-filter: blur(6px);
    }}

    hr {{
        border-color: rgba(255,255,255,0.16) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">TableTwo</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">find a restaurant that works for both of you.</div>',
    unsafe_allow_html=True
)


location = st.text_input(
    "where are you eating?",
    placeholder="orlando, fl"
)


st.divider()


st.subheader("person 1")

cuisine_one = st.text_input(
    "food preference",
    placeholder="italian",
    key="cuisine_one"
)

vibe_one = st.selectbox(
    "vibe",
    [
        "romantic",
        "chill",
        "lively",
        "upscale",
        "casual"
    ],
    key="vibe_one"
)


st.divider()


st.subheader("person 2")

cuisine_two = st.text_input(
    "food preference",
    placeholder="mexican",
    key="cuisine_two"
)

vibe_two = st.selectbox(
    "vibe",
    [
        "romantic",
        "chill",
        "lively",
        "upscale",
        "casual"
    ],
    key="vibe_two"
)


st.divider()


budget = st.selectbox(
    "maximum budget",
    [
        "$",
        "$$",
        "$$$"
    ]
)

budget_map = {
    "$": 1,
    "$$": 2,
    "$$$": 3
}


if st.button(
    "find our matches",
    use_container_width=True
):

    if (
        not location
        or not cuisine_one
        or not cuisine_two
    ):
        st.warning(
            "please enter a location and both food preferences."
        )

    else:
        with st.spinner(
            "finding restaurants..."
        ):

            try:
                restaurants = recommend_restaurants(
                    location.strip(),
                    cuisine_one.strip().lower(),
                    cuisine_two.strip().lower(),
                    vibe_one,
                    vibe_two,
                    budget_map[budget]
                )

            except Exception as error:
                st.error(
                    f"something went wrong: {error}"
                )
                st.stop()

        if not restaurants:
            st.warning(
                "no restaurants matched your search."
            )

        else:
            st.success(
                "we found some matches."
            )

            st.subheader(
                "your tabletwo matches"
            )

            for index, restaurant in enumerate(
                restaurants[:5],
                start=1
            ):

                score = restaurant["score"]

                if score >= 9:
                    match = "🔥 great match"
                elif score >= 6:
                    match = "✅ good match"
                else:
                    match = "👍 possible match"

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f'''
                        <h3 class="restaurant-name">
                            {index}. <a href="{restaurant["url"]}" target="_blank">
                            {restaurant["name"]}
                            </a>
                        </h3>
                        ''',
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            f"⭐ rating: {restaurant['rating']}"
                        )

                    with col2:
                        st.write(
                            f"💵 price: {restaurant['price']}"
                        )

                    st.write(
                        f"**{match}**"
                    )

                    st.link_button(
                        "view on yelp",
                        restaurant["url"],
                        use_container_width=True
                    )

                    st.write(
                        "**why it matches:**"
                    )

                    for reason in restaurant["reasons"]:
                        st.write(
                            f"• {reason.lower()}"
                        )