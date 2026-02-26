const { useState, useEffect } = React;

function App() {
  const [apiBase, setApiBase] = useState("http://127.0.0.1:8000");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authorId, setAuthorId] = useState("");
  const [content, setContent] = useState("");
  const [posts, setPosts] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const callApi = async (path, options = {}) => {
    const res = await fetch(`${apiBase}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
    return data;
  };

  const loadPosts = async () => {
    setLoading(true);
    try {
      const data = await callApi("/posts?limit=20&offset=0");
      setPosts(data);
      setError("");
    } catch (e) {
      setError(`Load posts failed: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPosts();
  }, []);

  const connect = async () => {
    try {
      await callApi("/health");
      setMessage(`Connected to ${apiBase}`);
      setError("");
      await loadPosts();
    } catch (e) {
      setError(`Connection failed: ${e.message}`);
    }
  };

  const register = async (event) => {
    event.preventDefault();
    try {
      const user = await callApi("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, username, password }),
      });
      setAuthorId(String(user.id));
      setEmail("");
      setUsername("");
      setPassword("");
      setMessage(`Registered user #${user.id}`);
      setError("");
    } catch (e) {
      setError(e.message);
    }
  };

  const createPost = async (event) => {
    event.preventDefault();
    try {
      const post = await callApi("/posts", {
        method: "POST",
        body: JSON.stringify({ author_id: Number(authorId), content }),
      });
      setContent("");
      setMessage(`Created post #${post.id}`);
      setError("");
      await loadPosts();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <main className="app">
      <header className="top-nav card">
        <div className="brand">
          <h1>Pulse</h1>
          <p>React Learning UI</p>
        </div>
        <div className="api-box">
          <input value={apiBase} onChange={(e) => setApiBase(e.target.value)} aria-label="API base URL" />
          <button onClick={connect}>Connect</button>
        </div>
      </header>

      <section className="grid">
        <article className="card">
          <h2>Create Account</h2>
          <form onSubmit={register} className="stack">
            <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Register</button>
          </form>
        </article>

        <article className="card">
          <h2>Create Post</h2>
          <form onSubmit={createPost} className="stack">
            <input
              type="number"
              placeholder="Author ID"
              value={authorId}
              onChange={(e) => setAuthorId(e.target.value)}
              required
            />
            <textarea
              placeholder="What’s happening?"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
            />
            <button type="submit">Publish</button>
          </form>
        </article>
      </section>

      <section className="card feed-card">
        <div className="feed-header">
          <h2>Feed</h2>
          <button className="ghost" onClick={loadPosts}>Refresh</button>
        </div>

        {loading && <div className="loader">Loading posts…</div>}

        {!loading && posts.length === 0 && <p className="muted">No posts yet. Publish your first update.</p>}

        {!loading && posts.map((p) => (
          <article key={p.id} className="post-item">
            <p className="post-meta">Post #{p.id} · Author #{p.author_id}</p>
            <p>{p.content}</p>
          </article>
        ))}
      </section>

      {message && <p className="ok">{message}</p>}
      {error && <p className="err">{error}</p>}
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
