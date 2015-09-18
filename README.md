# <p align="center">KoreaUSeoul-2015</p>
<p align="center"><img width=300px height=300px src="http://compbio.korea.ac.kr/712/images/kuigem_bottom.png"></p>


#712
##Introduction

Our team introduced a navigation system to the calculation of biological pathway. It calculates the optimal pathway from the source compound to the target compound by 4 criteria that we selected. 'Gil' shows nodes for chemicals and edges for reactions by adopting concept of network. 

This program can provide pathway which yields products you want from reactants that you can offer. :smile:

##Installation

###for everyone
We used the Web so that users, including ordinary people, can easily access to our software.

Click [Gil : The pathfinder for Synthetic Biologists](http://compbio.korea.ac.kr/712)

###for developers 

If you want to host a seperate copy of the server, Follow the instructions below:


---
#### 1. Download in the [release pages](https://github.com/igemsoftware/KoreaUSeoul-2015/releases) or using "download ZIP" button, in the right of github.

#### 2. Folder structure
+ __CSS__ 
+ __R_info_html__

 -`(R number).html` : Information of the reaction.
+ __C_info_html__
 
 -`(C number).html` : Information of the compound.
+ __js__
 
 -`path.js` : : Draws a network graph based on json.

 -`search.js` : Loads ‘name_to_C.tsv’ for auto complete.
 
 -`whole(criteria).js` : Shows total quantity of change in each selected paths using a bar graph.
+ __json__

 -`(C number)_(C number).json` : Includes the information of the pathway.
+ __data__

 -`mySQLdb.txt` : txt that contains the information of the whole path. 

 -`before_screening.txt` : txt that contains the calculation result of the whole path.

 -`name_to_C.tsv` : : tsv for auto complete. 

 -`tsv/(C number)_(C number).tsv` `tsv/(start compound)_(end compound).tsv` : tsv that contains the quantity of change of each reaction.
+ __graph.php__ : Receives the data entered by the user and shows the results through json, js, tsv, mySQL. 

+ __index.html__


#### 3. Upload to mySQL server 
+ You must have to build a mysql server. [mySQL](https://www.mysql.com/)
+ mySQLdb.txt / before_screening.txt

 -Basic settings mySQL : miseq.korea.ac.kr

 -Basic settings database : igem_712

 -Basic settings table : path_score_table / valid_path


+ 	How to upload mySQLdb.txt

 1) Create a table named 'path_score_table'.
```
CREATE TABLE IF NOT EXISTS path_score_table (
      id int auto_increment,
      path VARCHAR(255)
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

  2) Upload ‘mySQLdb.tx’ to 'path_score_table' of MySQL
```
load data local infile '/your folder/data/mySQLdb.txt' into table path_score_table IGNORE 1 LINES (path, showname, atp,      co2, nadh, nadph, net_name, reaction);
```

  3) Set index for faster calculation when the size of the database is massive.
```
alter table path_score_table add index index1(path);
```

+ •	How to upload before_screening.txt

 1) Create a 'valid_path' table.
```
CREATE TABLE IF NOT EXISTS valid_path (
    id int auto_increment,
    path VARCHAR(255),
    number_of_valid VARCHAR(255),
    PRIMARY KEY (id)
 );
```    
 2)Upload ‘before_screening.txt’ to 'valid_path' table of MySQL.
```
load data local infile '/your 712 folder/data/before_screening.txt' REPLACE INTO TABLE valid_path IGNORE 1 LINES (path,      number_of_vaild);
```
 3) Set up index.
```
alter table valid_path add index index2(path);
```

#### 4. File path modification

The code in the line 192 of ‘graph.php’ :
```
$filepath = "path of your json folder".$input[1]."_".$output[1].".json";
```
Enter Path of your json folder

#### 5. Trial using a sample
+ In the main page (index.html),

+ Type in the compound and click the one you want.
 - Sample for trial
 - C06891 -> C20424
 - C16653 -> C16656
 - C00805 -> C04793
 - C02635 -> C04793

+ Use the data that comes right after the semicolon(C number) and receives corresponding json data.

#### 6. Full data which are used in Gil program

+ There are 7 kinds of data that we use 

 - JSON files

 - TSV files

 - mySQLdb.txt

 - Biobrick ID file and KEGG gene files(html)

 - Reaction infomation table files(html) and Compound information table files(html)
 
+ If you want to get full data that we use, download these files by doing the following 
 
 1) Download the zip archive.
 2) Extract files from the archive to where you want to hold the server files.

 If you are using a terminal, just write down the commands below.
 ```
 wget https://compbio.korea.ac.kr/712/download/<file_name.tar.gz>
 unzip <file_name.tar.gz>
 
 <file_name.tar.gz> list
 JSON_fileddd
 dddd
 ddd
 ddd
 
```    





그림파일 : 각 화면에서 차지하는 파일들.

See API documentation for detailed information.

<p align="center"><img src="http://postfiles15.naver.net/20150825_222/azure0777_1440475809932MJtIA_JPEG/git_hub.jpg?type=w2"></p>

---
##Library includes in ‘712’
---
+ css
 - [font_awesome.min.css](https://fortawesome.github.io/Font-Awesome/get-started/)
 - [introLoader.min.css](http://factory.brainleaf.eu/jqueryIntroLoader/)
 - [bootstarap.css](http://getbootstrap.com/css/)
 - [ jui.css / jennifer.theme.css](https://github.com/seogi1004/jui)
+ js 
 - [jquery.introloader.pack.min.js](http://factory.brainleaf.eu/jqueryIntroLoader/)
 - [jui.min.js (jennifer UI)/autocomplete.js](https://github.com/seogi1004/jui)
 - [whole.js](https://github.com/PMSI-AlignAlytics/dimple/wiki)
 - [skel.min.js](https://github.com/n33/skel)
 - [init.js](http://templated.co/)
 - [jquery.battatech.excelexport.js](https://github.com/battatech/battatech_excelexport)
 - [d3.js](http://d3js.org/)
 - [autocomplete.js](http://www.brightpointinc.com/clients/brightpointinc.com/library/autocomplete/)



