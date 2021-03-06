========
 MrMsay
========

.. image:: https://img.shields.io/github/release/janeappleseed/MrMsay.svg
   :target: https://github.com/janeappleseed/MrMsay/releases/latest

.. image:: https://img.shields.io/badge/license-WTFPL-blue.svg
   :target: COPYING

MrM's wisdom, right in your terminal.

.. contents:: In this document:

Dependencies
------------

- Python 3.3 or later;
- ``cowsay``.

Installation
------------

1. Via Homebrew::

     brew install workbrew/core/mrmsay

2. From source::

     ./setup.py install

   or for developers::

     ./setup.py develop

   Installation within a virtualenv is highly recommended.

Usage
-----

::

  usage: mrmsay [-h] [--auth USER:TOKEN] [--offline] [-v]

  MrM's wisdom, right in your terminal.

  optional arguments:
    -h, --help         show this help message and exit
    --auth USER:TOKEN  GitHub credentials for higher API rate limit (USER is
                       your GitHub handle and TOKEN is a personal access token);
                       credentials are automatically saved, so you only need to
                       path --auth once
    --offline          do not attempt to fetch new comments; by default the
                       program fetches new comments if it hasn't done so in the
                       last ten minutes
    -v, --version      show program's version number and exit

MrMsay also comes with a daemon, `mrmd`, which collects MrM's wisdom in
the background nonstop, so that you never miss out on anything and enjoy
faster queries when you `mrmsay`::

  usage: mrmd [-h] [-v]

  Collect Mrm's wisdom nonstop.

  optional arguments:
    -h, --help     show this help message and exit
    -v, --version  show program's version number and exit

Roadmap
-------

- Make MrMsay a 3-SAT oracle machine.

Sample wisdom
-------------

::

  $ mrmsay
  Querying MrM...
   _________________________________________________________________________
  / > Can you provide some feedback about whether this was a design         \
  | decision                                                                |
  |                                                                         |
  | This was not a design decision. It seems like it would be a sensible    |
  | change but it's very down my personal list of priorities.               |
  |                                                                         |
  | > whether this facilitated implementation                               |
  |                                                                         |
  | This issue does not facilitate implementation. It does not suggest any  |
  | specifics and it does not use the process that we've created to discuss |
  | feature requests.                                                       |
  |                                                                         |
  | > I'd like to collaborate to improve the analytics data                 |
  |                                                                         |
  | Collaboration is best achieved through pull requests.                   |
  |                                                                         |
  | > I haven't invested enough time to understand the implementation       |
  |                                                                         |
  | I would suggest that it's worth doing this before opening issues.       |
  |                                                                         |
  | --                                                                      |
  |                                                                         |
  | As I've mentioned before: I think maintainers opening "personal         |
  | preference" issues they don't plan to work on is a project smell. If    |
  | you're the person who cares about this: you should be the person to     |
  | work on it and unless that's happening in the short-term the best bet   |
  | is to create a pull request when you are ready to work on it. Otherwise |
  | our open issue count keeps growing and growing and it becomes hard to   |
  | keep track of what are actual outstanding problems that need addressed  |
  | and what are just maintainer "nice-to-haves" that will not be worked    |
  \ on.                                                                     /
   -------------------------------------------------------------------------
    \                                  ,+*^^*+___+++_
     \                           ,*^^^^              )
      \                       _+*                     ^**+_
       \                    +^       _ _++*+_+++_,         )
                _+^^*+_    (     ,+*^ ^          \+_        )
               {       )  (    ,(    ,_+--+--,      ^)      ^\
              { (@)    } f   ,(  ,+-^ __*_*_  ^^\_   ^\       )
             {:;-/    (_+*-+^^^^^+*+*<_ _++_)_    )    )      /
            ( /  (    (        ,___    ^*+_+* )   <    <      \
             U _/     )    *--<  ) ^\-----++__)   )    )       )
              (      )  _(^)^^))  )  )\^^^^^))^*+/    /       /
            (      /  (_))_^)) )  )  ))^^^^^))^^^)__/     +^^
           (     ,/    (^))^))  )  ) ))^^^^^^^))^^)       _)
            *+__+*       (_))^)  ) ) ))^^^^^^))^^^^^)____*^
            \             \_)^)_)) ))^^^^^^^^^^))^^^^)
             (_             ^\__^^^^^^^^^^^^))^^^^^^^)
               ^\___            ^\__^^^^^^))^^^^^^^^)\\
                    ^^^^^\uuu/^^\uuu/^^^^\^\^\^\^\^\^\^\
                       ___) >____) >___   ^\_\_\_\_\_\_\)
                      ^^^//\\_^^//\\_^       ^(\_\_\_\)
                        ^^^ ^^ ^^^ ^

  https://git.io/vP6Nj
