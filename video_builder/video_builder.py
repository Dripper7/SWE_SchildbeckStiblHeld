import subprocess 


def build():
	subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "uploads/%02d.png","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "downloads/video.avi"])


if __name__ == "__main__":
	build()

