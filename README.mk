# pdf_table_extractor
1.What this do
```
This script will convert a pdf file into a binary pic with 0 represent white dot, and 1 for
any pixel that's not white. and then try to find the mesh of the table and convert it
accordingly. So with this setup things to NOTE:
1) stuff in any shaded area however light is the color, no text can be extracted
2) always assume the table is like a mesh, so merged cell won't display properly
other than these two problems, feel free to use this to extract CSV table from your PDF
```
2.How to use
```
Usage: bbpy tableFromPdf.py [options] -i <input pdf file>
OPIONS:
    -r : converting resolution, default to 300, which seems to be ideal
    -f : starting page number in pdf to convert default to 1
    -l : ending page number in pdf to convert default to 1
    -o : output csv file, default to out.csv
    -tbt : table boundry pixel length threshold, anything large will be treated as an edge,
    default to 500 pixel, which seems good (Need to have a better calculation here)
    -h | --help : print usage
```