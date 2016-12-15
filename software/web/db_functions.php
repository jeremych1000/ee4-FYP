<?php
//collection of functions for orthonics server side stuffs

function db_connect() {
    // Define connection as a static variable, to avoid connecting more than once 
    static $connection;
    if(!isset($connection)) {
        $config = parse_ini_file('/home/pi/db_config.ini'); 
        $connection = mysqli_connect($config['db_server'], $config['db_user'], $config['db_pass'], $config['db_database']);
    }

    if($connection === false) {
        return mysqli_connect_error(); 
    }

    return $connection;
}

function db_query($query) {
    $connection = db_connect();
    $result = mysqli_query($connection,$query);
    return $result;
}

function db_error() {
    $connection = db_connect();
    return mysqli_error($connection);
}

function db_select($query) {
    $rows = array();
    $result = db_query($query);

    if($result === false) {
        return false;
    }

    // If query was successful, retrieve all the rows into an array
    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = $row;
    }

    return $rows;
}

//escape quotes to prevent sql injection
function db_quote($value) {
    $connection = db_connect();
    //return "'" . mysqli_real_escape_string($connection,$value) . "'";
    return mysqli_real_escape_string($connection, $value);
}

function get_md5_name(){
    $hash = substr(md5(rand() . time()), 0, 20);
    return $hash;
}

function my_print($a) {
    echo '<pre>'.print_r($a,1).'</pre>';
}

function print_row(&$item) {
  echo('<tr>');
  array_walk($item, 'print_cell');
  echo('</tr>');
}

function print_cell(&$item) {
  echo('<td>');
  echo($item);
  echo('</td>');
}

function validateDate($date, $format = 'Y-m-d H:i:s')
{
    //http://php.net/manual/en/function.date.php
    $d = DateTime::createFromFormat($format, $date);
    return $d && $d->format($format) == $date;
}
//echo urlencode('2016-05-05 23:00:01');

function url_get_contents ($Url) {
    if (!function_exists('curl_init')){ 
        die('CURL is not installed!');
    }
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $Url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $output = curl_exec($ch);
    curl_close($ch);
    return $output;
}

//http://stackoverflow.com/questions/6054033/pretty-printing-json-with-php
function prettyPrint( $json )
{
    $result = '';
    $level = 0;
    $in_quotes = false;
    $in_escape = false;
    $ends_line_level = NULL;
    $json_length = strlen( $json );

    for( $i = 0; $i < $json_length; $i++ ) {
        $char = $json[$i];
        $new_line_level = NULL;
        $post = "";
        if( $ends_line_level !== NULL ) {
            $new_line_level = $ends_line_level;
            $ends_line_level = NULL;
        }
        if ( $in_escape ) {
            $in_escape = false;
        } else if( $char === '"' ) {
            $in_quotes = !$in_quotes;
        } else if( ! $in_quotes ) {
            switch( $char ) {
                case '}': case ']':
                    $level--;
                    $ends_line_level = NULL;
                    $new_line_level = $level;
                    break;

                case '{': case '[':
                    $level++;
                case ',':
                    $ends_line_level = $level;
                    break;

                case ':':
                    $post = " ";
                    break;

                case " ": case "\t": case "\n": case "\r":
                    $char = "";
                    $ends_line_level = $new_line_level;
                    $new_line_level = NULL;
                    break;
            }
        } else if ( $char === '\\' ) {
            $in_escape = true;
        }
        if( $new_line_level !== NULL ) {
            $result .= "\n".str_repeat( "\t", $new_line_level );
        }
        $result .= $char.$post;
    }

    return $result;
}

//http://ryanuber.com/07-31-2012/split-and-decode-json-php.html
function json_split_objects($json)
{
    $q = FALSE;
    $len = strlen($json);
    for($l=$c=$i=0;$i<$len;$i++)
    {   
        $json[$i] == '"' && ($i>0?$json[$i-1]:'') != '\\' && $q = !$q;
        if(!$q && in_array($json[$i], array(" ", "\r", "\n", "\t"))){continue;}
        in_array($json[$i], array('{', '[')) && !$q && $l++;
        in_array($json[$i], array('}', ']')) && !$q && $l--;
        (isset($objects[$c]) && $objects[$c] .= $json[$i]) || $objects[$c] = $json[$i];
        $c += ($l == 0);
    }   
    return $objects;
}

?>