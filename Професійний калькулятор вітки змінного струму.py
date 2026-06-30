import cmath
import math
import matplotlib.pyplot as plt

def calculate_circuit():
    print("--- Професійний калькулятор вітки змінного струму ---")
    print("1. Резистор (R)")
    print("2. Котушка (L)")
    print("3. Конденсатор (C)")
    print("4. Послідовне RL")
    print("5. Послідовне RC")
    print("6. Послідовне RLC (повна вітка)")
    
    choice = input("Виберіть тип вітки (1-6): ")
    
    # Ініціалізація значень за замовчуванням
    R = L_mH = C_uF = 0.0
    
    # Логіка вибору
    if choice in ['1', '4', '5', '6']: R = float(input("R (Ом): "))
    if choice in ['2', '4', '6']: L_mH = float(input("L (мГн): "))
    if choice in ['3', '5', '6']: C_uF = float(input("C (мкФ): "))
    
    f = float(input("Частота f (Гц): "))
    U_rms = float(input("Діюча напруга U (В): "))

    # Розрахунки
    omega = 2 * math.pi * f
    XL = omega * (L_mH / 1_000)
    XC = 1 / (omega * (C_uF / 1_000_000)) if C_uF != 0 else 0
    
    # Комплексний опір
    Z = complex(R, XL - XC)
    mod_Z = abs(Z)
    phi_rad = cmath.phase(Z)
    phi_deg = math.degrees(phi_rad)
    
    # Струм (Закон Ома: I = U / Z)
    # Приймаємо фазу напруги за 0: U = U_rms + 0j
    U = complex(U_rms, 0)
    I = U / Z
    mod_I = abs(I)
    psi_I_deg = math.degrees(cmath.phase(I))
    
    # Потужності
    S = U * I.conjugate() # Комплексна потужність
    P = S.real
    Q = S.imag

    # Вивід тексту
    print("\n" + "="*30)
    print(f"ІМПЕДАНС Z: {Z.real:.2f} {'+' if Z.imag >= 0 else '-'} j{abs(Z.imag):.2f} Ом")
    print(f"Експоненційна форма: {mod_Z:.2f} * e^(j * {phi_rad:.3f})")
    print(f"Фазовий кут φ: {phi_deg:.2f}°")
    print("-" * 30)
    print(f"СТРУМ I: {mod_I:.3f} А (кут зсуву {psi_I_deg:.2f}°)")
    print(f"ПОТУЖНІСТЬ: P = {P:.2f} Вт, Q = {Q:.2f} вар, S = {abs(S):.2f} ВА")
    print("="*30)

    # ГРАФІКА
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 1. Векторна діаграма опорів (Z)
    ax1.quiver(0, 0, Z.real, 0, angles='xy', scale_units='xy', scale=1, color='r', label='R')
    ax1.quiver(0, 0, 0, Z.imag, angles='xy', scale_units='xy', scale=1, color='b', label='X_res')
    ax1.quiver(0, 0, Z.real, Z.imag, angles='xy', scale_units='xy', scale=1, color='purple', label='Z')
    ax1.set_title("Діаграма опорів (Ом)")
    ax1.grid(True)
    ax1.legend()
    
    # Автомасштабування осей для Z
    limit_z = max(abs(Z.real), abs(Z.imag), 1) * 1.2
    ax1.set_xlim(-limit_z/4, limit_z)
    ax1.set_ylim(-limit_z, limit_z)

    # 2. Векторна діаграма Струму та Напруги
    # Масштабуємо струм для візуалізації поруч із напругою
    scale_factor = U_rms / mod_I if mod_I != 0 else 1
    ax2.quiver(0, 0, U.real, U.imag, angles='xy', scale_units='xy', scale=1, color='orange', label='U (В)')
    ax2.quiver(0, 0, I.real * scale_factor, I.imag * scale_factor, angles='xy', scale_units='xy', scale=1, color='green', label='I (масштаб)')
    ax2.set_title("Діаграма U та I (Фази)")
    ax2.grid(True)
    ax2.legend()

    limit_u = U_rms * 1.2
    ax2.set_xlim(-limit_u, limit_u)
    ax2.set_ylim(-limit_u, limit_u)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    calculate_circuit()