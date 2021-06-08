#!/bin/bash
#https://docs.google.com/presentation/d/1TNVgO1UMpuQsDulD3Tm-yqFvpZckuFEp3N_xk56xCoY/edit?usp=sharing

#https://docs.google.com/a/cloudxlab.com/presentation/d/128dmEz_L25hmZZ6OTzkChvKSXuFo3yeF62mEikn7wNI/edit?usp=sharing loading_saving_data
#https://docs.google.com/a/cloudxlab.com/presentation/d/10AKss5k4_b4lcFEruwLR48AFBJJwZM2hd9A7ySt6qcQ/edit?usp=sharing spark_advanced_programming_2
#https://docs.google.com/presentation/d/1f3xt5vIMFIzt1BfPpd3Mr0Q-XuySKpSMA3GiTL7DfK0/edit?usp=sharing spark_advanced_programming_1

# rm -rf rdd_more_operations running_on_cluster
# rm -rf loading_saving_data spark_advanced_programming_2 spark_advanced_programming_1

## 0. Extract Notes

#python extract_notes.py 10AKss5k4_b4lcFEruwLR48AFBJJwZM2hd9A7ySt6qcQ spark_advanced_programming_2
#python extract_notes.py 1f3xt5vIMFIzt1BfPpd3Mr0Q-XuySKpSMA3GiTL7DfK0 spark_advanced_programming_1

# python extract_notes.py 1QuGgM-CuVigVQCMj8xEchXLINrqmAVqwHAS36hfO6bc running_on_cluster

# python extract_notes.py 1QuGgM-CuVigVQCMj8xEchXLINrqmAVqwHAS36hfO6bc running_on_cluster

# python extract_notes.py 128dmEz_L25hmZZ6OTzkChvKSXuFo3yeF62mEikn7wNI loading_saving_data
# python extract_notes.py 1rK8zysBOYViMwS-Mlab1pVHByNNhaKS-yzOmmkiGKXQ sparksql_1
# python extract_notes.py 1AQjER033tWMiLFc5-0nuonPS3mnfsAtHla0_42vKDWs sparksql_2

python extract_notes.py 13eOi6RWxw9SLRRdRvqPfJ_oGvDuNluCW_yJgPWH4s3U spark_streaming_kafka
python extract_notes.py 1JwDDyKz1EjzX4EIw-hpEex73QTkb4wusxGYJb5l-36U sparkr
python extract_notes.py 1HDWXyi6rfGaEw0SjyOAbT3SGP8nvTwRRAFIsEPKSjb0 mllib
python extract_notes.py 1qW16Sv0bvIxvcwgpCnIOLjySwSLVXm4zjn5SJK3-lHU graphx
python extract_notes.py 1hRXo_0OnoMOuCEV2BEX0pbO46u-xqI7nRkwyoAJ-b-w aim_intro_1
python extract_notes.py 1VEVf9Vdf4CjSqdNmTMi0twQnFENC3R4qxbNSdL8uwjQ aim_ml_process
python extract_notes.py 1wdnYXdtcteQKKla6xsYUu8Te6Qxmp1TfLY587bJbmHI aim_end_to_end
python extract_notes.py 1G5OdnqgT3dkwSaea6yreM4pwW-8GPGjPQ02-XEooJmY aim_projects_forestfires
python extract_notes.py 1ra3_CViDlOlqyQqO15s1_6L6QOu7fUHGzilaMO0dEmk aim_projects_housing_azure
./concat_notes.sh aim_projects_forestfires aim_projects_housing_azure


python extract_notes.py 1wj9g4vk6RTNYG85v5KveA3LQBl606a-dh1CvBqKiibo classification
./concat_notes.sh aim_projects_forestfires classification

python extract_notes.py 1SHpt66tDkypD4CDg_tRWgtE3auHcHMITOIpl0pWp0as underpinning
./concat_notes.sh underpinning

python extract_notes.py 1NGWrducAtBZb3O-VJc6LGIVKjMQiC3UTEhycoC9ifnk constructs
./concat_notes.sh constructs


python extract_notes.py 1y6tXF7GkR0pLYJE6ljOyVZtZ1RGxiGual4T9ZVrrjHA challenges
./concat_notes.sh challenges

for d in constructs #aim_projects_forestfires aim_end_to_end aim_ml_process aim_intro_1 spark_streaming_kafka sparkr mllib graphx
do
	cd $d
	(for i in *.txt; do echo "======= $i =======";cat -s $i; done) >> all.txt
	cp all.txt all.txt.orig
	cd ..
done

### 1. Screenshots

#python create_screen_shots.py 1QuGgM-CuVigVQCMj8xEchXLINrqmAVqwHAS36hfO6bc running_on_cluster/screenshots 67
#python create_screen_shots.py 1TNVgO1UMpuQsDulD3Tm-yqFvpZckuFEp3N_xk56xCoY rdd_more_operations/screenshots
#python create_screen_shots.py 1f3xt5vIMFIzt1BfPpd3Mr0Q-XuySKpSMA3GiTL7DfK0 advanded_programming/screenshots
#https://docs.google.com/a/cloudxlab.com/presentation/d/10AKss5k4_b4lcFEruwLR48AFBJJwZM2hd9A7ySt6qcQ/edit?usp=sharing
#python create_screen_shots.py 10AKss5k4_b4lcFEruwLR48AFBJJwZM2hd9A7ySt6qcQ spark_advanced_programming_2/screenshots

python create_screen_shots.py 1rK8zysBOYViMwS-Mlab1pVHByNNhaKS-yzOmmkiGKXQ sparksql_1/screenshots
python create_screen_shots.py 1AQjER033tWMiLFc5-0nuonPS3mnfsAtHla0_42vKDWs sparksql_2/screenshots
python create_screen_shots.py 128dmEz_L25hmZZ6OTzkChvKSXuFo3yeF62mEikn7wNI loading_saving_data/screenshots
python create_screen_shots.py 1JwDDyKz1EjzX4EIw-hpEex73QTkb4wusxGYJb5l-36U sparkr/screenshots
python create_screen_shots.py 1HDWXyi6rfGaEw0SjyOAbT3SGP8nvTwRRAFIsEPKSjb0 mllib/screenshots
python create_screen_shots.py 1qW16Sv0bvIxvcwgpCnIOLjySwSLVXm4zjn5SJK3-lHU graphx/screenshots
python create_screen_shots.py 1g585NS_MwILVh6Q628aC5FOCrFZkrE_KFHARzG0ZxB4 spark_streaming_kafka/screenshots


##for i in *.wav; do nn=`echo $i|sed 's/MLIB 018_ *//g'`; mv "$i" "$nn"; done

## 2. Create Videos
for folder in sparksql_1 sparksql_2 loading_saving_data
do
cd $folder
python ../create_videos.py
cd ..
done 

## 3. Merge

#python ../merge_videos.py videos rdd_more_operations.mp4
#python ../merge_videos.py videos multi_videos Architecture:1-26 Launching:27-32 Localmode:33-39 Cluster-Mode-Standalone:40-42 Cluster-mode-YARN:43-45 Cluster-Mode-Mesos-AWS:46-47,55 Deployment-modes:48-54
#python ../merge_videos.py videos multi_videos UnderstandingPersistance:1-16 PersistanceStorageLevel:17-37 DataPartitioning:38-44 DataPartitioningExample:45-60 CustomPartitioner:61-63
#python ../merge_videos.py videos multi_videos SharedVariables:1 Accumulators:2-16 CustomAccumulators:17-24 BroadcastVariables:25-34 BroadcastVariablesExample:35-40 KeyPerformanceConsiderationsParallelism:41-44 KeyPerformanceConsiderationsPartitions:45-50 SerializationFormat:51-53 MemoryManagement:54-56 HardwareProvisioning:57-59
python ../merge_videos.py videos multi_videos CommonDataSources:1-8 CommonFileFormats:9-27 SequenceObjectFile:28-38 HadoopFormats:39-42 ProtocolBuffers:43-45 Compression:46-49 FileSystem:50-54
python ../merge_videos.py videos multi_videos HadoopFormats:39-42
#sparksql1
python ../merge_videos.py videos multi_videos introduction:1-4 dataframe_intro:5-9 getting_started:10-17 create_df_from_json:18-20 dataframe_ops:21-25 sql_queries_df:26-29 datasets:30-33 rdd_df_interop:34-36 infer_schema_reflection:37-49 programatic_schema:50-56

SparkSQL

#sparksql2
python ../merge_videos.py videos multi_videos loadingxml:2-5 avro:6-9 datasources:10-14 hivetables:15-18 jdbc:19-21 dist_sql:22-25 

#sparkR

python ../merge_videos.py videos multi_videos Sparkr:1-18
python ../merge_videos.py videos multi_videos Machine_learning:1-11 machine_learning_applications:12-17 machine_learning_types:18-24 mllib:25-27 collaborative_filtering:28-30 mllib_more:32-38
python ../merge_videos.py videos multi_videos Graphx:1-12

# Convert to v1
# for i in 038 044 054
# do
# ffmpeg -i screencast_synced/$i.mp4 -vcodec copy -acodec copy -ss 0 -to 30 screencast_syncedv1/$i.mp4
# done


python extract_notes.py 1y6tXF7GkR0pLYJE6ljOyVZtZ1RGxiGual4T9ZVrrjHA challenges
./concat_notes.sh challenges

python /Users/sandeep/projects/slidestovideos/extract_notes.py 1YTEHdCIwcIL8F5qj6IIc7ArtlernrDxfZt7q_U-fjMM zk_single_system_image
./concat_notes.sh zk_single_system_image