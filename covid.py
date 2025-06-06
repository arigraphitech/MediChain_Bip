import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow
 
P = np.array([
    [0.77, 0.1, 0.13, 0.0, 0.0],  # From Healthy
    [0.0, 1, 0.0, 0.0, 0.0],  # From Full inmunity
    [0.0, 0.4, 0.0, 0.6, 0.0],  # From Latent
    [0.8, 0.0, 0.0, 0.0, 0.2],  # From Sick
    [0.0, 0.0, 0.0, 0.0, 1],  # From Dead (absorbing)
])
 
P_old = np.array([
    [0.5, 0.1, 0.4, 0.0, 0.0],   # From Healthy — plus de risque de devenir Latent
    [0.0, 1.0, 0.0, 0.0, 0.0],   # Full Immunity (inchangée)
    [0.0, 0.1, 0.0, 0.9, 0.0],   # Latent — quasi-certitude de devenir malade
    [0.3, 0.0, 0.0, 0.0, 0.7],   # Sick — grande probabilité de décès
    [0.0, 0.0, 0.0, 0.0, 1.0],   # Dead (absorbing)
])
 
 
P_disease = np.array([
    [0.6, 0.1, 0.3, 0.0, 0.0],   # Healthy → more chance to become Latent
    [0.0, 1.0, 0.0, 0.0, 0.0],   # Full immunity = stable
    [0.0, 0.2, 0.0, 0.8, 0.0],   # Latent → more likely to become Sick
    [0.6, 0.0, 0.0, 0.0, 0.4],   # Sick → less likely to recover, more chance of death
    [0.0, 0.0, 0.0, 0.0, 1.0],   # Dead (absorbing)
])
 
P_old_disease = np.array([
    [0.4, 0.1, 0.5, 0.0, 0.0],   # Healthy → fort risque de devenir Latent
    [0.0, 1.0, 0.0, 0.0, 0.0],   # Full Immunity (stable)
    [0.0, 0.05, 0.0, 0.95, 0.0], # Latent → quasiment sûr de devenir Sick
    [0.2, 0.0, 0.0, 0.0, 0.8],   # Sick → très forte probabilité de décès
    [0.0, 0.0, 0.0, 0.0, 1.0],   # Dead (absorbing)
])
 
P_vaccinated = np.array([
    [0.85, 0.1, 0.05, 0.0, 0.0],    # Healthy → faible risque d’infection
    [0.0, 1.0, 0.0, 0.0, 0.0],      # Full Immunity = stable
    [0.0, 0.7, 0.0, 0.3, 0.0],      # Latent → + souvent vers Immunité
    [0.9, 0.0, 0.0, 0.0, 0.1],      # Sick → retour + probable vers Healthy
    [0.0, 0.0, 0.0, 0.0, 1.0],      # Dead = état absorbant
])
 
P_vaccinated_old = np.array([
    [0.7, 0.1, 0.2, 0.0, 0.0],    # Healthy → risque modéré de Latent
    [0.0, 1.0, 0.0, 0.0, 0.0],    # Full Immunity = stable
    [0.0, 0.5, 0.0, 0.5, 0.0],    # Latent → 50/50 chance d’immunité vs maladie
    [0.6, 0.0, 0.0, 0.0, 0.4],    # Sick → récupération possible, mais risque de décès significatif
    [0.0, 0.0, 0.0, 0.0, 1.0],    # Dead = absorbant
])
 
P_vaccinated_diseased = np.array([
    [0.75, 0.1, 0.15, 0.0, 0.0],    # From Healthy → bonne protection vaccinale
    [0.0, 1.0, 0.0, 0.0, 0.0],      # From Full Immunity = stable
    [0.0, 0.3, 0.0, 0.7, 0.0],      # From Latent → moins d’immunité, plus de progression
    [0.5, 0.0, 0.0, 0.0, 0.5],      # From Sick → moitié récupèrent, moitié vont vers Dead
    [0.0, 0.0, 0.0, 0.0, 1.0],      # From Dead = état absorbant
])
 
P_vaccinated_old_diseased = np.array([
    [0.6, 0.1, 0.3, 0.0, 0.0],    # From Healthy: risque non négligeable de devenir Latent
    [0.0, 1.0, 0.0, 0.0, 0.0],    # Full Immunity = état stable
    [0.0, 0.2, 0.0, 0.8, 0.0],    # Latent → progression souvent vers malade
    [0.4, 0.0, 0.0, 0.0, 0.6],    # Sick → chance modérée de guérison, mais risque réel de décès
    [0.0, 0.0, 0.0, 0.0, 1.0],    # Dead = état absorbant
])
 
 
 
 
 
imagePath="./base_(adult).png"
def show_results():
    plt.close('all')
    state = state_var.get()
    predispositions = []

    # Choix de la bonne matrice NON transposée pour la simulation
    if old_var.get() and disease_var.get() and vaccinate_var.get():
        imagePath = "./markov_chain_vaccinated_old_diseased.png"
        P_used = P_vaccinated_old_diseased
    elif disease_var.get() and vaccinate_var.get():
        imagePath = "./vaccinated_+_diseased.png"
        P_used = P_vaccinated_diseased
    elif old_var.get() and disease_var.get():
        imagePath = "./old_+_diseased.png"
        P_used = P_old_disease
    elif old_var.get() and vaccinate_var.get():
        imagePath = "./vaccinated_+_old.png"
        P_used = P_vaccinated_old
    elif old_var.get():
        imagePath = "./old.png"
        P_used = P_old
    elif disease_var.get():
        imagePath = "./diseased.png"
        P_used = P_disease
    elif vaccinate_var.get():
        imagePath = "./vaccinated.png"
        P_used = P_vaccinated
    else:
        imagePath = "./base_(adult).png"
        P_used = P

    if state == "healthy":
        fisrt_state = 0
    elif state == "latent":
        fisrt_state = 2
    elif state == "sick":
        fisrt_state = 3

    # Affichage de l'image
    image = Image.open(imagePath)
    image = image.resize((600, 400))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    states = ["Healthy", "Full immunity", "Latent", "Sick", "Dead"]

    # Graphique — on transpose ici uniquement pour l'affichage
    P_T = P_used.T
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(states))

    for i in range(len(states)):
        ax.bar(range(len(states)), P_T[i], bottom=bottom, label=states[i])
        bottom += P_T[i]

    ax.set_xticks(range(len(states)))
    ax.set_xticklabels([f"From {s}" for s in states], rotation=45)
    ax.set_ylabel("Transition Probability")
    ax.set_title("Stacked Bar Chart of Transition Probabilities for Each State")
    ax.legend(title="To State")
    plt.tight_layout()
    plt.show()

    # Simulation
    final_state_counts = np.zeros(len(states))
    np.random.seed(0)

    for i in range(10):
        current_state = fisrt_state
        for t in range(10):
            probs = P_used[current_state]
            probs = probs / np.sum(probs)  # 🔒 Sécurité pour s'assurer que la somme = 1
            next_state = np.random.choice(range(len(states)), p=probs)
            current_state = next_state
        final_state_counts[current_state] += 1

    final_state_probs = final_state_counts / 10

    # Diagramme des probabilités finales
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(states, final_state_probs, color='mediumseagreen')
    ax.set_ylabel("Probability")
    ax.set_title("Estimated Final State Probabilities (10 Simulations)")
    ax.set_ylim(0, 1)

    for bar, prob in zip(bars, final_state_probs):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.02,
                f'{prob:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
    plt.close('all')
 
 
current_state=0  
# Colors
bg_color = "#E6F0FA"
frame_color = "#D0E3F1"
button_color = "#62C370"
title_color = "#B00020"
 
root = tk.Tk()
root.title("Doctor Interface - COVID-19")
root.geometry("800x1250")
root.configure(bg=bg_color)
 
# Title
title_label = tk.Label(root, text="COVID-19", font=("Helvetica", 28, "bold"), bg=bg_color, fg=title_color)
title_label.pack(pady=25)
 
# State section
state_frame = tk.LabelFrame(root, text="🧬 State of the patient", font=("Helvetica", 12, "bold"),
                            bg=frame_color, fg="black", padx=10, pady=10)
state_frame.pack(padx=20, pady=10, fill="x")
 
state_var = tk.StringVar(value="healthy")
tk.Radiobutton(state_frame, text="Healthy", variable=state_var, value="healthy", bg=frame_color).pack(anchor="w")
tk.Radiobutton(state_frame, text="Latent", variable=state_var, value="latent", bg=frame_color).pack(anchor="w")
tk.Radiobutton(state_frame, text="Sick", variable=state_var, value="sick", bg=frame_color).pack(anchor="w")
 
# Predispositions section
pred_frame = tk.LabelFrame(root, text="⚠️ Predispositions", font=("Helvetica", 12, "bold"),
                           bg=frame_color, fg="black", padx=10, pady=10)
pred_frame.pack(padx=20, pady=10, fill="x")
 
old_var = tk.BooleanVar()
disease_var = tk.BooleanVar()
vaccinate_var = tk.BooleanVar()
 
tk.Checkbutton(pred_frame, text="Old age", variable=old_var, bg=frame_color).pack(anchor="w")
tk.Checkbutton(pred_frame, text="Underlying medical condition", variable=disease_var, bg=frame_color).pack(anchor="w")
tk.Checkbutton(pred_frame, text="Vaccinated", variable=vaccinate_var, bg=frame_color).pack(anchor="w")
 
# Show button
show_btn = tk.Button(root, text="Show", command=show_results,
                     bg=button_color, fg="white", font=("Helvetica", 12, "bold"),
                     padx=20, pady=5)
show_btn.pack(pady=20)
 
# Placeholder image label
image_label = tk.Label(root, bg=bg_color)
image_label.pack(pady=10)
 
 
 
root.mainloop()
 