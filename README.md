PhpVanity
=========

A Sublime Text 2 Plugin to assist with common PHP formatting issues.

Current list of shortcuts

- Cmd-alt-b will fix single line control statements that are missing curlies.

``` php
if( $something )
  do_it();
```

``` php
if ( $something ) {
  do_it();
}
```

- Cmd-alt-v will fix spacing on single line control statements. Space will be added between the control word and opening paren. Additionally, space will be added between the closing paren and opening curly.

``` php
if( $something ){
```

``` php
if ( $something ) {
```

![Vanity](http://www.apetogentleman.com/wp-content/uploads/2010/12/Patrick-Bateman-2.jpg)
