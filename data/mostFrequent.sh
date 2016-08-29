cat $1 | tr -dc [:alnum:][" \n"] | tr [:upper:] [:lower:] | sed "s/ /\n/g" | sort | uniq -c | sort -nr | head -n 100
