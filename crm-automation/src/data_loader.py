import pandas as pd
from pathlib import Path
from config.column_maps import COLUMN_MAPS

def load_and_normalize(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    df = pd.read_csv(p)
    mapping = COLUMN_MAPS.get(p.name)
    if mapping is None:
        colmap = {}
        # attempt to auto-detect
        for candidate in ['customer_id','id','client','cust_id']:
            if candidate in df.columns:
                colmap[candidate] = 'customer_id'
        for candidate in ['order_id','order','orderid']:
            if candidate in df.columns:
                colmap[candidate] = 'order_id'
        for candidate in ['order_date','date','last_order','signup_date']:
            if candidate in df.columns:
                colmap[candidate] = 'order_date'
        for candidate in ['order_amount','sum','amount','initial_purchase']:
            if candidate in df.columns:
                colmap[candidate] = 'order_amount'
        mapping = colmap
    inv_map = {k:v for k,v in mapping.items() if k in df.columns}
    df = df.rename(columns=inv_map)
    for col in ['customer_id','order_id','order_date','order_amount']:
        if col not in df.columns:
            df[col] = None
    df['customer_id'] = df['customer_id'].astype(str)
    df['order_id'] = df['order_id'].astype(str)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['order_amount'] = pd.to_numeric(df['order_amount'], errors='coerce').fillna(0.0)
    df = df[df['customer_id'].notna()]
    return df

def load_multiple_sources(paths):
    frames = []
    for p in paths:
        frames.append(load_and_normalize(p))
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame(columns=['customer_id','order_id','order_date','order_amount'])
