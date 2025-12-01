# 🚀 Guide de Démarrage Rapide

Ce guide vous permettra de lancer votre première vidéo en moins de 15 minutes !

## 📋 Prérequis (5 min)

### 1. Installer FFmpeg
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y ffmpeg

# macOS
brew install ffmpeg

# Vérifier l'installation
ffmpeg -version
```

### 2. Installer n8n
```bash
# Via npm (recommandé)
npm install -g n8n

# Via npx (sans installation)
npx n8n

# Via Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

## 🔑 Obtenir les API Keys (5 min)

### D-ID (Obligatoire)
1. Aller sur [D-ID](https://www.d-id.com/)
2. Créer un compte gratuit
3. Aller dans **Settings** → **API Keys**
4. Copier votre API Key

### OpenAI (Obligatoire)
1. Aller sur [OpenAI](https://platform.openai.com/)
2. Créer un compte
3. Aller dans **API Keys**
4. Créer une nouvelle clé

### TikTok/Instagram/YouTube (Optionnel pour commencer)
Vous pouvez configurer ces API plus tard. Pour l'instant, vous pouvez tester sans publier.

## ⚙️ Configuration (3 min)

### 1. Cloner et configurer le projet
```bash
git clone <votre-repo>
cd David

# Créer le fichier .env
cp .env.example .env

# Éditer le fichier .env
nano .env  # ou votre éditeur préféré
```

### 2. Configurer les variables essentielles
Dans `.env`, remplir au minimum :
```bash
# D-ID
DID_API_KEY=votre_clé_did

# OpenAI
OPENAI_API_KEY=sk-votre_clé_openai

# Dossier temporaire
TEMP_VIDEO_DIR=/tmp/n8n-videos
```

### 3. Créer le dossier temporaire
```bash
mkdir -p /tmp/n8n-videos
```

## 🎬 Lancer votre première vidéo (2 min)

### Option 1 : Via n8n (Recommandé)

1. **Démarrer n8n**
```bash
n8n start
```

2. **Ouvrir n8n dans le navigateur**
```
http://localhost:5678
```

3. **Importer le workflow**
   - Cliquer sur **Workflows** → **Import from File**
   - Sélectionner `workflows/avatar-video-automation.json`

4. **Configurer les credentials**
   - Cliquer sur les nœuds avec une icône de warning
   - Ajouter vos API Keys :
     - D-ID API Key
     - OpenAI API Key

5. **Exécuter le workflow**
   - Cliquer sur **Execute Workflow**
   - Attendre ~5 minutes (8 vidéos x ~30 secondes chacune)

### Option 2 : Mode Test Manuel

Si vous voulez juste tester la compilation sans générer de nouvelles vidéos :

1. **Télécharger des vidéos de test**
```bash
# Créer 8 vidéos de test (exemples)
cd /tmp/n8n-videos

# Option A: Utiliser des vidéos de test (si disponibles)
# Copier 8 vidéos MP4 nommées video_part_1.mp4, video_part_2.mp4, etc.

# Option B: Générer des vidéos de test avec FFmpeg
for i in {1..8}; do
  ffmpeg -f lavfi -i testsrc=duration=8:size=1080x1920:rate=30 \
    -f lavfi -i sine=frequency=1000:duration=8 \
    -pix_fmt yuv420p video_part_$i.mp4
done
```

2. **Compiler les vidéos**
```bash
# Via Node.js
node scripts/compile_videos.js /tmp/n8n-videos /tmp/final_video.mp4 --platform tiktok

# Via Python
python scripts/compile_videos.py /tmp/n8n-videos /tmp/final_video.mp4 --platform tiktok
```

3. **Vérifier le résultat**
```bash
# Voir la vidéo finale
ls -lh /tmp/final_video.mp4

# Obtenir les infos de la vidéo
ffmpeg -i /tmp/final_video.mp4
```

## 🎨 Personnaliser votre première vidéo

### Changer le sujet
Dans n8n, éditer le node **"Schedule Trigger"** :
```json
{
  "topic": "5 astuces pour être productif"
}
```

### Changer le style
Dans le node **"Generate Video Script"**, modifier le prompt :
```
Style : humoristique
Ton : casual
Public cible : jeunes
```

### Ajouter un filigrane
```bash
node scripts/compile_videos.js /tmp/n8n-videos /tmp/final.mp4 \
  --platform tiktok \
  --watermark "@MonChannel"
```

### Ajouter une musique
```bash
node scripts/compile_videos.js /tmp/n8n-videos /tmp/final.mp4 \
  --platform tiktok \
  --music /path/to/music.mp3 \
  --music-volume 0.2
```

## 📱 Publier sur les réseaux sociaux

### Test sans publication
Par défaut, le workflow NE publie PAS automatiquement. Pour tester :
1. Désactiver les nœuds de publication dans n8n
2. Récupérer la vidéo compilée dans `/tmp/n8n-videos/final_video.mp4`
3. Publier manuellement pour vérifier

### Activer la publication automatique

1. **Configurer TikTok**
   - Obtenir les credentials sur [TikTok for Developers](https://developers.tiktok.com/)
   - Ajouter dans `.env` :
     ```bash
     TIKTOK_ACCESS_TOKEN=votre_token
     ```

2. **Configurer Instagram**
   - Obtenir les credentials sur [Facebook Developers](https://developers.facebook.com/)
   - Ajouter dans `.env` :
     ```bash
     INSTAGRAM_ACCESS_TOKEN=votre_token
     ```

3. **Configurer YouTube**
   - Obtenir les credentials sur [Google Cloud Console](https://console.cloud.google.com/)
   - Ajouter dans `.env` :
     ```bash
     YOUTUBE_CLIENT_ID=votre_client_id
     YOUTUBE_CLIENT_SECRET=votre_client_secret
     ```

4. **Activer dans n8n**
   - Aller dans les nœuds de publication
   - Ajouter les credentials
   - Activer les nœuds

## 🔧 Résolution rapide des problèmes

### "FFmpeg not found"
```bash
# Vérifier l'installation
which ffmpeg
ffmpeg -version

# Réinstaller si nécessaire
sudo apt-get install --reinstall ffmpeg
```

### "Permission denied"
```bash
# Donner les permissions au dossier
sudo chmod 777 /tmp/n8n-videos
```

### "D-ID API error"
- Vérifier que votre API key est correcte
- Vérifier que vous avez des crédits disponibles
- D-ID gratuit : 20 crédits/mois

### "Videos not compiling"
```bash
# Vérifier que les 8 vidéos sont présentes
ls -la /tmp/n8n-videos/

# Tester FFmpeg manuellement
cd /tmp/n8n-videos
echo "file 'video_part_1.mp4'" > test_list.txt
echo "file 'video_part_2.mp4'" >> test_list.txt
ffmpeg -f concat -safe 0 -i test_list.txt -c copy test_output.mp4
```

## 📊 Exemple de Premier Workflow

Voici un exemple simple pour commencer :

1. **Sujet** : "3 astuces pour mieux dormir"
2. **Style** : Éducatif
3. **Durée** : 8 parties x 8 secondes = 64 secondes
4. **Format** : Vertical (9:16) pour TikTok
5. **Avatar** : Professionnel de la santé

### Script généré (exemple)
```
Partie 1: "Vous dormez mal ? Voici 3 astuces qui changent tout !"
Partie 2: "Astuce #1 : Évitez les écrans 1h avant de dormir"
Partie 3: "La lumière bleue perturbe votre mélatonine"
Partie 4: "Astuce #2 : Gardez votre chambre fraîche, entre 16-18°C"
Partie 5: "Le froid favorise l'endormissement naturel"
Partie 6: "Astuce #3 : Établissez une routine régulière"
Partie 7: "Couchez-vous et levez-vous à heures fixes"
Partie 8: "Suivez ces conseils et transformez vos nuits ! ✨"
```

## 🎯 Prochaines Étapes

Une fois votre première vidéo créée :

1. ✅ Tester différents sujets
2. ✅ Expérimenter avec les styles (humoristique, éducatif, etc.)
3. ✅ Ajouter des filigranes et musiques
4. ✅ Configurer la publication automatique
5. ✅ Planifier des créations quotidiennes

## 💡 Idées de Contenu pour Commencer

- **Motivation** : Citations inspirantes quotidiennes
- **Tips** : 5 astuces pour [X]
- **Éducation** : Le saviez-vous ?
- **Actualité** : Résumé de l'actualité du jour
- **Tutoriel** : Comment faire [X] en 60 secondes

## 📚 Ressources Utiles

- [Documentation complète](README.md)
- [Exemples de workflows](workflows/)
- [Scripts de compilation](scripts/)
- [Configuration avancée](config/)

## 🆘 Besoin d'aide ?

- Consulter la [documentation complète](README.md)
- Ouvrir une issue sur GitHub
- Rejoindre la communauté n8n

---

**Bravo ! Vous êtes prêt à créer vos premières vidéos automatisées ! 🎉**
