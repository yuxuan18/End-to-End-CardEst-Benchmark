# setup options
if [ -z "$DB_PATH" ]; then
    DB_PATH="."
fi
IMDB_DATASETS_DIRECTORY=$DB_PATH/imdb_data

if [-z "$BENCHMARK"]; then
    BENCHMARK="JOB"
fi

# install anaconda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
. ~/.bashrc

# setup conda env
conda create -y -n join
conda activate join
conda install -y -c conda-forge postgresql
conda install -y python=3.11

# setup database
if $BENCHMARK == "JOB"; then
    initdb -D $DB_PATH/postgres_db
    pg_ctl -D $DB_PATH/postgres_db -l $DB_PATH/postgres_db/logfile start
    wget http://homepages.cwi.nl/~boncz/job/imdb.tgz
    mkdir $DB_PATH/imdb_data
    tar -xvzf imdb.tgz -C $DB_PATH/imdb_data
    psql -d postgres -f $DB_PATH/imdb_data/schematext.sql
    cat scripts/sql/imdb_create.sql | sed "s|\$IMDB_DATASETS_DIRECTORY|$IMDB_DATASETS_DIRECTORY|g" | psql -d postgres
    psql -d postgres -f scripts/sql/imdb_index.sql
fi

if $BENCHMARK == "STATS"; then
    initdb -D $DB_PATH/postgres_db
    pg_ctl -D $DB_PATH/postgres_db -l $DB_PATH/postgres_db/logfile start
    psql -d postgres -f datasets/stats_simplified/stats.sql
    psql -d postgres -f scripts/sql/stats_load.sql
    psql -d postgres -f scripts/sql/stats_index.sql
fi

if $BENCHMARK == "BOTH"; then
    initdb -D $DB_PATH/postgres_db
    pg_ctl -D $DB_PATH/postgres_db -l $DB_PATH/postgres_db/logfile start
    wget http://homepages.cwi.nl/~boncz/job/imdb.tgz
    mkdir $DB_PATH/imdb_data
    tar -xvzf imdb.tgz -C $DB_PATH/imdb_data
    psql -d postgres -f $DB_PATH/imdb_data/schematext.sql
    cat scripts/sql/imdb_create.sql | sed "s|\$IMDB_DATASETS_DIRECTORY|$IMDB_DATASETS_DIRECTORY|g" | psql -d postgres
    psql -d postgres -f scripts/sql/imdb_index.sql
    psql -d postgres -f datasets/stats_simplified/stats.sql
    psql -d postgres -f scripts/sql/stats_load.sql
    psql -d postgres -f scripts/sql/stats_index.sql
fi