// Translation Dictionary
const translations = {
    vi: {
        app: {
            title: "Meeting Analyzer Pro",
            team: "Made by Team 3"
        },
        sidebar: {
            recording: "Ghi âm",
            upload: "Tải lên",
            chat: "Chat AI",
            history: "Lịch sử"
        },
        initial: {
            recordNow: "Ghi âm ngay lập tức",
            clickToStart: "Nhấn để bắt đầu ghi âm"
        },
        chat: {
            title: "Trò chuyện với AI",
            clear: "Xóa đoạn chat",
            welcomeTitle: "AI Assistant",
            welcomeMessage: "Hỏi tôi bất cứ điều gì về cuộc họp của bạn!",
            inputPlaceholder: "Nhập tin nhắn..."
        },
        history: {
            title: "Lịch sử Cuộc họp",
            refresh: "Làm mới",
            table: {
                name: "Tên cuộc họp",
                date: "Ngày tạo",
                duration: "Thời lượng",
                status: "Trạng thái",
                actions: "Thao tác"
            }
        },
        recording: {
            modal: {
                title: "Ghi âm ngay lập tức",
                titleLabel: "Tiêu đề",
                language: "Ngôn ngữ hợp",
                audioSource: "Nguồn âm thanh",
                microphone: "Microphone",
                screen: "Tab/Màn hình (Screen Audio)",
                autoTranslate: "Tự động dịch (Bạn có muốn bản phiên âm được dịch không?)",
                translateTo: "Dịch sang"
            },
            screenShare: {
                why: "Tại sao chúng tôi cần bạn chia sẻ màn hình của bạn?",
                explanation: "Nếu bạn chọn không chia sẻ màn hình, ứng dụng có thể không thu được âm thanh từ các nguồn bên ngoài như Teams hoặc Google Meet, và do đó có thể không hoạt động như mong đợi",
                howTo: "Cách thu âm:",
                step1: "Một cửa sổ bật lên sẽ yêu cầu bạn chọn màn hình chia sẻ",
                step2: "Chọn tab \"Thẻ trình duyệt Chrome\"",
                step3: "Chọn tab có audio đang phát",
                step4: "BẬT checkbox \"Chia sẻ cả âm thanh trên thẻ\"",
                step5: "Nhấn \"Chia sẻ\"",
                allow: "Cho phép ghi âm màn hình"
            }
        },
        common: {
            loading: "Đang tải...",
            back: "Quay lại",
            continue: "Tiếp tục",
            confirm: "Xác nhận",
            processing: "Đang xử lý...",
            pleaseWait: "Vui lòng đợi trong giây lát"
        }
    },
    en: {
        app: {
            title: "Meeting Analyzer Pro",
            team: "Made by Team 3"
        },
        sidebar: {
            recording: "Recording",
            upload: "Upload",
            chat: "Chat AI",
            history: "History"
        },
        initial: {
            recordNow: "Record Now",
            clickToStart: "Click to start recording"
        },
        chat: {
            title: "Chat with AI",
            clear: "Clear chat",
            welcomeTitle: "AI Assistant",
            welcomeMessage: "Ask me anything about your meetings!",
            inputPlaceholder: "Type a message..."
        },
        history: {
            title: "Meeting History",
            refresh: "Refresh",
            table: {
                name: "Meeting Name",
                date: "Date Created",
                duration: "Duration",
                status: "Status",
                actions: "Actions"
            }
        },
        recording: {
            modal: {
                title: "Record Now",
                titleLabel: "Title",
                language: "Language",
                audioSource: "Audio Source",
                microphone: "Microphone",
                screen: "Tab/Screen (Screen Audio)",
                autoTranslate: "Auto-translate (Do you want the transcript translated?)",
                translateTo: "Translate to"
            },
            screenShare: {
                why: "Why do we need you to share your screen?",
                explanation: "If you choose not to share your screen, the app may not capture audio from external sources like Teams or Google Meet, and may not work as expected",
                howTo: "How to record:",
                step1: "A popup will ask you to select a screen to share",
                step2: "Select the \"Chrome Browser Tab\" tab",
                step3: "Select the tab with audio playing",
                step4: "ENABLE the \"Share tab audio\" checkbox",
                step5: "Click \"Share\"",
                allow: "Allow screen recording"
            }
        },
        common: {
            loading: "Loading...",
            back: "Back",
            continue: "Continue",
            confirm: "Confirm",
            processing: "Processing...",
            pleaseWait: "Please wait a moment"
        }
    },
    ja: {
        app: {
            title: "Meeting Analyzer Pro",
            team: "Made by Team 3"
        },
        sidebar: {
            recording: "録音",
            upload: "アップロード",
            chat: "AIチャット",
            history: "履歴"
        },
        initial: {
            recordNow: "今すぐ録音",
            clickToStart: "クリックして録音を開始"
        },
        chat: {
            title: "AIとチャット",
            clear: "チャットをクリア",
            welcomeTitle: "AIアシスタント",
            welcomeMessage: "会議について何でも聞いてください！",
            inputPlaceholder: "メッセージを入力..."
        },
        history: {
            title: "会議履歴",
            refresh: "更新",
            table: {
                name: "会議名",
                date: "作成日",
                duration: "期間",
                status: "ステータス",
                actions: "アクション"
            }
        },
        recording: {
            modal: {
                title: "今すぐ録音",
                titleLabel: "タイトル",
                language: "言語",
                audioSource: "音声ソース",
                microphone: "マイク",
                screen: "タブ/画面（画面音声）",
                autoTranslate: "自動翻訳（トランスクリプトを翻訳しますか？）",
                translateTo: "翻訳先"
            },
            screenShare: {
                why: "なぜ画面共有が必要ですか？",
                explanation: "画面を共有しない場合、TeamsやGoogle Meetなどの外部ソースから音声をキャプチャできず、期待どおりに動作しない可能性があります",
                howTo: "録音方法：",
                step1: "ポップアップで共有する画面を選択するよう求められます",
                step2: "「Chromeブラウザタブ」タブを選択",
                step3: "音声が再生されているタブを選択",
                step4: "「タブの音声を共有」チェックボックスを有効にする",
                step5: "「共有」をクリック",
                allow: "画面録画を許可"
            }
        },
        common: {
            loading: "読み込み中...",
            back: "戻る",
            continue: "続ける",
            confirm: "確認",
            processing: "処理中...",
            pleaseWait: "しばらくお待ちください"
        }
    },
    ko: {
        app: {
            title: "Meeting Analyzer Pro",
            team: "Made by Team 3"
        },
        sidebar: {
            recording: "녹음",
            upload: "업로드",
            chat: "AI 채팅",
            history: "기록"
        },
        initial: {
            recordNow: "지금 녹음",
            clickToStart: "클릭하여 녹음 시작"
        },
        chat: {
            title: "AI와 채팅",
            clear: "채팅 지우기",
            welcomeTitle: "AI 어시스턴트",
            welcomeMessage: "회의에 대해 무엇이든 물어보세요!",
            inputPlaceholder: "메시지 입력..."
        },
        history: {
            title: "회의 기록",
            refresh: "새로고침",
            table: {
                name: "회의 이름",
                date: "생성일",
                duration: "기간",
                status: "상태",
                actions: "작업"
            }
        },
        recording: {
            modal: {
                title: "지금 녹음",
                titleLabel: "제목",
                language: "언어",
                audioSource: "오디오 소스",
                microphone: "마이크",
                screen: "탭/화면 (화면 오디오)",
                autoTranslate: "자동 번역 (녹취록을 번역하시겠습니까?)",
                translateTo: "번역 대상"
            },
            screenShare: {
                why: "화면 공유가 필요한 이유는 무엇입니까?",
                explanation: "화면을 공유하지 않으면 Teams 또는 Google Meet과 같은 외부 소스에서 오디오를 캡처하지 못할 수 있으며 예상대로 작동하지 않을 수 있습니다",
                howTo: "녹음 방법:",
                step1: "팝업에서 공유할 화면을 선택하라는 메시지가 표시됩니다",
                step2: "\"Chrome 브라우저 탭\" 탭 선택",
                step3: "오디오가 재생 중인 탭 선택",
                step4: "\"탭 오디오 공유\" 체크박스 활성화",
                step5: "\"공유\" 클릭",
                allow: "화면 녹화 허용"
            }
        },
        common: {
            loading: "로딩 중...",
            back: "뒤로",
            continue: "계속",
            confirm: "확인",
            processing: "처리 중...",
            pleaseWait: "잠시 기다려 주세요"
        }
    },
    zh: {
        app: {
            title: "Meeting Analyzer Pro",
            team: "Made by Team 3"
        },
        sidebar: {
            recording: "录音",
            upload: "上传",
            chat: "AI聊天",
            history: "历史"
        },
        initial: {
            recordNow: "立即录音",
            clickToStart: "点击开始录音"
        },
        chat: {
            title: "与AI聊天",
            clear: "清除聊天",
            welcomeTitle: "AI助手",
            welcomeMessage: "问我关于您的会议的任何问题！",
            inputPlaceholder: "输入消息..."
        },
        history: {
            title: "会议历史",
            refresh: "刷新",
            table: {
                name: "会议名称",
                date: "创建日期",
                duration: "持续时间",
                status: "状态",
                actions: "操作"
            }
        },
        recording: {
            modal: {
                title: "立即录音",
                titleLabel: "标题",
                language: "语言",
                audioSource: "音频源",
                microphone: "麦克风",
                screen: "标签/屏幕（屏幕音频）",
                autoTranslate: "自动翻译（您想翻译转录吗？）",
                translateTo: "翻译为"
            },
            screenShare: {
                why: "为什么我们需要您共享屏幕？",
                explanation: "如果您选择不共享屏幕，应用程序可能无法从Teams或Google Meet等外部源捕获音频，并且可能无法按预期工作",
                howTo: "如何录音：",
                step1: "弹出窗口将要求您选择要共享的屏幕",
                step2: "选择\"Chrome浏览器标签\"标签",
                step3: "选择正在播放音频的标签",
                step4: "启用\"共享标签音频\"复选框",
                step5: "点击\"共享\"",,
                allow: "允许屏幕录制"
            }
        },
        common: {
            loading: "加载中...",
            back: "返回",
            continue: "继续",
            confirm: "确认",
            processing: "处理中...",
            pleaseWait: "请稍候"
        }
    }
};
