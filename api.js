import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function searchUrl(url, query) {
  const resp = await axios.post(`${API_BASE}/search`, { url, query });
  return resp.data;
}

export async function indexUrl(url, query) {
  const resp = await axios.post(`${API_BASE}/index_url`, { url, query });
  return resp.data;
}

