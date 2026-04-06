from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

text = """
Space is vast and full of mysteries that continue to fascinate humans. It contains countless stars, planets, and galaxies spread across an endless expanse. The night sky gives us a small glimpse of this beauty, while scientists use telescopes and spacecraft to explore deeper into the universe. Planets orbit stars, comets travel through space, and black holes hold powerful gravitational forces. Despite many discoveries, much of space remains unknown, reminding us of how small yet curious we are in this immense universe.
Building on this curiosity, humans continue to push the boundaries of exploration and knowledge. Advanced missions and powerful telescopes are helping us uncover new planets and distant galaxies never seen before. Scientists search for signs of life beyond Earth, hoping to answer one of humanity’s biggest questions. Each discovery brings new insights, yet also reveals how much more there is to learn. As technology improves, our understanding of space will keep growing, inspiring future generations to explore the unknown.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20
)

chunks = splitter.split_text(text)

print(chunks)
 