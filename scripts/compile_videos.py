#!/usr/bin/env python3
"""
Script de compilation de vidéos pour l'automatisation n8n
Compile 8 vidéos de 8 secondes en une seule vidéo
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from typing import List


def create_filelist(video_files: List[str], output_path: str) -> str:
    """
    Crée un fichier texte listant toutes les vidéos à concaténer

    Args:
        video_files: Liste des chemins des fichiers vidéo
        output_path: Chemin du dossier de sortie

    Returns:
        Chemin du fichier de liste créé
    """
    filelist_path = os.path.join(output_path, 'filelist.txt')

    with open(filelist_path, 'w') as f:
        for video in sorted(video_files):
            # Format requis par ffmpeg
            f.write(f"file '{os.path.abspath(video)}'\n")

    return filelist_path


def compile_videos(input_dir: str, output_file: str) -> bool:
    """
    Compile toutes les vidéos du dossier en une seule vidéo

    Args:
        input_dir: Dossier contenant les vidéos à compiler
        output_file: Chemin du fichier de sortie

    Returns:
        True si la compilation a réussi, False sinon
    """
    try:
        # Récupérer tous les fichiers MP4
        video_files = sorted([
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.endswith('.mp4') and f.startswith('video_part_')
        ])

        if not video_files:
            print("❌ Aucune vidéo trouvée dans le dossier")
            return False

        print(f"📹 {len(video_files)} vidéos trouvées")

        # Créer le fichier de liste
        filelist_path = create_filelist(video_files, input_dir)
        print(f"📝 Fichier de liste créé: {filelist_path}")

        # Compiler avec ffmpeg
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', filelist_path,
            '-c', 'copy',
            '-y',  # Écraser si existe
            output_file
        ]

        print(f"🎬 Compilation en cours...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            print(f"✅ Vidéo compilée avec succès: {output_file}")
            print(f"📊 Taille: {file_size:.2f} MB")
            return True
        else:
            print(f"❌ Erreur lors de la compilation:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False


def add_intro_outro(input_file: str, output_file: str, intro: str = None, outro: str = None) -> bool:
    """
    Ajoute une intro et/ou outro à la vidéo compilée

    Args:
        input_file: Vidéo d'entrée
        output_file: Vidéo de sortie
        intro: Chemin de la vidéo d'intro (optionnel)
        outro: Chemin de la vidéo d'outro (optionnel)

    Returns:
        True si réussi, False sinon
    """
    try:
        videos = []
        if intro and os.path.exists(intro):
            videos.append(intro)

        videos.append(input_file)

        if outro and os.path.exists(outro):
            videos.append(outro)

        if len(videos) == 1:
            print("ℹ️ Pas d'intro/outro à ajouter")
            return True

        # Créer un fichier de liste temporaire
        temp_dir = os.path.dirname(input_file)
        filelist = create_filelist(videos, temp_dir)

        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', filelist,
            '-c', 'copy',
            '-y',
            output_file
        ]

        print(f"🎥 Ajout intro/outro...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur lors de l'ajout intro/outro: {str(e)}")
        return False


def add_watermark(input_file: str, output_file: str, watermark_text: str = None, watermark_image: str = None) -> bool:
    """
    Ajoute un filigrane (texte ou image) à la vidéo

    Args:
        input_file: Vidéo d'entrée
        output_file: Vidéo de sortie
        watermark_text: Texte du filigrane (optionnel)
        watermark_image: Chemin de l'image de filigrane (optionnel)

    Returns:
        True si réussi, False sinon
    """
    try:
        if watermark_text:
            # Ajouter un filigrane texte
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-vf', f"drawtext=text='{watermark_text}':fontsize=24:fontcolor=white@0.7:x=10:y=H-th-10",
                '-codec:a', 'copy',
                '-y',
                output_file
            ]
        elif watermark_image and os.path.exists(watermark_image):
            # Ajouter un filigrane image
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-i', watermark_image,
                '-filter_complex', 'overlay=W-w-10:H-h-10',
                '-codec:a', 'copy',
                '-y',
                output_file
            ]
        else:
            print("ℹ️ Pas de filigrane à ajouter")
            return True

        print(f"🏷️ Ajout du filigrane...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur lors de l'ajout du filigrane: {str(e)}")
        return False


def optimize_for_platform(input_file: str, output_file: str, platform: str = 'tiktok') -> bool:
    """
    Optimise la vidéo pour une plateforme spécifique

    Args:
        input_file: Vidéo d'entrée
        output_file: Vidéo de sortie
        platform: Plateforme cible (tiktok, instagram, youtube)

    Returns:
        True si réussi, False sinon
    """
    try:
        # Configuration par plateforme
        configs = {
            'tiktok': {
                'size': '1080:1920',  # Format vertical 9:16
                'bitrate': '3000k',
                'fps': 30
            },
            'instagram': {
                'size': '1080:1920',  # Reels format
                'bitrate': '3500k',
                'fps': 30
            },
            'youtube': {
                'size': '1920:1080',  # Format horizontal 16:9 ou shorts 9:16
                'bitrate': '5000k',
                'fps': 60
            }
        }

        config = configs.get(platform.lower(), configs['tiktok'])

        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f"scale={config['size']}:force_original_aspect_ratio=decrease,pad={config['size']}:(ow-iw)/2:(oh-ih)/2",
            '-r', str(config['fps']),
            '-b:v', config['bitrate'],
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            output_file
        ]

        print(f"⚙️ Optimisation pour {platform}...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur lors de l'optimisation: {str(e)}")
        return False


def main():
    """Fonction principale"""
    if len(sys.argv) < 3:
        print("Usage: python compile_videos.py <input_dir> <output_file> [--platform tiktok|instagram|youtube]")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    platform = None

    # Parser les arguments optionnels
    if '--platform' in sys.argv:
        idx = sys.argv.index('--platform')
        if idx + 1 < len(sys.argv):
            platform = sys.argv[idx + 1]

    print("🚀 Début de la compilation des vidéos")
    print(f"📂 Dossier d'entrée: {input_dir}")
    print(f"📹 Fichier de sortie: {output_file}")

    # Compilation basique
    temp_file = output_file.replace('.mp4', '_temp.mp4')
    if not compile_videos(input_dir, temp_file):
        sys.exit(1)

    # Optimisation pour la plateforme si spécifié
    if platform:
        if not optimize_for_platform(temp_file, output_file, platform):
            print("⚠️ Optimisation échouée, utilisation de la vidéo non optimisée")
            os.rename(temp_file, output_file)
        else:
            os.remove(temp_file)
    else:
        os.rename(temp_file, output_file)

    print("✅ Compilation terminée avec succès!")
    print(f"📊 Durée approximative: 64 secondes (8 parties x 8 secondes)")


if __name__ == '__main__':
    main()
