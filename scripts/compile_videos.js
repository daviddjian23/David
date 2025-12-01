#!/usr/bin/env node

/**
 * Script Node.js de compilation de vidéos pour n8n
 * Compile 8 vidéos de 8 secondes en une seule vidéo finale
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

/**
 * Configuration des plateformes
 */
const PLATFORM_CONFIGS = {
  tiktok: {
    size: '1080:1920',
    bitrate: '3000k',
    fps: 30,
    format: 'vertical'
  },
  instagram: {
    size: '1080:1920',
    bitrate: '3500k',
    fps: 30,
    format: 'vertical'
  },
  youtube_shorts: {
    size: '1080:1920',
    bitrate: '5000k',
    fps: 60,
    format: 'vertical'
  },
  youtube: {
    size: '1920:1080',
    bitrate: '5000k',
    fps: 60,
    format: 'horizontal'
  }
};

/**
 * Crée un fichier de liste pour ffmpeg
 */
async function createFileList(videoFiles, outputDir) {
  const filelistPath = path.join(outputDir, 'filelist.txt');
  const content = videoFiles
    .map(file => `file '${path.resolve(file)}'`)
    .join('\n');

  await fs.writeFile(filelistPath, content);
  console.log(`📝 Fichier de liste créé: ${filelistPath}`);

  return filelistPath;
}

/**
 * Récupère tous les fichiers vidéo triés
 */
async function getVideoFiles(inputDir) {
  const files = await fs.readdir(inputDir);

  const videoFiles = files
    .filter(f => f.endsWith('.mp4') && f.startsWith('video_part_'))
    .sort()
    .map(f => path.join(inputDir, f));

  return videoFiles;
}

/**
 * Compile les vidéos avec ffmpeg
 */
async function compileVideos(inputDir, outputFile) {
  try {
    console.log('🎬 Récupération des vidéos...');
    const videoFiles = await getVideoFiles(inputDir);

    if (videoFiles.length === 0) {
      throw new Error('Aucune vidéo trouvée dans le dossier');
    }

    console.log(`📹 ${videoFiles.length} vidéos trouvées`);

    // Créer le fichier de liste
    const filelistPath = await createFileList(videoFiles, inputDir);

    // Compiler avec ffmpeg
    console.log('🔄 Compilation en cours...');
    const cmd = `ffmpeg -f concat -safe 0 -i "${filelistPath}" -c copy -y "${outputFile}"`;

    const { stdout, stderr } = await execAsync(cmd);

    // Vérifier la taille du fichier
    const stats = await fs.stat(outputFile);
    const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);

    console.log(`✅ Vidéo compilée avec succès: ${outputFile}`);
    console.log(`📊 Taille: ${sizeMB} MB`);

    return true;
  } catch (error) {
    console.error('❌ Erreur lors de la compilation:', error.message);
    return false;
  }
}

/**
 * Optimise la vidéo pour une plateforme spécifique
 */
async function optimizeForPlatform(inputFile, outputFile, platform = 'tiktok') {
  try {
    const config = PLATFORM_CONFIGS[platform] || PLATFORM_CONFIGS.tiktok;

    console.log(`⚙️ Optimisation pour ${platform}...`);

    const cmd = `ffmpeg -i "${inputFile}" \
      -vf "scale=${config.size}:force_original_aspect_ratio=decrease,pad=${config.size}:(ow-iw)/2:(oh-ih)/2" \
      -r ${config.fps} \
      -b:v ${config.bitrate} \
      -c:v libx264 \
      -preset medium \
      -c:a aac \
      -b:a 128k \
      -y "${outputFile}"`;

    await execAsync(cmd);

    console.log(`✅ Optimisation pour ${platform} terminée`);
    return true;
  } catch (error) {
    console.error('❌ Erreur lors de l\'optimisation:', error.message);
    return false;
  }
}

/**
 * Ajoute un filigrane texte
 */
async function addTextWatermark(inputFile, outputFile, text, position = 'bottom-right') {
  try {
    const positions = {
      'top-left': 'x=10:y=10',
      'top-right': 'x=W-tw-10:y=10',
      'bottom-left': 'x=10:y=H-th-10',
      'bottom-right': 'x=W-tw-10:y=H-th-10',
      'center': 'x=(W-tw)/2:y=(H-th)/2'
    };

    const pos = positions[position] || positions['bottom-right'];

    console.log('🏷️ Ajout du filigrane texte...');

    const cmd = `ffmpeg -i "${inputFile}" \
      -vf "drawtext=text='${text}':fontsize=24:fontcolor=white@0.7:${pos}" \
      -codec:a copy \
      -y "${outputFile}"`;

    await execAsync(cmd);

    console.log('✅ Filigrane ajouté');
    return true;
  } catch (error) {
    console.error('❌ Erreur lors de l\'ajout du filigrane:', error.message);
    return false;
  }
}

/**
 * Ajoute une intro et/ou outro
 */
async function addIntroOutro(inputFile, outputFile, intro = null, outro = null) {
  try {
    const videos = [];

    if (intro && await fs.access(intro).then(() => true).catch(() => false)) {
      videos.push(intro);
    }

    videos.push(inputFile);

    if (outro && await fs.access(outro).then(() => true).catch(() => false)) {
      videos.push(outro);
    }

    if (videos.length === 1) {
      console.log('ℹ️ Pas d\'intro/outro à ajouter');
      return true;
    }

    console.log('🎥 Ajout intro/outro...');

    const tempDir = path.dirname(inputFile);
    const filelistPath = await createFileList(videos, tempDir);

    const cmd = `ffmpeg -f concat -safe 0 -i "${filelistPath}" -c copy -y "${outputFile}"`;
    await execAsync(cmd);

    console.log('✅ Intro/outro ajoutées');
    return true;
  } catch (error) {
    console.error('❌ Erreur lors de l\'ajout intro/outro:', error.message);
    return false;
  }
}

/**
 * Ajoute une musique de fond
 */
async function addBackgroundMusic(inputFile, outputFile, musicFile, volume = 0.3) {
  try {
    console.log('🎵 Ajout de la musique de fond...');

    const cmd = `ffmpeg -i "${inputFile}" -i "${musicFile}" \
      -filter_complex "[1:a]volume=${volume}[a1];[0:a][a1]amix=inputs=2:duration=first[aout]" \
      -map 0:v -map "[aout]" \
      -c:v copy \
      -c:a aac \
      -y "${outputFile}"`;

    await execAsync(cmd);

    console.log('✅ Musique de fond ajoutée');
    return true;
  } catch (error) {
    console.error('❌ Erreur lors de l\'ajout de la musique:', error.message);
    return false;
  }
}

/**
 * Génère des sous-titres automatiques (nécessite whisper ou service API)
 */
async function generateSubtitles(videoFile, outputSrtFile) {
  try {
    console.log('📝 Génération des sous-titres...');

    // Extraire l'audio
    const audioFile = videoFile.replace('.mp4', '.wav');
    await execAsync(`ffmpeg -i "${videoFile}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${audioFile}"`);

    console.log('ℹ️ Audio extrait. Utilisez un service comme Whisper API pour générer les sous-titres.');
    console.log(`   Audio: ${audioFile}`);
    console.log(`   Output SRT: ${outputSrtFile}`);

    // NOTE: Ici, vous devriez intégrer avec un service de transcription
    // comme OpenAI Whisper, Google Speech-to-Text, etc.

    return true;
  } catch (error) {
    console.error('❌ Erreur lors de la génération des sous-titres:', error.message);
    return false;
  }
}

/**
 * Fonction principale
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log('Usage: node compile_videos.js <input_dir> <output_file> [options]');
    console.log('\nOptions:');
    console.log('  --platform <platform>     Optimiser pour: tiktok, instagram, youtube_shorts, youtube');
    console.log('  --watermark <text>        Ajouter un filigrane texte');
    console.log('  --intro <file>            Ajouter une vidéo d\'intro');
    console.log('  --outro <file>            Ajouter une vidéo d\'outro');
    console.log('  --music <file>            Ajouter une musique de fond');
    console.log('  --music-volume <0-1>      Volume de la musique (défaut: 0.3)');
    process.exit(1);
  }

  const inputDir = args[0];
  const outputFile = args[1];

  // Parser les options
  const options = {
    platform: null,
    watermark: null,
    intro: null,
    outro: null,
    music: null,
    musicVolume: 0.3
  };

  for (let i = 2; i < args.length; i += 2) {
    const flag = args[i];
    const value = args[i + 1];

    switch (flag) {
      case '--platform':
        options.platform = value;
        break;
      case '--watermark':
        options.watermark = value;
        break;
      case '--intro':
        options.intro = value;
        break;
      case '--outro':
        options.outro = value;
        break;
      case '--music':
        options.music = value;
        break;
      case '--music-volume':
        options.musicVolume = parseFloat(value);
        break;
    }
  }

  console.log('🚀 Début de la compilation des vidéos');
  console.log(`📂 Dossier d'entrée: ${inputDir}`);
  console.log(`📹 Fichier de sortie: ${outputFile}`);

  // Fichiers temporaires
  const tempDir = path.dirname(outputFile);
  const tempFile1 = path.join(tempDir, 'temp_compiled.mp4');
  const tempFile2 = path.join(tempDir, 'temp_optimized.mp4');
  const tempFile3 = path.join(tempDir, 'temp_watermark.mp4');

  try {
    // 1. Compilation de base
    if (!await compileVideos(inputDir, tempFile1)) {
      process.exit(1);
    }

    let currentFile = tempFile1;

    // 2. Ajouter intro/outro
    if (options.intro || options.outro) {
      await addIntroOutro(currentFile, tempFile2, options.intro, options.outro);
      currentFile = tempFile2;
    }

    // 3. Ajouter musique de fond
    if (options.music) {
      const musicOutput = tempFile3;
      await addBackgroundMusic(currentFile, musicOutput, options.music, options.musicVolume);
      currentFile = musicOutput;
    }

    // 4. Ajouter filigrane
    if (options.watermark) {
      const watermarkOutput = path.join(tempDir, 'temp_final.mp4');
      await addTextWatermark(currentFile, watermarkOutput, options.watermark);
      currentFile = watermarkOutput;
    }

    // 5. Optimiser pour la plateforme
    if (options.platform) {
      await optimizeForPlatform(currentFile, outputFile, options.platform);
    } else {
      await fs.rename(currentFile, outputFile);
    }

    // Nettoyage des fichiers temporaires
    const tempFiles = [tempFile1, tempFile2, tempFile3, path.join(tempDir, 'temp_final.mp4')];
    for (const file of tempFiles) {
      try {
        await fs.unlink(file);
      } catch (e) {
        // Ignorer si le fichier n'existe pas
      }
    }

    console.log('✅ Compilation terminée avec succès!');
    console.log(`📊 Durée approximative: ${8 * 8} secondes (8 parties x 8 secondes)`);

  } catch (error) {
    console.error('❌ Erreur fatale:', error.message);
    process.exit(1);
  }
}

// Exporter les fonctions pour utilisation dans n8n
module.exports = {
  compileVideos,
  optimizeForPlatform,
  addTextWatermark,
  addIntroOutro,
  addBackgroundMusic,
  generateSubtitles,
  PLATFORM_CONFIGS
};

// Exécuter si appelé directement
if (require.main === module) {
  main();
}
