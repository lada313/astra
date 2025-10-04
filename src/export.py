import pandas as pd
import smtplib
from email.message import EmailMessage
from pathlib import Path
from config.email_settings import EMAIL_SETTINGS

def export_strategy_actions(df, output_path='strategy_actions.xlsx'):
    rows = []
    for _, row in df.iterrows():
        for action in row['strategies']:
            rows.append({
                'customer_id': row['customer_id'],
                'interaction': action.get('interaction'),
                'perk': action.get('perk'),
                'note': action.get('note')
            })
    out = Path(output_path)
    pd.DataFrame(rows).to_excel(out, index=False)
    return out

def send_email_with_attachment(to_email, subject, body, file_path):
    cfg = EMAIL_SETTINGS
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = cfg.get('from_addr') or cfg.get('login')
    msg['To'] = to_email
    msg.set_content(body)
    with open(file_path, 'rb') as f:
        data = f.read()
        name = Path(file_path).name
    msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=name)
    server = smtplib.SMTP(cfg['smtp_server'], cfg['smtp_port'])
    server.starttls()
    server.login(cfg['login'], cfg['password'])
    server.send_message(msg)
    server.quit()
    return True

if __name__ == '__main__':
    import glob
    from src.data_loader import load_multiple_sources
    clients = load_multiple_sources(glob.glob('data/clients/*.csv'))
    promotions = pd.read_csv('data/promotions.csv') if Path('data/promotions.csv').exists() else pd.DataFrame()
    from src.reminders import daily_reminders
    rem = daily_reminders(clients, promotions)
    out = export_strategy_actions(rem, 'data/strategy_actions.xlsx')
    print('Exported to', out)
