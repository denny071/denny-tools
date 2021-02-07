#!/bin/sh
prject_list=(
    "/var/www/release_demo" 
    "/var/www/release_demo1"
)
for prject in ${prject_list[*]}
do 
    cd $prject && git pull origin master
done