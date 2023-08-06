# protect-rm

A modified version of the rm protection

based on https://github.com/alanzchen/rm-protection

Added ability to setup protection for multiple files and directories with one profile.

use `protect + file_names...` to protect files and `protect -R + paths` to protect all files under certain directorys.

Change the /usr/bin/rm to rm_old

then you could change the /usr/local/bin/rm-p to rm