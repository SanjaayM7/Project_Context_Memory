import streamlit as st
from memory_store import MemoryStore, VALID_TYPES

st.set_page_config(page_title="Project Context Memory", page_icon="🧠", layout="wide")
store = MemoryStore("data/memory.db")
st.title("🧠 Project Context Memory")
st.caption("A local-first memory layer for research and coding agents.")

with st.sidebar:
    st.header("Project")
    project = st.text_input("Project key", "research-rag").strip() or "research-rag"
    st.metric("Saved memories", store.count(project))
    st.caption("Types: decisions, datasets, experiments, questions, notes")

add_tab, search_tab, browse_tab, export_tab = st.tabs(
    ["Add memory", "Search & agent context", "Browse memories", "Export Markdown"])

with add_tab:
    with st.form("add_memory", clear_on_submit=True):
        kind = st.selectbox("Memory type", sorted(VALID_TYPES))
        title = st.text_input("Title", placeholder="e.g. Use hybrid retrieval")
        content = st.text_area("Details", height=130, placeholder="Decision, rationale, dataset path, metrics, or open question")
        tags = st.text_input("Tags (comma-separated)")
        source = st.text_input("Source / reference (optional)")
        if st.form_submit_button("Save memory", type="primary"):
            try:
                mid = store.add(project, kind, title, content, tags, source)
                st.success(f"Saved memory #{mid}")
            except ValueError as e:
                st.error(str(e))

with search_tab:
    query = st.text_input("What should the agent remember?", placeholder="Which chunk size did we decide to test?")
    limit = st.slider("Maximum results", 1, 15, 6)
    if st.button("Search memories"):
        hits = store.search(query, project=project, limit=limit)
        if not hits:
            st.info("No matching memories. Save the answer once it is known.")
        for x in hits:
            with st.expander(f"#{x['id']} · {x['kind']} · {x['title']} · score {x['score']}"):
                st.write(x["content"])
                st.caption(f"Tags: {x['tags'] or 'none'} | Source: {x['source'] or 'not specified'}")
        context = store.build_context(project, query, limit)
        st.markdown("#### Context pack to inject into an LLM prompt")
        st.code(context, language="markdown")
        st.download_button("Download context pack", context, "retrieved_project_context.md")

with browse_tab:
    kind_filter = st.selectbox("Type", ["all"] + sorted(VALID_TYPES))
    status_filter = st.selectbox("Status", ["all", "active", "resolved", "superseded", "archived"])
    records = store.list(project, None if kind_filter == "all" else kind_filter,
                         None if status_filter == "all" else status_filter, 500)
    if not records:
        st.info("No memories match these filters.")
    for x in records:
        with st.expander(f"#{x['id']} · {x['kind']} · {x['title']}"):
            st.write(x["content"])
            st.caption(f"Tags: {x['tags'] or 'none'} | Source: {x['source'] or 'not specified'}")
            status = st.selectbox("Status", ["active", "resolved", "superseded", "archived"],
                                  index=(["active", "resolved", "superseded", "archived"].index(x["status"])
                                         if x["status"] in ["active", "resolved", "superseded", "archived"] else 0),
                                  key=f"status_{x['id']}")
            c1, c2 = st.columns(2)
            if c1.button("Update status", key=f"update_{x['id']}"):
                store.update_status(x["id"], status)
                st.rerun()
            confirm = c2.checkbox("Confirm delete", key=f"confirm_{x['id']}")
            if c2.button("Delete", key=f"delete_{x['id']}", disabled=not confirm):
                store.delete(x["id"])
                st.rerun()

with export_tab:
    output_name = st.text_input("Filename", "PROJECT_MEMORY.md")
    preview = store.export_markdown(project)
    st.caption("Review exported content before committing it to a public repository.")
    st.download_button("Download memory file", preview, output_name, mime="text/markdown")
    st.code(preview, language="markdown")
