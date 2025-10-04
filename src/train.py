import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from pathlib import Path
from src.features import build_rfm

FEATURES = Path('data/features.parquet')
MODEL = Path('models/model.pkl')

def prepare_training(features_df, orders_df):
    max_date = orders_df['order_date'].max()
    last_order = orders_df.groupby('customer_id')['order_date'].max().reset_index()
    last_order['bought_next_30'] = ((max_date - last_order['order_date']).dt.days <= 30).astype(int)
    df = features_df.merge(last_order[['customer_id','bought_next_30']], on='customer_id', how='left')
    df['bought_next_30'] = df['bought_next_30'].fillna(0).astype(int)
    return df

if __name__ == '__main__':
    import glob
    from src.data_loader import load_multiple_sources
    orders = load_multiple_sources(glob.glob('data/clients/*.csv'))
    if orders.empty:
        print('No orders to train on, add CSV files to data/clients/')
    else:
        features = build_rfm(orders)
        train_df = prepare_training(features, orders)
        feature_cols = [c for c in features.columns if c.endswith('_score')]
        X = train_df[feature_cols]
        y = train_df['bought_next_30']
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        MODEL.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL)
        print('Saved model to', MODEL)
