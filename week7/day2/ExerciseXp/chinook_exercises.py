# ============================================================
#  Chinook Database — SQLAlchemy Exercises
# ============================================================
import sqlalchemy
import pandas as pd

# ── Helper functions ─────────────────────────────────────────
def get_results(query):
    return pd.read_sql(query, engine)

def display_results(query, label=""):
    df = get_results(query)
    if label:
        print(f"\n{label}")
    print(df.to_string(index=False))
    print("\nSQL:", query)


# ============================================================
#  Exercise 1: Open the database
# ============================================================
print("=" * 55)
print("Exercise 1 — Connect to the database")
print("=" * 55)

engine = sqlalchemy.create_engine("sqlite:///chinook.db")
cur = engine.connect()
print("Connected successfully.")

# Reflect the existing schema — no automap needed
metadata = sqlalchemy.MetaData()
metadata.reflect(engine)

# Pull each table directly from metadata
Track       = metadata.tables["Track"]
Album       = metadata.tables["Album"]
Artist      = metadata.tables["Artist"]
InvoiceLine = metadata.tables["InvoiceLine"]


# ============================================================
#  Exercise 2: Table names
# ============================================================
print("\n" + "=" * 55)
print("Exercise 2 — All table names")
print("=" * 55)

for name in metadata.tables.keys():
    print(" •", name)


# ============================================================
#  Exercise 3: First 3 tracks
# ============================================================
print("\n" + "=" * 55)
print("Exercise 3 — First 3 tracks")
print("=" * 55)

query3 = sqlalchemy.select(Track).limit(3)
display_results(query3)


# ============================================================
#  Exercise 4: Track name + album title (first 20)
# ============================================================
print("\n" + "=" * 55)
print("Exercise 4 — Track name & album title (first 20)")
print("=" * 55)

query4 = (
    sqlalchemy.select(
        Track.c.Name.label("Track"),
        Album.c.Title.label("Album")
    )
    .join(Album, Track.c.AlbumId == Album.c.AlbumId)
    .limit(20)
)
display_results(query4)


# ============================================================
#  Exercise 5: First 10 track sales — name & quantity
# ============================================================
print("\n" + "=" * 55)
print("Exercise 5 — First 10 track sales (name + quantity)")
print("=" * 55)

query5 = (
    sqlalchemy.select(
        Track.c.Name.label("Track"),
        InvoiceLine.c.Quantity.label("Quantity")
    )
    .join(Track, InvoiceLine.c.TrackId == Track.c.TrackId)
    .limit(10)
)
display_results(query5)


# ============================================================
#  Exercise 6: Top 10 tracks sold
# ============================================================
print("\n" + "=" * 55)
print("Exercise 6 — Top 10 tracks by total quantity sold")
print("=" * 55)

query6 = (
    sqlalchemy.select(
        Track.c.Name.label("Track"),
        sqlalchemy.func.sum(InvoiceLine.c.Quantity).label("Times Sold")
    )
    .join(Track, InvoiceLine.c.TrackId == Track.c.TrackId)
    .group_by(Track.c.TrackId)
    .order_by(sqlalchemy.func.sum(InvoiceLine.c.Quantity).desc())
    .limit(10)
)
display_results(query6)


# ============================================================
#  Exercise 7: Top 10 selling artists
# ============================================================
print("\n" + "=" * 55)
print("Exercise 7 — Top 10 highest selling artists")
print("=" * 55)

query7 = (
    sqlalchemy.select(
        Artist.c.Name.label("Artist"),
        sqlalchemy.func.sum(InvoiceLine.c.Quantity).label("Total Sold")
    )
    .join(Track,  InvoiceLine.c.TrackId == Track.c.TrackId)
    .join(Album,  Track.c.AlbumId       == Album.c.AlbumId)
    .join(Artist, Album.c.ArtistId      == Artist.c.ArtistId)
    .group_by(Artist.c.ArtistId)
    .order_by(sqlalchemy.func.sum(InvoiceLine.c.Quantity).desc())
    .limit(10)
)
display_results(query7)

cur.close()
