# invoke converter
Invoke-RestMethod -Uri "https://raw.githubusercontent.com/r0manas/svg2xml/main/svg2xml.py" -OutFile "svg2xml.py"
python svg2xml.py $args[0]
