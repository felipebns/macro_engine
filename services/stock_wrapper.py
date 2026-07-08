import yfinance
import requests
import pandas as pd
from datetime import datetime

TODAY = datetime.today()

class StockWrapper:
    def __init__(self) -> None:
        self.b3_stocks = [
            "ALOS3.SA", "ABEV3.SA", "ASAI3.SA", "AURE3.SA", "AXIA3.SA",
            "AXIA6.SA", "AZZA3.SA", "B3SA3.SA", "BBSE3.SA", "BBDC3.SA",
            "BBDC4.SA", "BRAP4.SA", "BBAS3.SA", "BRKM5.SA", "BRAV3.SA",
            "BPAC11.SA", "CXSE3.SA", "CEAB3.SA", "CMIG4.SA", "COGN3.SA",
            "CSMG3.SA", "CPLE3.SA", "CSAN3.SA", "CPFE3.SA", "CMIN3.SA",
            "CURY3.SA", "CYRE3.SA", "DIRR3.SA", "EMBJ3.SA", "ENGI11.SA",
            "ENEV3.SA", "EGIE3.SA", "EQTL3.SA", "FLRY3.SA", "GGBR4.SA",
            "GOAU4.SA", "HAPV3.SA", "HYPE3.SA", "IGTI11.SA", "ISAE4.SA",
            "ITSA4.SA", "ITUB4.SA", "KLBN11.SA", "RENT3.SA", "LREN3.SA",
            "MGLU3.SA", "POMO4.SA", "MBRF3.SA", "BEEF3.SA", "MOTV3.SA",
            "MRVE3.SA", "MULT3.SA", "NATU3.SA", "PETR3.SA", "PETR4.SA",
            "RECV3.SA", "PSSA3.SA", "PRIO3.SA", "RADL3.SA", "RDOR3.SA",
            "RAIL3.SA", "SBSP3.SA", "SANB11.SA", "CSNA3.SA", "SLCE3.SA",
            "SMFT3.SA", "SUZB3.SA", "TAEE11.SA", "VIVT3.SA", "TIMS3.SA",
            "TOTS3.SA", "UGPA3.SA", "USIM5.SA", "VALE3.SA", "VAMO3.SA",
            "VBBR3.SA", "VIVA3.SA", "WEGE3.SA", "YDUQ3.SA"
        ]

        self.ticker_meta = {
            "ALOS3.SA": [0.556, "shopping centers"],
            "ABEV3.SA": [2.939, "alimentos e bebidas"],
            "ASAI3.SA": [0.482, "varejo"],
            "AURE3.SA": [0.160, "small_caps"],
            "AXIA3.SA": [3.990, "transportes"],
            "AXIA6.SA": [0.626, "transportes"],
            "AZZA3.SA": [0.086, "varejo"],
            "B3SA3.SA": [3.399, "bancos"],
            "BBSE3.SA": [0.904, "seguradoras"],
            "BBDC3.SA": [0.936, "bancos"],
            "BBDC4.SA": [3.733, "bancos"],
            "BRAP4.SA": [0.240, "mineração"],
            "BBAS3.SA": [2.375, "bancos"],
            "BRKM5.SA": [0.114, "exportadoras"],
            "BRAV3.SA": [0.402, "óleo e gás"],
            "BPAC11.SA": [2.638, "bancos"],
            "CXSE3.SA": [0.438, "seguradoras"],
            "CEAB3.SA": [0.097, "varejo"],
            "CMIG4.SA": [0.862, "small_caps"],
            "COGN3.SA": [0.198, "small_caps"],
            "CSMG3.SA": [0.412, "small_caps"],
            "CPLE3.SA": [1.791, "small_caps"],
            "CSAN3.SA": [0.364, "transportes"],
            "CPFE3.SA": [0.337, "small_caps"],
            "CMIN3.SA": [0.313, "mineração"],
            "CURY3.SA": [0.211, "construção civil"],
            "CYRE3.SA": [0.264, "construção civil"],
            "DIRR3.SA": [0.183, "construção civil"],
            "EMBJ3.SA": [2.150, "exportadoras"],
            "ENGI11.SA": [0.653, "small_caps"],
            "ENEV3.SA": [1.993, "small_caps"],
            "EGIE3.SA": [0.491, "small_caps"],
            "EQTL3.SA": [2.007, "small_caps"],
            "FLRY3.SA": [0.287, "small_caps"],
            "GGBR4.SA": [1.219, "siderurgia"],
            "GOAU4.SA": [0.347, "siderurgia"],
            "HAPV3.SA": [0.139, "small_caps"],
            "HYPE3.SA": [0.288, "alimentos e bebidas"],
            "IGTI11.SA": [0.221, "shopping centers"],
            "ISAE4.SA": [0.467, "small_caps"],
            "ITSA4.SA": [3.189, "bancos"],
            "ITUB4.SA": [8.320, "bancos"],
            "KLBN11.SA": [0.560, "papel e celulose"],
            "RENT3.SA": [1.693, "transportes"],
            "LREN3.SA": [0.618, "varejo"],
            "MGLU3.SA": [0.091, "varejo"],
            "POMO4.SA": [0.187, "transportes"],
            "MBRF3.SA": [0.504, "alimentos e bebidas"],   # provavelmente MRFG3
            "BEEF3.SA": [0.067, "alimentos e bebidas"],
            "MOTV3.SA": [0.593, "transportes"],
            "MRVE3.SA": [0.090, "construção civil"],
            "MULT3.SA": [0.392, "shopping centers"],
            "NATU3.SA": [0.345, "varejo"],
            "PETR3.SA": [4.380, "óleo e gás"],
            "PETR4.SA": [7.716, "óleo e gás"],
            "RECV3.SA": [0.129, "óleo e gás"],
            "PSSA3.SA": [0.359, "seguradoras"],
            "PRIO3.SA": [1.991, "óleo e gás"],
            "RADL3.SA": [0.982, "varejo"],
            "RDOR3.SA": [1.547, "small_caps"],
            "RAIL3.SA": [0.711, "transportes"],
            "SBSP3.SA": [3.278, "small_caps"],
            "SANB11.SA": [0.410, "bancos"],
            "CSNA3.SA": [0.200, "siderurgia"],
            "SLCE3.SA": [0.140, "exportadoras"],
            "SMFT3.SA": [0.428, "small_caps"],
            "SUZB3.SA": [1.043, "papel e celulose"],
            "TAEE11.SA": [0.356, "small_caps"],
            "VIVT3.SA": [0.984, "small_caps"],
            "TIMS3.SA": [0.709, "small_caps"],
            "TOTS3.SA": [0.771, "small_caps"],
            "UGPA3.SA": [1.136, "transportes"],
            "USIM5.SA": [0.241, "siderurgia"],
            "VALE3.SA": [12.091, "mineração"],
            "VAMO3.SA": [0.056, "transportes"],
            "VBBR3.SA": [1.492, "transportes"],
            "VIVA3.SA": [0.112, "varejo"],
            "WEGE3.SA": [2.674, "exportadoras"],
            "YDUQ3.SA": [0.103, "small_caps"]
        }
        
        self.end = TODAY.strftime("%d/%m/%Y")
        self.start = TODAY.replace(year=TODAY.year - 10).strftime("%d/%m/%Y")

        self.yf_end = TODAY.strftime("%Y-%m-%d")
        self.yf_start = TODAY.replace(year=TODAY.year - 10).strftime("%Y-%m-%d")

        self.base_url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{{CODE}}/dados?formato=json&dataInicial={self.start}&dataFinal={self.end}"

    @staticmethod
    def _normalize_in_semesters(values: list) -> dict:
        df = pd.DataFrame(values)
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df = df.dropna(subset=["data", "valor"])

        series = (
            df.set_index("data")["valor"]
            .sort_index()
            .resample("ME")
            .mean()
            .dropna()
        )

        rolling_mean = series.rolling(window=6).mean().dropna()

        pct_variation = rolling_mean.pct_change() * 100
        pct_variation = pct_variation.dropna()

        result = {}
        for end_date, value in pct_variation.items():
            start_date = (end_date - pd.DateOffset(months=5)).replace(day=1)
            label = f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            result[label] = round(float(value), 2)

        return result
    
    def _filter_stocks_by_period(self, stocks_data: pd.DataFrame, period: str) -> pd.DataFrame:
        start_str, end_str = period.split("/")
        start_date = pd.to_datetime(start_str)
        end_date = pd.to_datetime(end_str)
        return stocks_data.loc[start_date:end_date]

    def get_stocks(self) -> pd.DataFrame:
        print("Downloading stock data...")

        stocks = yfinance.download(
            self.b3_stocks,
            start=self.yf_start,
            end=self.yf_end,
            progress=True,
            auto_adjust=True,
            group_by="ticker"
        )

        return stocks
    
    def get_macro_metrics(self) -> pd.DataFrame:
        print("Downloading macroeconomic data...")

        codes = {
            "selic": 11, #Selic efetiva / diario
            "inflacao": 433, #IPCA / mensal
            "dolar": 1, # PTAX venda / diario
            "pib": 24364 #IBC - Br / mensal
        }
        dfs = {}

        for key, value in codes.items():
            adj_url = self.base_url.format(CODE=value)
            raw_values = requests.get(adj_url).json()
            dfs[key] = self._normalize_in_semesters(raw_values)

        df = pd.DataFrame(dfs)
        df.index.name = "periodo"
        df = df.dropna(how="any")
        return df
        
    def process_similar_macro_scenario(self, macro_data: pd.DataFrame, affected_metrics: dict) -> list:
        print("Starting to process similar macro scenaries...")
        current_state = pd.Series(affected_metrics, dtype=float)
        distances = (macro_data - current_state).abs().sum(axis=1)
        periods = distances.sort_values().head(5).index.tolist()
        return periods

    def process_best_worst_tickers(self, periods: list, stocks_data: pd.DataFrame) -> tuple:
        print("Choosing best stocks for macro scenary...")

        all_returns = {}
        
        for period in periods:
            period_data = self._filter_stocks_by_period(stocks_data, period)
            for ticker in self.b3_stocks:
                close_prices = period_data[ticker]["Close"].dropna()
                if close_prices.empty or len(close_prices) < 2 or close_prices.isna().any():
                    continue

                first_price = close_prices.iloc[0]
                last_price = close_prices.iloc[-1]
                pct_return = ((last_price - first_price) / first_price) * 100

                if ticker not in all_returns:
                    all_returns[ticker] = []
                all_returns[ticker].append(pct_return)
        
        avg_returns = {ticker: sum(rets) / len(rets) for ticker, rets in all_returns.items()}
        all_stocks_sorted = sorted(avg_returns.items(), key=lambda x: x[1], reverse=True)

        best_stocks = [ticker for ticker, _ in all_stocks_sorted[:3]]
        worst_stocks = [ticker for ticker, _ in all_stocks_sorted[-3:]]
        return best_stocks, worst_stocks, all_stocks_sorted

    def process_best_worst_sectors(self, all_stocks_sorted: list) -> tuple:
        print("Processing best sectors for macro scenary...")
        sector_weighted_sum = {}
        sector_weight_sum = {}
        for ticker, avg_ret in all_stocks_sorted:
            if ticker in self.ticker_meta.keys():
                weight, sector = self.ticker_meta[ticker]
                sector_weighted_sum[sector] = sector_weighted_sum.get(sector, 0) + (avg_ret * weight)
                sector_weight_sum[sector] = sector_weight_sum.get(sector, 0) + weight

        sector_score = {
            sector: (sector_weighted_sum[sector] / sector_weight_sum[sector])
            for sector in sector_weighted_sum
            if sector_weight_sum[sector]
        }
        
        sorted_sectors = sorted(sector_score.items(), key=lambda x: x[1], reverse=True)
        best_sectors = [sector for sector, _ in sorted_sectors[:3]]
        worst_sectors = [sector for sector, _ in sorted_sectors[-3:]]
        return best_sectors, worst_sectors, sorted_sectors
