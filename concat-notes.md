ffmpeg -y -f concat -safe 0 -i Local_to_merge.lst -c copy test_video/Local.mp4

NO:
ffmpeg -i videos/037.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts ivideos/037.ts
ffmpeg -i videos/038.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts ivideos/038.ts
ffmpeg -i "concat:ivideos/037.ts|ivideos/038.ts" -c copy -bsf:a aac_adtstoasc output.mp4



NO:
mkfifo 037 038
ffmpeg -i videos/037.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts 037 2> /dev/null & 
ffmpeg -i videos/038.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts 038 2> /dev/null & 
ffmpeg -f mpegts -i "concat:037|038" -c copy -bsf:a aac_adtstoasc output.mp4



Works:

ffmpeg -i videos/037.mp4 -i videos/038.mp4 -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mp4


ffmpeg -i videos/036.mp4 -i videos/037.mp4 -i videos/038.mp4 -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mp4

NO:
mp4box -cat videos/037.mp4 -cat videos/038.mp4 -new joined.mp4
