<!DOCTYPE HTML>

<!--
	Transit by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
-->
<html lang="en">
    <head>
        <!-- Get values from index.html page by bnmin Jul 23, 2015-->
        <?php
    $input = explode(';',$_GET["start_compound"]);
    $output = explode(';',$_GET["end_compound"]);
    $servername = "miseq.korea.ac.kr";
    $username = "root";
    $dbname = "igem_712";

    $conn = new mysqli($servername, $username, "", $dbname);

    if ($conn->connect_eror) {
       die("Connection failed: " . $conn->connect_error);
    }

    ?>
        <script>
            var input = "<?php echo $input[1]; ?>";
            var output = "<?php echo $output[1]; ?>";
        </script>
        <script charset="utf-8" src="http://d3js.org/d3.v3.min.js"></script>
        <script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"
            type='text/javascript'></script>
        <meta charset="UTF-8">
        <title>712 : The pathfinder for Synthetic Biologists</title>
        <meta content="text/html; charset=utf-8" http-equiv="content-type"/>
        <link href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css"
            rel="stylesheet">
        <script src="//code.jquery.com/jquery-1.10.2.js"></script>
        <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <link href="css/introLoader.min.css" rel="stylesheet">
        <link href="jui.css" rel="stylesheet"/>
        <link href="jennifer.theme.css" rel="stylesheet"/>
        <script src="js/skel.min.js"></script>
        <script src="js/skel-layers.min.js"></script>
        <script src="js/init.js"></script>
        <script src="js/jquery.introLoader.pack.min.js"></script>
        <script src="js/jquery.battatech.excelexport.js" type="text/javascript"></script>
        <script src="js/jui.min.js"></script>
        <script src="js/autocomplete.js" type="text/javascript"></script>

        <script>
            $(function () {
                $(document).tooltip();
            });
            $(document).ready(function () {
                $("#element").introLoader({
                    animation: {
                        name: 'simpleLoader',
                        options: {
                            exitFx: 'slideUp',
                            ease: "easeInOutCirc",
                            style: 'dark',
                            delayBefore: 1000,
                            exitTime: 500
                        }
                    },

                    spinJs: {
                        lines: 13, // The number of lines to draw
                        length: 20, // The length of each line
                        width: 10, // The line thickness
                        radius: 30, // The radius of the inner circle
                        corners: 1, // Corner roundness (0..1)
                        color: '#fff', // #rgb or #rrggbb or array of colors
                    }
                });
            });
        </script>
        <style>
            .col {
                padding: 50px;
            }
        </style>

        <link href="http://compbio.korea.ac.kr/712/logo/favicon.ico" rel="shortcut icon"
            type="image/x-icon">

    </head>
    <body class="jui">
        <div class="introLoading" id="element"></div>

        <!-- Header -->
        <header id="header">
            <h1>
                <a href="index.html"><img height=40% src="images/gilWhite.png" width=7%/></a>
            </h1>

            <nav id="nav">
                <ul>
                    <li>
                        <a href="index.html">Home</a>
                    </li>
                    <li>
                        <a href="tutorial.html">Tutorial</a>
                    </li>
                    <li>
                        <a href="aboutus.html">About 길</a>
                    </li>
                </ul>
            </nav>
        </header>
        <script>
            jui.ready(["uix.tab"], function (tab) {
                tab_1 = tab("#score1", {
                    event: {
                        change: function (data) {}
                    },
                    target: "#score2",
                    index: 1
                });
            });
        </script>
        <!-- Main -->
        <section class="wrapper" id="one" style="background-color:#f9f9f9;">
            <header class="major">
            </header>

            <ul class="actions">

                <form action="graph.php" align="center" method="get" name="searchForm">
                    <section id="three">
                        <div align="center" id="Form" width="75%">
                            <div id="auto3">From</div>
                            <div autocomplete="off" class="from" id="auto" name="input" type="text"></div>
                            <div id="auto4">To</div>
                            <div autocomplete="off" class="to" id="auto2" name="output" type="text"></div>

                            <div id="search">
                                <input class="button" name="button" onclick='verify()' type="submit"
                                    value="Search">
                                <script src="js/search.js" type="text/javascript"></script>
                            </div>
                        </div>

                        <div class="wrapper">
                            <div class="row 150%">

                                <div class="8u 12u$(medium)">
                                    <div class="a" id="content" style="background-color:white;">
                                        <div class="navbar">
                                            <p>When you press the button, the path corresponding to it is highlighted.
                                            </p>
                                            <div class="inline">
                                                <i class="icon fa-map-marker" title="highlihgt button"></i>
                                                <div class="group">
                                                    <a class="btn mini" onclick="hlpath1()"
                                                        title="Highlight pathway with the 1st largest ATP production">ATP_1</a>
                                                    <a class="btn mini" onclick="hlpath2()"
                                                        title="Highlight pathway with the 2nd largest ATP production">ATP_2</a>
                                                    <a class="btn mini" onclick="hlpath3()"
                                                        title="Highlight pathway with the 3rd largest ATP production ">ATP_3</a>
                                                </div>
                                                <div class="group">
                                                    <a class="btn mini" onclick="hlpath4()"
                                                        title="Highlight pathway with the 1st smallest loss">CO2_1</a>
                                                    <a class="btn mini" onclick="hlpath5()"
                                                        title="Highlight pathway with the 2nd smallest loss">CO2_2</a>
                                                    <a class="btn mini" onclick="hlpath6()"
                                                        title="Highlight pathway with the 3rd smallest loss">CO2_3</a>
                                                </div>
                                                <div class="group">
                                                    <a class="btn mini" onclick="hlpath7()"
                                                        title="Highlight pathway with the 1st largest production">NADH_1</a>
                                                    <a class="btn mini" onclick="hlpath8()"
                                                        title="Highlight pathway with the 2nd largest production">NADH_2</a>
                                                    <a class="btn mini" onclick="hlpath9()"
                                                        title="Highlight pathway with the 3rd largest production">NADH_3</a>
                                                </div>
                                                <div class="group">
                                                    <a class="btn mini" onclick="hlpath10()"
                                                        title="Highlight pathway with the 1st largest production">NADPH_1</a>
                                                    <a class="btn mini" onclick="hlpath11()"
                                                        title="Highlight pathway with the 2nd largest production">NADPH_2</a>
                                                    <a class="btn mini" onclick="hlpath12()"
                                                        title="Highlight pathway with the 3rd largest production">NADPH_3</a>
                                                </div>
                                                <a class="btn mini focus" onclick="hlecoli()"
                                                    title="Highlight pathways that exist in E.coli">
                                                    <i class="icon fa-search"></i>
                                                    E.coli Metabolism</a>

                                            </div>

                                        </div>

                                    </div>
                                    <!-- a div close-->
                                    <?php $filepath = "json/".$input[1]."_".$output[1].".json";
  if(file_exists($filepath))
  {
    echo '<script type="text/javascript" src="js/path.js"></script>';
  }
  else
  {
    echo"<script>parent.window.location.href='error.html'</script>";
  }
  ?>

                                </div>
                                <!-- medium close-->

                                <!--path infromation div-->

                                <div class="msgbox detail 4u$ 12u$(medium)">

                                    <div class="head">
                                        <div class="left">
                                            <h3>Pathway Information : Result From
                                                <?php echo $input[0]; ?>
                                                to
                                                <?php echo $output[0]; ?></h3>
                                        </div>
                                        <!-- left div close-->
                                    </div>
                                    <!-- head div close-->

                                    <div id="score">
                                        <ul class="tab top" id="score1">
                                            <li>
                                                <a href="#score-1" onclick="">ATP</a>
                                            </li>
                                            <li>
                                                <a href="#score-2" onclick="">NADH</a>
                                            </li>
                                            <li>
                                                <a href="#score-3" onclick="">NADPH</a>
                                            </li>
                                            <li>
                                                <a href="#score-4" onclick="">CO2</a>
                                            </li>

                                        </ul>
                                        <div id="score2">
                                            <div id="score-1">
                                                <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_atp%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>Path</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>

                                                <a class="btn focus" data-role="button" data-transition="fade" href="#atp_page"
                                                    style="float:right;">
                                                    <i class="icon fa-bar-chart"></i>
                                                    More Details</a>

                                            </div>
                                            <!-- div.score1 close-->

                                            <div id="score-2">
                                                <!---다른 기준에 대한정보-->

                                                <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_nadh%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>PATH</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>

                                                <a class="btn focus" href="#nadh_page" style="float:right;">
                                                    <i class="icon fa-bar-chart"></i>
                                                    More Details</a>

                                            </div>
                                            <!-- div.score2 close-->

                                            <div id="score-3">

                                                <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_nadph%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>PATH</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                                <a class="btn focus" href="#nadph_page" style="float:right;">
                                                    <i class="icon fa-bar-chart"></i>
                                                    More Details</a>

                                            </div>
                                            <!-- div.score3 close-->

                                            <div id="score-4">

                                                <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_co2%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>PATH</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                                <a class="btn focus" href="#co2_page" style="float:right;">
                                                    <i class="icon fa-bar-chart"></i>
                                                    More Details</a>

                                            </div>
                                            <!-- div.score4 close-->
                                        </div>

                                        <p align="right">If you want more information about this pathway, Click
                                        </p>

                                        <!--reaction and compound informati-->

                                    </div>
                                    <div class="head">
                                        <div class="left">
                                            <h3 title="Click the edge you wish to know">Reaction Information</h3>
                                        </div>
                                        <div class="right" style='font-size:15px; float:right;'>ΔG
                                            <a style='color:red;,size:20px;'
                                                title="ver1 is the formation energy of compound in standard conditions, pH7 and ionic strengh 0.1M.">ver1</a>
                                            /
                                            <a style='color:blue;'
                                                title="ver2 is the formation energy of compound in standard conditions, pH0 and ionic strength 0M.">ver2</a>
                                        </div>
                                        <p></p>
                                    </div>

                                    <div id="linkinfo">
                                        <table>
                                            <caption>R_number</caption>
                                            <tr>
                                                <td>Equation</td>
                                                <td>ex. Polyphosphate + n H2O
                                                    <=>
                                                        (n+1) Oligophosphate</td>
                                                </tr>
                                                <tr>
                                                    <td>C_Equation</td>
                                                    <td>ex. C00404 + n C00001
                                                        <=>
                                                            (n+1) C02174</td>
                                                    </tr>
                                                    <tr>
                                                        <td>deltaG</td>
                                                        <td>
                                                            No data /
                                                            <a style='color:red;'>ver1</a>
                                                            /
                                                            <a style='color:blue;'>ver2</a>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>Gene Download</td>
                                                        <td>
                                                            <a class="btn focus">
                                                                <i class="icon fa-download"></i>
                                                                Download
                                                            </a>
                                                        </td>
                                                    </tr>
                                                </table>
                                                ~
                                            </div>

                                            <div class="head">
                                                <div class="left">
                                                    <h3 title="Click the node you wish to know">Compound Information</h3>
                                                </div>
                                            </div>
                                            <div id="info">
                                                <table class="compoundtab" style="undefined;table-layout: fixed;">
                                                    <caption>C_number</caption>
                                                    <tr>
                                                        <td>Name</td>
                                                        <td>Chemical Name</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Formula</td>
                                                        <td>ex. C21H25ClFN3O3. C6H8O7. 2H2O</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Exact mass</td>
                                                        <td>ex. 649.205</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Mol weight</td>
                                                        <td>ex.650.047
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>Structure</td>
                                                        <td>
                                                            Database in KEGG
                                                        </tr>
                                                    </table>

                                                </div>
                                            </div>

                                        </section>

                                        <section class="wrapper style1 special" id="two">
                                            <div class="container">
                                                <header class="major">
                                                    <h2>Pathway information</h2>
                                                    <p></p>
                                                </header>

                                                <p align="center"></p>
                                                <p>
                                                    <a download="" href="#" id="btnExport">
                                                        <button class='btn focus large' style='float:center' type='button'>
                                                            <i class="icon fa-download"></i>
                                                            If you wish to download your Pathway information, Click here</button>
                                                    </a>
                                                </p>

                                                <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){
    
        echo "<table id='tblExport'>
                 <thead>
                    <tr>";
        echo "      <th>Path name</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "      <th>NET EQUATION</th>";
        echo "      <th>REACTIONS(R_NUM)</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "      <td>" . $row["net_name"] . "</td>";
          echo "      <td>" . $row["reaction"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                                <a class="button focus" href="#one">
                                                    <i class="icon fa-angle-double-up"></i>
                                                    To the Map</a>
                                                <script type="text/javascript">
                                                    $(document).ready(function () {

                                                        function itoStr($num) {
                                                            $num < 10
                                                                ? $num = '0' + $num
                                                                : $num;
                                                            return $num.toString();
                                                        }

                                                        var btn = $('#btnExport');
                                                        var tbl = 'tblExport';

                                                        btn.on('click', function () {
                                                            var dt = new Date();
                                                            var year = itoStr(dt.getFullYear());
                                                            var month = itoStr(dt.getMonth() + 1);
                                                            var day = itoStr(dt.getDate());
                                                            var hour = itoStr(dt.getHours());
                                                            var mins = itoStr(dt.getMinutes());
                                                            var pathname = input + '_' + output + '_'
                                                            var postfix = pathname + year + month + day +
                                                                "_" + hour + mins;
                                                            var fileName = "MyTable_" + postfix + ".xls";

                                                            var uri = $("#" + tbl).battatech_excelexport({
                                                                containerid: tbl,
                                                                datatype: 'table',
                                                                returnUri: true
                                                            });

                                                            $(this).attr('download', fileName).attr('href', uri).attr('target', '_blank');
                                                        });
                                                    });
                                                </script>

                                            </div>

                                        </section>

                                        <section class="wrapper style special" data-default-page="true"
                                            data-url="atp_page" id="atp_page">
                                            <div id="container">
                                                <header class="major">
                                                    <h2>ATP_Pathway analysis</h2>
                                                    <p></p>
                                                </header>

                                                <p align="center">
                                                    Bar graph on the right shows the total change of ATP quantity in its path. /
                                                    Line graph on the left shows the change of ATP quantity of each reaction.
                                                </p>
                                                <div id="chartContainer">
                                                    <script src="http://dimplejs.org/dist/dimple.v2.1.6.min.js"></script>

                                                    <?php
    $sql = "SELECT * FROM path_score_table where path like '$input[1]_$output[1]_atp%'";
    $result = $conn->query($sql);
    if ($result->num_rows >0) {
    echo "
                <script type='text/javascript'>
    var yMin = -5,
        yMax = 5,
        xLabel = 'PATH',
        yLabel = 'ATP';
        data = [ ";
    while($row= $result->fetch_assoc()) {
        echo "   { 'label':' " . $row["showname"] . " ', 'value':" . $row["atp"]  ." , 'type':'bar' },";
    }    
    echo"  ];";
    } else {
      echo "NO data" ; 
    }
?>

                                                </script>
                                                <script src="js/wholeatp.js" type="text/javascript"></script>
                                                <script type="text/javascript">
                                                    var pathname = input + '_' + output
                                                    var svg0 = dimple.newSvg("#chartContainer", 590, 400);
                                                    d3.tsv("data/tsv/" + pathname + ".tsv", function (data0) {
                                                        data0 = dimple.filterData(data0, "showname", [
                                                            '1st largest ATP production', '2nd largest ATP production', '3rd largest ATP production'
                                                        ])
                                                        var myChart0 = new dimple.chart(svg0, data0);
                                                        myChart0.setBounds(60, 30, 505, 305);
                                                        var x = myChart0.addCategoryAxis("x", "id");
                                                        x.addOrderRule("id");
                                                        myChart0.addMeasureAxis("y", "change");
                                                        myChart0.addSeries("showname", dimple.plot.line);
                                                        myChart0.addLegend(60, 10, 500, 20, "left");
                                                        myChart0.draw();
                                                    });
                                                </script>

                                            </div>
                                            <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_atp%' ";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>Path Name</th>";
        echo "      <th>ATP</th>";
        echo "      <th>CO2</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>NET EQUATION</th>";
        echo "      <th>REACTIONS(R_NUM)</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["net_name"] . "</td>";
          echo "      <td>" . $row["reaction"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                            <a class="button focus" href="#one" style="float:center;">
                                                <i class="icon fa-angle-double-up"></i>
                                                To the Map</a>

                                        </div>

                                    </section>
                                    <section class="wrapper style1 special" id="nadh_page"
                                        style="background-color:#fffffd">
                                        <div id="container">
                                            <header class="major">
                                                <h2>NADH_Pathway analysis</h2>
                                                <p></p>
                                            </header>

                                            <p align="center">Bar graph on the right shows the total change of NADH quantity
                                                in its path. / Line graph on the left shows the change of NADH quantity of each
                                                reaction.</p>
                                            <div id="chartContainer1">
                                                <?php
    $sql = "SELECT * FROM path_score_table where path like '$input[1]_$output[1]_nadh%'";
    $result = $conn->query($sql);
    if ($result->num_rows >0) {
    echo "
                <script type='text/javascript'>
    var yMin = -4,
        yMax = 4,
        xLabel = 'Bar',
        yLabel = 'Value';
        data = [ ";
    while($row= $result->fetch_assoc()) {
        echo "   { 'label':' " . $row["showname"] . " ', 'value':" . $row["nadh"]  ." , 'type':'bar' },";
    }
    echo"  ];";
    } else {
      echo "NO data" ;
    }
?>

                                            </script>
                                            <script src="js/wholenadh.js" type="text/javascript"></script>
                                            <script type="text/javascript">
                                                var svg1 = dimple.newSvg("#chartContainer1", 590, 400);
                                                d3.tsv("data/tsv/" + pathname + ".tsv", function (data1) {
                                                    data1 = dimple.filterData(data1, "showname", [
                                                        '1st largest NADH production', '2nd largest NADH production', '3rd largest NADH production'
                                                    ])
                                                    var myChart1 = new dimple.chart(svg1, data1);
                                                    myChart1.setBounds(60, 30, 505, 305);
                                                    var x = myChart1.addCategoryAxis("x", "id");
                                                    x.addOrderRule("id");
                                                    myChart1.addMeasureAxis("y", "change");
                                                    myChart1.addSeries("showname", dimple.plot.line);
                                                    myChart1.addLegend(60, 10, 500, 20, "left");
                                                    myChart1.draw();
                                                });
                                            </script>
                                        </div>
                                        <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_nadh%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>PATH</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "      <th>NET EQUATION</th>";
        echo "      <th>REACTIONS(R_NUM)</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "      <td>" . $row["net_name"] . "</td>";
          echo "      <td>" . $row["reaction"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                        <a class="button focus" href="#one" style="float:center;">
                                            <i class="icon fa-angle-double-up"></i>
                                            To the Map</a>

                                    </div>

                                </section>

                                <section class="wrapper style1 special" id="nadph_page"
                                    style="background:#fffffd">
                                    <div id="container">
                                        <header class="major">
                                            <h2>NADPH_Pathway analysis</h2>
                                            <p></p>
                                        </header>

                                        <p align="center">Bar graph on the right shows the total change of NADPH
                                            quantity in its path. / Line graph on the left shows the change of NADPH
                                            quantity of each reaction.</p>
                                        <div id="chartContainer2">
                                            <?php
    $sql = "SELECT * FROM path_score_table where path like '$input[1]_$output[1]_nadph%'";
    $result = $conn->query($sql);
    if ($result->num_rows >0) {
    echo "
                <script type='text/javascript'>
    var yMin = -4,
        yMax = 4,
        xLabel = 'Bar',
        yLabel = 'Value';
        data = [ ";
    while($row= $result->fetch_assoc()) {
        echo "   { 'label':' " . $row["showname"] . " ', 'value':" . $row["nadph"]  ." , 'type':'bar' },";
    }
    echo"  ];";
    } else {
      echo "NO data" ;
    }
?>

                                        </script>
                                        <script src="js/wholenadph.js" type="text/javascript"></script>
                                        <script type="text/javascript">
                                            var svg2 = dimple.newSvg("#chartContainer2", 590, 400);
                                            d3.tsv("data/tsv/" + pathname + ".tsv", function (data2) {
                                                data2 = dimple.filterData(data2, "showname", [
                                                    '1st largest NADPH production', '2nd largest NADPH production', '3rd largest NADPH production'
                                                ])
                                                var myChart2 = new dimple.chart(svg2, data2);
                                                myChart2.setBounds(60, 30, 505, 305);
                                                var x = myChart2.addCategoryAxis("x", "id");
                                                x.addOrderRule("id");
                                                myChart2.addMeasureAxis("y", "change");
                                                myChart2.addSeries("showname", dimple.plot.line);
                                                myChart2.addLegend(60, 10, 500, 20, "left");
                                                myChart2.draw();
                                            });
                                        </script>
                                    </div>
                                    <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_nadph%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>PATH</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "      <th>NET EQUATION</th>";
        echo "      <th>REACTIONS(R_NUM)</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "      <td>" . $row["net_name"] . "</td>";
          echo "      <td>" . $row["reaction"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                    <a class="button focus" href="#one" style="float:center;">
                                        <i class="icon fa-angle-double-up"></i>
                                        To the Map</a>

                                </div>

                            </section>

                            <section class="wrapper style1 special" id="co2_page">
                                <div id="container">
                                    <header class="major">
                                        <h2>CO2_Pathway analysis</h2>
                                        <p></p>
                                    </header>

                                    <p align="center">Bar graph on the right shows the total change of CO2 quantity
                                        in its path. / Line graph on the left shows the change of CO2 quantity of each
                                        reaction.
                                    </p>
                                    <div id="chartContainer3">
                                        <?php
    $sql = "SELECT * FROM path_score_table where path like '$input[1]_$output[1]_co2%'";
    $result = $conn->query($sql);
    if ($result->num_rows >0) {
    echo "
                <script type='text/javascript'>
    var yMin = -4,
        yMax = 4,
        xLabel = 'Bar',
        yLabel = 'Value';
        data = [ ";
    while($row= $result->fetch_assoc()) {
        echo "   { 'label':' " . $row["showname"] . " ', 'value':" . $row["co2"]  ." , 'type':'bar' },";
    }
    echo"  ];";
    } else {
      echo "NO data" ;
    }
?>

                                    </script>
                                    <script src="js/wholeco2.js" type="text/javascript"></script>
                                    <script type="text/javascript">
                                        var svg3 = dimple.newSvg("#chartContainer3", 590, 400);
                                        d3.tsv("data/tsv/" + pathname + ".tsv", function (data3) {
                                            data3 = dimple.filterData(data3, "showname", [
                                                '1st smallest CO2 loss', '2nd smallest CO2 loss', '3rd smallest CO2 loss'
                                            ])
                                            var myChart3 = new dimple.chart(svg3, data3);
                                            myChart3.setBounds(60, 30, 505, 305);
                                            var x = myChart3.addCategoryAxis("x", "id");
                                            x.addOrderRule("id");
                                            myChart3.addMeasureAxis("y", "change");
                                            myChart3.addSeries("showname", dimple.plot.line);
                                            myChart3.addLegend(60, 10, 500, 20, "left");
                                            myChart3.draw();
                                        });
                                    </script>
                                </div>
                                <?php
        $sql = "SELECT * FROM path_score_table where path  like '$input[1]_$output[1]_co2%'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){

        echo "<table>
                 <thead>
                    <tr>";
        echo "      <th>PATH</th>";
        echo "      <th>ATP</th>";
        echo "      <th>NADH</th>";
        echo "      <th>NADPH</th>";
        echo "      <th>CO2</th>";
        echo "      <th>NET EQUATION</th>";
        echo "      <th>REACTIONS(R_NUM)</th>";
        echo "    </tr>";
        echo "  </thead>";
        echo "  <tbody>";
        while($row = $result->fetch_assoc()) {
          echo "    <tr>";
          echo "      <td>" . $row["showname"] . "</td>";
          echo "      <td>" . $row["atp"] . "</td>";
          echo "      <td>" . $row["nadh"] . "</td>";
          echo "      <td>" . $row["nadph"] . "</td>";
          echo "      <td>" . $row["co2"] . "</td>";
          echo "      <td>" . $row["net_name"] . "</td>";
          echo "      <td>" . $row["reaction"] . "</td>";
          echo "    </tr>";
        }
        echo "  </tbody>";
        echo "</table>";

    } else {
      echo "No pathway information" ;
    }
   ?>
                                <a class="button focus" href="#one" style="float:center;">
                                    <i class="icon fa-angle-double-up"></i>
                                    To the Map</a>

                            </div>

                        </section>

                        <!-- Footer -->
                        <footer id="footer">
                            <div class="container">
                                <section class="links">
                                    <div class="row">
                                        <section class="3u 6u(medium) 12u$(small)">
                                            <h3>
                                                <a href="http://compbio.korea.ac.kr/712">Home</a>
                                            </h3>
                                        </section>
                                        <section class="3u 6u$(medium) 12u$(small)">
                                            <h3>
                                                <a href="http://compbio.korea.ac.kr/712/tutorial.html">Tutorial</a>
                                            </h3>
                                        </section>
                                        <section class="3u 6u(medium) 12u$(small)">
                                            <h3>
                                                <a href="http://compbio.korea.ac.kr/712/aboutus.html">About 길</a>
                                            </h3>
                                        </section>

                                    </div>
                                </section>
                                <div class="row">
                                    <div class="8u 12u$(medium)">
                                        <ul class="copyright">
                                            <li>&copy; 712 - The Pathfinder for Synthetics Biologists. All rights reserved.</li>
                                            <li>Web Template :
                                                <a href="http://templated.co">TEMPLATED</a>
                                            </li>
                                            <li>Modify & Contents :
                                                <a href="http://2015.igem.org/Team:Korea_U_Seoul">Korea U Seoul, 2015</a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </footer>

                    </body>
                </html>
