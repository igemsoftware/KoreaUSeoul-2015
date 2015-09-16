# KoreaUSeoul-2015

---
---
#712-web

---
##installation 설치방법
---
###1. github 우측 하단에 git clone을 통해 다운 받습니다.

###2. 다운 받아지는 폴더 구조
+ `CSS` 
+ `R_info_html`

 -(R number).html : 반응에 대한 정보가 들어갑니다.
+ `C_info_html`
 
 -(C number).html : 해당 컴파운드에 대한 정보가 들어갑니다.
+ `js`
 
 -path.js : json을 기반으로 network그래프를 그립니다.

 -search.js : 자동완성기능을 위해 name_to_C.tsv를 불러들입니다.
 
 -whole(criteria).js : 각 기준별로 선정된 경로 내에서 총 변화량을 bar graph를 통해서 보여줍니다.
+ `json`

 -(C number)_(C number).json : 경로에 대한 정보를 포함합니다.
+ `data`

 -mySQLdb.txt : 전체 경로에 대한 정보를 담고 있는 txt 

 -before_screening.txt : 총 경로 계산결과를 담고 있는 txt

 -name_to_C.tsv : 자동완성기능을 위한 tsv 

 -data/tsv

 -(C number)_(C number).tsv` `(start compound)_(end compound).tsv : 경로 내에서 반응이 진행됨에 따라 변화량을 담고 있는 tsv
+ `graph.php` : 사용자가 입력한 값을 받아 json, js, tsv, mySQL을 통해 결과를 표시합니다. 

 -index.html

###3. 테스트를 위한 sample다운받으면 안에 존재하는 (검색 가능한, 테스트할 수 있는) 경로

+ C06891 -> C20424

+ C16653 -> C16656

+ C00805 -> C04793

+ C02635 -> C04793

###4. mySQL 등록 

+ mySQLdb.txt / before_screening.txt

 -기본 지정 mySQL : miseq.korea.ac.kr

 -기본 지정 database : igem_712

 -기본 지정 table : path_score_table / valid_path


+ mySQLdb.txt 업로드 방법

 1) 'path_score_table' 라는 이름의 table을 만듭니다.
```
    CREATE TABLE IF NOT EXISTS path_score_table (
          id int auto_increment,
          path VARCHAR(255),
    showname VARCHAR(255),
          atp VARCHAR(255),
          co2 VARCHAR(255),
         nadh VARCHAR(255),
          nadph VARCHAR(255),
          net_name VARCHAR(255),
          reaction VARCHAR(255),
          PRIMARY KEY (id)
        );
```

  2) mySQLdb.txt를 mySQL의  'path_score_table'에 업로드합니다.
```
    load data local infile '/your folder/data/mySQLdb.txt' into table path_score_table IGNORE 1 LINES (path, showname, atp,      co2, nadh, nadph, net_name, reaction);
```

  3) database의 용량이 클 경우 웹에서의 속도를 빠르게 하기 위해 index를 설정합니다.
```
    alter table path_score_table add index index1(path);
```

+ before_screening.txt 업로드 방법

 1) 'valid_path' table을 만듭니다.
 ```
    CREATE TABLE IF NOT EXISTS valid_path (
        id int auto_increment,
        path VARCHAR(255),
	number_of_valid VARCHAR(255),
	PRIMARY KEY (id)
    );
```    
 2)before_screening.txt를 mySQL의 'valid_path' table에 업로드 합니다.
```
    load data local infile '/your 712 folder/data/before_screening.txt' REPLACE INTO TABLE valid_path IGNORE 1 LINES (path,      number_of_vaild);
```
 3) index를 설정합니다.
```
    alter table valid_path add index index2(path);
```


###5. sample을 통한 테스트 방법
+ 메인 검색화면 (index.html)에서 

+ 화학이름을 검색하고 원하는 물질을 클릭합니다.

+ 세미 콜론(;)를 기준으로 뒤엣 것(C number)을 받아 해당하는 json을 부릅니다.





그림파일 : 각 화면에서 차지하는 파일들.

 
더 자세한 내용은 API documentation
