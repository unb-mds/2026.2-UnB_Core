import { useState } from 'react'
import { api, ApiError } from '../services/api'
import { login } from '../state/auth'
import AuthForm from '../components/auth/AuthForm'
import SiteFooter from '../components/SiteFooter'
import SiteHeader from '../components/SiteHeader'
import './AuthPage.css'

function LoginPage({ onNavigate }) {
  const [error, setError] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleLogin(form) {
    setIsSubmitting(true)
    setError(null)

    try {
      const session = await api.post('/auth/login', { email: form.email, senha: form.senha })
      login(session)
      onNavigate('/editais')
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : 'Não foi possível entrar na conta.')
      throw requestError
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="auth-page-shell">
      <SiteHeader active="" onNavigate={onNavigate} />
      <main className="auth-page">
        <section className="auth-card" aria-labelledby="login-title">
          <p className="auth-card__eyebrow">Acesso à plataforma</p>
          <h1 id="login-title">Entre na sua conta</h1>
          <p className="auth-card__intro">Acompanhe contribuições e participe do UNB CORE.</p>
          <AuthForm mode="login" onSubmit={handleLogin} isSubmitting={isSubmitting} error={error} />
          <p className="auth-card__switch">Ainda não possui uma conta? <a href="/cadastro" onClick={(event) => { event.preventDefault(); onNavigate('/cadastro') }}>Cadastre-se</a></p>
        </section>
      </main>
      <SiteFooter />
    </div>
  )
}

export default LoginPage