from typing import Any, Dict


def update_instance(instance: Any, updates: Dict[str, Any]) -> None:
    """
    Обновляет атрибуты экземпляра модели.
    """

    for key, value in updates.items():
        setattr(instance, key, value)
