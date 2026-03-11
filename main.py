import time

# ==========================================
# НАСТРОЙКИ МАШИНЫ ТЬЮРИНГА (менять здесь)
# ==========================================

INITIAL_TAPE = "10101"  # Начальная строчка на ленте (можно оставить пустой "")
INITIAL_STATE = "q0"  # Стартовое состояние
FINAL_STATE = "qf"  # Конечное состояние (остановка)
BLANK = "#"  # Символ пустой ячейки

# Правила в формате словаря: 'состояние символ': 'новое_состояние новый_символ сдвиг'
# Сейчас тут написана инверсия: меняет 0 на 1 и 1 на 0, потом останавливается.
RULES = {
    'q0 0': 'q0 1 R',
    'q0 1': 'q0 0 R',
    'q0 #': 'qf # N'
}


# Если нужно базовое задание препода, закомментируй RULES выше и раскомментируй эти:
# RULES = {
#     'q0 #': 'q1 1 R',
#     'q1 #': 'qf 1 N'
# }

# ==========================================
# КОД ПРОГРАММЫ
# ==========================================

def print_tape(tape, head, state, step):
    """Простенькая функция для вывода ленты в консоль"""
    keys = list(tape.keys())
    if not keys:
        min_k, max_k = head - 1, head + 1
    else:
        # Берем края ленты + немного запаса для красоты
        min_k = min(min(keys), head) - 1
        max_k = max(max(keys), head) + 1

    tape_out = ""
    pointer = ""

    for i in range(min_k, max_k + 1):
        char = tape.get(i, BLANK)
        if i == head:
            tape_out += f"[{char}]"
            pointer += " ^ "
        else:
            tape_out += f" {char} "
            pointer += "   "

    print(f"Шаг: {step} | Текущее состояние: {state}")
    print(tape_out)
    print(pointer)
    print("-" * 30)


def main():
    # Загоняем начальную строку в словарь (индекс: символ)
    tape = {i: char for i, char in enumerate(INITIAL_TAPE)}
    state = INITIAL_STATE
    head = 0
    step = 0

    print(">>> ЗАПУСК МАШИНЫ ТЬЮРИНГА <<<")
    print_tape(tape, head, state, step)

    # Крутим цикл, пока не дойдем до финального состояния
    while state != FINAL_STATE:
        current_char = tape.get(head, BLANK)
        cmd_key = f"{state} {current_char}"

        # Проверяем, есть ли такое правило
        if cmd_key not in RULES:
            print(f"АВАРИЯ! Нет правила для '{cmd_key}'")
            break

        # Достаем команду и разбиваем по пробелам
        action = RULES[cmd_key].split()
        new_state = action[0]
        new_char = action[1]
        move = action[2]

        # Обновляем ленту и состояние
        tape[head] = new_char
        state = new_state

        # Двигаем головку
        if move == 'R':
            head += 1
        elif move == 'L':
            head -= 1
        elif move == 'N':
            pass
        else:
            print("Ошибка сдвига!")
            break

        step += 1
        time.sleep(0.4)  # Небольшая пауза, чтобы было видно, как она работает
        print_tape(tape, head, state, step)

    if state == FINAL_STATE:
        print(">>> АЛГОРИТМ УСПЕШНО ЗАВЕРШЕН <<<")


if __name__ == "__main__":
    main()