import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Настройки
n_users = 10000
days = 30
start_date = datetime(2023, 1, 1)
event_types = ['view', 'click', 'registration', 'purchase']

# Генерация пользователей (с группами A/B)
users = pd.DataFrame({
    'user_id': range(1, n_users+1),
    'group': np.random.choice(['A', 'B'], n_users, p=[0.5, 0.5]),
    'device': np.random.choice(['iOS', 'Android'], n_users)
})

# Генерация событий (логи)
events = []
for day in range(days):
    date = start_date + timedelta(days=day)
    # Количество событий в день (по Пуассону)
    n_events_day = np.random.poisson(200) + 500  # от 500 до ~700
    for _ in range(n_events_day):
        user = users.sample(1).iloc[0]
        user_id = user['user_id']
        group = user['group']
        device = user['device']
        # Время внутри дня
        time = date + timedelta(seconds=np.random.randint(0, 86400))
        # Выбор события с вероятностями (воронка)
        event = np.random.choice(event_types, p=[0.3, 0.4, 0.2, 0.1])  # view, click, registration, purchase
        # Для новых пользователей (регистрация только раз) - упростим
        events.append({
            'user_id': user_id,
            'event_type': event,
            'event_time': time,
            'group': group,
            'device': device
        })

# Сохраняем
df_events = pd.DataFrame(events)
df_events.to_csv('data/user_logs.csv', index=False)

print("Логи сгенерированы, сохранены в data/user_logs.csv")
