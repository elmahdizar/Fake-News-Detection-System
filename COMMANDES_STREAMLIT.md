# Commandes pour lancer Streamlit

Depuis le dossier du projet :

```powershell
cd "C:\Users\MSI GF63 11UC\Desktop\project pfe\Fake-News-Detection-System"
```

Installer Streamlit si ce n'est pas deja fait :

```powershell
pip install streamlit
```

Lancer l'application :

```powershell
streamlit run streamlit_app.py
```

Si la commande `streamlit` ne marche pas, utiliser :

```powershell
python -m streamlit run streamlit_app.py
```

Puis ouvrir l'adresse affichee dans le terminal, souvent :

```text
http://localhost:8501
```

## Mettre a jour GitHub

Verifier les fichiers modifies :

```bash
git status
```

Ajouter tous les changements :

```bash
git add -A
```

Creer un commit :

```bash
git commit -m "Update Streamlit deployment files"
```

Envoyer vers GitHub :

```bash
git push origin main
```

Apres le push, ouvrir Streamlit Cloud puis cliquer sur :

```text
Manage App > Reboot app
```
