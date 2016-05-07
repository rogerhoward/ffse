# ffse



```
ffmpeg -i MyMovie.mkv -vf scale=-1:720 -c:v libx264 -crf 18 -preset veryslow -c:a copy MyMovie_720p.mkv
```

