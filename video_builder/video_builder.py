import subprocess 


def build():
	fps, duration = 2, 5
	subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "uploads/%02d.png","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "downloads/video_new.avi"])


if __name__ == "__main__":
	build()
	print("All well!")
