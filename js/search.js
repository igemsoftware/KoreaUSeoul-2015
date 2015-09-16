var keys;

                                //Load US States as options from CSV - but this can also be created dynamically
                            d3.tsv("../712/data/name_to_C.tsv", function (tsv) {
                                keys=tsv;
                                start();
                            });

                             //Setup and render the autocomplete
                            function start() {
                                var mc = autocomplete(document.getElementById('auto'))
                                            .keys(keys)
                                            .dataField("Compound")
                                            .labelField("KEGG_ID")
                                            .placeHolder("Compound name")
                                            .width(2000)
                                            .height(500)
                                            .input_name("start_compound")
                                            .render();

                                var mc2 = autocomplete(document.getElementById('auto2'))
                                            .keys(keys)
                                            .dataField("Compound")
                                            .labelField("KEGG_ID")
                                            .placeHolder("Compound name")
                                            .width(960)
                                            .height(500)
                                            .input_name("end_compound")
                                            .render();

                                }

