# 🎥 Automatisation n8n - Génération de Vidéos avec Avatar IA

Automatisation complète pour générer des avatars IA et créer des vidéos compilées pour TikTok, Instagram et YouTube.

## 📋 Description

Cette automatisation n8n permet de :
- ✨ Générer un avatar IA personnalisé
- 🎬 Créer 8 vidéos de 8 secondes avec cet avatar
- 🔗 Compiler automatiquement les 8 vidéos en une seule (64 secondes)
- 📱 Publier sur TikTok, Instagram Reels et YouTube Shorts/Videos
- 🤖 Tout automatiser de bout en bout

## 🏗️ Architecture

```
┌─────────────────┐
│  Trigger n8n    │ (Manuel ou Programmé)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Génération de   │ (OpenAI/Claude)
│    Script       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Création Avatar │ (D-ID/HeyGen)
│      IA         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Génération de  │ (8 vidéos x 8s)
│   8 Vidéos      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Compilation    │ (FFmpeg)
│    Vidéo        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Publication    │ (TikTok/IG/YT)
│   Multi-Canal   │
└─────────────────┘
```

## 🚀 Installation

### Prérequis

1. **n8n** installé (self-hosted ou cloud)
2. **FFmpeg** installé sur le serveur
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg

   # macOS
   brew install ffmpeg

   # Windows
   # Télécharger depuis https://ffmpeg.org/download.html
   ```

3. **Node.js** (v16 ou supérieur)
4. **Python 3** (optionnel, pour le script Python)

### Installation du Projet

1. Cloner le repository :
   ```bash
   git clone <votre-repo>
   cd David
   ```

2. Créer le dossier temporaire pour les vidéos :
   ```bash
   mkdir -p /tmp/n8n-videos
   ```

3. Rendre les scripts exécutables :
   ```bash
   chmod +x scripts/compile_videos.py
   chmod +x scripts/compile_videos.js
   ```

4. Installer les dépendances Node.js (optionnel) :
   ```bash
   npm install
   ```

## 🔑 Configuration des API

### 1. D-ID (Génération d'avatars vidéo)

- Créer un compte sur [D-ID](https://www.d-id.com/)
- Obtenir votre API Key
- Alternative : [HeyGen](https://www.heygen.com/), [Synthesia](https://www.synthesia.io/)

### 2. OpenAI (Génération de scripts)

- Créer un compte sur [OpenAI](https://platform.openai.com/)
- Obtenir votre API Key
- Alternative : Claude API, Mistral AI

### 3. TikTok

- S'inscrire au [TikTok for Developers](https://developers.tiktok.com/)
- Créer une application
- Obtenir les credentials OAuth 2.0

### 4. Instagram

- Créer une [App Facebook](https://developers.facebook.com/)
- Activer Instagram Graph API
- Obtenir les tokens d'accès

### 5. YouTube

- Créer un projet sur [Google Cloud Console](https://console.cloud.google.com/)
- Activer YouTube Data API v3
- Configurer OAuth 2.0

## 📝 Configuration n8n

### Importer le Workflow

1. Ouvrir n8n
2. Aller dans **Workflows** → **Import from File**
3. Sélectionner `workflows/avatar-video-automation.json`
4. Configurer les credentials

### Configurer les Credentials

#### D-ID API
```
Type: Header Auth
Header Name: Authorization
Header Value: Basic <VOTRE_API_KEY>
```

#### OpenAI API
```
Type: OpenAI
API Key: sk-...
```

#### YouTube OAuth2
```
Type: OAuth2
Client ID: <VOTRE_CLIENT_ID>
Client Secret: <VOTRE_CLIENT_SECRET>
Scopes: https://www.googleapis.com/auth/youtube.upload
```

#### Instagram API
```
Type: Generic OAuth2
Access Token URL: https://api.instagram.com/oauth/access_token
Client ID: <VOTRE_APP_ID>
Client Secret: <VOTRE_APP_SECRET>
```

#### TikTok API
```
Type: Header Auth
Header Name: Authorization
Header Value: Bearer <VOTRE_ACCESS_TOKEN>
```

## 🎮 Utilisation

### Méthode 1 : Via n8n (Recommandé)

1. Ouvrir le workflow dans n8n
2. Cliquer sur "Execute Workflow"
3. Le workflow va :
   - Générer un script vidéo en 8 parties
   - Créer un avatar IA
   - Générer 8 vidéos de 8 secondes
   - Les compiler en une seule vidéo
   - Publier sur les 3 plateformes

### Méthode 2 : Scripts Standalone

#### Script Node.js
```bash
node scripts/compile_videos.js /tmp/n8n-videos /tmp/final_video.mp4 --platform tiktok --watermark "Mon Channel"
```

Options disponibles :
- `--platform` : tiktok, instagram, youtube_shorts, youtube
- `--watermark` : Texte du filigrane
- `--intro` : Chemin vers vidéo d'intro
- `--outro` : Chemin vers vidéo d'outro
- `--music` : Chemin vers musique de fond
- `--music-volume` : Volume de la musique (0-1)

#### Script Python
```bash
python scripts/compile_videos.py /tmp/n8n-videos /tmp/final_video.mp4 --platform tiktok
```

## 🎨 Personnalisation

### Modifier le Prompt de Génération de Script

Éditer le node "Generate Video Script" dans n8n :

```
Génère un script vidéo viral sur [VOTRE_SUJET] divisé en 8 parties de 8 secondes.

Style : [humoristique / éducatif / motivationnel]
Ton : [casual / professionnel / énergique]
Public cible : [jeunes / adultes / professionnels]

Chaque partie doit :
- Être engageante et captivante
- Se terminer par un hook pour la partie suivante
- Utiliser des mots simples et percutants

Format JSON:
{
  "avatar_description": "description détaillée de l'avatar",
  "parts": [
    {"part": 1, "duration": 8, "text": "script partie 1"},
    ...
  ]
}
```

### Personnaliser l'Avatar

Dans le node "Create AI Avatar", modifier :
- `source_url` : URL de l'image de base pour l'avatar
- `config.driver_expressions` : Expressions faciales (happy, sad, surprised, neutral)
- `config.stitch` : Activer/désactiver le stitching automatique

### Optimisation par Plateforme

Les configurations sont dans `scripts/compile_videos.js` :

```javascript
const PLATFORM_CONFIGS = {
  tiktok: {
    size: '1080:1920',      // Format vertical
    bitrate: '3000k',       // Qualité
    fps: 30                 // Images par seconde
  },
  instagram: {
    size: '1080:1920',
    bitrate: '3500k',
    fps: 30
  },
  youtube_shorts: {
    size: '1080:1920',
    bitrate: '5000k',
    fps: 60
  }
}
```

## 🔧 Résolution de Problèmes

### Erreur : "FFmpeg not found"
```bash
# Vérifier l'installation
ffmpeg -version

# Si non installé
sudo apt-get install ffmpeg
```

### Erreur : "D-ID API rate limit"
- D-ID a des limites de requêtes
- Ajouter des nodes "Wait" entre les générations
- Passer à un plan supérieur

### Vidéos non compilées
```bash
# Vérifier les permissions
chmod 777 /tmp/n8n-videos

# Vérifier les fichiers
ls -la /tmp/n8n-videos/

# Tester manuellement
cd /tmp/n8n-videos
ffmpeg -f concat -safe 0 -i filelist.txt -c copy test_output.mp4
```

### Publication échouée sur TikTok/Instagram
- Vérifier que les vidéos respectent les formats requis
- Vérifier les tokens d'API (expiration)
- Vérifier les limites de publication quotidienne

## 📊 Limitations

### D-ID
- Limite gratuite : 20 crédits/mois
- Limite payante : selon le plan
- Temps de génération : ~30 secondes par vidéo

### TikTok
- Format : 9:16 (vertical)
- Durée max : 10 minutes
- Taille max : 287.6 MB
- Formats : MP4, MOV

### Instagram Reels
- Format : 9:16 (vertical)
- Durée : 15-90 secondes
- Taille max : 4 GB
- Formats : MP4, MOV

### YouTube Shorts
- Format : 9:16 (vertical)
- Durée max : 60 secondes
- Taille max : 256 GB
- Formats : MP4, MOV, AVI, etc.

## 🎯 Cas d'Usage

### 1. Vidéos Motivationnelles
```javascript
topic: "Citation motivationnelle du jour"
style: "énergique et inspirant"
avatar: "Coach professionnel"
```

### 2. Tips & Astuces
```javascript
topic: "5 astuces pour augmenter sa productivité"
style: "éducatif et concis"
avatar: "Expert en productivité"
```

### 3. Actualités
```javascript
topic: "Résumé de l'actualité tech de la semaine"
style: "informatif et dynamique"
avatar: "Journaliste tech"
```

### 4. Tutoriels
```javascript
topic: "Comment utiliser n8n pour automatiser"
style: "pédagogique et clair"
avatar: "Instructeur technique"
```

## 🚀 Améliorations Futures

- [ ] Génération automatique de miniatures
- [ ] Ajout de sous-titres automatiques (Whisper API)
- [ ] Intégration avec Stable Diffusion pour avatars custom
- [ ] Support de Telegram, LinkedIn, Twitter
- [ ] Analytics et tracking des performances
- [ ] A/B testing de différents styles
- [ ] Génération de hashtags optimisés
- [ ] Planification de contenu sur plusieurs jours
- [ ] Intégration avec banques de musiques libres de droits
- [ ] Génération de voix IA multilingue

## 📚 Ressources

### Documentation
- [n8n Documentation](https://docs.n8n.io/)
- [D-ID API Docs](https://docs.d-id.com/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [TikTok API Docs](https://developers.tiktok.com/doc)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [YouTube Data API](https://developers.google.com/youtube/v3)

### Alternatives aux Services

#### Génération d'Avatars
- [HeyGen](https://www.heygen.com/) - Avatars IA réalistes
- [Synthesia](https://www.synthesia.io/) - Avatars professionnels
- [Colossyan](https://www.colossyan.com/) - Avatars multilingues
- [Pictory](https://pictory.ai/) - Conversion texte vers vidéo

#### Génération de Scripts
- [Claude](https://claude.ai/) - Excellent pour le contenu créatif
- [GPT-4](https://openai.com/) - Polyvalent
- [Mistral](https://mistral.ai/) - Open source

#### Édition Vidéo
- [Runway ML](https://runwayml.com/) - IA générative
- [Descript](https://www.descript.com/) - Édition par texte
- [Kapwing](https://www.kapwing.com/) - En ligne

## 💰 Coûts Estimés

### Configuration Minimale (100 vidéos/mois)
- D-ID : ~$50/mois
- OpenAI : ~$20/mois
- Serveur n8n : Gratuit (self-hosted) ou $20/mois (cloud)
- **Total : ~$70-90/mois**

### Configuration Professionnelle (1000 vidéos/mois)
- D-ID : ~$300/mois
- OpenAI : ~$100/mois
- Serveur n8n : $50/mois (cloud avec plus de ressources)
- **Total : ~$450/mois**

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir des issues pour signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## ⚠️ Avertissements

- Respectez les conditions d'utilisation de chaque plateforme
- Vérifiez les droits d'auteur des contenus générés
- Les avatars IA doivent être utilisés de manière éthique
- Certaines plateformes limitent le contenu généré par IA
- Testez toujours avant de publier massivement

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue GitHub
- Consulter la documentation
- Rejoindre la communauté n8n

---

**Fait avec ❤️ pour automatiser la création de contenu vidéo**
