container_name=ce-benchmark-9

for f in *.txt; do
    sudo docker cp $f $container_name:/var/lib/pgsql/13.1/data/$f
done

for f in ../datasets/stats_simplified/*.csv; do
    filename=$(basename -- "$f")
    sudo docker cp $f $container_name:/$filename
done