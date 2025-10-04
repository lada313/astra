CRM Automation - starter repo

Structure:
- data/: put your CSVs here (clients, promotions, bonus cards)
- src/: source code
- config/: column maps and email config
- models/: trained model (gitignored)
- tests/: pytest tests

Quick start:
1. create virtualenv: python -m venv venv
2. pip install -r requirements.txt
3. fill data/clients/*.csv, data/bonus_cards.csv, data/promotions.csv
4. python src/features.py
5. python src/train.py
6. python src/reminders.py
7. python src/export.py --send-email  (configure config/email_settings.py first)
