ffmpeg -i top.mp4 -vf 'pad=iw:2*ih [top]; movie=bottom.mp4 [bottom]; [top][bottom] overlay=0:main_h/2' final.mp4
