from services.llm_wrapper import LLM_Wrapper
from services.stock_wrapper import StockWrapper
from pathlib import Path
import json

class Pipeline:
    def __init__(self, user_scenery: str) -> None:
        self.user_scenery = user_scenery
        self.llm_wrapper = LLM_Wrapper()
        self.stock_wrapper = StockWrapper()

    @staticmethod
    def _dump_json(response: json) -> None:
        parsed_response = response
        
        path = "data/output/results.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(parsed_response, f, ensure_ascii=False, indent=4)

    @staticmethod
    def _dump_markdown(response: str) -> None:
        path = "data/output/report.md"

        with open(path, "w", encoding="utf-8") as f:
            f.write(response)

    @staticmethod
    def _group_context(best_stocks: list, worst_stocks: list, best_sectors: list, worst_sectors: list, all_stocks_sorted: list, sorted_sectors: list, periods: list, affected_metrics: dict) -> dict:
        return {
            "best_stocks": best_stocks,
            "worst_stocks": worst_stocks,
            "best_sectors": best_sectors,
            "worst_sectors": worst_sectors,
            "all_stocks_sorted": all_stocks_sorted,
            "sorted_sectors": sorted_sectors,
            "periods": periods,
            "affected_metrics": affected_metrics
        }

    def execute(self) -> dict:
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)

        plots_dir = Path("data/plots")
        plots_dir.mkdir(parents=True, exist_ok=True)

        print("Starting pipeline execution...")
        affected_metrics = self.llm_wrapper.parse_input(self.user_scenery)
        macro_data = self.stock_wrapper.get_macro_metrics() 
        stocks_data = self.stock_wrapper.get_stocks()
        periods = self.stock_wrapper.process_similar_macro_scenario(macro_data, affected_metrics)
        best_stocks, worst_stocks, all_stocks_sorted = self.stock_wrapper.process_best_worst_tickers(periods, stocks_data)
        best_sectors, worst_sectors, sorted_sectors = self.stock_wrapper.process_best_worst_sectors(all_stocks_sorted) 
        context = self._group_context(best_stocks, worst_stocks, best_sectors, worst_sectors, all_stocks_sorted, sorted_sectors, periods, affected_metrics)
        risks = self.llm_wrapper.analyse_risk(context) 
        final_json = self.llm_wrapper.generate_json(risks, context)
        markdown = self.llm_wrapper.generate_report(final_json)
        self._dump_json(final_json)
        self._dump_markdown(markdown)
        print("Pipeline execution completed.")

        return {
            "affected_metrics": affected_metrics,
            "context": context,
            "risks": risks,
            "final_json": final_json,
            "markdown": markdown,
            "best_stocks": best_stocks,
            "worst_stocks": worst_stocks,
            "all_stocks_sorted": all_stocks_sorted,
            "best_sectors": best_sectors,
            "worst_sectors": worst_sectors,
            "sorted_sectors": sorted_sectors,
            "periods": periods,
        }

    def run(self) -> None:
        self.execute()