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
    try {
      const data = await callApi("/posts?limit=20&offset=0");
      setPosts(data);
      setError("");
    } catch (e) {
      setError(`Load posts failed: ${e.message}`);
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
      <header className="header">
        <h1>Pulse React UI</h1>
        <div className="api-box">
          <input value={apiBase} onChange={(e) => setApiBase(e.target.value)} />
          <button onClick={connect}>Connect</button>
        </div>
      </header>

      <section className="grid">
        <article className="card">
          <h2>Register</h2>
          <form onSubmit={register} className="stack">
            <input placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <input placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <input
              type="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Create account</button>
          </form>
        </article>

        <article className="card">
          <h2>Create Post</h2>
          <form onSubmit={createPost} className="stack">
            <input
              type="number"
              placeholder="author id"
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

      <section className="card">
        <h2>Feed</h2>
        {posts.length === 0 ? <p>No posts yet.</p> : posts.map((p) => <p key={p.id}>#{p.id} by {p.author_id}: {p.content}</p>)}
      </section>

      {message && <p className="ok">{message}</p>}
      {error && <p className="err">{error}</p>}
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
