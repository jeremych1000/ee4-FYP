<?php
//header('Content-Type: application/json');
ini_set('display_errors',1);
error_reporting(E_ALL);

require_once 'db_functions.php';

// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
$image_name = $_GET["n"];
$region = $_GET["r"];

if (empty($image_name)) {
	die('Name cannot be empty, otherwise it will run on the entire directory!');
}

$exec_command = 'alpr --country '.$region.' --detect_region --json --topn 3'.' '.'upload/'.$image_name.' 2>&1';
$exec_output = shell_exec($exec_command);

//split video multiple json into array of json objects
$json = json_split_objects($exec_output);
my_print($json);

echo "\n-----------------------------\n";

//picture
if (sizeof($json) == 1){
	$exec_array = json_decode($json[0], true);
	if (json_last_error() == 0){
		my_print($exec_array);
	}
	else{
		die('JSON error code: '.json_last_error().', refer <a href="http://php.net/manual/en/function.json-last-error.php">here</a>.');
	}
}
//video
else{
	foreach ($json as $j) {
	    $exec_array = json_decode($j, true);
	    if (json_last_error() == 0){
			my_print($exec_array);
		}
		else{
			die('JSON error code: '.json_last_error().', refer <a href="http://php.net/manual/en/function.json-last-error.php">here</a>.');
		}
	}
}

echo "\n-----------------------------\n";



//$exec_array = json_encode($exec_array, JSON_PRETTY_PRINT);
//echo gettype($exec_array);

//echo gettype($exec_array);
//var_dump($exec_array);
//print_r($exec_array, true);
//$exec_json = json_encode($exec_output, JSON_PRETTY_PRINT);
//echo $exec_array;
//var_dump($exec_output);
//my_print($exec_array);

?>