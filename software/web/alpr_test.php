<?php
//header('Content-Type: application/json');
ini_set('display_errors',1);
error_reporting(E_ALL);

require_once 'db_functions.php';

//sorting functions
function usort_cmp_gr($a, $b){
    return ($a[2] < $b[2]);
}

// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
$image_name = $_GET["n"];
$region = $_GET["r"];

if (empty($image_name)) {
	die('Name cannot be empty, otherwise it will run on the entire directory!');
}

//define variables here
$result = array();

//--detect_region 
$exec_command = 'alpr --country '.$region.' --json --topn 3'.' '.'upload/'.$image_name.' 2>&1';
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
	    	//rememebr to use decoded json string and not json string itself
	    	//array ( plate number, count, confidence, avg confidence)
			foreach ($exec_array['results'] as $k) {
				//for each decoded result, search if already exists in array
				//if so, increment, if not, add
				//2D array, PLATE / COUNT
				$k_search = array_search($k['plate'], array_column($result, 0));
				if ($k_search !== FALSE){ //can add $strict = true to end of array_search if needed
					$result[$k_search][1] += 1; 
					$result[$k_search][2] += $k['confidence']; 
					//$result[$k_search][3] = ($result[$k_search][2] / $result[$k_search][1]); 
				}
				else{
					//append to end of array
					$result[] = array($k['plate'], 1, $k['confidence']);
				}
			}
		}
		else{
			die('JSON error code: '.json_last_error().', refer <a href="http://php.net/manual/en/function.json-last-error.php">here</a>.');
		}
	}
}

echo "\n-----------------------------\n";

echo "Printing array...\n";

my_print($result);

echo "\n-----------------------------\n";

echo "Sorting array...\n";

usort($result, 'usort_cmp_gr');

my_print($result);

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