<?php
$data = json_encode("test test");
$ch = curl_init();
curl_setopt($ch, CURLOPT_PORT, 781);
curl_setopt($ch, CURLOPT_URL, 'http://127.0.0.1:781/tr');
curl_setopt($ch, CURLOPT_POST, count($data));
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$target_response = curl_exec($ch);
curl_close($ch);
echo $target_response;
?>