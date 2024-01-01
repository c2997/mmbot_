import numpy as np
import pandas as pd

# サンプルデータの準備
mid_prices = [100, 102, 99, 101, 103, 97, 96, 100, 98, 99] # 直近10秒のミドルレート
trade_data = [(99,5), (103,3), (98,8), (97,10), (101,7), (100,6), (102,5), (96,9)] 
# 直近の約定データ(価格と数量)。売りは103と102、買いは96と99

# ロジックの定数 
N_SECONDS = 10 # 分析に使う直近の期間
ALPHA = 0.5 # リスク回避度  

# 中央値の計算
S = np.median(mid_prices)
print(f"Median mid price: {S}")

# 約定確率の計算
def calc_trade_probs(trade_data, mid):
    
    buy_trials = sell_trials = 0
    buy_traded = sell_traded = 0
    
    for price, volume in trade_data:
        
        if price > mid: # 売り約定 
            sell_trials += 1
            if volume > 0: 
                sell_traded += 1
      
        else: # 買い約定
            buy_trials += 1 
            if volume > 0:
                buy_traded += 1
                
    bp = buy_traded / buy_trials
    sp = sell_traded / sell_trials
    
    return bp, sp
    
# ボラティリティと約定確率の計算
rets = np.diff(np.log(mid_prices))
volatility = np.std(rets)  

bp, sp = calc_trade_probs(trade_data, S) 
print(f"Buy prob: {bp:.3f}, Sell prob: {sp:.3f}")

# 期待値計算関数 
def expected_pnl(buy_price, sell_price, bp, sp, v, alpha):
    
    profit = sell_price - buy_price 
    loss = v**alpha
    
    eprofit = bp * sp * profit
    eloss = (bp * (1-sp) + sp * (1-bp)) * loss
    
    return eprofit - eloss

# 最適レートの探索
candidate_rates = [(98, 103), (98, 102), (99, 103), (99,102)]

max_pnl = 0
best_rates = None

for b, s in candidate_rates:
    pnl = expected_pnl(b, s, bp, sp, volatility, ALPHA)
    print(f"{b}, {s} => {pnl:.3f}")
    
    if pnl > max_pnl:
        max_pnl = pnl
        best_rates = (b, s)
        
print(f"Best rates: {best_rates}")
