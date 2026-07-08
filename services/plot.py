from pathlib import Path
import matplotlib.pyplot as plt

class Plot:
    def __init__(self, output_dir: str = "data/plots") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _split_extremes(all_stocks_sorted: list) -> tuple[list, list]:
        top_stocks = all_stocks_sorted[:3]
        bottom_stocks = all_stocks_sorted[-3:]
        return top_stocks, bottom_stocks

    def _save_bar_plot(
        self,
        items: list,
        title: str,
        filename: str,
        color: str,
        y_label: str,
    ) -> str:
        labels = [label for label, _ in items]
        values = [value for _, value in items]

        figure, axis = plt.subplots(figsize=(8, 4))
        axis.bar(labels, values, color=color)
        axis.set_title(title)
        axis.set_ylabel(y_label)
        axis.grid(axis="y", linestyle="--", alpha=0.3)
        axis.axhline(0, color="black", linewidth=0.8)
        plt.xticks(rotation=20, ha="right")
        figure.tight_layout()

        output_path = self.output_dir / filename
        figure.savefig(output_path, dpi=180, bbox_inches="tight")
        plt.close(figure)
        return str(output_path)

    def plot_stock_extremes(self, all_stocks_sorted: list) -> dict:
        top_stocks, bottom_stocks = self._split_extremes(all_stocks_sorted)

        top_path = self._save_bar_plot(
            top_stocks,
            "Top 3 acoes mais favorecidas (retorno medio nos periodos)",
            "top_3_acoes.png",
            "#2e7d32",
            "Retorno medio (%) nos periodos selecionados",
        )

        bottom_path = self._save_bar_plot(
            bottom_stocks,
            "Top 3 acoes mais prejudicadas (retorno medio nos periodos)",
            "bottom_3_acoes.png",
            "#c62828",
            "Retorno medio (%) nos periodos selecionados",
        )

        return {
            "top_path": top_path,
            "bottom_path": bottom_path,
        }

    def plot_sector_extremes(self, sorted_sectors: list) -> dict:
        top_sectors, bottom_sectors = self._split_extremes(sorted_sectors)

        top_path = self._save_bar_plot(
            top_sectors,
                "Top 3 setores com melhor retorno ponderado",
            "top_3_setores.png",
            "#1565c0",
                "Retorno normalizado (%)",
        )

        bottom_path = self._save_bar_plot(
            bottom_sectors,
                "Top 3 setores com pior retorno ponderado",
            "bottom_3_setores.png",
            "#6a1b9a",
                "Retorno normalizado (%)",
        )

        return {
            "top_path": top_path,
            "bottom_path": bottom_path,
        }