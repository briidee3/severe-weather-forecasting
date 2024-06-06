# This folder contains a modified version of the [MS-RNN repo](https://github.com/mazhf/MS-RNN/tree/main).

The original MS-RNN repo was not created by me (BD).

I have, however, customized it to an extent, including a custom data loader/handler (which was mostly derived from `util/load_kth.py`) for the custom dataset I put together from GOES ABI data.

The original config file that came with the repo has been copied to `config_default.py`, and the custom one is listed here as `config.py`.

I have also modified several of the other files in order to make them compatible with my custom data handler.


I have more plans to implement other things, however this is where I'm at as of right now (7-27-23).
