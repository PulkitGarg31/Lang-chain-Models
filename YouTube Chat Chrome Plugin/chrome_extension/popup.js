const BACKEND = "http://localhost:8000/chat";
let currentUrl = "";
let isLoading = false;

// Detect YouTube URL
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url;
  if (url && url.includes("youtube.com/watch")) {
    currentUrl = url;
    const params = new URL(url).searchParams;
    const videoId = params.get("v");
    document.getElementById("video-url").textContent = "v=" + videoId;
    document.getElementById("status-dot").classList.remove("off");

    chrome.storage.session.get(videoId, (data) => {
      if (data[videoId] && data[videoId].length > 0) {
        hideEmpty();
        data[videoId].forEach(msg => addMessage(msg.text, msg.role));
      }
    });

  } else {
    document.getElementById("video-url").textContent = "No YouTube video detected";
    document.getElementById("send").disabled = true;
    document.getElementById("error-msg").textContent = "Open a YouTube video to start chatting.";
  }
});

function hideEmpty() {
  const e = document.getElementById("empty-state");
  if (e) e.remove();
}

// Parse simple markdown → HTML
function parseMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^### (.+)$/gm, '<strong>$1</strong>')
    .replace(/^## (.+)$/gm, '<strong>$1</strong>')
    .replace(/^\* (.+)$/gm, '<li>$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/\n{2,}/g, '</p><p>')
    .replace(/^(?!<)(.+)$/gm, '$1');
}

function addMessage(text, role) {
  hideEmpty();
  const chatBox = document.getElementById("chat-box");
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${role === "user" ? "user-av" : "bot-av"}`;
  avatar.textContent = role === "user" ? "Y" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (role === "user") {
    bubble.textContent = text;
  } else {
    bubble.innerHTML = `<p>${parseMarkdown(text)}</p>`;
  }

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
  return bubble;
}
function saveMessage(text, role) {
  const videoId = new URL(currentUrl).searchParams.get("v");
  chrome.storage.session.get(videoId, (data) => {
    const history = data[videoId] || [];
    history.push({ text, role });
    chrome.storage.session.set({ [videoId]: history });
  });
}
function addTyping() {
  hideEmpty();
  const chatBox = document.getElementById("chat-box");
  const row = document.createElement("div");
  row.className = "msg-row bot";
  row.id = "typing-row";

  const avatar = document.createElement("div");
  avatar.className = "avatar bot-av";
  avatar.textContent = "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
  return row;
}

async function sendQuery() {
  if (isLoading) return;
  const query = document.getElementById("query").value.trim();
  if (!query || !currentUrl) return;

  isLoading = true;
  document.getElementById("send").disabled = true;
  document.getElementById("error-msg").textContent = "";
  document.getElementById("query").value = "";
  document.getElementById("query").style.height = "auto";

  addMessage(query, "user");
  saveMessage(query, "user");

  const typingRow = addTyping();

  try {
    const response = await fetch(BACKEND, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: currentUrl, query }),
    });

    typingRow.remove();
    const bubble = addMessage("", "bot");

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      fullText += decoder.decode(value);
      bubble.innerHTML = `<p>${parseMarkdown(fullText)}</p>`;
      document.getElementById("chat-box").scrollTop = document.getElementById("chat-box").scrollHeight;
    }

    saveMessage(fullText, "bot");
  } catch (err) {
    typingRow.remove();
    addMessage("Could not reach backend. Make sure it's running on port 8000.", "bot");
    document.getElementById("error-msg").textContent = "Backend unreachable.";
  }

  isLoading = false;
  document.getElementById("send").disabled = false;
  document.getElementById("query").focus();
}

// Auto-resize textarea
document.getElementById("query").addEventListener("input", function() {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 80) + "px";
});

document.getElementById("send").addEventListener("click", sendQuery);
document.getElementById("query").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendQuery();
  }
});