
def get_loss_rate(percent: float, light: bool = False) -> str:
    """ Цвета для обозначения уровня потерь на карте """
    if percent < -20:
        return '#c7ffd4' * light or '#28a745'   # Зеленый
    elif -20 <= percent <= -5:
        return '#ffff9b' * light or '#ffc107'   # Желтый
    return '#fccec7' * light or '#dc3545'       # Красный


def get_days_overdue_msg(days_overdue: int) -> str:
    """ Сообщение для менеджера о количестве дней до окончания товара """
    if days_overdue > 0:
        return f'Товар закончился {days_overdue} дн. назад'
    elif days_overdue == 0:
        return 'Товар закончится сегодня'
    return f'Дней до окончания товара: {-days_overdue}'
