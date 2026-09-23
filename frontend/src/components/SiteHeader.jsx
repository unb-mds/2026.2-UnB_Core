import './ui/ui.css'

function SiteHeader({ active = 'editais' }) {
  return (
    <nav className="topbar" aria-label="Navegação principal">
      <a className="topbar__logo" href="/">unbcore</a>
      <div className="topbar__links">
        <a className={active === 'conhecimento' ? 'topbar__link--active' : ''} href="/base-de-conhecimentos">
          Base de conhecimento
        </a>
        <a className={active === 'editais' ? 'topbar__link--active' : ''} href="/editais" aria-current={active === 'editais' ? 'page' : undefined}>
          Editais
        </a>
        <a className="topbar__login" href="/login">Entrar</a>
      </div>
    </nav>
  )
}

export default SiteHeader