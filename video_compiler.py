#!/usr/bin/env python3
"""
Script de compilation de vidéos pour l'automatisation n8n
Compile 8 vidéos de 8 secondes en une seule vidéo finale
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Optional


class VideoCompiler:
    """Classe pour compiler plusieurs vidéos en une seule"""

    def __init__(self, input_dir: str = "/tmp/video_segments", output_dir: str = "/tmp/final_videos"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_segment_files(self, num_segments: int = 8) -> List[Path]:
        """Récupère les fichiers de segments dans l'ordre"""
        segments = []
        for i in range(1, num_segments + 1):
            segment_path = self.input_dir / f"segment_{i}.mp4"
            if not segment_path.exists():
                raise FileNotFoundError(f"Segment {i} not found: {segment_path}")
            segments.append(segment_path)
        return segments

    def create_concat_file(self, segments: List[Path]) -> Path:
        """Crée le fichier de concaténation pour FFmpeg"""
        concat_file = self.input_dir / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for segment in segments:
                # Format FFmpeg concat: file '/path/to/file.mp4'
                f.write(f"file '{segment.absolute()}'\n")
        return concat_file

    def compile_videos(self, output_filename: str = "final_video.mp4",
                       add_transitions: bool = False) -> Path:
        """
        Compile les vidéos en utilisant FFmpeg

        Args:
            output_filename: Nom du fichier de sortie
            add_transitions: Ajouter des transitions entre les segments

        Returns:
            Path vers la vidéo finale
        """
        try:
            # Récupère les segments
            segments = self.get_segment_files()
            print(f"✓ {len(segments)} segments trouvés")

            # Crée le fichier de concaténation
            concat_file = self.create_concat_file(segments)
            print(f"✓ Fichier de concaténation créé: {concat_file}")

            # Chemin de sortie
            output_path = self.output_dir / output_filename

            if add_transitions:
                # Compilation avec transitions (crossfade)
                output_path = self._compile_with_transitions(segments, output_path)
            else:
                # Compilation simple (plus rapide)
                output_path = self._compile_simple(concat_file, output_path)

            print(f"✓ Vidéo finale créée: {output_path}")
            print(f"✓ Taille: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

            return output_path

        except Exception as e:
            print(f"✗ Erreur lors de la compilation: {e}", file=sys.stderr)
            raise

    def _compile_simple(self, concat_file: Path, output_path: Path) -> Path:
        """Compilation simple sans transitions"""
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',  # Copie directe sans réencodage (plus rapide)
            '-y',  # Écrase le fichier existant
            str(output_path)
        ]

        print(f"Exécution: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        return output_path

    def _compile_with_transitions(self, segments: List[Path], output_path: Path) -> Path:
        """Compilation avec transitions crossfade entre les segments"""

        # Durée de transition en secondes
        transition_duration = 0.5

        # Construit le filtre complexe FFmpeg
        filter_parts = []
        current_stream = "[0:v]"

        for i in range(len(segments) - 1):
            next_stream = f"[v{i}]"
            # Crossfade entre le segment actuel et le suivant
            filter_parts.append(
                f"{current_stream}[{i+1}:v]xfade=transition=fade:"
                f"duration={transition_duration}:offset={8*(i+1)-transition_duration}{next_stream}"
            )
            current_stream = next_stream

        filter_complex = ";".join(filter_parts)

        # Commande FFmpeg avec filtre complexe
        cmd = [
            'ffmpeg',
            *[item for seg in segments for item in ['-i', str(seg)]],  # Tous les inputs
            '-filter_complex', filter_complex,
            '-map', current_stream,  # Le dernier stream du filtre
            '-map', '0:a',  # Audio du premier segment
            '-c:v', 'libx264',  # Réencodage nécessaire pour les transitions
            '-preset', 'fast',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-y',
            str(output_path)
        ]

        print(f"Exécution avec transitions...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        return output_path

    def get_video_info(self, video_path: Path) -> dict:
        """Récupère les informations d'une vidéo"""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(video_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFprobe error: {result.stderr}")

        return json.loads(result.stdout)

    def cleanup_segments(self):
        """Supprime les fichiers de segments temporaires"""
        for segment_file in self.input_dir.glob("segment_*.mp4"):
            segment_file.unlink()
            print(f"✓ Supprimé: {segment_file}")

        concat_file = self.input_dir / "concat_list.txt"
        if concat_file.exists():
            concat_file.unlink()
            print(f"✓ Supprimé: {concat_file}")


def main():
    """Fonction principale pour utilisation en ligne de commande"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Compile 8 vidéos de 8 secondes en une seule vidéo'
    )
    parser.add_argument(
        '--input-dir',
        default='/tmp/video_segments',
        help='Répertoire contenant les segments (défaut: /tmp/video_segments)'
    )
    parser.add_argument(
        '--output-dir',
        default='/tmp/final_videos',
        help='Répertoire de sortie (défaut: /tmp/final_videos)'
    )
    parser.add_argument(
        '--output-name',
        default='final_video.mp4',
        help='Nom du fichier de sortie (défaut: final_video.mp4)'
    )
    parser.add_argument(
        '--transitions',
        action='store_true',
        help='Ajouter des transitions entre les segments'
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Supprimer les segments après compilation'
    )
    parser.add_argument(
        '--info',
        action='store_true',
        help='Afficher les informations de la vidéo finale'
    )

    args = parser.parse_args()

    try:
        compiler = VideoCompiler(args.input_dir, args.output_dir)

        # Compile les vidéos
        output_path = compiler.compile_videos(
            output_filename=args.output_name,
            add_transitions=args.transitions
        )

        # Affiche les informations si demandé
        if args.info:
            info = compiler.get_video_info(output_path)
            print("\nInformations de la vidéo:")
            print(json.dumps(info, indent=2))

        # Nettoyage si demandé
        if args.cleanup:
            print("\nNettoyage des segments...")
            compiler.cleanup_segments()

        # Retourne le chemin pour n8n
        print(f"\nOUTPUT_PATH={output_path}")
        return 0

    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
