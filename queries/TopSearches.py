import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import psutil
import os
import sys
import time


class SearchRate:
    """
    This class allows you to calculate the searches
    that have increased and decreased in percentage
    with respect to the total, compared to their minimum
    and maximum percentages in the previous 5 weeks.
    """

    def __init__(self, shop: str, type: str = 'rise',
                 weeks: int = 5, ):
        local_time = time.localtime()
        self.week_to_search = dt.date(local_time.tm_year, local_time.tm_mon,
                                      local_time.tm_mday - 1)
        self.delta = dt.timedelta(days=7)
        self.type = type
        self.start = []
        self.end = []
        self.weeks = weeks
        self.shop = shop
        # Creates the dates on which the statistics will be calculated
        for i in range(self.weeks, -1, -1):
            self.start.append((self.week_to_search -
                              (self.delta * (i+1))).isoformat())
            self.end.append((self.week_to_search -
                            (self.delta * (i))).isoformat())
        self.period = []
        # Join the dates to create the weeks to be analyzed
        for i in range(self.weeks + 1):
            self.period.append(self.start[i] + '/' + self.end[i])
        # Url where SQL Queries are loaded
        self.url_total = "http://localhost:8888/druid/v2/sql/"
        # Url where Native Druid Queries are loaded
        self.url_rate = "http://localhost:8888/druid/v2/?pretty/"

        self.total = np.zeros(self.weeks + 1)
        # Query that count all the searches in a interval
        # where de start date it's included but not de final
        self.total_query = "SELECT \
                           COUNT(*) AS \"Count\" \
                           FROM \"{} SEARCH TEXT\" \
                           WHERE TIME_IN_INTERVAL(__time, '{}/{}')"

        # Query in Native Druid that compute the percentage of each
        # search by the total for 6 weeks, grouping by certain list
        # of keywords available in replacement.json, that are used
        # to do a lookUp. Also calculate the min and max in the six
        # weeks, an the difference with week searched
        self.percentage_query = "{\
            \"queryType\": \"groupBy\",\
              \"dataSource\": {\
                \"type\": \"join\",\
                \"left\": {\
                  \"type\": \"join\",\
                  \"left\": {\
                    \"type\": \"join\",\
                    \"left\": {\
                      \"type\": \"join\",\
                      \"left\": {\
                        \"type\": \"join\",\
                        \"left\": {\
                          \"type\": \"query\",\
                          \"query\": {\
                            \"queryType\": \"groupBy\",\
                            \"dataSource\": {\
                              \"type\": \"table\",\
                              \"name\": \"%s SEARCH TEXT\"\
                            },\
                            \"intervals\": {\
                              \"type\": \"intervals\",\
                              \"intervals\": [\
                                \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                              ]\
                            },\
                            \"filter\": {\
                              \"type\": \"selector\",\
                              \"dimension\": \"qfinal\",\
                              \"value\": \"1\"\
                            },\
                            \"granularity\": {\
                              \"type\": \"all\"\
                            },\
                            \"dimensions\": [\
                              {\
                                \"type\": \"extraction\",\
                                \"dimension\": \"query\",\
                                \"outputName\": \"d0\",\
                                \"outputType\": \"STRING\",\
                                \"extractionFn\": {\
                                  \"type\": \"registeredLookup\",\
                                  \"lookup\": \"ReemplazosInfanti\",\
                                  \"retainMissingValue\": true,\
                                  \"injective\": null,\
                                  \"optimize\": true\
                                }\
                              }\
                            ],\
                            \"aggregations\": [\
                              {\
                                \"type\": \"count\",\
                                \"name\": \"a0\"\
                              }\
                            ],\
                            \"postAggregations\": [\
                              {\
                                \"type\": \"expression\",\
                                \"name\": \"p0\",\
                                \"expression\": \"((a0 * 100.0) / %s)\"\
                              }\
                            ],\
                            \"limitSpec\": {\
                              \"type\": \"NoopLimitSpec\"\
                            },\
                            \"context\": {\
                              \"sqlOuterLimit\": 1001,\
                              \"sqlQueryId\": \"beefe18d-ce56-4a71\
                              -a8b4-6645578d3ca2\",\
                              \"useNativeQueryExplain\": true\
                            }\
                          }\
                        },\
                        \"right\": {\
                          \"type\": \"query\",\
                          \"query\": {\
                            \"queryType\": \"scan\",\
                            \"dataSource\": {\
                              \"type\": \"query\",\
                              \"query\": {\
                                \"queryType\": \"groupBy\",\
                                \"dataSource\": {\
                                  \"type\": \"table\",\
                                  \"name\": \"%s SEARCH TEXT\"\
                                },\
                                \"intervals\": {\
                                  \"type\": \"intervals\",\
                                  \"intervals\": [\
                                    \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                                  ]\
                                },\
                                \"filter\": {\
                                  \"type\": \"selector\",\
                                  \"dimension\": \"qfinal\",\
                                  \"value\": \"1\"\
                                },\
                                \"granularity\": {\
                                  \"type\": \"all\"\
                                },\
                                \"dimensions\": [\
                                  {\
                                    \"type\": \"extraction\",\
                                    \"dimension\": \"query\",\
                                    \"outputName\": \"d0\",\
                                    \"outputType\": \"STRING\",\
                                    \"extractionFn\": {\
                                      \"type\": \"registeredLookup\",\
                                      \"lookup\": \"ReemplazosInfanti\",\
                                      \"retainMissingValue\": true,\
                                      \"injective\": null,\
                                      \"optimize\": true\
                                    }\
                                  }\
                                ],\
                                \"aggregations\": [\
                                  {\
                                    \"type\": \"count\",\
                                    \"name\": \"a0\"\
                                  }\
                                ],\
                                \"limitSpec\": {\
                                  \"type\": \"NoopLimitSpec\"\
                                },\
                                \"context\": {\
                                  \"sqlOuterLimit\": 1001,\
                                  \"sqlQueryId\": \"beefe18d-ce56-4a71\
                                  -a8b4-6645578d3ca2\",\
                                  \"useNativeQueryExplain\": true\
                                }\
                              }\
                            },\
                            \"intervals\": {\
                              \"type\": \"intervals\",\
                              \"intervals\": [\
                                \"-146136543-09-08T08:23:32.096Z/146140482-04-24T15:36:27.903Z\"\
                              ]\
                            },\
                            \"resultFormat\": \"compactedList\",\
                            \"columns\": [\
                              \"a0\",\
                              \"d0\"\
                            ],\
                            \"legacy\": false,\
                            \"context\": {\
                              \"sqlOuterLimit\": 1001,\
                              \"sqlQueryId\": \"beefe18d-ce56-4a71-a8b4\
                              -6645578d3ca2\",\
                              \"useNativeQueryExplain\": true\
                            },\
                            \"granularity\": {\
                              \"type\": \"all\"\
                            }\
                          }\
                        },\
                        \"rightPrefix\": \"j0\",\
                        \"condition\": \"(d0 == j0d0)\",\
                        \"joinType\": \"INNER\"\
                      },\
                      \"right\": {\
                        \"type\": \"query\",\
                        \"query\": {\
                          \"queryType\": \"groupBy\",\
                          \"dataSource\": {\
                            \"type\": \"table\",\
                            \"name\": \"%s SEARCH TEXT\"\
                          },\
                          \"intervals\": {\
                            \"type\": \"intervals\",\
                            \"intervals\": [\
                              \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                            ]\
                          },\
                          \"filter\": {\
                            \"type\": \"selector\",\
                            \"dimension\": \"qfinal\",\
                            \"value\": \"1\"\
                          },\
                          \"granularity\": {\
                            \"type\": \"all\"\
                          },\
                          \"dimensions\": [\
                            {\
                              \"type\": \"extraction\",\
                              \"dimension\": \"query\",\
                              \"outputName\": \"d0\",\
                              \"outputType\": \"STRING\",\
                              \"extractionFn\": {\
                                \"type\": \"registeredLookup\",\
                                \"lookup\": \"ReemplazosInfanti\",\
                                \"retainMissingValue\": true,\
                                \"injective\": null,\
                                \"optimize\": true\
                              }\
                            }\
                          ],\
                          \"aggregations\": [\
                            {\
                              \"type\": \"count\",\
                              \"name\": \"a0\"\
                            }\
                          ],\
                          \"postAggregations\": [\
                            {\
                              \"type\": \"expression\",\
                              \"name\": \"p0\",\
                              \"expression\": \"((a0 * 100.0) / %s})\"\
                            }\
                          ],\
                          \"limitSpec\": {\
                            \"type\": \"NoopLimitSpec\"\
                          },\
                          \"context\": {\
                            \"sqlOuterLimit\": 1001,\
                            \"sqlQueryId\": \"beefe18d-ce56-4a71-a8b4\
                            -6645578d3ca2\",\
                            \"useNativeQueryExplain\": true\
                          }\
                        }\
                      },\
                      \"rightPrefix\": \"_j0\",\
                      \"condition\": \"(d0 == _j0d0)\",\
                      \"joinType\": \"INNER\"\
                    },\
                    \"right\": {\
                      \"type\": \"query\",\
                      \"query\": {\
                        \"queryType\": \"groupBy\",\
                        \"dataSource\": {\
                          \"type\": \"table\",\
                          \"name\": \"%s SEARCH TEXT\"\
                        },\
                        \"intervals\": {\
                          \"type\": \"intervals\",\
                          \"intervals\": [\
                            \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                          ]\
                        },\
                        \"filter\": {\
                          \"type\": \"selector\",\
                          \"dimension\": \"qfinal\",\
                          \"value\": \"1\"\
                        },\
                        \"granularity\": {\
                          \"type\": \"all\"\
                        },\
                        \"dimensions\": [\
                          {\
                            \"type\": \"extraction\",\
                            \"dimension\": \"query\",\
                            \"outputName\": \"d0\",\
                            \"outputType\": \"STRING\",\
                            \"extractionFn\": {\
                              \"type\": \"registeredLookup\",\
                              \"lookup\": \"ReemplazosInfanti\",\
                              \"retainMissingValue\": true,\
                              \"injective\": null,\
                              \"optimize\": true\
                            }\
                          }\
                        ],\
                        \"aggregations\": [\
                          {\
                            \"type\": \"count\",\
                            \"name\": \"a0\"\
                          }\
                        ],\
                        \"postAggregations\": [\
                          {\
                            \"type\": \"expression\",\
                            \"name\": \"p0\",\
                            \"expression\": \"((a0 * 100.0) / %s)\"\
                          }\
                        ],\
                        \"limitSpec\": {\
                          \"type\": \"NoopLimitSpec\"\
                        },\
                        \"context\": {\
                          \"sqlOuterLimit\": 1001,\
                          \"sqlQueryId\": \"beefe18d-ce56-4a71-a8b4\
                          -6645578d3ca2\",\
                          \"useNativeQueryExplain\": true\
                        }\
                      }\
                    },\
                    \"rightPrefix\": \"__j0\",\
                    \"condition\": \"(d0 == __j0d0)\",\
                    \"joinType\": \"INNER\"\
                  },\
                  \"right\": {\
                    \"type\": \"query\",\
                    \"query\": {\
                      \"queryType\": \"groupBy\",\
                      \"dataSource\": {\
                        \"type\": \"table\",\
                        \"name\": \"%s SEARCH TEXT\"\
                      },\
                      \"intervals\": {\
                        \"type\": \"intervals\",\
                        \"intervals\": [\
                          \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                        ]\
                      },\
                      \"filter\": {\
                        \"type\": \"selector\",\
                        \"dimension\": \"qfinal\",\
                        \"value\": \"1\"\
                      },\
                      \"granularity\": {\
                        \"type\": \"all\"\
                      },\
                      \"dimensions\": [\
                        {\
                          \"type\": \"extraction\",\
                          \"dimension\": \"query\",\
                          \"outputName\": \"d0\",\
                          \"outputType\": \"STRING\",\
                          \"extractionFn\": {\
                            \"type\": \"registeredLookup\",\
                            \"lookup\": \"ReemplazosInfanti\",\
                            \"retainMissingValue\": true,\
                            \"injective\": null,\
                            \"optimize\": true\
                          }\
                        }\
                      ],\
                      \"aggregations\": [\
                        {\
                          \"type\": \"count\",\
                          \"name\": \"a0\"\
                        }\
                      ],\
                      \"postAggregations\": [\
                        {\
                          \"type\": \"expression\",\
                          \"name\": \"p0\",\
                          \"expression\": \"((a0 * 100.0) / %s)\"\
                        }\
                      ],\
                      \"limitSpec\": {\
                        \"type\": \"NoopLimitSpec\"\
                      },\
                      \"context\": {\
                        \"sqlOuterLimit\": 1001,\
                        \"sqlQueryId\": \"beefe18d-ce56-4a71-a8b4\
                        -6645578d3ca2\",\
                        \"useNativeQueryExplain\": true\
                      }\
                    }\
                  },\
                  \"rightPrefix\": \"___j0\",\
                  \"condition\": \"(d0 == ___j0d0)\",\
                  \"joinType\": \"INNER\"\
                },\
                \"right\": {\
                  \"type\": \"query\",\
                  \"query\": {\
                    \"queryType\": \"groupBy\",\
                    \"dataSource\": {\
                      \"type\": \"table\",\
                      \"name\": \"%s SEARCH TEXT\"\
                    },\
                    \"intervals\": {\
                      \"type\": \"intervals\",\
                      \"intervals\": [\
                        \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                      ]\
                    },\
                    \"filter\": {\
                      \"type\": \"selector\",\
                      \"dimension\": \"qfinal\",\
                      \"value\": \"1\"\
                    },\
                    \"granularity\": {\
                      \"type\": \"all\"\
                    },\
                    \"dimensions\": [\
                      {\
                        \"type\": \"extraction\",\
                        \"dimension\": \"query\",\
                        \"outputName\": \"d0\",\
                        \"outputType\": \"STRING\",\
                        \"extractionFn\": {\
                          \"type\": \"registeredLookup\",\
                          \"lookup\": \"ReemplazosInfanti\",\
                          \"retainMissingValue\": true,\
                          \"injective\": null,\
                          \"optimize\": true\
                        }\
                      }\
                    ],\
                    \"aggregations\": [\
                      {\
                        \"type\": \"count\",\
                        \"name\": \"a0\"\
                      }\
                    ],\
                    \"postAggregations\": [\
                      {\
                        \"type\": \"expression\",\
                        \"name\": \"p0\",\
                        \"expression\": \"((a0 * 100.0) / %s)\"\
                      }\
                    ],\
                    \"limitSpec\": {\
                      \"type\": \"NoopLimitSpec\"\
                    },\
                    \"context\": {\
                      \"sqlOuterLimit\": 1001,\
                      \"sqlQueryId\": \"beefe18d-ce56-4a71-a8b4\
                      -6645578d3ca2\",\
                      \"useNativeQueryExplain\": true\
                    }\
                  }\
                },\
                \"rightPrefix\": \"____j0\",\
                \"condition\": \"(d0 == ____j0d0)\",\
                \"joinType\": \"INNER\"\
              },\
              \"intervals\": {\
                \"type\": \"intervals\",\
                \"intervals\": [\
                  \"-146136543-09-08T08:23:32.096Z/146140482-04-24T15:36:27.903Z\"\
                ]\
              },\
              \"virtualColumns\": [\
              {\
                \"type\": \"expression\",\
                \"name\": \"v0\",\
                \"expression\": \"%s\",\
                \"outputType\": \"DOUBLE\"\
              },\
              {\
                \"type\": \"expression\",\
                \"name\": \"v1\",\
                \"expression\": \"greatest(((j0a0 * 100.0) / %s),\
                  _j0p0,__j0p0,___j0p0,____j0p0)\",\
                \"outputType\": \"DOUBLE\"\
              },\
              {\
                \"type\": \"expression\",\
                \"name\": \"v2\",\
                \"expression\": \"least(((j0a0 * 100.0) / %s),\
                _j0p0,__j0p0,___j0p0,____j0p0)\",\
                \"outputType\": \"DOUBLE\"\
              },\
                {\
                  \"type\": \"expression\",\
                  \"name\": \"v3\",\
                  \"expression\": \"((j0a0 * 100.0) / %s)\",\
                  \"outputType\": \"DOUBLE\"\
                }\
            ],\
              \"granularity\": {\
                \"type\": \"all\"\
              },\
              \"dimensions\": [\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"d0\",\
                  \"outputName\": \"_d0\",\
                  \"outputType\": \"STRING\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"v0\",\
                  \"outputName\": \"_d1\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"v1\",\
                  \"outputName\": \"_d2\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"v2\",\
                  \"outputName\": \"_d3\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"p0\",\
                  \"outputName\": \"_d4\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"v3\",\
                  \"outputName\": \"_d5\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"_j0p0\",\
                  \"outputName\": \"_d6\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"__j0p0\",\
                  \"outputName\": \"_d7\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"___j0p0\",\
                  \"outputName\": \"_d8\",\
                  \"outputType\": \"DOUBLE\"\
                },\
                {\
                  \"type\": \"default\",\
                  \"dimension\": \"____j0p0\",\
                  \"outputName\": \"_d9\",\
                  \"outputType\": \"DOUBLE\"\
                }\
              ],\
              \"limitSpec\": {\
                \"type\": \"default\",\
                \"columns\": [\
                  {\
                    \"dimension\": \"_d1\",\
                    \"direction\": \"%s\",\
                    \"dimensionOrder\": {\
                      \"type\": \"numeric\"\
                    }\
                  }\
                ]\
              },\
              \"context\": {\
                \"sqlOuterLimit\": 1001,\
                \"sqlQueryId\": \"beefe18d-ce56-4a71-a8b4-6645578d3ca2\",\
                \"useNativeQueryExplain\": true\
              }\
            }"

        self.percentage_query_10 = "{\
  \"queryType\": \"groupBy\",\
  \"dataSource\": {\
    \"type\": \"join\",\
    \"left\": {\
      \"type\": \"join\",\
      \"left\": {\
        \"type\": \"join\",\
        \"left\": {\
          \"type\": \"join\",\
          \"left\": {\
            \"type\": \"join\",\
            \"left\": {\
              \"type\": \"join\",\
              \"left\": {\
                \"type\": \"join\",\
                \"left\": {\
                  \"type\": \"join\",\
                  \"left\": {\
                    \"type\": \"join\",\
                    \"left\": {\
                      \"type\": \"join\",\
                      \"left\": {\
                        \"type\": \"query\",\
                        \"query\": {\
                          \"queryType\": \"groupBy\",\
                          \"dataSource\": {\
                            \"type\": \"table\",\
                            \"name\": \"%s SEARCH TEXT\"\
                          },\
                            \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                          \"intervals\": {\
                            \"type\": \"intervals\",\
                            \"intervals\": [\
                              \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                            ]\
                          },\
                          \"filter\": {\
                            \"type\": \"selector\",\
                            \"dimension\": \"qfinal\",\
                            \"value\": \"1\"\
                          },\
                          \"granularity\": {\
                            \"type\": \"all\"\
                          },\
                          \"dimensions\": [\
                            {\
                              \"type\": \"extraction\",\
                              \"dimension\": \"query\",\
                              \"outputName\": \"d0\",\
                              \"outputType\": \"STRING\",\
                              \"extractionFn\": {\
                                \"type\": \"registeredLookup\",\
                                \"lookup\": \"ReemplazosInfanti\",\
                                \"retainMissingValue\": true,\
                                \"injective\": null,\
                                \"optimize\": true\
                              }\
                            }\
                          ],\
                          \"aggregations\": [\
                            {\
                              \"type\": \"count\",\
                              \"name\": \"a0\"\
                            }\
                          ],\
                          \"postAggregations\": [\
                            {\
                              \"type\": \"expression\",\
                              \"name\": \"p0\",\
                              \"expression\": \"((a0 * 100.0) / %s)\"\
                            }\
                          ],\
                          \"context\": {\
                            \"sqlOuterLimit\": 1001,\
                            \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951\
                            -bbc22e38edb7\",\
                            \"useNativeQueryExplain\": true\
                          }\
                        }\
                      },\
                      \"right\": {\
                        \"type\": \"query\",\
                        \"query\": {\
                          \"queryType\": \"scan\",\
                          \"dataSource\": {\
                            \"type\": \"query\",\
                            \"query\": {\
                              \"queryType\": \"groupBy\",\
                              \"dataSource\": {\
                                \"type\": \"table\",\
                                \"name\": \"%s SEARCH TEXT\"\
                              },\
                                \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                              \"intervals\": {\
                                \"type\": \"intervals\",\
                                \"intervals\": [\
                                  \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                                ]\
                              },\
                              \"filter\": {\
                                \"type\": \"selector\",\
                                \"dimension\": \"qfinal\",\
                                \"value\": \"1\"\
                              },\
                              \"granularity\": {\
                                \"type\": \"all\"\
                              },\
                              \"dimensions\": [\
                                {\
                                  \"type\": \"extraction\",\
                                  \"dimension\": \"query\",\
                                  \"outputName\": \"d0\",\
                                  \"outputType\": \"STRING\",\
                                  \"extractionFn\": {\
                                    \"type\": \"registeredLookup\",\
                                    \"lookup\": \"ReemplazosInfanti\",\
                                    \"retainMissingValue\": true,\
                                    \"injective\": null,\
                                    \"optimize\": true\
                                  }\
                                }\
                              ],\
                              \"aggregations\": [\
                                {\
                                  \"type\": \"count\",\
                                  \"name\": \"a0\"\
                                }\
                              ],\
                              \"context\": {\
                                \"sqlOuterLimit\": 1001,\
                                \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-\
                                bbc22e38edb7\",\
                                \"useNativeQueryExplain\": true\
                              }\
                            }\
                          },\
                          \"intervals\": {\
                            \"type\": \"intervals\",\
                            \"intervals\": [\
                              \"-146136543-09-08T08:23:32.096Z/146140482-04-24T15:36:27.903Z\"\
                            ]\
                          },\
                          \"resultFormat\": \"compactedList\",\
                          \"columns\": [\
                            \"a0\",\
                            \"d0\"\
                          ],\
                          \"legacy\": false,\
                          \"context\": {\
                            \"sqlOuterLimit\": 1001,\
                            \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-\
                            bbc22e38edb7\",\
                            \"useNativeQueryExplain\": true\
                          },\
                          \"granularity\": {\
                            \"type\": \"all\"\
                          }\
                        }\
                      },\
                      \"rightPrefix\": \"j0\",\
                      \"condition\": \"(d0 == j0d0)\",\
                      \"joinType\": \"INNER\"\
                    },\
                    \"right\": {\
                      \"type\": \"query\",\
                      \"query\": {\
                        \"queryType\": \"groupBy\",\
                        \"dataSource\": {\
                          \"type\": \"table\",\
                          \"name\": \"%s SEARCH TEXT\"\
                        },\
                          \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                        \"intervals\": {\
                          \"type\": \"intervals\",\
                          \"intervals\": [\
                            \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                          ]\
                        },\
                        \"filter\": {\
                          \"type\": \"selector\",\
                          \"dimension\": \"qfinal\",\
                          \"value\": \"1\"\
                        },\
                        \"granularity\": {\
                          \"type\": \"all\"\
                        },\
                        \"dimensions\": [\
                          {\
                            \"type\": \"extraction\",\
                            \"dimension\": \"query\",\
                            \"outputName\": \"d0\",\
                            \"outputType\": \"STRING\",\
                            \"extractionFn\": {\
                              \"type\": \"registeredLookup\",\
                              \"lookup\": \"ReemplazosInfanti\",\
                              \"retainMissingValue\": true,\
                              \"injective\": null,\
                              \"optimize\": true\
                            }\
                          }\
                        ],\
                        \"aggregations\": [\
                          {\
                            \"type\": \"count\",\
                            \"name\": \"a0\"\
                          }\
                        ],\
                        \"postAggregations\": [\
                          {\
                            \"type\": \"expression\",\
                            \"name\": \"p0\",\
                            \"expression\": \"((a0 * 100.0) / %s)\"\
                          }\
                        ],\
                        \"context\": {\
                          \"sqlOuterLimit\": 1001,\
                          \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-\
                          bbc22e38edb7\",\
                          \"useNativeQueryExplain\": true\
                        }\
                      }\
                    },\
                    \"rightPrefix\": \"_j0\",\
                    \"condition\": \"(d0 == _j0d0)\",\
                    \"joinType\": \"INNER\"\
                  },\
                  \"right\": {\
                    \"type\": \"query\",\
                    \"query\": {\
                      \"queryType\": \"groupBy\",\
                      \"dataSource\": {\
                        \"type\": \"table\",\
                        \"name\": \"%s SEARCH TEXT\"\
                      },\
                        \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                      \"intervals\": {\
                        \"type\": \"intervals\",\
                        \"intervals\": [\
                          \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                        ]\
                      },\
                      \"filter\": {\
                        \"type\": \"selector\",\
                        \"dimension\": \"qfinal\",\
                        \"value\": \"1\"\
                      },\
                      \"granularity\": {\
                        \"type\": \"all\"\
                      },\
                      \"dimensions\": [\
                        {\
                          \"type\": \"extraction\",\
                          \"dimension\": \"query\",\
                          \"outputName\": \"d0\",\
                          \"outputType\": \"STRING\",\
                          \"extractionFn\": {\
                            \"type\": \"registeredLookup\",\
                            \"lookup\": \"ReemplazosInfanti\",\
                            \"retainMissingValue\": true,\
                            \"injective\": null,\
                            \"optimize\": true\
                          }\
                        }\
                      ],\
                      \"aggregations\": [\
                        {\
                          \"type\": \"count\",\
                          \"name\": \"a0\"\
                        }\
                      ],\
                      \"postAggregations\": [\
                        {\
                          \"type\": \"expression\",\
                          \"name\": \"p0\",\
                          \"expression\": \"((a0 * 100.0) / %s)\"\
                        }\
                      ],\
                      \"context\": {\
                        \"sqlOuterLimit\": 1001,\
                        \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-\
                        bbc22e38edb7\",\
                        \"useNativeQueryExplain\": true\
                      }\
                    }\
                  },\
                  \"rightPrefix\": \"__j0\",\
                  \"condition\": \"(d0 == __j0d0)\",\
                  \"joinType\": \"INNER\"\
                },\
                \"right\": {\
                  \"type\": \"query\",\
                  \"query\": {\
                    \"queryType\": \"groupBy\",\
                    \"dataSource\": {\
                      \"type\": \"table\",\
                      \"name\": \"%s SEARCH TEXT\"\
                    },\
                      \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                    \"intervals\": {\
                      \"type\": \"intervals\",\
                      \"intervals\": [\
                        \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                      ]\
                    },\
                    \"filter\": {\
                      \"type\": \"selector\",\
                      \"dimension\": \"qfinal\",\
                      \"value\": \"1\"\
                    },\
                    \"granularity\": {\
                      \"type\": \"all\"\
                    },\
                    \"dimensions\": [\
                      {\
                        \"type\": \"extraction\",\
                        \"dimension\": \"query\",\
                        \"outputName\": \"d0\",\
                        \"outputType\": \"STRING\",\
                        \"extractionFn\": {\
                          \"type\": \"registeredLookup\",\
                          \"lookup\": \"ReemplazosInfanti\",\
                          \"retainMissingValue\": true,\
                          \"injective\": null,\
                          \"optimize\": true\
                        }\
                      }\
                    ],\
                    \"aggregations\": [\
                      {\
                        \"type\": \"count\",\
                        \"name\": \"a0\"\
                      }\
                    ],\
                    \"postAggregations\": [\
                      {\
                        \"type\": \"expression\",\
                        \"name\": \"p0\",\
                        \"expression\": \"((a0 * 100.0) / %s)\"\
                      }\
                    ],\
                    \"context\": {\
                      \"sqlOuterLimit\": 1001,\
                      \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-\
                      bbc22e38edb7\",\
                      \"useNativeQueryExplain\": true\
                    }\
                  }\
                },\
                \"rightPrefix\": \"___j0\",\
                \"condition\": \"(d0 == ___j0d0)\",\
                \"joinType\": \"INNER\"\
              },\
              \"right\": {\
                \"type\": \"query\",\
                \"query\": {\
                  \"queryType\": \"groupBy\",\
                  \"dataSource\": {\
                    \"type\": \"table\",\
                    \"name\": \"%s SEARCH TEXT\"\
                  },\
                    \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                  \"intervals\": {\
                    \"type\": \"intervals\",\
                    \"intervals\": [\
                      \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                    ]\
                  },\
                  \"filter\": {\
                    \"type\": \"selector\",\
                    \"dimension\": \"qfinal\",\
                    \"value\": \"1\"\
                  },\
                  \"granularity\": {\
                    \"type\": \"all\"\
                  },\
                  \"dimensions\": [\
                    {\
                      \"type\": \"extraction\",\
                      \"dimension\": \"query\",\
                      \"outputName\": \"d0\",\
                      \"outputType\": \"STRING\",\
                      \"extractionFn\": {\
                        \"type\": \"registeredLookup\",\
                        \"lookup\": \"ReemplazosInfanti\",\
                        \"retainMissingValue\": true,\
                        \"injective\": null,\
                        \"optimize\": true\
                      }\
                    }\
                  ],\
                  \"aggregations\": [\
                    {\
                      \"type\": \"count\",\
                      \"name\": \"a0\"\
                    }\
                  ],\
                  \"postAggregations\": [\
                    {\
                      \"type\": \"expression\",\
                      \"name\": \"p0\",\
                      \"expression\": \"((a0 * 100.0) / %s})\"\
                    }\
                  ],\
                  \"context\": {\
                    \"sqlOuterLimit\": 1001,\
                    \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
                    \"useNativeQueryExplain\": true\
                  }\
                }\
              },\
              \"rightPrefix\": \"____j0\",\
              \"condition\": \"(d0 == ____j0d0)\",\
              \"joinType\": \"INNER\"\
            },\
            \"right\": {\
              \"type\": \"query\",\
              \"query\": {\
                \"queryType\": \"groupBy\",\
                \"dataSource\": {\
                  \"type\": \"table\",\
                  \"name\": \"%s SEARCH TEXT\"\
                },\
                  \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
                \"intervals\": {\
                  \"type\": \"intervals\",\
                  \"intervals\": [\
                    \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                  ]\
                },\
                \"filter\": {\
                  \"type\": \"selector\",\
                  \"dimension\": \"qfinal\",\
                  \"value\": \"1\"\
                },\
                \"granularity\": {\
                  \"type\": \"all\"\
                },\
                \"dimensions\": [\
                  {\
                    \"type\": \"extraction\",\
                    \"dimension\": \"query\",\
                    \"outputName\": \"d0\",\
                    \"outputType\": \"STRING\",\
                    \"extractionFn\": {\
                      \"type\": \"registeredLookup\",\
                      \"lookup\": \"ReemplazosInfanti\",\
                      \"retainMissingValue\": true,\
                      \"injective\": null,\
                      \"optimize\": true\
                    }\
                  }\
                ],\
                \"aggregations\": [\
                  {\
                    \"type\": \"count\",\
                    \"name\": \"a0\"\
                  }\
                ],\
                \"postAggregations\": [\
                  {\
                    \"type\": \"expression\",\
                    \"name\": \"p0\",\
                    \"expression\": \"((a0 * 100.0) / %s)\"\
                  }\
                ],\
                \"context\": {\
                  \"sqlOuterLimit\": 1001,\
                  \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
                  \"useNativeQueryExplain\": true\
                }\
              }\
            },\
            \"rightPrefix\": \"_____j0\",\
            \"condition\": \"(d0 == _____j0d0)\",\
            \"joinType\": \"INNER\"\
          },\
          \"right\": {\
            \"type\": \"query\",\
            \"query\": {\
              \"queryType\": \"groupBy\",\
              \"dataSource\": {\
                \"type\": \"table\",\
                \"name\": \"%s SEARCH TEXT\"\
              },\
                \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
              \"intervals\": {\
                \"type\": \"intervals\",\
                \"intervals\": [\
                  \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
                ]\
              },\
              \"filter\": {\
                \"type\": \"selector\",\
                \"dimension\": \"qfinal\",\
                \"value\": \"1\"\
              },\
              \"granularity\": {\
                \"type\": \"all\"\
              },\
              \"dimensions\": [\
                {\
                  \"type\": \"extraction\",\
                  \"dimension\": \"query\",\
                  \"outputName\": \"d0\",\
                  \"outputType\": \"STRING\",\
                  \"extractionFn\": {\
                    \"type\": \"registeredLookup\",\
                    \"lookup\": \"ReemplazosInfanti\",\
                    \"retainMissingValue\": true,\
                    \"injective\": null,\
                    \"optimize\": true\
                  }\
                }\
              ],\
              \"aggregations\": [\
                {\
                  \"type\": \"count\",\
                  \"name\": \"a0\"\
                }\
              ],\
              \"postAggregations\": [\
                {\
                  \"type\": \"expression\",\
                  \"name\": \"p0\",\
                  \"expression\": \"((a0 * 100.0) / %s)\"\
                }\
              ],\
              \"context\": {\
                \"sqlOuterLimit\": 1001,\
                \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
                \"useNativeQueryExplain\": true\
              }\
            }\
          },\
          \"rightPrefix\": \"______j0\",\
          \"condition\": \"(d0 == ______j0d0)\",\
          \"joinType\": \"INNER\"\
        },\
        \"right\": {\
          \"type\": \"query\",\
          \"query\": {\
            \"queryType\": \"groupBy\",\
            \"dataSource\": {\
              \"type\": \"table\",\
              \"name\": \"%s SEARCH TEXT\"\
            },\
              \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
            \"intervals\": {\
              \"type\": \"intervals\",\
              \"intervals\": [\
                \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
              ]\
            },\
            \"filter\": {\
              \"type\": \"selector\",\
              \"dimension\": \"qfinal\",\
              \"value\": \"1\"\
            },\
            \"granularity\": {\
              \"type\": \"all\"\
            },\
            \"dimensions\": [\
              {\
                \"type\": \"extraction\",\
                \"dimension\": \"query\",\
                \"outputName\": \"d0\",\
                \"outputType\": \"STRING\",\
                \"extractionFn\": {\
                  \"type\": \"registeredLookup\",\
                  \"lookup\": \"ReemplazosInfanti\",\
                  \"retainMissingValue\": true,\
                  \"injective\": null,\
                  \"optimize\": true\
                }\
              }\
            ],\
            \"aggregations\": [\
              {\
                \"type\": \"count\",\
                \"name\": \"a0\"\
              }\
            ],\
            \"postAggregations\": [\
              {\
                \"type\": \"expression\",\
                \"name\": \"p0\",\
                \"expression\": \"((a0 * 100.0) / %s)\"\
              }\
            ],\
            \"context\": {\
              \"sqlOuterLimit\": 1001,\
              \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
              \"useNativeQueryExplain\": true\
            }\
          }\
        },\
        \"rightPrefix\": \"_______j0\",\
        \"condition\": \"(d0 == _______j0d0)\",\
        \"joinType\": \"INNER\"\
      },\
      \"right\": {\
        \"type\": \"query\",\
        \"query\": {\
          \"queryType\": \"groupBy\",\
          \"dataSource\": {\
            \"type\": \"table\",\
            \"name\": \"%s SEARCH TEXT\"\
          },\
            \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
          \"intervals\": {\
            \"type\": \"intervals\",\
            \"intervals\": [\
              \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
            ]\
          },\
          \"filter\": {\
            \"type\": \"selector\",\
            \"dimension\": \"qfinal\",\
            \"value\": \"1\"\
          },\
          \"granularity\": {\
            \"type\": \"all\"\
          },\
          \"dimensions\": [\
            {\
              \"type\": \"extraction\",\
              \"dimension\": \"query\",\
              \"outputName\": \"d0\",\
              \"outputType\": \"STRING\",\
              \"extractionFn\": {\
                \"type\": \"registeredLookup\",\
                \"lookup\": \"ReemplazosInfanti\",\
                \"retainMissingValue\": true,\
                \"injective\": null,\
                \"optimize\": true\
              }\
            }\
          ],\
          \"aggregations\": [\
            {\
              \"type\": \"count\",\
              \"name\": \"a0\"\
            }\
          ],\
          \"postAggregations\": [\
            {\
              \"type\": \"expression\",\
              \"name\": \"p0\",\
              \"expression\": \"((a0 * 100.0) / %s)\"\
            }\
          ],\
          \"context\": {\
            \"sqlOuterLimit\": 1001,\
            \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
            \"useNativeQueryExplain\": true\
          }\
        }\
      },\
      \"rightPrefix\": \"________j0\",\
      \"condition\": \"(d0 == ________j0d0)\",\
      \"joinType\": \"INNER\"\
    },\
    \"right\": {\
      \"type\": \"query\",\
      \"query\": {\
        \"queryType\": \"groupBy\",\
        \"dataSource\": {\
          \"type\": \"table\",\
          \"name\": \"%s SEARCH TEXT\"\
        },\
          \"metric\": {\
                          \"type\": \"dimension\",\
                          \"ordering\": {\
                            \"type\": \"lexicochart\"\
                          }\
                        },\
        \"intervals\": {\
          \"type\": \"intervals\",\
          \"intervals\": [\
            \"%sT00:00:00.000Z/%sT00:00:00.000Z\"\
          ]\
        },\
        \"filter\": {\
          \"type\": \"selector\",\
          \"dimension\": \"qfinal\",\
          \"value\": \"1\"\
        },\
        \"granularity\": {\
          \"type\": \"all\"\
        },\
        \"dimensions\": [\
          {\
            \"type\": \"extraction\",\
            \"dimension\": \"query\",\
            \"outputName\": \"d0\",\
            \"outputType\": \"STRING\",\
            \"extractionFn\": {\
              \"type\": \"registeredLookup\",\
              \"lookup\": \"ReemplazosInfanti\",\
              \"retainMissingValue\": true,\
              \"injective\": null,\
              \"optimize\": true\
            }\
          }\
        ],\
        \"aggregations\": [\
          {\
            \"type\": \"count\",\
            \"name\": \"a0\"\
          }\
        ],\
        \"postAggregations\": [\
          {\
            \"type\": \"expression\",\
            \"name\": \"p0\",\
            \"expression\": \"((a0 * 100.0) / %s)\"\
          }\
        ],\
        \"context\": {\
          \"sqlOuterLimit\": 1100,\
          \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
          \"useNativeQueryExplain\": true\
        }\
      }\
    },\
    \"rightPrefix\": \"_________j0\",\
    \"condition\": \"(d0 == _________j0d0)\",\
    \"joinType\": \"INNER\"\
  },\
  \"intervals\": {\
    \"type\": \"intervals\",\
    \"intervals\": [\
      \"-146136543-09-08T08:23:32.096Z/146140482-04-24T15:36:27.903Z\"\
    ]\
  },\
  \"virtualColumns\": [\
    {\
      \"type\": \"expression\",\
      \"name\": \"v0\",\
      \"expression\": \"%s\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"expression\",\
      \"name\": \"v1\",\
      \"expression\": \"greatest(((j0a0 * 100.0) / %s),_j0p0,__j0p0,___j0p0,\
      ____j0p0,_____j0p0,______j0p0,_______j0p0,________j0p0,_________j0p0)\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"expression\",\
      \"name\": \"v2\",\
      \"expression\": \"least(((j0a0 * 100.0) / %s),_j0p0,__j0p0,___j0p0,\
      ____j0p0,_____j0p0,______j0p0,_______j0p0,________j0p0,_________j0p0)\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"expression\",\
      \"name\": \"v3\",\
      \"expression\": \"((j0a0 * 100.0) / %s)\",\
      \"outputType\": \"DOUBLE\"\
    }\
  ],\
  \"granularity\": {\
    \"type\": \"all\"\
  },\
  \"dimensions\": [\
    {\
      \"type\": \"default\",\
      \"dimension\": \"d0\",\
      \"outputName\": \"_d0\",\
      \"outputType\": \"STRING\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"v0\",\
      \"outputName\": \"_d1\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"v1\",\
      \"outputName\": \"_d2\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"v2\",\
      \"outputName\": \"_d3\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"p0\",\
      \"outputName\": \"_d4\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"v3\",\
      \"outputName\": \"_d5\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"_j0p0\",\
      \"outputName\": \"_d6\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"__j0p0\",\
      \"outputName\": \"_d7\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"___j0p0\",\
      \"outputName\": \"_d8\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"____j0p0\",\
      \"outputName\": \"_d9\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"_____j0p0\",\
      \"outputName\": \"_d10\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"______j0p0\",\
      \"outputName\": \"_d11\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"_______j0p0\",\
      \"outputName\": \"_d12\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"________j0p0\",\
      \"outputName\": \"_d13\",\
      \"outputType\": \"DOUBLE\"\
    },\
    {\
      \"type\": \"default\",\
      \"dimension\": \"_________j0p0\",\
      \"outputName\": \"_d14\",\
      \"outputType\": \"DOUBLE\"\
    }\
  ],\
  \"limitSpec\": {\
    \"type\": \"default\",\
    \"columns\": [\
      {\
        \"dimension\": \"_d1\",\
        \"direction\": \"%s\",\
        \"dimensionOrder\": {\
          \"type\": \"numeric\"\
        }\
      }\
    ]\
  },\
  \"context\": {\
    \"sqlOuterLimit\": 1001,\
    \"sqlQueryId\": \"4aebd457-0d3b-49d9-a951-bbc22e38edb7\",\
    \"useNativeQueryExplain\": true\
  }\
}"

    def set_diff(self):
        """
        Set de parameters of the native query, distinguishing by the type
        of the query needed.
        """

        if self.type == "rise":
            if self.weeks == 5:
                self.change = "(p0 - greatest(((j0a0* 100.0) / %s),_j0p0,\
                               __j0p0, ___j0p0,____j0p0))" % self.total[0]
            elif self.weeks == 10:
                self.change = "(p0 - greatest(((j0a0 * 100.0) / %s),_j0p0,\
                               __j0p0, ___j0p0,____j0p0,_____j0p0,\
                               ______j0p0,_______j0p0,\
                               ________j0p0,_________j0p0))" % self.total[0]
            self.direction = "descending"
        else:
            if self.weeks == 5:
                self.change = "(p0 - least(((j0a0 * 100.0) / %s),_j0p0,__j0p0,\
                               ___j0p0,____j0p0))" % self.total[0]
            elif self.weeks == 10:
                self.change = "(p0 - least(((j0a0 * 100.0) / %s),_j0p0,__j0p0,\
                               ___j0p0,____j0p0,_____j0p0,______j0p0,_______j0p0,\
                               ________j0p0,_________j0p0))" % self.total[0]
            self.direction = "ascending"

    def calculate_totals(self):
        """
        Compute the total count for each week in the period
        and save it in one attribute of the class
        """
        for i in range(self.weeks + 1):
            count_total_search = self.total_query.format(self.shop,
                                                         self.start[i],
                                                         self.end[i])
            payload_total_searches = json.dumps({"query": count_total_search,
                                                "resultFormat": "array",
                                                 "context": {
                                                  "maxNumTasks": 4}})
            headers = {'Content-Type': 'application/json'}
            response_total_searches = (
              requests.request("POST", self.url_total, headers=headers,
                               data=payload_total_searches))

            # We retain de total number of seaches for each week
            self.total[i] = response_total_searches.json()[0][0]

    def generate_parameters(self):
        """
        Generates the paremeters for the query, including the shop,
        dates, totals, type and direction.
        """
        self.parameters = [self.shop, self.start[self.weeks],
                           self.end[self.weeks], self.total[self.weeks],
                           self.shop, self.start[0], self.end[0]]

        for i in range(1, self.weeks):
            self.parameters.append(self.shop)
            self.parameters.append(self.start[i])
            self.parameters.append(self.end[i])
            self.parameters.append(self.total[i])

        self.parameters.append(self.change)
        for i in range(3):
            self.parameters.append(self.total[0])
        self.parameters.append(self.direction)

    def generate_dataframe(self):
        """
        Compute the native query, where the percentage, min, max
        and the difference or change is calculated, the save it in
        a dataFrame
        """

        pretty_query = (self.percentage_query if self. weeks == 5
                        else self.percentage_query_10) % tuple(self.parameters)

        headers = {
            'Content-Type': 'application/json'
        }
        response_porcentajes = requests.request("POST", self.url_rate,
                                                headers=headers,
                                                data=pretty_query).json()

        # We save each result in an list
        # print(response_porcentajes)
        arr = []
        chart_array = []
        for i in range(len(response_porcentajes)):
            event = response_porcentajes[i]["event"]
            arr.append(event)
            for j in range(4, self.weeks + 5):
                info = {
                        "__time": self.start[j-5],
                        "Query": event["_d0"],
                        "Participation": event["_d" + str(j)],
                        "Change": event["_d1"]
                }
                chart_array.append(info)
        df = pd.DataFrame(arr)
        columns = []
        rename_columns = {"_d0": "Query", "_d1": "Change",
                          "_d2": "MAX", "_d3": "MIN"}
        for i in range(self.weeks + 5):
            if i != 4:
                columns.append('_d' + str(i))
            if i >= 5:
                rename_columns['_d' + str(i)] = self.period[i-5]
        columns.append('_d4')
        rename_columns['_d4'] = "Last week"

        df = df.reindex(columns=columns)
        df = df.rename(columns=rename_columns)
        self.final_dataFrame = df
        df_chart = pd.DataFrame(chart_array)
        self.final_chart_dataFrame = df_chart

    def show_graph(self):
        """
        Show a graph, with the first 10 searches with the the greater
        or lesser change, depending on the indicated type of query, of
        search rate with the maximum or minimun respectively
        """
        plt.figure(figsize=(8, 6))
        for i in range(10):
            plt.plot(self.period, self.final_dataFrame.iloc[i, 4:], 'v-',
                     label=self.final_dataFrame.iloc[i, 0])
        plt.xticks(self.period, rotation=60, fontsize=5)
        plt.ylabel("Search Rate")
        plt.xlabel("Period")
        plt.title(self.type[0].upper()+self.type[1:] +
                  " rate of searches in period")
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        plt.show()

    def generate_xlsx(self, type: str = 'table', route: str = ''):
        """
        Export the current dateframe to an excel file
        with extension xlsx
        """
        if type == 'table':
            self.final_dataFrame.to_excel(route + self.type + 'samples' +
                                          '_table_' +
                                          self.start[self.weeks] + '.' +
                                          self.end[self.weeks] + '.' +
                                          str(self.weeks) + self.shop +
                                          '.xlsx', index=False)
        elif type == 'chart':
            self.final_chart_dataFrame.to_excel(route + self.type +
                                                'samples' + '_chart_' +
                                                self.start[self.weeks] +
                                                '.' + self.end[self.weeks]
                                                + '.' + str(self.weeks)
                                                + self.shop + '.xlsx',
                                                index=False)

    def generate_csv(self, type: str = 'table', route: str = ''):
        """
        Export the current dateframe to an csv file
        """
        if type == 'table':
            self.final_dataFrame.to_csv(route + self.shop + "_" +
                                        self.type + "_table" + '.csv',
                                        index=False)
        elif type == 'chart':
            self.final_chart_dataFrame.to_csv(route + self.shop + "_" +
                                              self.type + "_chart" + '.csv',
                                              index=False)

    def save_graph(self, route: str = ''):
        """
        Export the current graph to an image file
        with extension png
        """
        plt.figure(figsize=(8, 6))
        for i in range(10):
            plt.plot(self.period, self.final_dataFrame.iloc[i, 4:], 'v-',
                     label=self.final_dataFrame.iloc[i, 0])
        plt.xticks(self.period, rotation=60, fontsize=5)
        plt.ylabel("Search Rate")
        plt.xlabel("Period")
        plt.title(self.type[0].upper()+self.type[1:] +
                  " rate of searches in period")
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        plt.savefig(route + self.type + 'samples' + self.start[self.weeks] +
                    '.' + self.end[self.weeks] + '.' + str(self.weeks) +
                    self.shop + '.png')

    def memory_usage_psutil(self) -> float:
        # return the memory usage in MB
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / float(2 ** 20)
        return mem


start = time.time()
if len(sys.argv) != 4:
    print('Use: python3 topsearches.py shop')
    sys.exit(1)
search_rate = SearchRate(shop=sys.argv[1], type='rise',
                         weeks=10)
search_rate.calculate_totals()
search_rate.set_diff()
search_rate.generate_parameters()
search_rate.generate_dataframe()
end = time.time()
print("Total time in seconds:", round(end - start, 2))
print("Peak Ram in MB:", round(search_rate.memory_usage_psutil(), 2))
search_rate.generate_csv('table')
search_rate.generate_csv('chart')
search_rate = SearchRate(shop=sys.argv[1], type='fall',
                         weeks=10)
search_rate.calculate_totals()
search_rate.set_diff()
search_rate.generate_parameters()
search_rate.generate_dataframe()
end = time.time()
print("Total time in seconds:", round(end - start, 2))
print("Peak Ram in MB:", round(search_rate.memory_usage_psutil(), 2))
search_rate.generate_csv('table')
search_rate.generate_csv('chart')
