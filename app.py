from services.pipeline import Pipeline
from services.plot import Plot
import streamlit as st
import json

st.set_page_config(page_title="Case 2 - Macro Scenario Engine", layout="wide")

BASELINE_METRICS = {
    "selic": 13.25,
    "inflacao": 5.09,
    "dolar": 5.16,
    "pib": 1.90,
}

def renderizar_resultados(result: dict) -> None:
    final_json = result["final_json"]
    markdown = result["markdown"]
    all_stocks_sorted = result["all_stocks_sorted"]
    sorted_sectors = result["sorted_sectors"]
    affected_metrics = result["affected_metrics"]
    baseline_metrics = BASELINE_METRICS
    periods = result["periods"]

    plotter = Plot()
    plot_paths = plotter.plot_stock_extremes(all_stocks_sorted)
    sector_plot_paths = plotter.plot_sector_extremes(sorted_sectors)

    st.subheader("Cenário macro atual")
    scenario_table = []
    for key in ["selic", "inflacao", "dolar", "pib"]:
        unidade = "%" if key != "dolar" else "R$/US$"
        if key == "dolar":
            projected_value = round(
                baseline_metrics.get(key, 0) * (1 + float(affected_metrics.get(key, 0)) / 100),
                2,
            )
        else:
            projected_value = round(
                baseline_metrics.get(key, 0) + float(affected_metrics.get(key, 0)),
                2,
            )
        diff_unit = "%" if key == "dolar" else "p.p."
        scenario_table.append(
            {
                "Variavel": key,
                "Unidade": unidade,
                "Projeção Focus": baseline_metrics.get(key),
                "Cenário do usuário": projected_value,
                "Diferenca": affected_metrics.get(key),
                "Unid. Dif.": diff_unit,
            }
        )
    st.table(scenario_table)

    st.subheader("Períodos com variações mais próximas ao cenário projetado")
    period_table = [{"Periodo": period} for period in periods]
    st.table(period_table)

    st.subheader("Gráficos salvos em data/plots")
    col_top, col_bottom = st.columns(2)
    with col_top:
        st.image(
            plot_paths["top_path"],
            caption="3 melhores acoes (retorno medio nos periodos selecionados)",
            use_container_width=True,
        )
    with col_bottom:
        st.image(
            plot_paths["bottom_path"],
            caption="3 piores acoes (retorno medio nos periodos selecionados)",
            use_container_width=True,
        )

    col_sector_top, col_sector_bottom = st.columns(2)
    with col_sector_top:
        st.image(
            sector_plot_paths["top_path"],
            caption="3 melhores setores (retorno normalizado %)",
            use_container_width=True,
        )
    with col_sector_bottom:
        st.image(
            sector_plot_paths["bottom_path"],
            caption="3 piores setores (retorno normalizado %)",
            use_container_width=True,
        )

    st.subheader("Relatório em markdown")
    st.markdown(markdown)

    st.subheader("JSON final")
    st.json(final_json)

    st.download_button(
        "Baixar relatório em markdown",
        data=markdown,
        file_name="report.md",
        mime="text/markdown",
    )

    st.download_button(
        "Baixar JSON final",
        data=json.dumps(final_json, ensure_ascii=False, indent=4),
        file_name="results.json",
        mime="application/json",
    )


if "resultado_pipeline" not in st.session_state:
    st.session_state["resultado_pipeline"] = None


st.title("Case 2 - Macro Scenario Engine")
st.caption("Digite um cenário macroeconômico, execute a análise e veja o relatório com os gráficos gerados.")

with st.form("formulario_cenario"):
    user_scenery = st.text_area(
        "Cenário macroeconômico",
        placeholder="Exemplo: Selic cai, inflação desacelera, dólar enfraquece e PIB acelera.",
        height=150,
    )
    submitted = st.form_submit_button("Analisar cenário")


if submitted:
    if not user_scenery.strip():
        st.warning("Digite um cenário antes de analisar.")
    else:
        with st.spinner("Processando o cenário completo..."):
            try:
                resultado = Pipeline(user_scenery=user_scenery).execute()
            except Exception as exc:
                st.session_state["resultado_pipeline"] = None
                st.error(f"Falha ao processar a análise: {exc}")
            else:
                st.session_state["resultado_pipeline"] = resultado


if st.session_state["resultado_pipeline"] is not None:
    renderizar_resultados(st.session_state["resultado_pipeline"])