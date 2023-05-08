#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';

# perl -CSD -w -i -pe ... *.txt

# 删除俄文注释
s/\([^\p{Han}\)]*\)//;

# 删除特殊注释
s/^.*(【|〈|\[).*//m; # ?

# 删除俄文行
s/.*\p{Cyrillic}.*[^\n]//;

# 删除空格和空行
s/\s*//; # ?

# 添加空格
s/(\)|\,)/$1 /g;
s/(\()/ $1/g;

s/[ ]+/ /g;    # 删除重复的空格
s/\) ,/),/g;   # 删除多余的空格
s/(^ | $)//mg; # 删除行首行尾多余的空格

# 列表化
s/^(.)/· $1/mg;