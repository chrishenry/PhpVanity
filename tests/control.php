<?php

/**
 * Test that the control statement functionality works
 *
 * If default key bindings are used, then hit alt+cmd+
 *
 */

$x = false;

if($x = 2)
  echo 'yaya!';


if($x = 2) // a comment
  echo 'yaya!';


switch($x){
  case 1:
    echo 'stuff';
    break;
}
