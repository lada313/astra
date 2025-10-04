import streamlit as st
import pandas as pd
import os
import sys

# Добавляем корень проекта в путь Python, чтобы импорт из src работал
sys.path.append(os.path.dirname(__file__))

from src.predict import score_customer, load_all

st.set_page_config(page_title="CRM Automation", layout="wide")
st.title("CRM Автоматизация клиентов")

# -------------------------------
# 1. Загрузка базы клиентов
# -------------------------------
uploaded_file = st.file_uploader("Загрузите CSV или Excel с клиентами", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        clients_df = pd.read_csv(uploaded_file)
    else:
        clients_df = pd.read_excel(uploaded_file)
    
    st.success(f"Загружено {len(clients_df)} клиентов")
    st.dataframe(clients_df.head())

    # -------------------------------
    # 2. Добавление/редактирование акций
    # -------------------------------
    st.subheader("Добавить акции")
    discount = st.number_input("Скидка на товар (%)", min_value=0, max_value=100, value=10)
    gift = st.text_input("Подарок от суммы заказа", value="Бесплатная доставка")

    # -------------------------------
    # 3. Загрузка бонусных карт для синхронизации
    # -------------------------------
    bonus_file = st.file_uploader("Загрузите бонусные карты клиентов", type=["csv", "xlsx"])
    if bonus_file:
        if bonus_file.name.endswith(".csv"):
            bonuses_df = pd.read_csv(bonus_file)
        else:
            bonuses_df = pd.read_excel(bonus_file)
        st.success(f"Загружено {len(bonuses_df)} бонусных карт")
        # Синхронизация по номеру бонусной карты
        clients_df = clients_df.merge(bonuses_df, on="bonus_card_number", how="left")

    # -------------------------------
    # 4. Прогноз вероятности покупки
    # -------------------------------
    st.subheader("Прогноз вероятности покупки")
    model, feats = load_all()
    def get_score(cid):
        try:
            return score_customer(str(cid))
        except:
            return 0
    clients_df["purchase_probability"] = clients_df["customer_id"].apply(get_score)
    st.dataframe(clients_df[["customer_id", "purchase_probability"]].head())

    # -------------------------------
    # 5. Генерация Excel с рекомендациями
    # -------------------------------
    st.subheader("Генерация рекомендаций")
    if st.button("Создать Excel с рекомендациями"):
        output_path = os.path.join("output", "recommendations.xlsx")
        os.makedirs("output", exist_ok=True)

        def strategy(row):
            if row["purchase_probability"] > 0.7:
                return "Акция + SMS"
            elif row["purchase_probability"] > 0.4:
                return "Email + Бонус"
            else:
                return "Напоминание / Подарок"

        clients_df["strategy"] = clients_df.apply(strategy, axis=1)
        clients_df.to_excel(output_path, index=False)
        st.success(f"Excel создан: {output_path}")
        st.write(clients_df.head())
