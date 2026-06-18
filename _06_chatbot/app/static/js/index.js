/*
    index.js 
    
    1. 로딩 UI 제어하기
    2. 채팅 메시지를 동적으로 화면에 추가하기
    3. fetch 공통 요청 함수 만들기
    4. 새 상담 세션 생성하기
    5. 사용자 메시지 전송하고 AI 응답 출력하기
    6. 세션 목록을 동적으로 렌더링하기
    7. 세션 클릭 시 과거 대화 복원하기
*/

const $app = document.querySelector("#app");

const API = {
    initConversation: $app.dataset.initUrl,
    chatbot: $app.dataset.chatbotUrl,
    removeConversation: $app.dataset.removeUrl,
    sessionList: $app.dataset.sessionListUrl,
    sessionMessages: $app.dataset.sessionMessagesUrl,
};

const STORAGE_KEY = "it-career-chatbot-session-id";

const state = {
    sessionId: null,
    isLoading: false,
};

const $ = {
    body: document.body,

    chatForm: document.querySelector("#chat-form"),
    userInput: document.querySelector("#user-input"),
    sendBtn: document.querySelector("#send-btn"),
    chatMessages: document.querySelector("#chat-messages"),

    loading: document.querySelector("#loading"),
    loadingText: document.querySelector("#loading-text"),
    status: document.querySelector("#status"),

    topSessionLabel: document.querySelector("#top-session-label"),
    currentSessionChip: document.querySelector("#current-session-chip"),
    drawerSessionId: document.querySelector("#drawer-session-id"),

    drawer: document.querySelector("#drawer"),
    drawerBackdrop: document.querySelector("#drawer-backdrop"),
    openDrawerBtn: document.querySelector("#open-drawer-btn"),
    closeDrawerBtn: document.querySelector("#close-drawer-btn"),

    newSessionBtn: document.querySelector("#new-session-btn"),
    endSessionBtn: document.querySelector("#end-session-btn"),

    sessionList: document.querySelector("#session-list"),
    sessionCount: document.querySelector("#session-count"),
};

/*
    TODO 1. 로딩 상태 처리

    1. state.isLoading 값을 isLoading으로 변경한다.
    2. $.loading 요소에 active 클래스를 추가하거나 제거한다.
    3. $.loadingText의 문구를 message 값으로 변경한다.
    4. $.sendBtn, $.userInput을 isLoading 값에 따라 비활성화한다.
*/
const setLoading = (isLoading, message = "처리 중입니다...") => {
    // TODO 1
    state.isLoading = isLoading;

    $.loading.classList.toggle("active", isLoading);
    $.loadingText.textContent = message;

    $.sendBtn.disabled = isLoading;
    $.userInput.disabled = isLoading;
};

const showStatus = (message, type = "success") => {
    $.status.textContent = message;
    $.status.className = `status show ${type}`;

    clearTimeout(showStatus.timer);

    showStatus.timer = setTimeout(() => {
        $.status.className = "status";
        $.status.textContent = "";
    }, 2600);
};

const getShortSessionId = (sessionId) => {
    if (!sessionId) return "없음";
    return `${sessionId.slice(0, 8)}...${sessionId.slice(-6)}`;
};

const updateSessionUI = () => {
    const label = state.sessionId ? getShortSessionId(state.sessionId) : "없음";

    $.topSessionLabel.textContent = state.sessionId ? `세션 ${label}` : "세션 없음";
    $.currentSessionChip.textContent = state.sessionId ? `현재 세션: ${state.sessionId}` : "현재 세션: 없음";
    $.drawerSessionId.textContent = state.sessionId || "없음";
};

const saveSessionId = (sessionId) => {
    state.sessionId = sessionId;

    if (sessionId) {
        sessionStorage.setItem(STORAGE_KEY, sessionId);
    } else {
        sessionStorage.removeItem(STORAGE_KEY);
    }

    updateSessionUI();
};

/*
    TODO 3. fetch 공통 JSON 요청 함수 만들기

    1. fetch(url, options)로 서버에 요청을 보낸다.
    2. response.ok가 false이면 Error를 발생시킨다.
    3. 응답이 성공이면 response.json() 결과를 반환한다.
*/
const requestJSON = async (url, options = {}) => {
    // TODO 3
    const response = await fetch(url, options);

    if(!response.ok) {
        throw new Error(`HTTP ${response.status}`)
    }

    return response.json();
};

/*
    TODO 2. 채팅 메시지를 화면에 추가하기

    1. message-row div를 생성한다.
    2. message div를 생성한다.
    3. sender 값에 따라 className을 지정한다.
       - row: message-row user 또는 message-row bot
       - message: message user 또는 message bot
    4. content를 message의 textContent로 넣는다.
    5. row 안에 message를 추가한다.
    6. chatMessages 영역에 row를 추가한다.
    7. 스크롤을 가장 아래로 이동시킨다.
*/
const addMessage = (content, sender = "bot") => {
    // TODO 2
    const row = document.createElement('div');
    row.className = `message-row ${sender}`;

    const message = document.createElement('div');
    message.className = `message ${sender}`
    message.textContent = content;

    row.appendChild(message);
    $.chatMessages.appendChild(row);
    $.chatMessages.scrollTop = $.chatMessages.scrollHeight;
};

const resetChatMessages = (message) => {
    $.chatMessages.innerHTML = "";
    addMessage(message, "bot");
};

const renderMessages = (messages) => {
    $.chatMessages.innerHTML = "";

    if (!messages.length) {
        addMessage("아직 저장된 대화 메시지가 없습니다.", "bot");
        return;
    }

    messages.forEach((message) => {
        const sender = message.type === "human" ? "user" : "bot";
        addMessage(message.content, sender);
    });
};

const escapeHTML = (value) => {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
};

const loadConversationMessages = async (sessionId) => {
    const url = `${API.sessionMessages}?session_id=${encodeURIComponent(sessionId)}`;
    const data = await requestJSON(url);

    return data.messages || [];
};

/*
    TODO 7. 선택한 세션의 과거 대화 복원하기

    1. 로딩 상태를 켠다.
    2. loadConversationMessages(sessionId)를 호출해 과거 메시지를 가져온다.
    3. 현재 sessionId를 선택한 sessionId로 저장한다.
    4. renderMessages(messages)로 채팅창을 다시 그린다.
    5. renderActiveSessionItem()으로 현재 선택된 세션 표시를 갱신한다.
    6. 성공 상태 메시지를 보여준다.
    7. Drawer를 닫는다.
*/
const restoreConversation = async (sessionId) => {
    try {
        // TODO 7
        setLoading(true, "대화 내용을 불러오는 중입니다...");

        const messages = await loadConversationMessages(sessionId);

        saveSessionId(sessionId);
        renderMessages(messages);
        renderActiveSessionItem();

        showStatus("세션을 전환했습니다.", "success");
        closeDrawer();

    } catch (error) {
        console.error(error);
        showStatus("세션 전환에 실패했습니다.", "error");
    } finally {
        setLoading(false);
        $.userInput.focus();
    }
};

const renderActiveSessionItem = () => {
    const items = $.sessionList.querySelectorAll(".session-item");

    items.forEach((item) => {
        item.classList.toggle("active", item.dataset.sessionId === state.sessionId);
    });
};

/*
    TODO 6. 세션 목록 렌더링하기

    1. 기존 세션 목록 영역을 비운다.
    2. 세션 개수를 화면에 표시한다.
    3. 세션이 없으면 안내 메시지를 출력하고 함수를 종료한다.
    4. sessionList를 반복하면서 button 요소를 만든다.
    5. button의 type, dataset.sessionId, className을 설정한다.
    6. button 내부에 세션 번호와 sessionId를 출력한다.
    7. button 클릭 시 restoreConversation(sessionId)를 호출한다.
    8. sessionList 영역에 button을 추가한다.
*/
const renderSessionList = (sessionList) => {
    // TODO 6
    $.sessionList.innerHTML = ``;
    $.sessionCount.textContent = `${sessionList.length}개`;

    if(!sessionList.length) {
        $.sessionList.innerHTML = `
            <div class="empty-session">
                서버에 남아있는 세션이 없습니다.<br>
                새 상담을 시작해주세요.
            </div>
        `;
        return;
    }

    sessionList.forEach((sessionId, index) => {
        const button = document.createElement("button");

        button.type = "button";
        button.dataset.sessionId = sessionId;
        button.className = `session-item ${sessionId === state.sessionId ? "active" : ""}`;
        button.innerHTML = `
            세션 ${index+1}
            <small>${escapeHTML(sessionId)}</small>
        `;

        // 세션 목록을 클릭하면 해당 세션으로 전환한 뒤 과거 메세지를 복원한다.
        button.addEventListener("click", () => {
            restoreConversation(sessionId);
        });

        $.sessionList.appendChild(button);
    })


};

const loadSessionList = async () => {
    try {
        $.sessionList.innerHTML = `<div class="empty-session">세션 목록을 불러오는 중입니다.</div>`;

        const data = await requestJSON(API.sessionList);
        renderSessionList(data.session_list || []);
    } catch (error) {
        console.error(error);

        $.sessionList.innerHTML = `
            <div class="empty-session">
                세션 목록을 불러오지 못했습니다.
            </div>
        `;

        $.sessionCount.textContent = "0개";
    }
};

const openDrawer = async () => {
    $.body.classList.add("drawer-open");
    $.drawer.classList.add("open");
    $.drawerBackdrop.classList.add("open");

    // Drawer를 열 때마다 별도 버튼 없이 세션 목록을 자동 조회한다.
    await loadSessionList();
};

const closeDrawer = () => {
    $.body.classList.remove("drawer-open");
    $.drawer.classList.remove("open");
    $.drawerBackdrop.classList.remove("open");
};

/*
    TODO 4. 새 상담 세션 시작하기

    1. 로딩 상태를 켠다.
    2. 새 상담 세션 생성 API에 POST 요청을 보낸다.
    3. 응답으로 받은 session_id를 저장한다.
    4. 채팅 메시지 영역을 새 상담 안내 문구로 초기화한다.
    5. 세션 목록을 다시 불러온다.
    6. 성공 상태 메시지를 보여준다.
    7. Drawer를 닫는다.
*/
const newConversation = async () => {
    try {
        // TODO 4
        setLoading(true, "새 상담 세션을 생성하는 중입니다...");

        const data = await requestJSON(API.initConversation, {
            method: 'POST'
        })

        saveSessionId(data.session_id)

        resetChatMessages(
            "새 상담이 시작 되었습니다.\n현재 관심있는 IT 분야나 고민을 말씀해주세요."
        );

        await loadSessionList();

        showStatus("새로운 상담이 시작 되었습니다.", "success");
        closeDrawer();

    } catch (error) {
        console.error(error);
        showStatus("상담 시작에 실패했습니다.", "error");
    } finally {
        setLoading(false);
        $.userInput.focus();
    }
};

/*
    TODO 5. 사용자 메시지 전송하기

    1. 입력값을 가져오고 trim 처리한다.
    2. 입력값이 없으면 안내 메시지를 보여주고 종료한다.
    3. 현재 sessionId가 없으면 Drawer를 열고 종료한다.
    4. 로딩 상태를 켠다.
    5. 사용자 메시지를 화면에 먼저 추가한다.
    6. 입력창을 비운다.
    7. FormData를 만들고 session_id, query를 추가한다.
    8. chatbot API에 POST 요청을 보낸다.
    9. 응답으로 받은 AI 메시지를 화면에 추가한다.
*/
const sendMessage = async () => {
    // TODO 5
    const query = $.userInput.value.trim();

    if(!query) {
        showStatus("메세지를 입력해주세요.", "error");
        return;
    }

    if(!state.sessionId) {
        showStatus("먼저 새 상담을 시작해주세요.", "error");
        openDrawer();
        return;
    }

    try {
        setLoading(true, "상담사가 답변을 준비하고 있습니다...");

        addMessage(query, "user");
        $.userInput.value = "";

        const formData = new FormData();
        formData.append("session_id", state.sessionId);
        formData.append("query", query);

        const data = await requestJSON(API.chatbot, {
            method: 'POST',
            body: formData
        })

        addMessage(data.content, "bot")

    } catch(error) {
        console.error(error);
        addMessage("답변을 받는 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.", "bot");
        showStatus("답변 요청에 실패했습니다.", "error");
    } finally {
        setLoading(false);
        $.userInput.focus();
    }
};

const endConversation = async () => {
    if (!state.sessionId) {
        showStatus("종료할 세션이 없습니다.", "error");
        return;
    }

    const confirmed = window.confirm("현재 상담 세션을 종료하시겠습니까?");
    if (!confirmed) return;

    try {
        setLoading(true, "상담 세션을 종료하는 중입니다...");

        await requestJSON(API.removeConversation, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                session_id: state.sessionId,
            }),
        });

        saveSessionId(null);

        resetChatMessages(
            "상담이 종료되었습니다.\n다시 상담을 받으려면 세션 관리에서 새 상담 시작을 눌러주세요."
        );

        await loadSessionList();

        showStatus("상담이 종료되었습니다.", "success");
    } catch (error) {
        console.error(error);
        showStatus("상담 종료에 실패했습니다.", "error");
    } finally {
        setLoading(false);
    }
};

const init = async () => {
    const savedSessionId = sessionStorage.getItem(STORAGE_KEY);

    if (!savedSessionId) {
        updateSessionUI();
        return;
    }

    try {
        setLoading(true, "이전 세션을 복원하는 중입니다...");

        const messages = await loadConversationMessages(savedSessionId);

        saveSessionId(savedSessionId);
        renderMessages(messages);
    } catch (error) {
        /*
            개발 서버가 재시작되면 views.py의 전역 store가 초기화된다.
            이 경우 브라우저에는 session_id가 남아 있어도 서버에는 해당 세션이 없다.

            DB 기반 history로 변경하면 서버를 재시작해도 DB에 저장된 세션은 유지된다.
        */
        console.error(error);

        saveSessionId(null);
        resetChatMessages(
            "저장된 세션을 서버에서 찾을 수 없습니다.\n새 상담을 시작해주세요."
        );
    } finally {
        setLoading(false);
        $.userInput.focus();
    }
};

$.chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage();
});

$.openDrawerBtn.addEventListener("click", openDrawer);
$.closeDrawerBtn.addEventListener("click", closeDrawer);
$.drawerBackdrop.addEventListener("click", closeDrawer);

$.newSessionBtn.addEventListener("click", newConversation);
$.endSessionBtn.addEventListener("click", endConversation);

window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeDrawer();
    }
});

init();