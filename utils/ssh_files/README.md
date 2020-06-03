## the viz scripts takes the output from the funr scaling experiment *("exp_records(example)")* as input into the data pipeline it implements to produce figures as seen in ~/figures

set up python3 env:
- use output from exp_records(example) as input to the chart_all_full.py script, then run the chartit_error_bars.py.
- parameters for both scripts are [Query] [dir_name_of_exp_output] e.g. [solrj OR direct] [11-26::2_4_8_16_krgoejv]
e.g.
- `$ python3 chart_all_full.py direct 11-26::2_4_8_16_krgoejv`
  -> produces a compiled csv file for error_bar viz
- `$ python3 chartit_error_bars.py direct 11-26::2_4_8_16_krgoejv`
  -> produces html of the viz. 
