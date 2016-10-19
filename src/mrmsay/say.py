#!/usr/bin/env python3

import sh

# Specify custsom cowsay(1) path with the cowsay argument.
def say(body, cowsay=None):
    cowsay = sh.Command(cowsay if cowsay else 'cowsay')
    try:
        return str(cowsay(f='turkey', W='72', _in=body))
    except sh.ErrorReturnCode:
        # There's bug in older versions of Perl, e.g. system Perl (5.18.2) on
        # macOS 10.12 which could lead to cowsay spitting an error like
        #
        #     This shouldn't happen at /System/Library/Perl/5.18/Text/Wrap.pm
        #     line 84, <STDIN> line 1.
        #
        # in certain cases. The bug is in Text::Wrap 2012.0818 and was fixed in
        # 2013.0523. See http://www.perlmonks.org/?node_id=1070469#1070721.
        return str(cowsay(f='turkey', W='72', _in='...'))
