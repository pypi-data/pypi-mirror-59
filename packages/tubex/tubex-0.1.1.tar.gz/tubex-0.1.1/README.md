# Tubex

Command Line Interface to download and tag MP3 from youtube.

```
tubex download <youtube_playlist_url> --album <album_name> --artist <artist_name>
```

## Example
```bash
$ pipx install tubex

$ tubex download https://www.youtube.com/playlist?list=PLSdmnemG6jbv1-GRf23jwDsYWkjz7mblP \
  --album test --artist mixed
 
# Enjoy the music (e.g using `vlc`)
$ vlc tubex_out
```

