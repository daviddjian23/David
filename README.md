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

## 📋 Workflow n8n - JSON Complet à Copier-Coller

Voici le workflow n8n complet avec toutes les notes explicatives. **Copier-coller ce JSON directement dans n8n** :

### 🚀 Comment Importer

1. **Sélectionner tout le JSON ci-dessous** (Ctrl+A dans le bloc de code)
2. **Copier** (Ctrl+C)
3. **Ouvrir n8n**
4. **Workflows** → **Import from File** → **Paste JSON**
5. **Configurer les credentials** (voir section suivante)

### 📝 JSON du Workflow

<details>
<summary><b>Cliquer pour voir le JSON complet (789 lignes)</b></summary>

```json
{
  "name": "Avatar Video Automation - TikTok/Instagram/YouTube",
  "nodes": [
    {
      "parameters": {
        "height": 680,
        "width": 800,
        "content": "# 🎬 AUTOMATISATION VIDÉO AVEC AVATAR IA\n\n## 📋 DESCRIPTION DU WORKFLOW\nCe workflow automatise complètement la création de vidéos avec avatar IA :\n\n✅ **Génère un script viral** divisé en 8 parties de 8 secondes\n✅ **Crée un avatar IA** réaliste avec D-ID\n✅ **Génère 8 vidéos** de 8 secondes chacune (64s total)\n✅ **Compile automatiquement** toutes les vidéos en un seul fichier\n✅ **Publie simultanément** sur TikTok, Instagram et YouTube\n\n---\n\n## 🔑 API NÉCESSAIRES (OBLIGATOIRES)\n\n### 1️⃣ D-ID API (Génération d'avatars vidéo)\n**Pourquoi :** Crée des avatars IA qui parlent\n**Lien :** https://www.d-id.com/\n**Tarif :** Gratuit (20 crédits/mois) ou Payant ($5.9+/mois)\n**Inscription :** Créer un compte → Settings → API Keys\n\n### 2️⃣ OpenAI API (Génération de scripts)\n**Pourquoi :** Génère les scripts vidéo viraux\n**Lien :** https://platform.openai.com/\n**Tarif :** Pay-as-you-go (~$0.01-0.03 par script)\n**Inscription :** Créer un compte → API Keys → Create new key\n\n---\n\n## 📱 API RÉSEAUX SOCIAUX (OPTIONNELLES)\n\n### 3️⃣ TikTok for Developers\n**Lien :** https://developers.tiktok.com/\n**Inscription :** Créer une app → OAuth 2.0 → Obtenir access token\n\n### 4️⃣ Instagram Graph API\n**Lien :** https://developers.facebook.com/\n**Inscription :** Créer une app Facebook → Activer Instagram API\n\n### 5️⃣ YouTube Data API v3\n**Lien :** https://console.cloud.google.com/\n**Inscription :** Créer un projet → Activer YouTube API → OAuth 2.0\n\n---\n\n## ⚙️ CONFIGURATION REQUISE\n\n✔️ **FFmpeg** installé sur le serveur\n✔️ **Dossier temporaire** : /tmp/n8n-videos\n✔️ **Credentials** configurés dans n8n\n\n---\n\n## 🚀 DÉMARRAGE RAPIDE\n\n1. Configurer toutes les credentials dans n8n\n2. Modifier le sujet dans \"Schedule Trigger\"\n3. Cliquer sur \"Execute Workflow\"\n4. Attendre ~5-8 minutes\n5. Les vidéos seront publiées automatiquement !\n\n---\n\n## 💰 COÛT ESTIMÉ PAR VIDÉO\n\n- D-ID : ~$0.30-0.50 (8 générations)\n- OpenAI : ~$0.02-0.03 (script)\n- **Total : ~$0.35 par vidéo complète**\n\n---\n\n## ⏱️ TEMPS DE GÉNÉRATION\n\n- Script : ~10 secondes\n- Avatar initial : ~30 secondes\n- 8 vidéos : ~4-5 minutes\n- Compilation : ~10 secondes\n- Publication : ~30 secondes\n**Total : ~6-8 minutes par vidéo**"
      },
      "id": "main-info-note",
      "name": "Note - Info Principale",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        -200,
        -300
      ]
    },
    {
      "parameters": {
        "height": 280,
        "width": 380,
        "content": "## 🎯 DÉCLENCHEUR\n\n**Ce qu'il fait :**\nDémarre le workflow automatiquement toutes les 24h\n\n**Configuration :**\n- Interval : 24 heures\n- Vous pouvez aussi le déclencher manuellement\n\n**Personnalisation :**\nAjoutez un input JSON pour personnaliser :\n```json\n{\n  \"topic\": \"5 astuces productivité\",\n  \"style\": \"éducatif\",\n  \"tone\": \"énergique\"\n}\n```\n\n**Alternative :**\nRemplacez par un Webhook pour déclencher depuis une API externe"
      },
      "id": "note-trigger",
      "name": "Note",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        140,
        80
      ]
    },
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 24
            }
          ]
        }
      },
      "id": "schedule-trigger",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [
        240,
        380
      ]
    },
    {
      "parameters": {
        "height": 320,
        "width": 380,
        "content": "## 📝 GÉNÉRATION DE SCRIPT IA\n\n**Ce qu'il fait :**\nUtilise OpenAI GPT-4 pour générer un script viral divisé en 8 parties\n\n**API Requise :** OpenAI\n**Lien :** https://platform.openai.com/api-keys\n\n**Format de sortie :**\n```json\n{\n  \"avatar_description\": \"Coach professionnel souriant\",\n  \"parts\": [\n    {\"part\": 1, \"duration\": 8, \"text\": \"Script partie 1\"},\n    {\"part\": 2, \"duration\": 8, \"text\": \"Script partie 2\"},\n    ...\n  ]\n}\n```\n\n**Personnalisation :**\nModifiez le prompt pour changer le style :\n- Humoristique, éducatif, motivationnel\n- Ton : casual, professionnel, énergique"
      },
      "id": "note-script-generation",
      "name": "Note1",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        360,
        80
      ]
    },
    {
      "parameters": {
        "content": "=Génère un script vidéo viral pour {{ $json.topic }} divisé en 8 parties de 8 secondes chacune. Chaque partie doit être engageante et se terminer par un hook pour la partie suivante. Format JSON:\n{\n  \"avatar_description\": \"description détaillée de l'avatar à créer\",\n  \"parts\": [\n    {\"part\": 1, \"duration\": 8, \"text\": \"script partie 1\"},\n    {\"part\": 2, \"duration\": 8, \"text\": \"script partie 2\"},\n    ...\n  ]\n}",
        "options": {}
      },
      "id": "generate-script",
      "name": "Generate Video Script",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.6,
      "position": [
        460,
        380
      ],
      "credentials": {
        "openAiApi": {
          "id": "openai-credentials",
          "name": "OpenAI API"
        }
      }
    },
    {
      "parameters": {
        "height": 360,
        "width": 380,
        "content": "## 🎭 CRÉATION DE L'AVATAR INITIAL\n\n**Ce qu'il fait :**\nCrée le premier avatar IA avec D-ID qui servira de base\n\n**API Requise :** D-ID\n**Lien :** https://studio.d-id.com/account-settings\n**Doc API :** https://docs.d-id.com/reference/api-overview\n\n**Credentials n8n :**\n- Type : Header Auth\n- Header Name : `Authorization`\n- Header Value : `Basic VOTRE_API_KEY`\n\n**Paramètres :**\n- `source_url` : URL de l'image de l'avatar\n- `script` : Texte de la première partie\n- `config.stitch` : Active le stitching automatique\n- `config.result_format` : Format MP4\n\n**Coût :** ~1 crédit D-ID par génération\n\n**Alternative :** HeyGen, Synthesia"
      },
      "id": "note-create-avatar",
      "name": "Note2",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        580,
        80
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.d-id.com/talks",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "source_url",
              "value": "={{ $json.avatar_image_url }}"
            },
            {
              "name": "script",
              "value": "={{ $json.parts[0].text }}"
            },
            {
              "name": "config",
              "value": "={\"stitch\": true, \"result_format\": \"mp4\"}"
            }
          ]
        },
        "options": {}
      },
      "id": "create-avatar",
      "name": "Create AI Avatar",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        680,
        380
      ],
      "credentials": {
        "httpHeaderAuth": {
          "id": "did-api-key",
          "name": "D-ID API Key"
        }
      }
    },
    {
      "parameters": {
        "height": 240,
        "width": 380,
        "content": "## 💾 STOCKAGE DES VARIABLES\n\n**Ce qu'il fait :**\nStocke les données importantes pour les réutiliser\n\n**Variables sauvegardées :**\n- `videoParts` : Les 8 parties du script\n- `avatarUrl` : URL de l'avatar créé\n- `topic` : Le sujet de la vidéo\n\n**Pourquoi c'est important :**\nPermet de réutiliser ces données dans les nœuds suivants sans avoir à rechercher dans les nœuds précédents\n\n**Utilisation :**\nAccès via `$('Set Variables').item.json.avatarUrl`"
      },
      "id": "note-set-variables",
      "name": "Note3",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        800,
        80
      ]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "video-parts",
              "name": "videoParts",
              "value": "={{ $json.parts }}",
              "type": "array"
            },
            {
              "id": "avatar-url",
              "name": "avatarUrl",
              "value": "={{ $json.result_url }}",
              "type": "string"
            },
            {
              "id": "topic",
              "name": "topic",
              "value": "={{ $('Schedule Trigger').item.json.topic || 'Motivation quotidienne' }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "id": "set-variables",
      "name": "Set Variables",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.3,
      "position": [
        900,
        380
      ]
    },
    {
      "parameters": {
        "height": 520,
        "width": 1360,
        "content": "## 🔄 BOUCLE DE GÉNÉRATION DES 8 VIDÉOS\n\n**Ce bloc génère 8 vidéos de 8 secondes chacune**\n\n### 📊 Flux de travail :\n\n1️⃣ **Split Into Parts** : Divise les 8 parties en items individuels\n2️⃣ **Generate Video Part** : Crée une vidéo pour chaque partie avec D-ID\n3️⃣ **Wait for Processing** : Attend 30s que D-ID traite la vidéo\n4️⃣ **Check Video Status** : Vérifie si la vidéo est prête\n5️⃣ **Download Video Part** : Télécharge la vidéo générée\n6️⃣ **Add to File List** : Ajoute le nom du fichier à la liste de compilation\n7️⃣ **All Parts Done?** : Vérifie si toutes les 8 vidéos sont générées\n   - ❌ **Non** → Retour à l'étape 1 pour la partie suivante\n   - ✅ **Oui** → Passe à la compilation\n\n### ⏱️ Temps total : ~4-5 minutes (8 vidéos x 30-40s)\n\n### 💡 Astuce : \nSi vous voulez modifier le nombre de parties, changez le nombre dans le script de génération ET ajustez la boucle"
      },
      "id": "note-video-loop",
      "name": "Note4",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        1020,
        -120
      ]
    },
    {
      "parameters": {
        "batchSize": 1,
        "options": {}
      },
      "id": "split-parts",
      "name": "Split Into Parts",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [
        1120,
        380
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.d-id.com/talks",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "source_url",
              "value": "={{ $('Set Variables').item.json.avatarUrl }}"
            },
            {
              "name": "script",
              "value": "={{ $json.text }}"
            },
            {
              "name": "config",
              "value": "={\"stitch\": true, \"result_format\": \"mp4\", \"driver_expressions\": {\"expressions\": [{\"expression\": \"happy\", \"start_frame\": 0, \"intensity\": 1.0}]}}"
            }
          ]
        },
        "options": {}
      },
      "id": "generate-video-part",
      "name": "Generate Video Part",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        1340,
        380
      ],
      "credentials": {
        "httpHeaderAuth": {
          "id": "did-api-key",
          "name": "D-ID API Key"
        }
      }
    },
    {
      "parameters": {
        "amount": 30,
        "unit": "seconds"
      },
      "id": "wait-processing",
      "name": "Wait for Processing",
      "type": "n8n-nodes-base.wait",
      "typeVersion": 1.1,
      "position": [
        1560,
        380
      ],
      "webhookId": "video-processing-wait"
    },
    {
      "parameters": {
        "method": "GET",
        "url": "=https://api.d-id.com/talks/{{ $json.id }}",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "options": {}
      },
      "id": "check-video-status",
      "name": "Check Video Status",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        1780,
        380
      ],
      "credentials": {
        "httpHeaderAuth": {
          "id": "did-api-key",
          "name": "D-ID API Key"
        }
      }
    },
    {
      "parameters": {
        "url": "={{ $json.result_url }}",
        "options": {
          "fileName": "=video_part_{{ $('Split Into Parts').context.currentRunIndex + 1 }}.mp4"
        }
      },
      "id": "download-video",
      "name": "Download Video Part",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        2000,
        380
      ]
    },
    {
      "parameters": {
        "command": "=cd /tmp/n8n-videos && echo \"file 'video_part_{{ $('Split Into Parts').context.currentRunIndex + 1 }}.mp4'\" >> filelist.txt"
      },
      "id": "add-to-filelist",
      "name": "Add to File List",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [
        2220,
        380
      ]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "check-more-parts",
              "leftValue": "={{ $('Split Into Parts').context.noItemsLeft }}",
              "rightValue": true,
              "operator": {
                "type": "boolean",
                "operation": "true"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "check-all-done",
      "name": "All Parts Done?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        2440,
        380
      ]
    },
    {
      "parameters": {
        "height": 280,
        "width": 380,
        "content": "## 🎞️ COMPILATION AVEC FFMPEG\n\n**Ce qu'il fait :**\nAssemble les 8 vidéos en une seule vidéo de 64 secondes\n\n**Prérequis :**\n✅ FFmpeg doit être installé sur le serveur\n```bash\nsudo apt-get install ffmpeg\n```\n\n**Commande exécutée :**\n```bash\nffmpeg -f concat -safe 0 \\\n  -i filelist.txt \\\n  -c copy \\\n  final_video.mp4\n```\n\n**Durée :** ~10 secondes\n**Format de sortie :** MP4, optimisé pour les réseaux sociaux\n\n**Fichier créé :** /tmp/n8n-videos/final_video.mp4"
      },
      "id": "note-compilation",
      "name": "Note5",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        2560,
        -80
      ]
    },
    {
      "parameters": {
        "command": "cd /tmp/n8n-videos && ffmpeg -f concat -safe 0 -i filelist.txt -c copy final_video.mp4"
      },
      "id": "compile-videos",
      "name": "Compile Videos with FFmpeg",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [
        2660,
        280
      ]
    },
    {
      "parameters": {
        "height": 560,
        "width": 620,
        "content": "## 📱 PUBLICATION MULTI-PLATEFORMES\n\n**Ce bloc publie automatiquement sur 3 plateformes en parallèle**\n\n---\n\n### 🎥 YOUTUBE\n**API :** YouTube Data API v3\n**Lien :** https://console.cloud.google.com/apis/library/youtube.googleapis.com\n\n**Configuration :**\n1. Créer un projet Google Cloud\n2. Activer YouTube Data API v3\n3. Créer des credentials OAuth 2.0\n4. Configurer dans n8n\n\n**Format :** Shorts (9:16) ou Standard (16:9)\n**Visibilité :** Public, Unlisted ou Private\n\n---\n\n### 📸 INSTAGRAM REELS\n**API :** Instagram Graph API\n**Lien :** https://developers.facebook.com/docs/instagram-api\n\n**Configuration :**\n1. Créer une app Facebook\n2. Ajouter Instagram Graph API\n3. Obtenir un User Access Token\n4. Lier votre compte Instagram professionnel\n\n**Format :** Vertical 9:16, 15-90 secondes\n**Limite :** 25 publications/jour\n\n---\n\n### 🎵 TIKTOK\n**API :** TikTok for Developers\n**Lien :** https://developers.tiktok.com/\n\n**Configuration :**\n1. S'inscrire sur TikTok for Developers\n2. Créer une application\n3. Obtenir Client Key et Client Secret\n4. Générer Access Token via OAuth 2.0\n\n**Format :** Vertical 9:16, jusqu'à 10 minutes\n**Limite :** Selon le plan API"
      },
      "id": "note-publication",
      "name": "Note6",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        2780,
        -320
      ]
    },
    {
      "parameters": {
        "operation": "upload",
        "binaryPropertyName": "data",
        "options": {
          "title": "={{ $('Set Variables').item.json.topic }}",
          "description": "Vidéo générée automatiquement #IA #Avatar #Motivation",
          "categoryId": "22",
          "privacyStatus": "public"
        }
      },
      "id": "upload-youtube",
      "name": "Upload to YouTube",
      "type": "n8n-nodes-base.youtube",
      "typeVersion": 1,
      "position": [
        2880,
        180
      ],
      "credentials": {
        "youTubeOAuth2Api": {
          "id": "youtube-oauth",
          "name": "YouTube OAuth2"
        }
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://graph.facebook.com/v18.0/me/media",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "instagramApi",
        "sendQuery": true,
        "queryParameters": {
          "parameters": [
            {
              "name": "video_url",
              "value": "={{ $json.videoUrl }}"
            },
            {
              "name": "caption",
              "value": "={{ $('Set Variables').item.json.topic }} #IA #Avatar"
            },
            {
              "name": "media_type",
              "value": "REELS"
            }
          ]
        },
        "options": {}
      },
      "id": "upload-instagram",
      "name": "Upload to Instagram",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        2880,
        280
      ],
      "credentials": {
        "instagramApi": {
          "id": "instagram-api",
          "name": "Instagram API"
        }
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://open.tiktokapis.com/v2/post/publish/video/init/",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Authorization",
              "value": "=Bearer {{ $credentials.token }}"
            },
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "post_info",
              "value": "={\"title\": \"{{ $('Set Variables').item.json.topic }}\", \"privacy_level\": \"PUBLIC_TO_EVERYONE\", \"disable_duet\": false, \"disable_comment\": false, \"disable_stitch\": false, \"video_cover_timestamp_ms\": 1000}"
            },
            {
              "name": "source_info",
              "value": "={\"source\": \"FILE_UPLOAD\", \"video_size\": {{ $json.videoSize }}, \"chunk_size\": 10000000, \"total_chunk_count\": 1}"
            }
          ]
        },
        "options": {}
      },
      "id": "upload-tiktok",
      "name": "Upload to TikTok",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        2880,
        380
      ],
      "credentials": {
        "httpHeaderAuth": {
          "id": "tiktok-api",
          "name": "TikTok API"
        }
      }
    },
    {
      "parameters": {
        "height": 220,
        "width": 380,
        "content": "## ✅ FINALISATION\n\n**Merge Upload Results :**\nCombine les résultats des 3 publications en un seul output\n\n**Cleanup Temp Files :**\nNettoie le dossier temporaire pour libérer l'espace :\n- Supprime tous les fichiers MP4\n- Supprime le fichier filelist.txt\n- Recrée le dossier vide pour la prochaine exécution\n\n**Important :** \nSi vous voulez conserver les vidéos, désactivez le nœud Cleanup"
      },
      "id": "note-cleanup",
      "name": "Note7",
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        3000,
        -80
      ]
    },
    {
      "parameters": {
        "mode": "combine",
        "combinationMode": "mergeByPosition",
        "options": {}
      },
      "id": "merge-results",
      "name": "Merge Upload Results",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 2.1,
      "position": [
        3100,
        280
      ]
    },
    {
      "parameters": {
        "command": "rm -rf /tmp/n8n-videos && mkdir -p /tmp/n8n-videos"
      },
      "id": "cleanup",
      "name": "Cleanup Temp Files",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [
        3320,
        280
      ]
    }
  ],
  "pinData": {},
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Generate Video Script",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Video Script": {
      "main": [
        [
          {
            "node": "Create AI Avatar",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create AI Avatar": {
      "main": [
        [
          {
            "node": "Set Variables",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Set Variables": {
      "main": [
        [
          {
            "node": "Split Into Parts",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Split Into Parts": {
      "main": [
        [
          {
            "node": "Generate Video Part",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Video Part": {
      "main": [
        [
          {
            "node": "Wait for Processing",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Wait for Processing": {
      "main": [
        [
          {
            "node": "Check Video Status",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check Video Status": {
      "main": [
        [
          {
            "node": "Download Video Part",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download Video Part": {
      "main": [
        [
          {
            "node": "Add to File List",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Add to File List": {
      "main": [
        [
          {
            "node": "All Parts Done?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "All Parts Done?": {
      "main": [
        [
          {
            "node": "Compile Videos with FFmpeg",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Split Into Parts",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Compile Videos with FFmpeg": {
      "main": [
        [
          {
            "node": "Upload to YouTube",
            "type": "main",
            "index": 0
          },
          {
            "node": "Upload to Instagram",
            "type": "main",
            "index": 0
          },
          {
            "node": "Upload to TikTok",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Upload to YouTube": {
      "main": [
        [
          {
            "node": "Merge Upload Results",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Upload to Instagram": {
      "main": [
        [
          {
            "node": "Merge Upload Results",
            "type": "main",
            "index": 1
          }
        ]
      ]
    },
    "Upload to TikTok": {
      "main": [
        [
          {
            "node": "Merge Upload Results",
            "type": "main",
            "index": 2
          }
        ]
      ]
    },
    "Merge Upload Results": {
      "main": [
        [
          {
            "node": "Cleanup Temp Files",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "1",
  "meta": {
    "instanceId": "n8n-avatar-automation"
  },
  "id": "avatar-video-automation",
  "tags": []
}
```

</details>

### ✅ Ce Que Contient le Workflow

- **16 nœuds fonctionnels** (Schedule, Generate Script, Create Avatar, etc.)
- **8 notes explicatives** avec tous les détails
- **Tous les liens API** directement dans les notes
- **Instructions de configuration** pour chaque étape
- **Prêt à l'emploi** après configuration des credentials

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
