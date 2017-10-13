<?php
// Created: 18.08.2016
// Vladimir Vons, VladVons@gmail.com
//
// Echo client program



class TSockClient
{
    function __construct($aHost, $aPort)
    {
        $this->BufSize = 4096;
        $this->Connect($aHost, $aPort);
    }

    function __destruct()
    {
        $this->Close();
    }

    function Close()
    {
        if ($this->Sock)
            socket_close($this->Sock);
    }

    function Connect($aHost, $aPort)
    {
        $this->Sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($this->Sock !== false)
          socket_connect($this->Sock, $aHost, $aPort);
    }

    function Receive()
    {
        $Result = "";
        while (true) {
            $Data = socket_read($this->Sock, $this->BufSize);
            if ($Data) {
                $Result .= $Data;
                if (strlen($Data) < $this->BufSize)
                    break;
            }else
                break;
        }
        return $Result;
    }

    function Send($aData)
    {
        socket_write($this->Sock, $aData, strlen($aData));
        //$Result = socket_read($this->Sock, 1024);
        $Result = $this->Receive();
        return $Result;
    }

    function CallFunc()
    {
        $ArgCnt = func_num_args();
        if ($ArgCnt == 1)
          $Arr = array('Type' => 'Func', 'Name' => func_get_arg(0));
        elseif ($ArgCnt >= 2) {
          $Args = array();
          for ($i = 1; $i < $ArgCnt; $i++)
            $Args[] = func_get_arg($i);

          $Arr = array('Type' => 'Func', 'Name' => func_get_arg(0), 'Arg' => $Args);
        }else
          $Arr = array('Type' => 'Unknown');

        $Data = $this->Send(json_encode($Arr));
        return json_decode($Data, true)["Data"];
    }

    function Login($aUser, $aPassw)
    {
        return $this->CallFunc("AuthUser", $aUser, $aPassw);
    }
}

?>