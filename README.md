Should run on anything with python3 out of the box.

Change the `API_KEY` global variable in `upload_file.py`.

There were some ambiguous requirements:

* The filename returned is the filename output by the api. If you upload a file and it was hashed under a different name, they will differ.
* In the sample output, engines return `"Clean"` when a file is clean. In reality, it looks like the api returns `""`. I chose to just return the latter.


