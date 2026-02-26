const API = import.meta.env.VITE_API_URL || ''

export const authHeaders = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function api(path: string, options: RequestInit = {}) {
  const headers: Record<string, string> = { ...authHeaders(), ...(options.headers as Record<string, string> || {}) }
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }
  const response = await fetch(`${API}${path}`, { ...options, headers })
  if (!response.ok) throw new Error(await response.text())
  const text = await response.text()
  return text ? JSON.parse(text) : {}
}
