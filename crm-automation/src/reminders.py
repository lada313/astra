import pandas as pd
from src.strategy import generate_strategies
from pathlib import Path

def daily_reminders(clients_df, promotions_df=None):
    strategies = generate_strategies(clients_df, promotions_df)
    strategies['has'] = strategies['strategies'].apply(lambda x: len(x) > 0)
    return strategies[strategies['has']].drop(columns=['has'])

if __name__ == '__main__':
    import glob
    from src.data_loader import load_multiple_sources
    clients = load_multiple_sources(glob.glob('data/clients/*.csv'))
    promotions = pd.read_csv('data/promotions.csv') if Path('data/promotions.csv').exists() else pd.DataFrame()
    reminders = daily_reminders(clients, promotions)
    out = Path('data/strategy_actions.xlsx')
    rows = []
    for _, r in reminders.iterrows():
        for action in r['strategies']:
            rows.append({'customer_id': r['customer_id'], 'interaction': action.get('interaction'), 'perk': action.get('perk'), 'note': action.get('note')})
    pd.DataFrame(rows).to_excel(out, index=False)
    print('Wrote', out)
