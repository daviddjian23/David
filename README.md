# 🎥 Automatisation n8n - Génération de Vidéos avec Avatar IA

Une automatisation complète n8n qui génère un avatar IA, crée des vidéos courtes, et les publie automatiquement sur TikTok, Instagram Reels et YouTube Shorts.

## 🌟 Fonctionnalités

- ✅ **Génération d'avatar IA** personnalisé avec HeyGen ou alternatives
- ✅ **Création de scripts** optimisés pour vidéos courtes via GPT-4
- ✅ **Génération de 8 vidéos** de 8 secondes chacune avec D-ID
- ✅ **Compilation automatique** des 8 segments en une vidéo de 64 secondes
- ✅ **Publication multi-plateforme** sur TikTok, Instagram et YouTube
- ✅ **Planification automatique** avec cron
- ✅ **Transitions fluides** entre les segments (optionnel)

## 📋 Prérequis

### Logiciels requis

- **n8n** (version 1.0+)
- **Python 3.8+**
- **FFmpeg** (pour la compilation vidéo)
- **Node.js** 18+ (pour n8n)

### Installation des dépendances système

#### Sur Ubuntu/Debian
```bash
# Installer FFmpeg
sudo apt update
sudo apt install ffmpeg

# Installer Python 3 et pip
sudo apt install python3 python3-pip

# Installer n8n globalement
npm install -g n8n
```

#### Sur macOS
```bash
# Installer FFmpeg
brew install ffmpeg

# Installer Python 3
brew install python3

# Installer n8n
npm install -g n8n
```

#### Sur Windows
```powershell
# Installer FFmpeg via Chocolatey
choco install ffmpeg

# Installer Python 3
choco install python

# Installer n8n
npm install -g n8n
```

### Comptes API nécessaires

Vous aurez besoin de créer des comptes et obtenir des clés API pour :

1. **HeyGen** - Génération d'avatars IA
   - Site : https://www.heygen.com/
   - Plan gratuit : 1 crédit/mois
   - Plan payant : À partir de 24$/mois

2. **D-ID** - Génération de vidéos avec avatars parlants
   - Site : https://www.d-id.com/
   - Plan gratuit : 20 crédits/mois
   - Plan payant : À partir de 4.70$/mois

3. **OpenAI** - Génération de scripts avec GPT-4
   - Site : https://platform.openai.com/
   - Tarification : Pay-as-you-go (~0.03$/requête)

4. **Instagram/Facebook** - Publication sur Instagram Reels
   - Guide : https://developers.facebook.com/docs/instagram-api
   - Gratuit (compte Business requis)

5. **TikTok for Developers** - Publication sur TikTok
   - Site : https://developers.tiktok.com/
   - Gratuit (en beta)

6. **YouTube Data API** - Publication sur YouTube Shorts
   - Console : https://console.developers.google.com/
   - Gratuit (quotas généreux)

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/n8n-avatar-video-automation.git
cd n8n-avatar-video-automation
```

### 2. Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec vos clés API
nano .env
```

Remplissez toutes les clés API nécessaires dans le fichier `.env`.

### 3. Rendre le script Python exécutable

```bash
chmod +x video_compiler.py
```

### 4. Créer les répertoires de travail

```bash
mkdir -p /tmp/video_segments
mkdir -p /tmp/final_videos
```

### 5. Importer le workflow dans n8n

```bash
# Démarrer n8n
n8n start

# Ouvrir votre navigateur sur http://localhost:5678
# Aller dans Workflows > Import from File
# Sélectionner le fichier workflow-avatar-video-automation.json
```

### 6. Configurer les credentials dans n8n

Dans n8n, configurez les credentials suivants :

#### YouTube OAuth2
1. Allez dans **Settings** > **Credentials** > **Add Credential**
2. Sélectionnez **YouTube OAuth2 API**
3. Entrez vos Client ID et Client Secret
4. Cliquez sur **Connect my account** et autorisez

#### Variables d'environnement
1. Dans n8n, allez dans **Settings** > **Environments**
2. Ajoutez toutes les variables du fichier `.env`

## 📖 Utilisation

### Lancer l'automatisation manuellement

1. Ouvrez votre workflow dans n8n
2. Cliquez sur **Execute Workflow**
3. Le workflow va :
   - Générer un avatar IA
   - Créer 8 scripts de 8 secondes
   - Générer 8 vidéos
   - Compiler les vidéos
   - Publier sur les 3 plateformes

### Planification automatique

Le workflow est configuré pour s'exécuter automatiquement :
- **Par défaut** : Tous les jours à 9h (modifiable dans le nœud "Schedule Trigger")
- **Personnalisable** : Modifiez la variable `SCHEDULE_CRON` dans `.env`

Exemples de planning :
```bash
# Toutes les 6 heures
SCHEDULE_CRON="0 */6 * * *"

# Du lundi au vendredi à 9h
SCHEDULE_CRON="0 9 * * 1-5"

# 3 fois par jour (9h, 14h, 20h)
SCHEDULE_CRON="0 9,14,20 * * *"
```

### Personnaliser les vidéos

Vous pouvez personnaliser plusieurs aspects :

#### 1. Changer le sujet de la vidéo
Modifiez la variable dans le nœud "Schedule Trigger" :
```json
{
  "video_topic": "5 astuces pour être productif",
  "style": "professional",
  "gender": "female",
  "age_range": "25-35"
}
```

#### 2. Changer la voix
Dans `.env`, modifiez :
```bash
VOICE_ID=fr-FR-HenriNeural  # Pour une voix masculine
```

Voix françaises disponibles :
- `fr-FR-DeniseNeural` - Femme, standard
- `fr-FR-HenriNeural` - Homme, standard
- `fr-FR-BrigitteNeural` - Femme, premium
- `fr-FR-AlainNeural` - Homme, premium

#### 3. Ajouter des transitions
Pour des transitions fluides entre les segments :
```bash
# Dans .env
ADD_TRANSITIONS=true

# Ou en ligne de commande
python3 video_compiler.py --transitions
```

## 🛠️ Utilisation du script de compilation

Le script `video_compiler.py` peut être utilisé indépendamment :

```bash
# Compilation simple
python3 video_compiler.py

# Avec transitions
python3 video_compiler.py --transitions

# Avec nettoyage des segments
python3 video_compiler.py --cleanup

# Personnaliser les chemins
python3 video_compiler.py \
  --input-dir /chemin/vers/segments \
  --output-dir /chemin/vers/sortie \
  --output-name ma_video.mp4

# Afficher les informations de la vidéo
python3 video_compiler.py --info

# Aide complète
python3 video_compiler.py --help
```

## 🔧 Architecture du workflow

```
┌─────────────────────┐
│  Schedule Trigger   │  Déclenche l'automatisation
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────────┐ ┌─▼──────────────┐
│ Generate   │ │ Generate       │
│ AI Avatar  │ │ Scripts (GPT)  │
└───┬────────┘ └─┬──────────────┘
    │            │
    └─────┬──────┘
          │
┌─────────▼──────────┐
│ Create 8 Segments  │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ Loop Through       │  Boucle 8 fois
│ 8 Segments         │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ Generate Video     │  D-ID API
│ Segment (8sec)     │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ Wait & Check       │  Attendre génération
│ Status             │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ Download & Save    │  Sauvegarder segment
│ Segment            │
└─────────┬──────────┘
          │
    [Répéter 8 fois]
          │
┌─────────▼──────────┐
│ Compile 8 Videos   │  FFmpeg
│ (64 secondes)      │
└─────────┬──────────┘
          │
    ┌─────┴─────┬─────────────┐
    │           │             │
┌───▼────┐ ┌────▼────┐ ┌─────▼────┐
│ TikTok │ │Instagram│ │ YouTube  │
└────────┘ └─────────┘ └──────────┘
```

## 📊 Spécifications techniques

### Vidéos générées

- **Format** : MP4 (H.264)
- **Résolution** : 1080x1920 (format vertical pour Reels/Shorts/TikTok)
- **Durée totale** : 64 secondes (8 segments de 8 secondes)
- **Framerate** : 30 FPS
- **Audio** : AAC, 192 kbps

### Limites des plateformes

| Plateforme | Durée max | Résolution recommandée | Format |
|-----------|-----------|----------------------|--------|
| TikTok    | 10 min    | 1080x1920           | MP4    |
| Instagram | 90 sec    | 1080x1920           | MP4    |
| YouTube   | 60 sec    | 1080x1920           | MP4    |

**Note** : La vidéo de 64 secondes dépasse la limite de YouTube Shorts (60 sec). Vous pouvez :
1. Réduire à 7 segments (56 secondes)
2. Publier sur YouTube comme vidéo normale (pas Short)
3. Créer deux workflows : un pour TikTok/Instagram (8 segments) et un pour YouTube (7 segments)

## 🔐 Sécurité

### Bonnes pratiques

1. **Ne jamais committer le fichier `.env`** avec vos clés API
2. **Utiliser des variables d'environnement** dans n8n (Settings > Environments)
3. **Limiter les permissions** des tokens API au strict nécessaire
4. **Activer l'authentification** sur votre instance n8n
5. **Utiliser HTTPS** si vous exposez n8n sur Internet

### Protection des clés API

```bash
# Ajouter .env au .gitignore
echo ".env" >> .gitignore

# Vérifier que .env n'est pas tracké
git status
```

## 🐛 Dépannage

### Problème : FFmpeg non trouvé

```bash
# Vérifier l'installation
ffmpeg -version

# Si non installé
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

### Problème : Erreur D-ID "Avatar not ready"

La génération d'avatar peut prendre 2-5 minutes. Le workflow attend automatiquement.

Si l'erreur persiste :
1. Vérifiez votre crédit D-ID
2. Vérifiez la qualité de l'image source
3. Augmentez le temps d'attente dans le nœud "Wait for Video Generation"

### Problème : Upload Instagram échoue

Instagram requiert :
1. Un compte **Business** ou **Creator**
2. Une **page Facebook** liée
3. Le **Graph API** configuré

Suivez le guide : https://developers.facebook.com/docs/instagram-api/getting-started

### Problème : Vidéo corrompue après compilation

```bash
# Tester la compilation manuellement
python3 video_compiler.py --info

# Vérifier les segments individuels
ffprobe /tmp/video_segments/segment_1.mp4
```

Si les segments sont corrompus :
1. Vérifiez votre crédit D-ID
2. Réduisez la qualité vidéo dans les paramètres D-ID
3. Augmentez le temps d'attente

### Problème : Scripts GPT-4 trop longs/courts

Ajustez le prompt dans le nœud "Generate Scripts with GPT-4" :

```json
{
  "role": "system",
  "content": "Tu es un expert en création de scripts pour des vidéos courtes. Crée 8 segments de script, chacun devant contenir EXACTEMENT 20-25 mots pour durer 8 secondes quand lu à voix normale. Chaque segment doit être engageant et se connecter naturellement au suivant."
}
```

## 📈 Optimisations

### Réduire les coûts

1. **Réutiliser l'avatar** : Sauvegardez l'URL de l'avatar et réutilisez-le au lieu d'en générer un nouveau à chaque fois
2. **Batch processing** : Générez plusieurs vidéos en une seule exécution
3. **Utiliser des alternatives** : Testez des APIs moins chères (Synthesia trials, etc.)

### Améliorer la qualité

1. **Transitions fluides** : Activez `ADD_TRANSITIONS=true`
2. **Voix premium** : Utilisez ElevenLabs pour des voix ultra-réalistes
3. **Scripts optimisés** : Fournissez des exemples de scripts réussis à GPT-4
4. **Post-processing** : Ajoutez des sous-titres, musique de fond, effets

### Scalabilité

1. **Multiple topics** : Créez plusieurs workflows pour différents sujets
2. **A/B Testing** : Testez différents styles d'avatars et voix
3. **Analytics** : Intégrez l'API Analytics de chaque plateforme
4. **Stockage cloud** : Sauvegardez les vidéos sur S3/GCS pour archivage

## 🤝 Alternatives et intégrations

### Alternatives aux services

| Service | Alternative 1 | Alternative 2 | Alternative 3 |
|---------|--------------|--------------|--------------|
| HeyGen | Ready Player Me | Synthesia | Runway ML |
| D-ID | Synthesia | Runway ML | Pictory |
| GPT-4 | Claude (Anthropic) | Gemini (Google) | Llama 3 |
| ElevenLabs | Azure TTS | Google TTS | Amazon Polly |

### Intégrations possibles

- **Webhook** pour notifications (Slack, Discord, Email)
- **Analytics** pour suivre les performances
- **CMS** pour gérer les sujets de vidéos
- **Database** pour stocker l'historique
- **Zapier/Make** pour automatisations supplémentaires

## 📝 Roadmap

- [ ] Support pour vidéos horizontales (YouTube classique)
- [ ] Sous-titres automatiques
- [ ] Musique de fond
- [ ] Effets visuels et transitions avancées
- [ ] Interface web pour gérer les vidéos
- [ ] Dashboard analytics
- [ ] Support multi-langues
- [ ] Templates de vidéos prédéfinis
- [ ] A/B testing automatique

## 📄 Licence

MIT License - Vous êtes libre d'utiliser, modifier et distribuer ce projet.

## 🙏 Remerciements

- [n8n](https://n8n.io/) - Plateforme d'automatisation
- [HeyGen](https://www.heygen.com/) - Génération d'avatars IA
- [D-ID](https://www.d-id.com/) - Vidéos avec avatars parlants
- [OpenAI](https://openai.com/) - GPT-4 pour les scripts
- [FFmpeg](https://ffmpeg.org/) - Compilation vidéo

## 📧 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation n8n : https://docs.n8n.io/
- Rejoignez la communauté n8n : https://community.n8n.io/

## ⚠️ Avertissements

1. **Coûts API** : Les services d'IA peuvent devenir coûteux. Surveillez votre utilisation.
2. **Quotas** : Respectez les limites de taux des APIs.
3. **Droits d'auteur** : Assurez-vous d'avoir les droits sur le contenu généré.
4. **Règles des plateformes** : Respectez les guidelines de TikTok, Instagram et YouTube.
5. **RGPD** : Si vous collectez des données, conformez-vous au RGPD.

---

**Créé avec ❤️ pour automatiser la création de contenu vidéo**
