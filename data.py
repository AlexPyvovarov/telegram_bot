import json


def get_data(file_path:str = "data.json", my_playlist_id:int|None = None) -> list[dict] | dict:
    with open(file_path, 'r') as _:
        data = json.load(_)
        if my_playlist_id != None:
            my_playlist = data.get("my_playlist")
            if my_playlist_id < len(my_playlist):
                return my_playlist[my_playlist_id]
        return data
    

def add_songs(
   song: dict,
   file_path: str = "data.json",
):
   data = get_data(file_path=file_path, my_playlist_id=None)
   songs = data.get("my_playlist")
   if songs:
       songs.append(song)
       with open(file_path, "w") as fp:
           json.dump(
               data,
               fp,
               indent=4,
               ensure_ascii=False,
           )
