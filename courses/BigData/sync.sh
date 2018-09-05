#!/bin/bash
#cat sync.sh
jekyll build 2>&1 
echo 'jekyll build complete'
# http://serverfault.com/questions/24622/how-to-use-rsync-over-ftp
scp -r  _site/. mobitec@lx1.ie.cuhk.edu.hk:htdocs/iems5709Fall2016/
echo 'scp complete'
