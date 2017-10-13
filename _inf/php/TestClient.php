#!/usr/bin/php

<?php
require_once("SockClient.php");

function SockConnect()
{
    $Port = 51002;
    $Host = "localhost";
    print("Client $Host, $Port\n");

    $SockClient = new TSockClient($Host, $Port);
    $Login = $SockClient->Login("VladVons", "1234");
    if ($Login == true) {
        print("Login OK\n");
        return $SockClient;
    }else{
        print("Login failed\n");
        exit();
    }
}

//---
function TestSocket()
{
    $SockClient = SockConnect();

    printf("SockClient.CallFunc:TAppMan.GetVersion() %s\n",        implode(",", $SockClient->CallFunc("TAppMan.GetVersion")));
    printf("SockClient.CallFunc:TAppMan.LoadFile() %s\n",          $SockClient->CallFunc("TAppMan.LoadFile", "samba.json"));
    printf("SockClient.CallFunc:TAppMan.User.List() %s\n",         $SockClient->CallFunc("TAppMan.User.List"));
}


//---
TestSocket();

?>