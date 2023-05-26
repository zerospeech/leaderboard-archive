#  Zerospeech Challenges Leaderboards

This repository contains the archives of all the zerospeech challenge leaderboard entries.

Entries are split into individual `[.yaml|.json]` files inside an entry folder.


For more information on the zerospeech challenges you can visit our website: [zerospeech.com](http://zerospeech.com).

# List of challenges


| challenge                  	                | url                                          	| status   	 |
|---------------------------------------------|----------------------------------------------	|------------|
| [zr2015](data/challenges/zr2015/README.md) 	 | http://zerospeech.com/tracks/2015/tasks/     	| archived 	 |
| [zr2017](data/challenges/zr2017/README.md) 	 | http://zerospeech.com/tracks/2017/tasks/     	| archived 	 |
| [zr2019](data/challenges/zr2019/README.md) 	 | http://zerospeech.com/tracks/2019/tasks/     	| archived 	 |
| [zr2020](data/challenges/zr2020/README.md) 	 | http://zerospeech.com/tracks/2020/tasks/     	| archived 	 |
| [zr2021](data/challenges/zr2021/README.md) 	 | http://zerospeech.com/tracks/2021/02_track1/ 	| archived   |



## Submit your scores


To submit into an active challenge you are encouraged to follow the instructions 
on the website [zerospeech.com](http://zerospeech.com).


Archived challenges have published benchmarks (or will be published at a future 
date) so evaluations of entries can happen locally, you can send us those results 
in the form of a pull request.


Fork this repository, add the corresponding entries into their respective folder, 
and create a pull request.

>In your pull request it is recommended to add a link to a published paper; and explanation of your results.


## Scripts

**extract.py :** a script allowing to unpack a leaderboard.json into individual entries.

**pack.py :** a script allowing to pack individual entries into a single leaderboard.json file.

**convert.py :** a script allowing to convert yaml files to json.


## Contact

If you face any issue or have questions you can open an issue on this repository,
or send us an email on [contact@zerospeech.com](mailto:contact@zerospeech.com)