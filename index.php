<?php
require __DIR__ . '/vendor/autoload.php';

use LINE\LINEBot;
use LINE\LINEBot\HTTPClient\CurlHTTPClient;
use LINE\LINEBot\Event\MessageEvent\TextMessage;
use LINE\LINEBot\MessageBuilder\FlexMessageBuilder;
use LINE\LINEBot\MessageBuilder\Flex\ContainerBuilder\BubbleContainerBuilder;
use LINE\LINEBot\MessageBuilder\Flex\ComponentBuilder\ImageComponentBuilder;
use LINE\LINEBot\MessageBuilder\Flex\ComponentBuilder\TextComponentBuilder;
use LINE\LINEBot\MessageBuilder\Flex\ComponentBuilder\BoxComponentBuilder;
use LINE\LINEBot\TemplateActionBuilder\UriTemplateActionBuilder;
use LINE\LINEBot\TemplateActionBuilder\MessageTemplateActionBuilder;

$channelAccessToken = '7S6uRt1efIK0AUIui+qa9vt2bWnz86gnDcPNjABtR3P5uByKuYJJDHeOgFAAZzsG+EtJBX40Pwy0Jcy8WNEVdBURddWDACSMpOyYMH2LPaNcHjYq1Izo21Zc4ueGnJTavVa4QQg+7P3l/jQgGXSyZAdB04t89/1O/w1cDnyilFU=';
$channelSecret = 'cbe452940ec4cc7ddd8eff15f25b37cb';

$httpClient = new CurlHTTPClient($channelAccessToken);
$bot = new LINEBot($httpClient, ['channelSecret' => $channelSecret]);

$host = 'localhost';
$db   = 'durian_project';
$user = 'root';
$pass = 'woon043697';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
    throw new \PDOException($e->getMessage(), (int)$e->getCode());
}

$signature = $_SERVER['HTTP_' . LINEBot\Constant\HTTPHeader::LINE_SIGNATURE];
$events = $bot->parseEventRequest(file_get_contents('php://input'), $signature);


// ...

foreach ($events as $event) {
    if ($event instanceof TextMessage) {
        $messageText = $event->getText();
        
        if ($messageText == 'เริ่มต้นใช้งาน') {
            $replyText = 'ต้องการให้ช่วยเรื่องอะไรครับ';
        } elseif ($messageText == 'ติดต่อแอดมิน') {
            $replyText = 'กรุณาติดต่อแอดมินที่เบอร์โทรศัพท์ต่อไปนี้ 095-2812895';
        } else {
            $stmt = $pdo->prepare('SELECT username FROM users WHERE cause = ?');
            $stmt->execute([$messageText]);
            $name = $stmt->fetchColumn();
            
            if ($name) {
                $flexMessage = FlexMessageBuilder::builder()
                    ->setAltText('ข้อมูลนักเรียน')
                    ->setContents(
                        BubbleContainerBuilder::builder()
                            ->setBody(
                                BoxComponentBuilder::builder()
                                    ->setLayout('vertical')
                                    ->setContents([
                                        TextComponentBuilder::builder()
                                            ->setText('ชื่อนักเรียน:')
                                            ->setWeight('bold'),
                                        TextComponentBuilder::builder()
                                            ->setText($name)
                                            ->setWrap(true)
                                    ])
                            )
                    );
                $bot->replyMessage($event->getReplyToken(), $flexMessage);
                return;
            } else {
                $replyText = 'ไม่พบเลขประจำตัวนักเรียนที่ระบุ';
            }
        }
        
        $bot->replyText($event->getReplyToken(), $replyText);
    }
}