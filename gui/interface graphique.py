import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

from pipeline_complet import compresser_image_vers_png


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur PNG maison")
        self.root.geometry("520x360")
        self.root.resizable(False, False)

        self.chemin_source = None
        self.chemin_sortie = None

        
        tk.Label(
            root, text="Compression PNG from scratch",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            root, text="Filtrage + LZ77 + Huffman + DEFLATE + zlib, codés à la main",
            font=("Segoe UI", 9), fg="gray"
        ).pack(pady=(0, 20))

        
        frame1 = tk.Frame(root)
        frame1.pack(pady=8, fill="x", padx=30)

        tk.Button(
            frame1, text="1. Choisir une image",
            command=self.choisir_image, width=25, height=2
        ).pack()

        self.label_source = tk.Label(
            frame1, text="Aucun fichier sélectionné", fg="gray", wraplength=450
        )
        self.label_source.pack(pady=(5, 0))

        
        frame2 = tk.Frame(root)
        frame2.pack(pady=15, fill="x", padx=30)

        options_frame = tk.Frame(frame2)
        options_frame.pack()
        tk.Label(options_frame, text="Taille max (côté, en pixels) :").pack(side="left")
        self.taille_var = tk.StringVar(value="100")
        tk.Entry(options_frame, textvariable=self.taille_var, width=6).pack(side="left", padx=5)

        self.bouton_convertir = tk.Button(
            frame2, text="2. Convertir en PNG",
            command=self.lancer_conversion, width=25, height=2,
            state="disabled"
        )
        self.bouton_convertir.pack(pady=(10, 0))

        # --- Barre de statut / progression ---
        self.label_statut = tk.Label(root, text="", fg="blue", wraplength=450, justify="left")
        self.label_statut.pack(pady=10)

        
        self.bouton_telecharger = tk.Button(
            root, text="3. Enregistrer le PNG obtenu",
            command=self.telecharger, width=25, height=2,
            state="disabled"
        )
        self.bouton_telecharger.pack(pady=5)

   

    def choisir_image(self):
        chemin = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[
                ("Toutes les images", "*.rw2 *.cr2 *.nef *.arw *.dng *.jpg *.jpeg *.png *.bmp"),
                ("RAW", "*.rw2 *.cr2 *.nef *.arw *.dng"),
                ("Images classiques", "*.jpg *.jpeg *.png *.bmp"),
                ("Tous les fichiers", "*.*"),
            ]
        )
        if chemin:
            self.chemin_source = chemin
            self.label_source.config(text=os.path.basename(chemin), fg="black")
            self.bouton_convertir.config(state="normal")
            self.bouton_telecharger.config(state="disabled")
            self.label_statut.config(text="")

    def lancer_conversion(self):
        if not self.chemin_source:
            return

        try:
            max_taille = int(self.taille_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "La taille doit être un nombre entier.")
            return

        self.bouton_convertir.config(state="disabled")
        self.label_statut.config(text="Conversion en cours...", fg="blue")
        self.root.update()

        thread = threading.Thread(target=self._convertir, args=(max_taille,))
        thread.start()

    def _convertir(self, max_taille):
        try:
            lignes, largeur, hauteur, bpp = self._charger_image(self.chemin_source, max_taille)

            dossier_tmp = os.path.dirname(os.path.abspath(self.chemin_source))
            nom_base = os.path.splitext(os.path.basename(self.chemin_source))[0]
            self.chemin_sortie = os.path.join(dossier_tmp, f"{nom_base}_compresse.png")

            import io
            import contextlib
            buffer_logs = io.StringIO()
            with contextlib.redirect_stdout(buffer_logs):
                compresser_image_vers_png(lignes, largeur, hauteur, bpp, self.chemin_sortie)

            logs = buffer_logs.getvalue()
            self.root.after(0, self._conversion_terminee, logs)

        except Exception as e:
            self.root.after(0, self._conversion_echouee, str(e))

    def _charger_image(self, chemin, max_taille):
        ext = os.path.splitext(chemin)[1].lower()

        if ext in (".rw2", ".cr2", ".nef", ".arw", ".dng"):
            import rawpy
            with rawpy.imread(chemin) as raw:
                rgb = raw.postprocess()
        else:
            from PIL import Image
            import numpy as np
            img = Image.open(chemin).convert("RGB")
            rgb = np.array(img)

        hauteur_totale, largeur_totale, canaux = rgb.shape
        largeur = min(max_taille, largeur_totale)
        hauteur = min(max_taille, hauteur_totale)
        rgb_rogne = rgb[:hauteur, :largeur, :]

        lignes = [bytes(rgb_rogne[y].flatten()) for y in range(hauteur)]
        return lignes, largeur, hauteur, canaux

    def _conversion_terminee(self, logs):
        self.label_statut.config(
            text=f"Conversion réussie.\n\n{logs.strip()}", fg="dark green"
        )
        self.bouton_convertir.config(state="normal")
        self.bouton_telecharger.config(state="normal")

    def _conversion_echouee(self, message_erreur):
        self.label_statut.config(text=f"Erreur : {message_erreur}", fg="red")
        self.bouton_convertir.config(state="normal")
        messagebox.showerror("Erreur de conversion", message_erreur)

    

    def telecharger(self):
        if not self.chemin_sortie or not os.path.exists(self.chemin_sortie):
            messagebox.showerror("Erreur", "Aucun fichier PNG à enregistrer.")
            return

        destination = filedialog.asksaveasfilename(
            title="Enregistrer le PNG",
            defaultextension=".png",
            filetypes=[("Image PNG", "*.png")],
            initialfile=os.path.basename(self.chemin_sortie),
        )
        if destination:
            import shutil
            shutil.copy(self.chemin_sortie, destination)
            messagebox.showinfo("Enregistré", f"Fichier enregistré :\n{destination}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
