#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';

# perl -w -i -pe "`cat resources/regex/regex.pl`" resources/datasets/russian/chinese2russian/*.txt

# 将不在行首的"·"移动至行首
s/(?<!^)·/\n·/mg;

# 统一词性的大小写
s/\[`(.*)`\]/[`\L$1`]/mg;

# 括号前后空格
s/([^\s]+)(\()/$1 $2/mg;
s/([^\s]+)(\[)/$1 $2/mg;
s/(\])([^\s]+)/$1 $2/mg;

# ++++++++++
s/\++/++++++++++/mg;

# 删除冗余的空格
s/(^\ +|\ +$)//mg;

# handle [`...`]
s/\[`([^`]+)`\]/[<span style="color: black;"; style="font-weight: bold;">$1<\/span>]/mg;

# handle `...`
s/`([^`]+)`/<span style="color: red;">$1<\/span>/mg;

# handle 1. ...
s/(^\d.+$)/<div class="point">\n\t$1\n<\/div>/mg;

# handle · ...
s/(^·.+$)/<ul>\n$1\n<\/ul>/mg;
s/^· (.*)$/\t<li>$1<\/li>/mg;
s/([,.?!"']) \(/$1 <br> \(/mg;