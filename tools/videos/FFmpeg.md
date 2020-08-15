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

Reference:

https://ffmpeg.org/
