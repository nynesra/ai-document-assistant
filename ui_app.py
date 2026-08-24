import streamlit as st

from src.controlled_flow import (
    run_controlled_flow,
)

from src.retriever import (
    build_tfidf_index,
)

from src.trace_logger import read_traces

# ==========================================
# SAYFA AYARLARI
# ==========================================

st.set_page_config(
    page_title="AI Doküman Asistanı",
    page_icon="📄",
    layout="centered",
)


# ==========================================
# TF-IDF INDEX
# ==========================================

@st.cache_resource
def load_tfidf_index():
    """
    TF-IDF indeksini yalnızca bir kez
    oluşturur ve Streamlit cache içinde tutar.
    """

    return build_tfidf_index()


(
    chunks,
    vectorizer,
    tfidf_matrix,
) = load_tfidf_index()


# ==========================================
# BAŞLIK
# ==========================================

st.title(
    "📄 AI Doküman Asistanı"
)

st.write(
    """
    Teknik dokümanlar hakkında soru sorabilir
    veya basit matematiksel işlemler yapabilirsiniz.
    """
)

st.divider()


# ==========================================
# KULLANICI SORGUSU
# ==========================================

query = st.text_area(
    "Sorunuzu yazın:",
    placeholder=(
        "Örnek: Python nasıl kurulur?"
    ),
    height=100,
)


submit_button = st.button(
    "Gönder",
    type="primary",
    use_container_width=True,
)


# ==========================================
# SORGU ÇALIŞTIRMA
# ==========================================

if submit_button:

    response = run_controlled_flow(
        query=query,
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    route = response[
        "route"
    ]

    selected_tool = response[
        "selected_tool"
    ]

    status = response[
        "status"
    ]

    message = response[
        "message"
    ]

    st.divider()

    st.subheader(
        "Sonuç"
    )

    # ======================================
    # CALCULATOR
    # ======================================

    if (
        route == "calculator"
        and status == "success"
    ):

        st.success(
            "Hesaplama başarıyla tamamlandı."
        )

        st.metric(
            label="Hesaplama Sonucu",
            value=response["result"],
        )

    # ======================================
    # RETRIEVAL
    # ======================================

    elif (
        route == "retrieval"
        and status == "success"
    ):

        st.success(
            "İlgili doküman parçaları bulundu."
        )

        results = response[
            "results"
        ]

        for index, result in enumerate(
            results,
            start=1,
        ):

            st.markdown(
                f"### Kaynak {index}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Dosya:**",
                    result["source"],
                )

                st.write(
                    "**Bölüm:**",
                    result["section"],
                )

            with col2:

                st.write(
                    "**Chunk ID:**",
                    result["chunk_id"],
                )

                st.write(
                    "**Similarity Score:**",
                    f"{result['score']:.4f}",
                )

            st.write(
                "**İçerik:**"
            )

            st.info(
                result["text"]
            )

    # ======================================
    # INSUFFICIENT SOURCE
    # ======================================

    elif (
        route == "retrieval"
        and status
        == "insufficient_source"
    ):

        st.warning(
            "Dokümanlarda bu soruyu "
            "yanıtlamak için yeterli "
            "kaynak bulunamadı."
        )

    # ======================================
    # OUT OF SCOPE
    # ======================================

    elif route == "out_of_scope":

        st.warning(
            "Bu soru mevcut teknik doküman "
            "bilgi tabanının kapsamı dışındadır."
        )

    # ======================================
    # INVALID
    # ======================================

    elif route == "invalid":

        st.warning(
            "Geçerli bir soru giriniz."
        )

    # ======================================
    # GUARDRAIL BLOCKED
    # ======================================

    elif status == "guardrail_blocked":

        st.error(
            "Bu sorgu güvenlik kontrolü "
            "tarafından engellendi."
        )

        st.write(
            "**Neden:**",
            response[
                "trace"
            ][
                "guardrail_reason"
            ],
        )

    # ======================================
    # DİĞER HATALAR
    # ======================================

    else:

        st.error(
            message
        )

    # ======================================
    # KARAR BİLGİLERİ
    # ======================================

    st.divider()

    with st.expander(
        "🔍 Karar ve Trace Bilgileri"
    ):

        trace = response[
            "trace"
        ]

        st.write(
            "**Route:**",
            route,
        )

        st.write(
            "**Selected Tool:**",
            selected_tool,
        )

        st.write(
            "**Status:**",
            status,
        )

        st.write(
            "**Guardrail Allowed:**",
            trace.get(
                "guardrail_allowed"
            ),
        )

        st.write(
            "**Guardrail Reason:**",
            trace.get(
                "guardrail_reason"
            ),
        )

        st.write(
            "**Top Source:**",
            trace.get(
                "top_source"
            ),
        )

        top_score = trace.get(
            "top_score"
        )

        if top_score is not None:

            st.write(
                "**Top Score:**",
                f"{top_score:.4f}",
            )

        else:

            st.write(
                "**Top Score:**",
                None,
            )

        st.write(
            "**Result Count:**",
            trace.get(
                "result_count"
            ),
        )

        st.write(
            "**Timestamp:**",
            trace.get(
                "timestamp"
            ),
        )

    # ==========================================
# SON KARAR LOGLARI
# ==========================================

st.divider()

with st.expander(
    "🧾 Son Karar Logları"
):

    traces = read_traces()

    if not traces:

        st.info(
            "Henüz kayıtlı decision trace bulunmuyor."
        )

    else:

        recent_traces = traces[-5:]

        st.write(
            f"Toplam log kaydı: {len(traces)}"
        )

        st.write(
            "Son 5 karar kaydı:"
        )

        for index, trace in enumerate(
            reversed(recent_traces),
            start=1,
        ):

            st.markdown(
                f"### Log {index}"
            )

            st.write(
                "**Timestamp:**",
                trace.get("timestamp"),
            )

            st.write(
                "**Query:**",
                repr(
                    trace.get(
                        "query"
                    )
                ),
            )

            st.write(
                "**Route:**",
                trace.get("route"),
            )

            st.write(
                "**Selected Tool:**",
                trace.get(
                    "selected_tool"
                ),
            )

            st.write(
                "**Tool Status:**",
                trace.get(
                    "tool_status"
                ),
            )

            st.write(
                "**Guardrail Allowed:**",
                trace.get(
                    "guardrail_allowed"
                ),
            )

            st.write(
                "**Guardrail Reason:**",
                trace.get(
                    "guardrail_reason"
                ),
            )

            st.write(
                "**Top Source:**",
                trace.get(
                    "top_source"
                ),
            )

            top_score = trace.get(
                "top_score"
            )

            if top_score is not None:

                st.write(
                    "**Top Score:**",
                    f"{top_score:.4f}",
                )

            else:

                st.write(
                    "**Top Score:**",
                    None,
                )

            st.divider()