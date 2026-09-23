import { useState } from 'react'
import { api, ApiError } from '../services/api'
import AuthForm from '../components/auth/AuthForm'
import SiteFooter from '../components/SiteFooter'
import SiteHeader from '../components/SiteHeader'
import './AuthPage.css'

function CadastroPage({ onNavigate }) {
  const [error, setError] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSignup(form) {
    setIsSubmitting(true)
    setError(null)

    try {
      await api.post('/auth/cadastro', form)
      onNavigate('/login?cadastro=sucesso')
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : 'Não foi possível criar sua conta.')
      throw requestError
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="auth-page-shell">
      <SiteHeader active="" onNavigate={onNavigate} />
      <main className="auth-page">
        <section className="auth-card" aria-labelledby="signup-title">
          <p className="auth-card__eyebrow">Primeiro acesso</p>
          <h1 id="signup-title">Crie sua conta</h1>
          <p className="auth-card__intro">Participe da comunidade acadêmica da UnB.</p>
          <AuthForm mode="signup" onSubmit={handleSignup} isSubmitting={isSubmitting} error={error} />
          <p className="auth-card__switch">Já possui uma conta? <a href="/login" onClick={(event) => { event.preventDefault(); onNavigate('/login') }}>Entrar</a></p>
        </section>
      </main>
      <SiteFooter />
    </div>
  )
}

export default CadastroPage