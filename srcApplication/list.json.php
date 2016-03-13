<?php
header('Access-Control-Allow-Origin: *');

echo '{
"data":{
"list":[
"Notification 1 content example",
"User xyz has liked your status",
"User abc has commented on the code diff #123"
]
}
}';