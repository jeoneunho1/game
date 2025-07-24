import random

# 무기 목록과 데미지 정의
weapon_list = ["Sword", "Gun", "Banana", "Hammer", "Grenade"]
weapon_damage = {
    "Sword": (15, 30),
    "Gun": (20, 35),
    "Banana": (5, 15),
    "Hammer": (10, 25),
    "Grenade": (25, 40)
}

def assign_random_weapon():
    return random.choice(weapon_list)

def simulate_fight():
    p1_weapon = assign_random_weapon()
    p2_weapon = assign_random_weapon()

    p1_damage = random.randint(*weapon_damage[p1_weapon])
    p2_damage = random.randint(*weapon_damage[p2_weapon])

    if p1_damage > p2_damage:
        winner = "플레이어 1"
    elif p2_damage > p1_damage:
        winner = "플레이어 2"
    else:
        winner = "무승부"

    return p1_weapon, p2_weapon, winner

# 실행 테스트
if __name__ == "__main__":
    p1_weapon, p2_weapon, winner = simulate_fight()
    print(f"플레이어 1 무기: {p1_weapon}")
    print(f"플레이어 2 무기: {p2_weapon}")
    print(f"승리자: {winner}")
