import time
import logging
import random
import string
from typing import Dict

# ========= Налаштування =========
POLL_INTERVAL_SEC = 2        # інтервал "опитування" (секунд)
NEW_CONTRACT_PROB = 0.6      # ймовірність появи нового контракту за один цикл (0..1)
# ================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

checked_count = 0  # глобальний лічильник перевірених контрактів

def generate_mock_contract() -> str:
    """Генерує фейкову BSC-адресу контракту (40 hex-символів)."""
    return "0x" + "".join(random.choices("0123456789abcdef", k=40))

def mock_fetch_new_contracts() -> list[str]:
    """
    Імітує отримання нових контрактів з мережі.
    З ймовірністю NEW_CONTRACT_PROB повертає 0..3 нових адрес.
    """
    contracts = []
    if random.random() < NEW_CONTRACT_PROB:
        for _ in range(random.randint(1, 3)):
            contracts.append(generate_mock_contract())
    return contracts

def quick_safety_check(address: str) -> Dict[str, bool]:
    """
    Дуже проста “заглушка” перевірки безпеки:
    - 10% адрес помічаємо як risk_mint
    - 10% як high_tax
    - 10% як owner_can_withdraw
    """
    return {
        "risk_mint": random.random() < 0.10,
        "high_tax": random.random() < 0.10,
        "owner_can_withdraw": random.random() < 0.10,
    }

def decide_action(safety: Dict[str, bool]) -> str:
    """
    Спрощене рішення:
    - якщо є будь-який ризик → "SKIP"
    - інакше → "WATCH" (пізніше тут буде логіка авто-купівлі)
    """
    return "SKIP" if any(safety.values()) else "WATCH"

def handle_contract(address: str) -> None:
    """Обробка одного контракту: швидка перевірка + рішення."""
    global checked_count
    checked_count += 1

    safety = quick_safety_check(address)
    decision = decide_action(safety)

    if decision == "WATCH":
        green = "\033[92m"
        reset = "\033[0m"
        print("\n" + "-"*60)
        print(f"{green}✅ SAFE — монета #{checked_count} пройшла перевірку, можна купувати{reset}")
        print(f"Контракт: {address}")
        print(f"Всього перевірено: {checked_count}")
        print("-"*60 + "\n")
    else:
        logging.info(
            "Контракт %s | перевірка=%s → рішення=%s",
            address, safety, decision
        )

def main():
    logging.info("Старт консольного бота моніторингу (mock)...")
    seen: set[str] = set()
    try:
        while True:
            new_contracts = [c for c in mock_fetch_new_contracts() if c not in seen]
            if new_contracts:
                logging.info("Знайдено %d нових контракт(ів).", len(new_contracts))
                for addr in new_contracts:
                    seen.add(addr)
                    handle_contract(addr)
            else:
                logging.debug("Нових контрактів не знайдено.")

            time.sleep(POLL_INTERVAL_SEC)
    except KeyboardInterrupt:
        logging.info("Зупинка бота (Ctrl+C). До зустрічі!")

if __name__ == "__main__":
    main()
