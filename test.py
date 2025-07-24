import streamlit as st
from PIL import Image
import os
import random

# 무기 이미지 없으면 임시로 생성
from PIL import ImageDraw

def ensure_weapon_images():
    os.makedirs("assets/weapons", exist_ok=True)
    for name in weapon_list:
        path = f"assets/weapons/{name.lower()}.png"
        if not os.path.exists(path):
            img = Image.new('RGB', (200, 200), color=(random.randint(50,200), random.randint(50,200), random.randint(50,200)))
            draw = ImageDraw.Draw(img)
            draw.text((10, 90), name, fill="white")
            img.save(path)

ensure_weapon_images()


# 무기 설정
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

# Streamlit 화면 시작
st.set_page_config(page_title="2인용 얼굴 격투 게임", layout="centered")
st.title("🥊 내 얼굴로 하는 2인용 격투 게임")

# 얼굴 업로드
st.header("👤 플레이어 얼굴 업로드")
col1, col2 = st.columns(2)

with col1:
    player1_file = st.file_uploader("플레이어 1 얼굴", type=["jpg", "jpeg", "png"], key="p1")
    if player1_file:
        img1 = Image.open(player1_file).resize((200, 200))
        os.makedirs("players", exist_ok=True)
        img1.save("players/player1.jpg")
        st.image(img1, caption="플레이어 1")

with col2:
    player2_file = st.file_uploader("플레이어 2 얼굴", type=["jpg", "jpeg", "png"], key="p2")
    if player2_file:
        img2 = Image.open(player2_file).resize((200, 200))
        os.makedirs("players", exist_ok=True)
        img2.save("players/player2.jpg")
        st.image(img2, caption="플레이어 2")

# 전투 버튼
if st.button("⚔️ 전투 시작!"):
    if not (player1_file and player2_file):
        st.warning("두 플레이어 모두 얼굴을 업로드해주세요.")
    else:
        p1_weapon, p2_weapon, winner = simulate_fight()
        st.subheader("🔫 무기 배정 결과")
        wcol1, wcol2 = st.columns(2)

        with wcol1:
            st.markdown(f"**플레이어 1 무기:** {p1_weapon}")
            st.image(f"assets/weapons/{p1_weapon.lower()}.png", width=150)

        with wcol2:
            st.markdown(f"**플레이어 2 무기:** {p2_weapon}")
            st.image(f"assets/weapons/{p2_weapon.lower()}.png", width=150)

        st.markdown("## 🏆 승리자:")
        st.success(f"{winner}의 승리!")
