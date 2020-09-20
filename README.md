# TweetDeck-棒読みちゃんバイパス

## 本ツールについて

TweetDeck のポップアップ通知を利用して  
タイムラインに流れるツイート文章を 「棒読みちゃん」 に読んでもらうツール  
(VOICEROIDに読んでもらうことも可能)  

___

## システムイメージ

　**TweetDeck**  
　　　↓ ポップアップ通知  
　**TweetDuck Plugin**  
　　　↓ ducktext出力  
　監視フォルダ　⇐　**bouyomi_bypass.exe** ：フォルダ監視 (Python: watchdog)  
　　　　　　　　　　　　↓ ファイル検知時: ducktext読み込み & コマンドライン実行  
　　　　　　　　　**RemoteTalk.exe**  
　　　　　　　　　　　　↓  起動  
　　　　　　　　　**棒読みちゃん.exe** ：合成音声の読み上げ  
　　　　　　　　　　　　↓  ※オプション ：読み上げ文章転送 (Voiceroid Talk Plus)  
　　　　　　　　　**VOICEROID**  
___

## 導入手順

1. 必要なソフトウェア
    - TweetDuck - https://tweetduck.chylex.com  
        TweetDeck の単独アプリケーション  
        各種設定の強化とCSSによる介入ができる拡張性の高いソフト  

        JavaScriptベースの Plugin を実装することで独自機能追加も可能  
        → TweetDeck のポップアップ通知イベントにてツイートを検知しファイルに出力  

        **☆☆ ----- お知らせ ----- ☆☆**  
        TweetDuck を初めて使う方向けに  
        *「漢字が中華フォントっぽくなってしまう問題」* が解決できるCSSがあります。  
        　→ (Git) `TweetDuckCSS` フォルダ内 `browser_adjust.css`    

        **【カスタムCSSの設定】**  
        画面上で右クリック、メニューの [Options] から [Advanced] を開く  
        CONFIGURATION の [Edit CSS] をクリック  
        [Browser]タブにカスタムCSSを書き込み [Apply]  
        .

    - 棒読みちゃん - https://chi.usamimi.info/Program/Application/BouyomiChan/  
        入力した日本語の文章を合成音声で読み上げるツール  
        → ファイルに出力されたツイート内容を本ツールで展開し、ここに文字列を送る  

    - **【任意】** VOICEROID系ソフトウェア  
        棒読みちゃんに追加するプラグインを利用することで VOICEROID による読み上げが可能  
        対応ソフトは [Voiceroid Talk Plus](https://ch.nicovideo.jp/Wangdora/blomaga/ar126461) を参照  

        ・VOICEROID - https://www.ah-soft.com/voiceroid/  
        （個人的にはここが本ツールの目的）  

2. TweetDuck Plugin の設定  
    - 画面上で右クリック、メニューの [Options] から [Notifications] を開く  
      Duration の時間をなるべく小さめに設定 (TL速度によっては最低値推奨)  

    - 画面上で右クリック、メニューの [Plugins] を開く  
      左下の [Open Plugin Folder] をクリック  

      <インストールディレクトリ>/TweetDuck/plugins/user フォルダに  
      (Git) `TweetDuckPlugin` フォルダにある `notification_bridge` のフォルダ以下をコピー  
      ```
      [配置イメージ]
      ...\TweetDuck\plugins\user\notification_bridge\.meta
      ...\TweetDuck\plugins\user\notification_bridge\.browser.js
      ...\TweetDuck\plugins\user\notification_bridge\.notification.js
      ```
      配置後は [Reload All] ボタンで再読み込みを行うと、追加したプラグインが表示される  

3. TweetDeck (TweetDuck) ポップアップ通知 の設定  
    - 各カラムのヘッダ部・右側にある設定ボタンをクリック  
      Preferences を選択して展開し [Enable desktop notifications] をチェックする  
      設定ボタンを再度クリックしてカラムの設定を閉じる  
      → とりあえず設定する場合は Home カラムへの設定を推奨  


4. 棒読みちゃん の設定  
    - [Voiceroid Talk Plus](https://ch.nicovideo.jp/Wangdora/blomaga/ar126461) のリンクを参照  
      プラグインの設定項目を変更した後は 棒読みちゃん の再起動を忘れずに  


5. VOICEROID の設定  
    - 特に設定する必要はなし  
      お気に入りのVOICEROIDを起動して待機  


6. bouyomi_bypass.exe の設定  
    - (Git) `ExecutableFile` フォルダにある `bouyomi_bypass.exe` を任意のフォルダにコピー  
      (同一ディレクトリにある `config.ini` は一緒にコピーしてもいいですが中身の情報は実質空)  

    - [監視フォルダ] には TweetDuck の監視先ディレクトリである以下を指定  
    ```
    C:\Users\<ユーザ名>\AppData\Local\TweetDuck\TD_Plugin\custom\notification_bridge  
    ```

    - [RemoteTalk] には「棒読みちゃん」に同梱されている `RemoteTalk` フォルダにある exe を指定  
    ```
    <棒読みちゃんフォルダ>\RemoteTalk\RemoteTalk.exe
    ```

    - [転送開始] で監視フォルダへの ducktext ファイルの追加を監視する処理を開始  
      [停止] で監視を終了  

    - [設定を保存] をクリックすると bouyomi_bypass.exe があるフォルダに `config.ini` を出力  
      次回起動時、`config.ini` を元に「監視フォルダ」と「RemoteTalk」のパスを自動で設定する  

    - 本ツールは画面を閉じてもタスクトレイに常駐しています  
      タスクkill (完全に終了) するにはタスクトレイの本アイコンを右クリックし [Exit] で終了  

    - 何らかのエラーが発生してエラーダイアログが表示した場合、内部の処理は停止します。  
      再度使用する場合は bouyomi_bypass.exe を一旦終了してから起動し直して下さい。  

___  

## ヘルプ

- 設定したポップアップ通知がONになっているのに通知されない／通知されなくなった  
→ 自分もとても悩まされた。  
　憶測の域を出ないが TweetDeck と TweetDuck 間での設定の同期バグの可能性。  

　　　以下の操作を行うと通知が来なくなる可能性があることを予め把握しておいて下さい  
　　　　- TweetDuck の右クリックメニュー [Reload browser] によるリフレッシュ  
　　　　- ポップアップ通知の ON/OFF 切り替え操作を短時間に続けて行う  
　　　　- TweetDuck の再起動  

　　　対処としては、通知していた or 通知させたいカラムを新たに追加し  
　　　追加したそのカラムのポップアップ通知を ON に設定することで通知が復活します  
　　　(ダメなら TweetDuck 本体の再起動なども試すこと)  

　　　例) Notifications カラムの通知が来なくなった場合  
　　　　(1) "Notifications" カラムを新たに追加する (新Notifications)  
　　　　(2) 新Notifications のポップアップ通知を ON にする (フィルタ設定なし)  
　　　　(3) 通知が来なくなってしまった　旧Notifications カラムを削除する  
　　　　(4) 新Notifications カラムが通知を受けることができたら解決  
　　　　　  (通知を受信することが出来た後にフィルタ設定を行うこと推奨)  

- 一時的に読み上げを行わないようにする方法は？  
→ 止める手段としては複数あるので、いずれかの方法で止めて下さい  
　  - `bouyomi_bypass.exe` の停止  
　  - TweetDuck Plugin `"Notification Bridge"` を `Disable` に設定  
　  - TweetDuck の右クリックメニュー [Mute Notifications] を ON に設定  

　　　　ポップアップ通知を OFF にすることでも対応は可能ですが  
　　　　直前に挙げた懸念がある為、復帰させる予定がある場合は推奨できません  

- 監視フォルダの掃除はどうするのか？  
→ 考えたけど、システムファイルやらを削除してしまったらシャレにならないので現時点では未実装。  
  ducktext ファイル限定にすれば良さそう。  
  しかしファイル追加の監視と読み込み処理に衝突しない、安全な非同期処理の考慮が必要なため保留。  
  ~~というかまだ Python 勉強して数日なので許して欲しい。~~  

___

## おすすめの通知用カラム設定

いずれもデフォルトの 「Home」 「Notifications」 が既にある状態で  
普段のタイムラインを確認する用とは別に、読み上げ専用のカラムを追加すると便利  

1. Home カラム  

| 設定項目 | 設定値 | 備考 |
---|---|---
| Tweet content - Excluding | <自分のID> | Notifications との併用時に読み上げ重複を避ける為 |
| Tweet content - Retweets | excluded | リツートを除外 |
| Preferences - MEDIA PREVIEW SIZE | Hidden | 読上げ用カラムのため不要 |

.

2. Notifications カラム  

| 設定項目 | 設定値 | 備考 |
---|---|---
| Notification types | Mentions, Quoted Tweets のみ | 読み上げの都合の問題 |
| Preferences - MEDIA PREVIEW SIZE | Hidden | 読上げ用カラムのため不要 |

.

3. 気になるジャンルのイラスト検索カラム 設定例

| 設定項目 | 設定値 | 備考 |
---|---|---
| Tweet content - Showing | Tweets with images | 画像付きツイートのみ |
| Tweet content - Matching | <キーワード> | ハッシュタグでもよい |
| Tweet content - Retweets | excluded | リツートを除外 |
| Engagement - Retweets | 5 (任意) | リツート指定回以上 (AND条件) |
| Engagement - likes | 10 (任意) | いいね指定回以上 (AND条件) |

___

## ライセンス

MIT Licence

___

## 免責事項

本ソフトウェアはフリーソフトです。  
個人・法人に限らず利用者は自由に使用することができますが  
著作権は放棄していないことをご留意下さい。  

また、本ツールを利用した事によるいかなる損害も作者は一切の責任を負いません。  
自己の責任の上でご使用下さい。  

勉強の一貫で作成したツールではありますが  
バグや要望については可能な範囲で行うかもしれませんし行わないかもしれません。  

なお、このツール以上に良いものを作成できる自信をお持ちの方は  
もっと良いものを作って世に発信して頂けたらと思います。  

by yuzuriha
