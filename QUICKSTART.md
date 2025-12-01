# 🚀 Guide de Démarrage Rapide

Ce guide vous permettra de lancer votre première vidéo automatisée en moins de 30 minutes.

## ⚡ Installation Rapide

### Option 1 : Installation locale (Recommandé pour débuter)

```bash
# 1. Cloner le projet
git clone https://github.com/votre-username/n8n-avatar-video-automation.git
cd n8n-avatar-video-automation

# 2. Installer n8n
npm install -g n8n

# 3. Installer FFmpeg
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# 4. Configurer les variables
cp .env.example .env
nano .env  # Éditer avec vos clés API

# 5. Créer les répertoires
mkdir -p /tmp/video_segments /tmp/final_videos

# 6. Démarrer n8n
n8n start
```

### Option 2 : Installation avec Docker (Recommandé pour production)

```bash
# 1. Cloner le projet
git clone https://github.com/votre-username/n8n-avatar-video-automation.git
cd n8n-avatar-video-automation

# 2. Configurer les variables
cp .env.example .env
nano .env  # Éditer avec vos clés API

# 3. Lancer avec Docker
docker-compose up -d

# 4. Vérifier que tout fonctionne
docker-compose logs -f n8n
```

## 🔑 Obtenir les Clés API (Étape Essentielle)

### 1. HeyGen (Avatar IA) - GRATUIT pour commencer

1. Allez sur https://www.heygen.com/
2. Créez un compte gratuit
3. Allez dans **Settings** > **API Keys**
4. Cliquez sur **Create API Key**
5. Copiez la clé dans votre `.env` :
   ```bash
   HEYGEN_API_KEY=votre_cle_heygen_ici
   ```

### 2. D-ID (Vidéos) - GRATUIT pour commencer

1. Allez sur https://www.d-id.com/
2. Créez un compte gratuit (20 crédits gratuits)
3. Allez dans **Settings** > **API Key**
4. Copiez la clé dans votre `.env` :
   ```bash
   DID_API_KEY=votre_cle_did_ici
   ```

### 3. OpenAI (Scripts GPT-4) - PAYANT mais peu coûteux

1. Allez sur https://platform.openai.com/
2. Créez un compte et ajoutez 5$ de crédit
3. Allez dans **API Keys** > **Create new secret key**
4. Copiez la clé dans votre `.env` :
   ```bash
   OPENAI_API_KEY=sk-votre_cle_openai_ici
   ```

### 4. Instagram (Optionnel au début)

**Configuration complète requise** - Vous pouvez commencer sans et ajouter plus tard.

Pour l'instant, laissez ces variables vides :
```bash
INSTAGRAM_ACCOUNT_ID=
INSTAGRAM_ACCESS_TOKEN=
```

Guide complet : https://developers.facebook.com/docs/instagram-api/getting-started

### 5. TikTok (Optionnel au début)

**API en beta** - Vous pouvez commencer sans et ajouter plus tard.

Pour l'instant, laissez ces variables vides :
```bash
TIKTOK_ACCESS_TOKEN=
```

Guide : https://developers.tiktok.com/

### 6. YouTube (Optionnel au début)

**Configuration OAuth requise** - Vous pouvez commencer sans et ajouter plus tard.

Pour l'instant, laissez ces variables vides :
```bash
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
```

Guide : https://developers.google.com/youtube/v3/getting-started

## 📥 Importer le Workflow

1. Ouvrez votre navigateur sur http://localhost:5678
2. Connectez-vous (si vous avez activé l'authentification)
3. Cliquez sur **Workflows** dans le menu
4. Cliquez sur **Import from File**
5. Sélectionnez `workflow-avatar-video-automation.json`
6. Cliquez sur **Import**

## ⚙️ Configuration Minimale pour Tester

Dans votre fichier `.env`, configurez AU MINIMUM ces variables :

```bash
# OBLIGATOIRE pour générer des vidéos
HEYGEN_API_KEY=votre_cle_heygen
DID_API_KEY=votre_cle_did
OPENAI_API_KEY=votre_cle_openai

# OPTIONNEL pour la voix (défaut = voix française féminine)
VOICE_ID=fr-FR-DeniseNeural

# OPTIONNEL pour les uploads (vous pouvez tester sans au début)
# INSTAGRAM_ACCOUNT_ID=
# INSTAGRAM_ACCESS_TOKEN=
# TIKTOK_ACCESS_TOKEN=
# YOUTUBE_CLIENT_ID=
# YOUTUBE_CLIENT_SECRET=
```

## 🎬 Lancer Votre Première Vidéo

### Test Simple (Sans Upload)

1. Dans n8n, ouvrez le workflow importé
2. Désactivez temporairement les nœuds d'upload :
   - Clic droit sur "Upload to Instagram" > **Deactivate**
   - Clic droit sur "Upload to TikTok" > **Deactivate**
   - Clic droit sur "Upload to YouTube" > **Deactivate**
3. Modifiez le nœud "Schedule Trigger" :
   ```json
   {
     "video_topic": "3 astuces pour être productif au quotidien",
     "style": "professional",
     "gender": "female"
   }
   ```
4. Cliquez sur **Execute Workflow**
5. Attendez 5-10 minutes (génération des vidéos)
6. Récupérez votre vidéo dans `/tmp/final_videos/final_video.mp4`

### Test Complet (Avec Upload)

Une fois que vous avez configuré les APIs de réseaux sociaux :

1. Réactivez les nœuds d'upload
2. Vérifiez que toutes les variables sont dans n8n :
   - **Settings** > **Environments**
   - Ajoutez toutes les variables du `.env`
3. Exécutez le workflow
4. Vérifiez que les vidéos sont publiées sur vos plateformes

## 🔍 Vérifier que Tout Fonctionne

### Test FFmpeg

```bash
ffmpeg -version
python3 video_compiler.py --help
```

Vous devriez voir les informations de version.

### Test de Compilation Manuelle

```bash
# Créer des vidéos de test
mkdir -p /tmp/video_segments
for i in {1..8}; do
  ffmpeg -f lavfi -i color=c=blue:s=1080x1920:d=8 \
    -vf "drawtext=text='Segment $i':fontsize=100:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
    /tmp/video_segments/segment_$i.mp4
done

# Compiler
python3 video_compiler.py

# Vérifier
ls -lh /tmp/final_videos/final_video.mp4
```

### Test des APIs

```bash
# Tester HeyGen
curl -X GET "https://api.heygen.com/v1/avatar.list" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# Tester D-ID
curl -X GET "https://api.d-id.com/talks" \
  -H "Authorization: Basic $DID_API_KEY"

# Tester OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## ⏰ Planifier l'Exécution Automatique

Par défaut, le workflow s'exécute tous les jours à 9h. Pour modifier :

1. Dans n8n, ouvrez le nœud **"Schedule Trigger"**
2. Modifiez l'expression cron :
   ```
   0 9 * * *     → Tous les jours à 9h
   0 */6 * * *   → Toutes les 6 heures
   0 9,14,20 * * * → 3 fois par jour (9h, 14h, 20h)
   ```

## 🎨 Personnaliser Vos Vidéos

### Changer le Sujet

Modifiez dans le nœud "Schedule Trigger" :
```json
{
  "video_topic": "Votre sujet ici"
}
```

### Changer l'Avatar

```json
{
  "gender": "male",  // ou "female"
  "age_range": "25-35",  // ou "18-25", "35-50", "50+"
  "style": "professional"  // ou "casual", "creative"
}
```

### Changer la Voix

Dans `.env` :
```bash
# Voix femme
VOICE_ID=fr-FR-DeniseNeural

# Voix homme
VOICE_ID=fr-FR-HenriNeural
```

Toutes les voix : https://speech.microsoft.com/portal/voicegallery

## 💡 Idées de Sujets de Vidéos

Consultez `video-topics-examples.md` pour des centaines d'idées de sujets !

Quelques exemples :
- "5 astuces pour être productif"
- "Comment apprendre une langue rapidement"
- "Les secrets d'une bonne routine matinale"
- "Erreurs à éviter en investissement"
- "Recette rapide : Pasta en 5 minutes"

## 🐛 Problèmes Courants

### "FFmpeg not found"
```bash
# Installer FFmpeg
sudo apt install ffmpeg  # Ubuntu
brew install ffmpeg      # macOS
```

### "API Key invalid"
- Vérifiez que vous avez copié la clé complète
- Vérifiez qu'il n'y a pas d'espaces avant/après
- Vérifiez que la clé n'a pas expiré

### "No credits remaining"
- Vérifiez votre compte D-ID/HeyGen
- Ajoutez des crédits ou passez à un plan payant

### "Vidéo corrompue"
- Attendez plus longtemps (la génération peut prendre 5-10 min)
- Vérifiez votre connexion Internet
- Testez avec un script plus court

## 📚 Prochaines Étapes

1. ✅ Configurez les uploads sur les réseaux sociaux
2. ✅ Testez différents sujets et styles
3. ✅ Ajoutez des transitions (`ADD_TRANSITIONS=true`)
4. ✅ Créez plusieurs workflows pour différents sujets
5. ✅ Analysez les performances de vos vidéos
6. ✅ Optimisez vos scripts pour plus d'engagement

## 💬 Besoin d'Aide ?

- 📖 Lisez le README complet : `README.md`
- 🐛 Signalez un bug : GitHub Issues
- 💡 Partagez vos idées : GitHub Discussions
- 📧 Contact : [votre email]

## 🎉 Félicitations !

Vous êtes maintenant prêt à créer des vidéos automatiquement ! 🚀

**Astuce** : Commencez petit, testez beaucoup, et améliorez progressivement votre workflow.
