import pandas as pd
def generate_strategy_for_row(row, promotions_df=None):
    strategy = []
    if row.get('rfm_score',0) >= 400:
        strategy.append({'interaction':'call','perk':'consultation','note':'VIP customer'})
    days_to_expire = row.get('days_to_expire')
    if days_to_expire is not None and days_to_expire <= 7:
        strategy.append({'interaction':'email','perk':'discount','note':'Product expires soon'})
    if row.get('points',0) > 0 and row.get('points_expire_in',999) <= 14:
        strategy.append({'interaction':'sms','perk':'expiring_bonus','note':'Points expire soon'})
    if promotions_df is not None and not promotions_df.empty:
        today = pd.Timestamp.today()
        active = promotions_df[(promotions_df['start_date'] <= today) & (promotions_df['end_date'] >= today)]
        for _, promo in active.iterrows():
            strategy.append({'interaction':'email','perk':promo.get('type'),'note':f"Promo {promo.get('promotion_id')}: {promo.get('type')}"})
    return strategy

def generate_strategies(clients_df, promotions_df=None):
    rows = []
    for _, r in clients_df.iterrows():
        strat = generate_strategy_for_row(r, promotions_df)
        rows.append({'customer_id': r.get('customer_id'), 'strategies': strat})
    return pd.DataFrame(rows)
