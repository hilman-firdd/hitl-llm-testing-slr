# Scopus export goes here

1. Run the three block queries in `data/search/scopus_blocks.txt` in Scopus Advanced search.
2. Combine them in Search history: `#1 AND #2 AND #3 AND PUBYEAR > 2020 AND PUBYEAR < 2027`.
3. Limit to Document type = Article and Conference paper, Language = English.
4. Export the combined set only: Export > CSV > select all information > Export.
5. Put the CSV file in this folder and run `python scripts/06_merge_scopus.py`.

The script refuses to treat the file as valid when fewer than 80% of the records contain a term from all three blocks
(a common mistake is exporting one block instead of the combined set).
