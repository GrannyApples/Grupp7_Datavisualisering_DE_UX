import pandas as pd
from src.schemas.movie_schema import MovieSchema

GENRE_MAP = {
    12: "Adventure", 14: "Fantasy", 16: "Animation",
    28: "Action", 27: "Horror", 35: "Comedy",
    10751: "Family", 878: "Sci-Fi", 53: "Thriller",
    80: "Crime", 18: "Drama", 10749: "Romance"
}

CATEGORY_MAP = {
    "Dark Fantasy": [
        "Demon Slayer: Kimetsu no Yaiba Infinity Castle",
        "JUJUTSU KAISEN: Execution", "KPop Demon Hunters",
        "Dracula", "Frankenstein", "Coraline", "Twilight",
        "The Mummy", "Corpse Bride",
        "Chainsaw Man - The Movie: Reze Arc",
        "The Twilight Saga: Breaking Dawn - Part 1",
        "Jujutsu Kaisen 0",
        "Demon Slayer -Kimetsu no Yaiba- The Movie: Mugen Train",
        "The Bride!", "Blind Vaysha", "Hatching"
    ],
    "Fantasy Epic": [
        "Avatar: Fire and Ash",
        "The Lord of the Rings: The Fellowship of the Ring",
        "The Lord of the Rings: The Two Towers",
        "The Lord of the Rings: The Return of the King",
        "Harry Potter and the Philosopher's Stone",
        "Harry Potter and the Chamber of Secrets",
        "Harry Potter and the Prisoner of Azkaban",
        "Harry Potter and the Goblet of Fire",
        "Harry Potter and the Order of the Phoenix",
        "Harry Potter and the Half-Blood Prince",
        "Harry Potter and the Deathly Hallows: Part 1",
        "Harry Potter and the Deathly Hallows: Part 2",
        "The Hobbit: An Unexpected Journey",
        "The Hobbit: The Desolation of Smaug",
        "The Hobbit: The Battle of the Five Armies",
        "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe",
        "How to Train Your Dragon", "How to Train Your Dragon 2",
        "Wicked", "Wicked: For Good", "Princess Mononoke",
        "Howl's Moving Castle", "Ne Zha 2", "Ramayana",
        "Kantara - A Legend: Chapter 1", "Solo Leveling -ReAwakening-",
        "The Legend of Hei 2", "Flow", "Versa",
        "Cosmic Princess Kaguya!", "Turbulence"
    ],
    "Sword and Sorcery": [
        "Red Sonja", "Deathstalker", "Doctor Strange",
        "Doctor Strange in the Multiverse of Madness",
        "Wonder Woman", "Thor: Love and Thunder",
        "Batman v Superman: Dawn of Justice",
        "Pirates of the Caribbean: The Curse of the Black Pearl",
        "Pirates of the Caribbean: Dead Man's Chest",
        "Pirates of the Caribbean: At World's End",
        "Pirates of the Caribbean: On Stranger Tides",
        "Kong: Skull Island", "The Green Mile",
        "Kung Fu Hustle", "The Mask", "Red One",
        "E.T. the Extra-Terrestrial"
    ],
    "Fairy Tale": [
        "Spirited Away", "Frozen", "Beauty and the Beast",
        "Cinderella", "Aladdin", "Snow White", "Shrek", "Shrek 2",
        "Moana 2", "Brave", "The Wizard of Oz", "Alice in Wonderland",
        "The Boy and the Heron", "My Neighbor Totoro",
        "Puss in Boots: The Last Wish", "Turning Red",
        "The Super Mario Bros. Movie", "The Super Mario Galaxy Movie",
        "Kung Fu Panda 4", "Ratatouille", "Soul", "Elemental",
        "Charlie and the Chocolate Factory",
        "The SpongeBob Movie: Search for SquarePants",
        "A Minecraft Movie", "Smurfs", "Ted", "Ted 2",
        "Teddy's Christmas", "Tom and Jerry: Forbidden Compass",
        "Miraculous World: Tokyo, Stellar Force",
        "You Drive Me Crazy", "In Your Dreams", "Dust Bunny", "Troll 2"
    ]
}

def get_category(title, genres=""):
    
    for category, titles in CATEGORY_MAP.items():
        if title in titles:
            return category

    
    g = genres.lower()

    if "horror" in g or ("thriller" in g and "fantasy" in g):
        return "Dark Fantasy"
    elif "animation" in g or "family" in g or "comedy" in g:
        return "Fairy Tale"
    elif "action" in g and "adventure" in g:
        return "Sword and Sorcery"
    else:
        return "Fantasy Epic"

class Transform:
    @staticmethod
    def to_dataframe(data):
        validated_rows = []
        invalid_count = 0
        for movie in data:
            try:
                validated = MovieSchema(
                    movie_id=movie.get("id"),
                    title=movie.get("title"),
                    release_date=movie.get("release_date"),
                    rating=movie.get("vote_average"),
                    popularity=movie.get("popularity"),
                    genre_ids=movie.get("genre_ids", [])
                )
                row = validated.model_dump()
                genre_names = [GENRE_MAP.get(gid, str(gid)) for gid in (row["genre_ids"] or [])]
                row["genres"] = ", ".join(genre_names) if genre_names else "Unknown"
                row["category"] = get_category(row["title"], row["genres"])
                validated_rows.append(row)
            except Exception as e:
                invalid_count += 1

        print(f"Valid rows: {len(validated_rows)}")
        print(f"Invalid rows skipped: {invalid_count}")
        df = pd.DataFrame(validated_rows)
        df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
        df = df.drop(columns=["genre_ids"])
        return df
