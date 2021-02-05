BACKUP_WD=$(dirname $(readlink -f $0))
for x in $BACKUP_WD/ams/*/store/; do
  echo $x
  for p in $x/*.p; do
    p_name=$(basename "$p")
    echo "  cp $p_name $p_name.bak"
    cp "$p" "$p.bak"
  done
done
