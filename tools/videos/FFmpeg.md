## FFmpeg

> 2020.08.12

A complete, cross-platform solution to record, convert and stream audio and video.

Converting video and audio has never been so easy.

```
$ ffmpeg -i input.mp4 output.avi
```

### 合并视频和音频文件


有没有那种不需要转文件格式（保留现有WEBM格式)，直接将一段视频与音频合成为一段视频文件的工具或插件？

```
ffmpeg.exe -i video.webm  -i audio.weba -c copy out.webm
```

### 转文件编码格式为H265

```
D:\application\ffmpeg-20200809-6e951d0-win64-static\bin\ffmpeg.exe -i "TimeScapes 4k CineForm.avi" -c:v libx265 -c:a copy -preset veryslow -crf 0 out.mkv
D:\application\ffmpeg-20200809-6e951d0-win64-static\bin\ffmpeg.exe -i "TimeScapes 4k CineForm.avi"  -i TIMESCAPES_6TRK.wav -c:v libx265 out.mkv
```

### 转换文件码率

```
C:\app\ffmpeg-n4.4-19-g8d172d9409-win64-gpl-4.4\bin\ffmpeg.exe -i input.mp4  -b 3000K output.mp4

or

C:\app\ffmpeg-n4.4-19-g8d172d9409-win64-gpl-4.4\bin\ffmpeg.exe -i input.mp4  -b 3048K -minrate 3048K -maxrate 8800K -bufsize 4000K output.mp4
```

### 转换字幕格式

```
ffmpeg.exe -i "imput.vtt" "output.srt"
```

Reference:

https://ffmpeg.org/

https://trac.ffmpeg.org/wiki/Encode/H.265
