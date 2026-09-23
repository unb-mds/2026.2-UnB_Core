import './ui.css'

const statusLabels = {
  ativa: 'Ativo',
  encerrada: 'Encerrado',
  arquivada: 'Arquivado',
}

function StatusBadge({ status, variant = 'status' }) {
  const label = statusLabels[status] || status || 'Não informado'
  const tone = status || 'unknown'

  return <span className={`badge badge-${variant} badge-${tone}`}>{label}</span>
}

export default StatusBadge