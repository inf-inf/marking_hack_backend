def get_loss_rate(percent: float,
                  good_percent_limit: int = -20,
                  warn_percent_limit: int = -5,
                  light: bool = False) -> str:
    """ Цвета для обозначения уровня потерь на карте """
    if percent < good_percent_limit:
        return '#93ffac' * light or '#28a745'   # Зеленый
    elif good_percent_limit <= percent <= warn_percent_limit:
        return '#ffff9b' * light or '#ffc107'   # Желтый
    return '#fc7462' * light or '#dc3545'       # Красный


def get_days_overdue_msg(days_overdue: int) -> str:
    """ Сообщение для менеджера о количестве дней до окончания товара """
    if days_overdue > 0:
        return f'Товар закончился {days_overdue} дн. назад'
    elif days_overdue == 0:
        return 'Товар закончится сегодня'
    return f'Дней до окончания товара: {-days_overdue}'
