/usr/local/bin/ffmpeg -i /Users/rogerhoward/Desktop/minions.mp4 -y -vf scale=-1:360 -c:v libx264 -crf 22 -c:a copy /Users/rogerhoward/Desktop/minions_default.mp4

ffmpeg('-i /Users/rogerhoward/Desktop/minions.mp4', '-y', '-vf scale=-1:360', '-c:v libx264', '-crf 22', '-c:a copy', '/Users/rogerhoward/Desktop/minions_default.mp4')