
Input in the form:

Artist|Song Title
Artist Feat. Other Artist|Another Song Title
Artist vs. DJ|More Song Titles


$ cat /tmp/top20.csv | while read line; do artist=$(echo "$line" | cut -d'|' -f1 | sed -e 's/ feat.*//i' -e 's/ vs.*//i'); song=$(echo "$line" | cut -d'|' -f2); echo "Artist: $artist === Song: $song" >&2; echo "$artist" | ~/projects/mvid_dl/mvid_dl.py | grep -i "$song" | while read url name; do youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "$url"; done; done

$ cat /tmp/top20.csv | while read line
> do
>     artist=$(echo "$line" | cut -d'|' -f1 | sed -e 's/ feat.*//i' -e 's/ vs.*//i')
>     song=$(echo "$line" | cut -d'|' -f2)
>     echo "Artist: $artist === Song: $song" >&2
>     echo "$artist" | ~/projects/mvid_dl/mvid_dl.py | grep -i "$song" | while read url name
>     do
>         youtube-dl --recode-video mp4 --output "${name}.mp4" --continue -f best "$url"
>     done
> done
