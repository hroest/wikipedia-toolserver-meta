//by cyroxx
<?php
	function ConnectToMyDBServer($SqlServer = "sql-s2") {
		// Gibt die MySQL-Kennung der geöffneten Verbindung zurück
		
		// Hole die Zugangsdaten zur MySQL-Datenbank
		$filename = "/home/hroest/.my.cnf";

		if (!file_exists($filename)) {
			die("Zugangsdaten koennen nicht eingelesen werden. Datei nicht gefunden.");
		}
			
		$handle = fopen ($filename, "r");
		while (!feof($handle)) {
		   $buffer = fgets($handle, 4096);
		   $cnf_data .= $buffer;
		}
		fclose ($handle);

		// Extrahiere die Zugangsdaten
		$UserMuster = "/user = (.*)\n/";
		preg_match($UserMuster, $cnf_data, $treffer);
		$loginusername = $treffer[1];

		$PwdMuster = "/password = \"(.*)\"\n/";
		preg_match($PwdMuster, $cnf_data, $treffer);
		$loginpwd = $treffer[1];

		// Zugangsdaten extrahiert
		// Verbinde mit Datenbank

		/* Verbindung aufbauen */
		$link = mysql_connect($SqlServer, $loginusername, $loginpwd)
		   or die("Keine Verbindung moeglich: " . mysql_error());
		//echo "Verbindung zum Datenbankserver erfolgreich";
		
		return $link;
	}
?>
