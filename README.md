# KoreaUSeoul-2015

---
#712-web

---
##installation 설치방법
---
###1. github 우측 하단에 git clone을 통해 다운 받습니다.

###2. 다운 받아지는 폴더 구조
+ `CSS` 
+ `R_info_html`

 -RXxXXX.html : 반응에 대한 정보가 들어갑니다.
+ `C_info_html`
 
 -CXXXXX.html : 해당 컴파운드에 대한 정보가 들어갑니다.
+ `js`
 
 -path.js : json을 기반으로 network그래프를 그립니다.

 -search.js : 자동완성기능을 위해 name_to_C.tsv를 불러들입니다.
+ `json`

 -CXXXXX_CXXXX.json : 경로에 대한 정보를 포함합니다.
+ `data`

 -mySQLdb.txt : 전체 경로에 대한 정보를 담고 있는 txt 

 -before_screening.txt : 총 계산결과를 담고 있는 txt

 -name_to_C.tsv : 자동완성기능을 위한 tsv 

 -data/tsv

 -CXXXXX_CXXXXX.tsv` `(start compound)_(end compound).tsv : 경로 내에서 반응이 진행됨에 따라 변화량을 담고 있는 tsv
+ `graph.php` : 사용자가 입력한 값을 받아 json, js, tsv, mySQL을 통해 결과를 표시합니다. 

 -index.html

###3. 테스트를 위한 sample다운받으면 안에 존재하는 (검색 가능한, 테스트할 수 있는) 경로

+ C06891   C20424

+ C16653   C16656

+ C00805   C04793

+ C02635   C04793

