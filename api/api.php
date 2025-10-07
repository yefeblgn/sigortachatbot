<?php
header("Content-Type: application/json; charset=utf-8");
header("Access-Control-Allow-Origin: *");
require_once "db.php";

$allowed = ["musteri", "hasar_dosya", "kasko_teklif", "trafik_teklif", "ai_oturum", "log", "hasar_detay"];

$table = $_GET["table"] ?? "";
$id = isset($_GET["id"]) ? intval($_GET["id"]) : 0;
$tckn = $_GET["tckn"] ?? null;

if (!in_array($table, $allowed)) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid table name"]);
    exit;
}

try {
    if ($table === "hasar_detay") {
        if (!$tckn) {
            echo json_encode(["error" => "TCKN parametresi gerekli."]);
            exit;
        }
        $stmt = $conn->prepare("
            SELECT 
                h.dosya_no,
                h.police_no,
                h.durum,
                h.tutanak,
                h.tarih,
                m.ad,
                m.soyad,
                m.tckn,
                m.telefon,
                m.email
            FROM hasar_dosya h
            INNER JOIN musteri m ON h.musteri_id = m.id
            WHERE m.tckn = ?
            ORDER BY h.tarih DESC
            LIMIT 1
        ");
        $stmt->execute([$tckn]);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);
        echo json_encode(["success" => true, "data" => $data], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        exit;
    }

    if ($id > 0) {
        $stmt = $conn->prepare("SELECT * FROM $table WHERE id = ?");
        $stmt->execute([$id]);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);
    } else {
        $stmt = $conn->query("SELECT * FROM $table ORDER BY id DESC");
        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    echo json_encode(["success" => true, "data" => $data], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["error" => "Query failed", "detail" => $e->getMessage()]);
}
?>
