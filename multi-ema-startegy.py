from AlgorithmImports import *

class EMAMovingAverageStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2017, 1, 1)
        self.SetEndDate(2024, 12, 30)
        self.SetCash(100000)

        # Add all symbols in S&P 500
        self.symbols = [
                    "AAPL", "MSFT", "GOOGL", "AMZN", "FB", "JPM", "V", "PG",  # Original symbols
                    "NVDA", "TSLA", "BRK.B", "UNH", "JNJ", "XOM", "META",  # Technology, financials, healthcare, energy
                    "KO", "PEP", "HD", "MCD", "NFLX", "DIS", "CVX",  # Consumer staples, discretionary, communication services
                    "NKE", "LLY", "PFE", "MRK", "BA", "COST", "CRM",  # Healthcare, industrials, retail
                    "ADBE", "INTC", "BAC", "GS", "TMO", "CAT", "RTX",  # Tech, finance, healthcare, industrials
                    "WMT", "ABT", "HON", "MMM", "DUK", "NEE", "MDLZ"  # Consumer staples, utilities
]

        
        # Initialize indicators and rolling windows for each symbol
        self.indicators = {}
        self.ema60_tracks = {}

        for symbol in self.symbols:
            equity = self.AddEquity(symbol, Resolution.DAILY)
            self.indicators[symbol] = {
                "ema9": self.EMA(equity.Symbol, 9, Resolution.DAILY),
                "ema15": self.EMA(equity.Symbol, 15, Resolution.DAILY),
                "ema65": self.EMA(equity.Symbol, 65, Resolution.DAILY),
                "ema200": self.EMA(equity.Symbol, 150, Resolution.DAILY),
                "ema35": self.EMA(equity.Symbol, 35 , Resolution.DAILY),
                "rsi": self.RSI(equity.Symbol, 14, Resolution.DAILY),
               
            }
            self.ema60_tracks[symbol] = RollingWindow[IndicatorDataPoint](60)

        self.SetWarmUp(200)

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        for symbol in self.symbols:
            if data.ContainsKey(symbol):
                current_data = data[symbol]
                if current_data:
                    self.ema60_tracks[symbol].Add(self.indicators[symbol]["ema35"].Current)
        
        for symbol in self.symbols:
            if self.ema60_tracks[symbol].IsReady:
                self.TradeSymbol(symbol)
        

    def TradeSymbol(self, symbol):
        indicators = self.indicators[symbol]
        ema60_track = self.ema60_tracks[symbol]  # Corrected attribute name
        

        if self.IsBuyCondition(indicators, ema60_track):  # Pass ema60_track to IsBuyCondition
            self.SetHoldings(symbol, 1)
           
        elif self.IsSellCondition(indicators, ema60_track):  # Pass ema60_track to IsSellCondition
           self.Liquidate(symbol)
        elif self.Portfolio[symbol].Invested:
            if self.IsExitBuyCondition(indicators):
                self.Liquidate(symbol)
            # elif self.IsExitSellCondition(indicators):
            #     self.Liquidate(symbol)
        
                 

    def IsBuyCondition(self, indicators, ema60_track):  # Added ema60_track parameter
        ema_condition = (indicators["ema9"].Current.Value > indicators["ema15"].Current.Value > indicators["ema65"].Current.Value > indicators["ema200"].Current.Value)
        ema35_condition = indicators["rsi"].Current.Value > 50
        
        return ema_condition and ema35_condition

    def IsSellCondition(self, indicators, ema60_track):  # Added ema60_track parameter
        ema_condition = (indicators["ema9"].Current.Value < indicators["ema15"].Current.Value < indicators["ema65"].Current.Value < indicators["ema200"].Current.Value)
        ema35_condition = indicators["rsi"].Current.Value < 50
        return ema_condition and ema35_condition

    def IsExitBuyCondition(self, indicators):
        ema_cross_condition = (indicators["ema9"].Current.Value < indicators["ema65"].Current.Value or indicators["ema15"].Current.Value < indicators["ema65"].Current.Value)
        rsi_condition = indicators["rsi"].Current.Value < 40
        return ema_cross_condition and rsi_condition

    def IsExitSellCondition(self, indicators):
        ema_cross_condition = (indicators["ema9"].Current.Value > indicators["ema65"].Current.Value or indicators["ema15"].Current.Value > indicators["ema65"].Current.Value)
        rsi_condition = indicators["rsi"].Current.Value > 60
        return ema_cross_condition and rsi_condition
