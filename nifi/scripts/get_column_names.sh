#echo "Reading file=$1....."
# print column names  from a CSV file (columms delimited by |)

if [ $2 ]
then
    sep=$2
else
    sep=","
fi


cat "$1" | head -1 | awk -F$sep '
BEGIN{
   counter=1
}
{ 
  for(i=1; i <= NF; i++) 
      print counter++ "). " $i
      
}'
