# 📥 Comment Importer le Workflow dans n8n

Ce guide vous explique comment importer et configurer le workflow d'automatisation vidéo avec avatar IA.

## 🚀 Importation Rapide

### Méthode 1 : Copier-Coller (Recommandé)

1. **Ouvrir le fichier JSON**
   - Ouvrir le fichier `avatar-video-automation.json` dans un éditeur de texte
   - Sélectionner TOUT le contenu (Ctrl+A ou Cmd+A)
   - Copier (Ctrl+C ou Cmd+C)

2. **Dans n8n**
   - Ouvrir n8n dans votre navigateur
   - Cliquer sur **"Workflows"** dans le menu
   - Cliquer sur le bouton **"+"** pour créer un nouveau workflow
   - Cliquer sur les **3 petits points** en haut à droite
   - Sélectionner **"Import from File"**
   - Coller le JSON (Ctrl+V ou Cmd+V)
   - Cliquer sur **"Import"**

### Méthode 2 : Import via Fichier

1. **Télécharger le fichier**
   - Télécharger `avatar-video-automation.json`

2. **Dans n8n**
   - Aller dans **Workflows**
   - Cliquer sur **"Import from File"**
   - Sélectionner le fichier JSON téléchargé
   - Cliquer sur **"Import"**

## 📋 Le Workflow Contient

### ✅ Nœuds de Workflow (16 nœuds)
- **Schedule Trigger** - Déclenchement automatique
- **Generate Video Script** - Génération du script IA
- **Create AI Avatar** - Création de l'avatar initial
- **Set Variables** - Stockage des variables
- **Split Into Parts** - Division en 8 parties
- **Generate Video Part** - Génération de chaque vidéo
- **Wait for Processing** - Attente du traitement
- **Check Video Status** - Vérification du statut
- **Download Video Part** - Téléchargement des vidéos
- **Add to File List** - Ajout à la liste de compilation
- **All Parts Done?** - Vérification de fin
- **Compile Videos with FFmpeg** - Compilation finale
- **Upload to YouTube** - Publication YouTube
- **Upload to Instagram** - Publication Instagram
- **Upload to TikTok** - Publication TikTok
- **Merge Upload Results** - Fusion des résultats
- **Cleanup Temp Files** - Nettoyage

### 📝 Notes Explicatives (8 notes)
Chaque note contient :
- 🎯 **Note Principale** - Vue d'ensemble complète avec tous les liens API
- 📌 **Notes par section** - Explications détaillées de chaque étape
- 🔗 **Liens directs** - Vers toutes les API nécessaires
- ⚙️ **Configuration** - Instructions de setup
- 💡 **Astuces** - Conseils de personnalisation

## 🔑 Configuration des API Nécessaires

Après l'import, vous devez configurer les credentials :

### 1️⃣ D-ID API (OBLIGATOIRE)

**Obtenir l'API Key :**
1. Aller sur https://www.d-id.com/
2. Créer un compte (gratuit avec 20 crédits)
3. Aller dans **Settings** → **API Keys**
4. Copier votre API Key

**Configurer dans n8n :**
1. Cliquer sur le nœud **"Create AI Avatar"**
2. Dans **Credentials**, cliquer sur **"Create New"**
3. Choisir **"Header Auth"**
4. Remplir :
   - **Name** : `D-ID API Key`
   - **Header Name** : `Authorization`
   - **Header Value** : `Basic VOTRE_API_KEY`
5. Cliquer sur **"Save"**

Répéter pour le nœud **"Generate Video Part"**

### 2️⃣ OpenAI API (OBLIGATOIRE)

**Obtenir l'API Key :**
1. Aller sur https://platform.openai.com/
2. Créer un compte
3. Aller dans **API Keys**
4. Cliquer sur **"Create new secret key"**
5. Copier la clé (vous ne pourrez plus la voir après !)

**Configurer dans n8n :**
1. Cliquer sur le nœud **"Generate Video Script"**
2. Dans **Credentials**, cliquer sur **"Create New"**
3. Choisir **"OpenAI API"**
4. Remplir :
   - **Name** : `OpenAI API`
   - **API Key** : `sk-VOTRE_CLE`
5. Cliquer sur **"Save"**

### 3️⃣ YouTube API (OPTIONNEL)

**Configuration :**
1. Aller sur https://console.cloud.google.com/
2. Créer un projet
3. Activer **YouTube Data API v3**
4. Créer des credentials OAuth 2.0
5. Télécharger le fichier JSON des credentials

**Configurer dans n8n :**
1. Cliquer sur le nœud **"Upload to YouTube"**
2. Suivre les instructions OAuth 2.0
3. Autoriser l'accès à votre chaîne YouTube

### 4️⃣ Instagram API (OPTIONNEL)

**Configuration :**
1. Aller sur https://developers.facebook.com/
2. Créer une app Facebook
3. Ajouter **Instagram Graph API**
4. Obtenir un User Access Token
5. Lier votre compte Instagram Business

**Configurer dans n8n :**
1. Cliquer sur le nœud **"Upload to Instagram"**
2. Configurer les credentials Instagram

### 5️⃣ TikTok API (OPTIONNEL)

**Configuration :**
1. Aller sur https://developers.tiktok.com/
2. S'inscrire comme développeur
3. Créer une application
4. Obtenir Client Key et Client Secret
5. Générer un Access Token via OAuth 2.0

**Configurer dans n8n :**
1. Cliquer sur le nœud **"Upload to TikTok"**
2. Configurer les credentials TikTok

## ⚙️ Configuration Système

### Installer FFmpeg

**Ubuntu/Debian :**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS :**
```bash
brew install ffmpeg
```

**Windows :**
Télécharger depuis https://ffmpeg.org/download.html

### Créer le Dossier Temporaire

```bash
mkdir -p /tmp/n8n-videos
chmod 777 /tmp/n8n-videos
```

## 🎮 Utilisation

### Première Exécution

1. **Vérifier les Credentials**
   - Tous les nœuds avec une icône ⚠️ doivent être configurés
   - Vérifier que toutes les API keys sont correctes

2. **Personnaliser le Sujet**
   - Modifier le nœud **"Schedule Trigger"**
   - Ou ajouter un JSON d'input :
   ```json
   {
     "topic": "5 astuces pour mieux dormir"
   }
   ```

3. **Tester le Workflow**
   - Désactiver les nœuds de publication (YouTube, Instagram, TikTok)
   - Cliquer sur **"Execute Workflow"**
   - Vérifier que tout fonctionne jusqu'à la compilation

4. **Activer la Publication**
   - Une fois le test réussi, réactiver les nœuds de publication
   - Exécuter à nouveau

### Exécution Automatique

1. **Activer le Schedule**
   - Modifier l'interval dans **"Schedule Trigger"**
   - Activer le workflow (bouton ON/OFF en haut)

2. **Surveiller les Exécutions**
   - Aller dans **"Executions"**
   - Vérifier les logs en cas d'erreur

## 📊 Comprendre les Notes Visuelles

Une fois importé, vous verrez 8 grandes notes jaunes dans le workflow :

### 🎬 Note Principale (en haut à gauche)
- **Position** : Début du workflow
- **Contenu** : Vue d'ensemble complète, tous les liens API, coûts, temps
- **Utilité** : Guide de référence rapide

### 📌 Notes par Section
Chaque section du workflow a sa propre note explicative :

1. **🎯 Déclencheur** - Comment personnaliser le trigger
2. **📝 Script IA** - Configuration OpenAI et format de sortie
3. **🎭 Avatar** - Setup D-ID et paramètres de l'avatar
4. **💾 Variables** - Données stockées pour réutilisation
5. **🔄 Boucle** - Processus de génération des 8 vidéos
6. **🎞️ Compilation** - Commandes FFmpeg et prérequis
7. **📱 Publication** - Configuration détaillée des 3 plateformes
8. **✅ Finalisation** - Nettoyage et merge des résultats

## 🎨 Personnalisation

### Changer le Nombre de Parties

1. **Modifier le Prompt** (Generate Video Script)
   - Changer "8 parties" par le nombre désiré

2. **Ajuster la Durée**
   - Si vous voulez 10 parties de 6 secondes au lieu de 8x8s

### Changer le Style de Contenu

Modifier le prompt dans **"Generate Video Script"** :
```
Style : humoristique (au lieu de motivationnel)
Ton : casual (au lieu de énergique)
Public : jeunes (au lieu de adultes)
```

### Ajouter un Filigrane

Modifier le nœud **"Compile Videos with FFmpeg"** :
```bash
ffmpeg -f concat -safe 0 -i filelist.txt \
  -vf "drawtext=text='@VotreChannel':fontsize=24:fontcolor=white@0.7:x=10:y=H-th-10" \
  -c:a copy final_video.mp4
```

## 🔧 Résolution de Problèmes

### Erreur : "Credentials not found"
➡️ Configurer toutes les API keys dans les credentials

### Erreur : "FFmpeg command not found"
➡️ Installer FFmpeg sur le serveur :
```bash
sudo apt-get install ffmpeg
```

### Erreur : "Permission denied /tmp/n8n-videos"
➡️ Créer le dossier avec les bonnes permissions :
```bash
sudo mkdir -p /tmp/n8n-videos
sudo chmod 777 /tmp/n8n-videos
```

### Vidéos non compilées
➡️ Vérifier que les 8 vidéos sont bien téléchargées :
```bash
ls -la /tmp/n8n-videos/
```

### D-ID rate limit
➡️ Augmenter le temps d'attente dans **"Wait for Processing"** (30s → 60s)

### Publication échouée
➡️ Vérifier :
- Les tokens ne sont pas expirés
- Les limites quotidiennes ne sont pas atteintes
- Le format vidéo est compatible avec la plateforme

## 💡 Conseils d'Utilisation

### Pour Débuter
1. Commencer avec D-ID + OpenAI seulement
2. Désactiver les nœuds de publication
3. Tester la génération et compilation
4. Vérifier les vidéos manuellement
5. Activer la publication progressivement (YouTube → Instagram → TikTok)

### Pour Optimiser
1. Ajuster le temps d'attente selon vos besoins
2. Personnaliser les hashtags par plateforme
3. Créer plusieurs versions du workflow pour différents contenus
4. Utiliser des variables d'environnement pour les credentials

### Pour Scaler
1. Utiliser un webhook au lieu du schedule trigger
2. Intégrer avec un système de gestion de contenu
3. Ajouter des analytics pour tracker les performances
4. Créer des variations A/B testing

## 📚 Ressources Complémentaires

- **Documentation n8n** : https://docs.n8n.io/
- **D-ID Docs** : https://docs.d-id.com/
- **OpenAI Docs** : https://platform.openai.com/docs
- **FFmpeg Guide** : https://ffmpeg.org/ffmpeg.html
- **README du projet** : ../README.md
- **Guide de démarrage rapide** : ../QUICKSTART.md

## ❓ Support

Si vous rencontrez des problèmes :
1. Consulter les notes visuelles dans le workflow
2. Vérifier la section **Résolution de Problèmes** ci-dessus
3. Consulter le README principal
4. Ouvrir une issue sur GitHub

---

**Bon développement avec n8n ! 🎉**
