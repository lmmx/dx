BACKUP_WD=$(dirname $(readlink -f $0))
for x in $BACKUP_WD/ams/*/store/; do
  echo $x
  for b in $x/*.p.bak; do
    b_name=$(basename "$b")
    echo "  rm $b_name"
    rm "$b"
  done
done
