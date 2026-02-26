const state = { apiBase: "http://127.0.0.1:8000" };

const el = (id) => document.getElementById(id);

function setMsg(id, text, ok = true) {
  const node = el(id);
  node.textContent = text;
  node.style.color = ok ? "#86efac" : "#fca5a5";
}

async function api(path, options = {}) {
  const res = await fetch(`${state.apiBase}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
  return data;
}

async function loadPosts() {
  try {
    const posts = await api("/posts?limit=20&offset=0");
    const feed = el("feed");
    feed.innerHTML = "";
    if (!posts.length) {
      feed.innerHTML = '<div class="post"><div class="meta">No posts yet</div>Create one using the form above.</div>';
      return;
    }
    posts.forEach((post) => {
      const card = document.createElement("article");
      card.className = "post";
      card.innerHTML = `
        <div class="meta">post #${post.id} · author #${post.author_id}</div>
        <div>${post.content}</div>
      `;
      feed.appendChild(card);
    });
  } catch (err) {
    setMsg("postResult", `Failed loading posts: ${err.message}`, false);
  }
}

el("connectApi").addEventListener("click", async () => {
  state.apiBase = el("apiBase").value.trim().replace(/\/$/, "");
  try {
    await api("/health");
    setMsg("postResult", `Connected to ${state.apiBase}`);
    await loadPosts();
  } catch (err) {
    setMsg("postResult", `Connection failed: ${err.message}`, false);
  }
});

el("userForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    email: el("email").value.trim(),
    username: el("username").value.trim(),
  };
  try {
    const user = await api("/users", { method: "POST", body: JSON.stringify(payload) });
    setMsg("userResult", `Created user #${user.id} (${user.username})`);
    el("authorId").value = user.id;
    event.target.reset();
    el("authorId").value = user.id;
  } catch (err) {
    setMsg("userResult", err.message, false);
  }
});

el("postForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    author_id: Number(el("authorId").value),
    content: el("postContent").value.trim(),
  };
  try {
    const post = await api("/posts", { method: "POST", body: JSON.stringify(payload) });
    setMsg("postResult", `Published post #${post.id}`);
    el("postContent").value = "";
    await loadPosts();
  } catch (err) {
    setMsg("postResult", err.message, false);
  }
});

el("refreshPosts").addEventListener("click", loadPosts);
loadPosts();
