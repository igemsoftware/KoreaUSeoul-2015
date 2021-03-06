# <p align="center">KoreaUSeoul-2015</p>
<p align="center"><img width=300px height=300px src="http://compbio.korea.ac.kr/712/images/kuigem_bottom.png"></p>


#Gil (712)
##Introduction

Our team introduced a navigation system to the calculation of biological pathway. It calculates the optimal pathway from the source compound to the target compound by 4 criteria that we selected. 'Gil' shows nodes for chemicals and edges for reactions by adopting concept of network. 

This program can provide pathway which yields products you want from reactants that you can offer. :smile:

##Installation

###for everyone
We used the Web so that users, including ordinary people, can easily access to our software.

Click [Gil : The pathfinder for Synthetic Biologists](http://compbio.korea.ac.kr/712)

'Gil' is optimized for Chrome.

###for developers 

If you want to host a seperate copy of the server, Follow the instructions below:


---
#### 1. [Download](https://github.com/igemsoftware/KoreaUSeoul-2015/releases).

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

 -`name_to_C.tsv` : : tsv for auto complete. 

 -`tsv/(C number)_(C number).tsv` `(tsv/(start compound)_(end compound).tsv)` : tsv that contains the quantity of change of each reaction.
+ __BioBrick__

 -` (Gene ID).html` : html that connects to biobrick_parts webpage of gene id

+ __Gene_download__

 -`(R number).html` : html that contains the gene information corresponding to the reaction

+ __graph.php__ : Receives the data entered by the user and shows the results through json, js, tsv, mySQL. 

+ __index.html__


#### 3. Upload to mySQL server 
+ You must have to build a mySQL server. [mySQL](https://www.mysql.com/)

+ Change the default settings that suits for you  (rows 14~16, graph.php)

 -default mySQL server : miseq.korea.ac.kr 

 -default database : igem_712


+ 	How to upload mySQLdb.txt to the Server (in mySQL)


  1) Select your database ($USE 'your database name') and create a table named 'path_score_table'.
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

  2) Upload ‘mySQLdb.txt’ to 'path_score_table' of MySQL
```
load data local infile '/your Gil folder path/data/mySQLdb.txt' into table path_score_table IGNORE 1 LINES (path, showname, atp,      co2, nadh, nadph, net_name, reaction);
```

  3) Set index for faster calculation when the size of the database is massive.
```
alter table path_score_table add index index1(path);
```

#### 4. Trial using a sample
+ In the main page (index.html),

+ Type in the compound and click the one you want.
 - Sample for trial
 - C01399 -> C00022
 - C01399 -> C00124
 - C01399 -> C20680

+ For trial, just put ';C01399' into the 'from' input and  ';C00022' into the 'to' input.
+ Use the data that comes right after the semicolon(C number) and receives corresponding json data.


#### 5. Full data which are used in Gil program

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
  wget http://compbio.korea.ac.kr/712/download/[file_name]
  unzip [file_name]
 ```
  - [file_name] list
  - JSON_files(80G) -> JSON_files_release_v1.0.tar.gz
  - TSV files(40G) -> TSV_files_release_v1.0.tar.gz
  - mySQLdb.txt(34G) -> mySQLdb.txt
  - Biobrick ID file(80G) -> Biobrick_ID_file_release_v1.0.tar.gz
  - KEGG gene files(html)(5.5G) -> Gene_download_release_v1.0.tar.gz 
  - Reaction infomation table files(html)(44M) -> Reaction_information_table_release_v1.0.tar.gz
  - Compound information table files(html)(71M) -> Compound_information_table_release_v1.0.tar.gz
 





See [API documentation](http://2015.igem.org/wiki/images/6/6c/Gil_API_documentation.pdf) for detailed information.


---
##Library includes in ‘Gil’
---
+ css
 - [font_awesome.min.css](https://fortawesome.github.io/Font-Awesome/get-started/)
 - [introLoader.min.css](http://factory.brainleaf.eu/jqueryIntroLoader/)
 - [bootstarap.css](http://getbootstrap.com/css/)
 - [ jui.css / jennifer.theme.css](https://github.com/seogi1004/jui)
+ js 
 - [jquery.introloader.pack.min.js](http://factory.brainleaf.eu/jqueryIntroLoader/)
 - [jui.min.js (jennifer UI)](https://github.com/seogi1004/jui)
 - [whole.js](https://github.com/PMSI-AlignAlytics/dimple/wiki)
 - [skel.min.js](https://github.com/n33/skel)
 - [init.js](http://templated.co/)
 - [jquery.battatech.excelexport.js](https://github.com/battatech/battatech_excelexport)
 - [d3.js](http://d3js.org/)
 - [autocomplete.js](http://www.brightpointinc.com/clients/brightpointinc.com/library/autocomplete/)



