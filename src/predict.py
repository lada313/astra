import joblib
import pandas as pd
from pathlib import Path

MODEL = Path('models/model.pkl')
FEATURES = Path('data/features.parquet')

_model = None
_features = None

def load_all():
    global _model, _features
    if _model is None:
        _model = joblib.load(MODEL)
    if _features is None:
        _features = pd.read_parquet(FEATURES).set_index('customer_id')
    return _model, _features

def score_customer(customer_id):
    model, feats = load_all()
    if customer_id not in feats.index:
        return None
    x = feats.loc[[customer_id]][[c for c in feats.columns if c.endswith('_score')]]
    return float(model.predict_proba(x)[0,1])
