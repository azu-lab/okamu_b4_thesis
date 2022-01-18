TGFF_FILES=`find -wholename "./$1/*.tgff"`

rm ./DATA/$2.txt

for TGFF_FILE in $TGFF_FILES; do
    python3 python/test2.py ${TGFF_FILE} $2 >> ./DATA/$2.txt
done
