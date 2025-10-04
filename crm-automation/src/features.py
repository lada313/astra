from pathlib import Path
import pandas as pd
from src.data_loader import load_multiple_sources

OUT = Path('data/features.parquet')

def build_rfm(orders_df, as_of=None):
    if orders_df.empty:
        return pd.DataFrame()
    if as_of is None:
        as_of = orders_df['order_date'].max() + pd.Timedelta(days=1)
    grp = orders_df.groupby('customer_id').agg(
        recency_days=('order_date', lambda x: int((as_of - x.max()).days) if x.notna().any() else 9999),
        frequency=('order_id', 'nunique'),
        monetary=('order_amount', 'sum')
    ).reset_index()
    for col in ['recency_days','frequency','monetary']:
        try:
            grp[col + '_score'] = pd.qcut(grp[col].rank(method='first'), q=5, labels=False) + 1
        except Exception:
            grp[col + '_score'] = 1
    grp['recency_days_score'] = grp['recency_days_score'].astype(int)
    grp['frequency_score'] = grp['frequency_score'].astype(int)
    grp['monetary_score'] = grp['monetary_score'].astype(int)
    grp['rfm_score'] = grp['recency_days_score']*100 + grp['frequency_score']*10 + grp['monetary_score']
    return grp

if __name__ == '__main__':
    import glob
    orders = load_multiple_sources(glob.glob('data/clients/*.csv'))
    if orders.empty:
        print('No orders found in data/clients/')
    else:
        rfm = build_rfm(orders)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        rfm.to_parquet(OUT, index=False)
        print('Saved features to', OUT)
