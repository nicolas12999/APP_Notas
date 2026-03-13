<?php
$host = getenv('DB_HOST') ?: 'db';
$user = getenv('DB_USER') ?: 'root';
$pass = getenv('DB_PASSWORD') ?: '';
$db   = getenv('DB_NAME') ?: 'test_db';

echo "<h1>Probando la conexión a MariaDB</h1>";

// Ocultar warnings para manejar el error manualmente
mysqli_report(MYSQLI_REPORT_OFF);

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    echo "<p style='color:red;'>Error de conexión: " . htmlspecialchars($conn->connect_error) . "</p>";
} else {
    echo "<p style='color:green;'>¡Conectado exitosamente a la base de datos usando mysqli normal!</p>";
}

// Información del sistema
echo "<h3>Versiones:</h3>";
echo "<ul>";
echo "<li>PHP Version: " . phpversion() . "</li>";
echo "<li>MariaDB Server Info: " . (isset($conn) && !$conn->connect_error ? $conn->server_info : 'N/A') . "</li>";
echo "</ul>";

if (!$conn->connect_error) {
    $conn->close();
}
?>
