# KoreaUSeoul-2015

---
---
#712-web

---
##installation
---
####Download using git clone, in the bottom right of github.

####Folder structure
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

 -`data/tsv`

 -`(C number)_(C number).tsv` `(start compound)_(end compound).tsv` : tsv that contains the quantity of change of each reaction.
+ __graph.php__ : Receives the data entered by the user and shows the results through json, js, tsv, mySQL. 

+ __index.html__



그림파일 : 각 화면에서 차지하는 파일들.

See API documentation for detailed information.

<p align="center"><img src="http://postfiles15.naver.net/20150825_222/azure0777_1440475809932MJtIA_JPEG/git_hub.jpg?type=w2"></p>

---
##Library includes in ‘GIL’
---
+ css
 - [font_awesome.min.css](https://fortawesome.github.io/Font-Awesome/get-started/)
 - [introLoader.min.css](http://factory.brainleaf.eu/jqueryIntroLoader/)
 - [bootstarap.css](http://getbootstrap.com/css/)
 - [ jui.css / jennifer.theme.css](https://github.com/seogi1004/jui)
+ js 
 - [jquery.introloader.pack.min.js](http://factory.brainleaf.eu/jqueryIntroLoader/)
 - [jui.min.js (jennifer UI)/autocomplete.js](https://github.com/seogi1004/jui)
 - autocomplete.js
```
/**
 Copyright (c) 2014 BrightPoint Consulting, Inc.

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
 */
```

 - [whole.js](https://github.com/PMSI-AlignAlytics/dimple/wiki)
 - [skel.min.js](https://github.com/n33/skel)
 - [init.js](http://templated.co/)
 - [jquery.battatech.excelexport.js](https://github.com/battatech/battatech_excelexport)
 - [d3.js](http://d3js.org/)
