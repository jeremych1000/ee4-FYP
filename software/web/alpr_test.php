<?php
//header('Content-Type: application/json');

// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
$image_name = $_GET["n"];
$region = $_GET["r"];

require_once 'db_functions.php';

//echo $image_name;
$exec_command = 'alpr -c '.$region.' --clock --detect_region'.' '.'upload/'.$image_name.' 2>&1';
//passthru($exec_output, $exec_return, $exec_output);
$exec_output = shell_exec($exec_command);
//echo gettype($exec_output);

//$exec_json = json_encode($exec_output, JSON_PRETTY_PRINT);
//echo pprettyPrint( $exec_output );
//var_dump($exec_output);
my_print($exec_output);
//array_walk($exec_output, 'print_row');
//echo exec('alpr '.$image_name);
?>