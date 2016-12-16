<?php

ini_set('display_errors',1);
error_reporting(E_ALL);

require_once 'db_functions.php';

//mysql_* is deprecated, use mysqli instead
//$db = db_connect();

//////////////////////////////////////
$run_alpr = @$_POST["run_alpr"];
$alpr_region = @$_POST["region"];

if(isset($_FILES['image'])){
	$errors= array();

	$img_dir = 'upload/';

	$file_tmp = $_FILES['image']['tmp_name'];
	$file_name = $_FILES['image']['name'];
	$file_size = $_FILES['image']['size'];
	$file_type = $_FILES['image']['type'];   
	$file_mime = @mime_content_type($file_tmp); //use mime type as html header has no extension
	//$file_ext = strtolower(end(explode('/',$file_ext)));
	//$file_ext = pathinfo($file_name, PATHINFO_EXTENSION);

	//allowed extensions
	switch($file_mime){
		case 'image/png':
			$file_ext = 'png';
			break;
		case 'image/jpeg':
			$file_ext = 'jpg';
			break;
		case 'video/mp4':
			$file_ext = 'mp4';
			break;
		default:
			$file_ext = 'not_allowed'; //http://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types
			break;
	}
	
	//$extensions= array('jpg','png'); 		
	if($file_ext === 'not_allowed'){
		$errors[]='No file selected, or extension not allowed, please choose a JPEG or PNG (preferred) file.';
		die('No file selected, or extension not allowed, please choose a JPEG or PNG (preferred) file.');
	}

	$max_file_size = 20;
	if(($file_size > $max_file_size*1024*1024) OR ($file_size === 0)){
		$errors[]='File size must be larger than 0 bytes and smaller than '.$max_file_size.' MB.';
		die('File size must be larger than 0 bytes and smaller than '.$max_file_size.' MB.');
	}		
	
	if(empty($errors)===true){
		//UPLOAD AND ENTER INTO DATABASE HERE
		//do{ //check if duplicate file name (should never happen...)
			$hash = get_md5_name();
			$newName = $hash . '.' . $file_ext;
			$fullName = $img_dir.$newName;
		//} while (file_exists($fullName) === true);

		//standardize everything to PNG
		//if($file_ext == 'jpeg' || $file_ext == 'jpg'){
		//	imagepng(imagecreatefromjpeg($file_tmp), $fullName);
		//}

		$move_success = move_uploaded_file($file_tmp, $fullName);

		if ($move_success === true){
			//echo $fullName;
			if ($run_alpr){
				header( 'Location: http://jeremych.zapto.org/~pi/ee4-FYP/software/web/alpr_test.php?r='.$alpr_region.'&n='.$newName );
			}
			else{
				die('Upload successful, alpr not run.');
			}
		}
		else{
			print_r($errors);
			die('Failed to move file.');
		}
				
		
	}
	else{
		print_r($errors);
		die();
	}
}
else{
	echo 'No image in POST request. <br /> Current POST request is: <br />';
	echo '<pre>';
	var_dump($_POST);
	echo '</pre>';
}
?>
