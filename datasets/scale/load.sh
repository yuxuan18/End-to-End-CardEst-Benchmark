start_scale=$1
end_scale=$2
data_path=$3
username=$4
dbname=$5

echo "drop index"
for i in $(seq $start_scale $end_scale)
do
    psql -d $dbname -U $username -f drop_index.sql
    echo "loading from $data_path/badges_$i.csv"
    psql -d $dbname -U $username -c "\copy badges from '$data_path/badges_$i.csv' with CSV header;"
    echo "loading from $data_path/comments_$i.csv"
    psql -d $dbname -U $username -c "\copy comments from '$data_path/comments_$i.csv' with CSV header;"
    echo "loading from $data_path/users_$i.csv"
    psql -d $dbname -U $username -c "\copy users from '$data_path/users_$i.csv' with CSV header;"
    echo "loading from $data_path/tags_$i.csv"
    psql -d $dbname -U $username -c "\copy tags from '$data_path/tags_$i.csv' with CSV header;"
    echo "loading from $data_path/posts_$i.csv"
    psql -d $dbname -U $username -c "\copy posts from '$data_path/posts_$i.csv' with CSV header;"
    echo "loading from $data_path/votes_$i.csv"
    psql -d $dbname -U $username -c "\copy votes from '$data_path/votes_$i.csv' with CSV header;"
    echo "loading from $data_path/postHistory_$i.csv"
    psql -d $dbname -U $username -c "\copy posthistory from '$data_path/postHistory_$i.csv' with CSV header;"
    echo "loading from $data_path/postLinks_$i.csv"
    psql -d $dbname -U $username -c "\copy postlinks from '$data_path/postLinks_$i.csv' with CSV header;"
done
echo "create index"
psql -d $dbname -U $username -f create_index.sql