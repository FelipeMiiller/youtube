from pytube import YouTube, Playlist
from tqdm import tqdm
from moviepy.editor import VideoFileClip
import os


def show_progress_bar(stream, _chunk, _file_handle, bytes_remaining, pbar):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100

    pbar.n = bytes_downloaded
    pbar.set_description(f"Baixando ({percentage_of_completion:.2f}%)")
    pbar.refresh()


def pasta(path="youtube"):
    try:
        full_path = os.path.join(os.getcwd(), path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print("Diretório criado:", full_path)
        else:
            print("Diretório já existente:", full_path)

        return full_path

    except OSError as e:
        print("Erro: Criando diretório.", path)
        print(e)
        return None


def file_exists(path):
    return os.path.exists(path)


def download_video(url, output_path=None, video_only=True):
    try:
        # Verifica se a URL é de uma playlist
        if 'list=' in url:
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                download_single_video(video_url, output_path, video_only)
        else:
            download_single_video(url, output_path, video_only)

    except Exception as e:
        print("Ocorreu um erro durante o download:", e)


def download_single_video(url, output_path=None, video_only=True):
    try:
        yt = YouTube(url)

        if video_only:
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.get_lowest_resolution()

        filename = stream.default_filename
        output_path = pasta()

        # Caminho completo do arquivo
        path_stream = os.path.join(output_path, filename)

        # Verifica se o arquivo já existe
        if file_exists(path_stream):
            print(
                f"O arquivo {filename} já existe. Pulando para o próximo vídeo.")
            return

        # Download do vídeo ou áudio
        with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Baixando") as pbar:
            yt.register_on_progress_callback(lambda stream, chunk, bytes_remaining: show_progress_bar(
                stream, chunk, None, bytes_remaining, pbar))
            stream.download(output_path, filename=path_stream)
        print(f"Baixando: {path_stream}")

        # Conversão para MP3 se for áudio
        if not video_only:
            video_clip = VideoFileClip(path_stream)
            audio_clip = video_clip.audio
            # Substitui a extensão .mp4 por .mp3
            mp3_output_path = os.path.splitext(path_stream)[0] + ".mp3"

            audio_clip.write_audiofile(mp3_output_path)
            audio_clip.close()
            video_clip.close()

            print(f"Conversão para MP3 concluída: {mp3_output_path}")

    except Exception as e:
        print(f"Ocorreu um erro durante o download do vídeo {url}: {e}")


if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Baixar vídeos de uma playlist do YouTube (Melhor Qualidade)")
        print("2. Baixar áudios de uma playlist do YouTube")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            playlist_url = input("Digite a URL da playlist do YouTube: ")
            download_video(playlist_url, video_only=True)
        elif choice == '2':
            playlist_url = input("Digite a URL da playlist do YouTube: ")
            download_video(playlist_url, video_only=False)
        elif choice == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
