# Our Chengdu Story

Modular Streamlit repository generated from the uploaded single-file source.
The Landing page and Home swipe stack are frozen and retain their original
markup, CSS, JavaScript, artwork, and interactions. The former Explore module
has been removed. Its lightweight nearby shortcuts now live in Food and open
AMap directly without loading an in-app map. Expenses is preserved.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Push this directory to GitHub and select `app.py` as the entry point. If family
expense syncing is needed, configure the optional Supabase values shown in
`.streamlit/secrets.toml.example` using Streamlit's Secrets settings. Without
them, Expenses continues in browser-local mode, matching the original app.

## Module boundaries

- `app.py`: Streamlit entry point only
- `landing.py`: frozen Landing CSS, markup, and behavior
- `home.py`: frozen Home and swipe-stack data, CSS, and behavior
- `food.py`: Food data, nearby utilities, and direct AMap links
- `expenses.py`: Expenses and split-ledger behavior
- `shared.py`: common data, location engine, navigation, payload, and assembly
- `assets/`: original embedded media decoded without recompression
