// Helpers para enriquecer dados de análise com contexto

export interface EnrichedDate {
  value: string
  type: 'inicio' | 'termino' | 'renovacao' | 'prazo' | 'outro'
  description: string
}

export interface EnrichedValue {
  value: string
  type: 'salario' | 'taxa' | 'multa' | 'total' | 'outro'
  description: string
}

export interface EnrichedClause {
  value: string
  type: 'confidencialidade' | 'multa' | 'rescisao' | 'pagamento' | 'lgpd' | 'outro'
  description: string
  risk: 'baixo' | 'medio' | 'alto'
}

export function enrichDates(dates: string[]): EnrichedDate[] {
  return dates.map(date => {
    let type: EnrichedDate['type'] = 'outro'
    let description = ''

    const lowerDate = date.toLowerCase()

    if (lowerDate.includes('início') || lowerDate.includes('inicio') || lowerDate.includes('começa') || lowerDate.includes('a partir')) {
      type = 'inicio'
      description = 'Data de início do contrato'
    } else if (lowerDate.includes('término') || lowerDate.includes('termino') || lowerDate.includes('fim') || lowerDate.includes('até')) {
      type = 'termino'
      description = 'Data de término/expiração do contrato'
    } else if (lowerDate.includes('renovação') || lowerDate.includes('renovacao') || lowerDate.includes('renova')) {
      type = 'renovacao'
      description = 'Data de renovação automática ou revisão'
    } else if (lowerDate.includes('prazo') || lowerDate.includes('dias') || lowerDate.includes('meses')) {
      type = 'prazo'
      description = 'Prazo para cumprimento de obrigações'
    } else {
      // Tentar inferir pela data
      const datePattern = /\d{1,2}\/\d{1,2}\/\d{4}|\d{4}-\d{2}-\d{2}/
      if (datePattern.test(date)) {
        description = 'Data importante do contrato'
      }
    }

    return { value: date, type, description }
  })
}

export function enrichValues(values: string[]): EnrichedValue[] {
  return values.map(value => {
    let type: EnrichedValue['type'] = 'outro'
    let description = ''

    const lowerValue = value.toLowerCase()

    if (lowerValue.includes('mensal') || lowerValue.includes('mês')) {
      type = 'salario'
      description = 'Valor mensal de pagamento'
    } else if (lowerValue.includes('total') || lowerValue.includes('estimado')) {
      type = 'total'
      description = 'Valor total do contrato'
    } else if (lowerValue.includes('multa') || lowerValue.includes('penalidade')) {
      type = 'multa'
      description = 'Multa por descumprimento'
    } else if (lowerValue.includes('%') || lowerValue.includes('percentual')) {
      type = 'taxa'
      description = 'Taxa ou percentual aplicável'
    } else if (/r\$\s*[\d.,]+/i.test(value)) {
      // Detectar valores em reais
      if (value.includes('multa')) {
        type = 'multa'
        description = 'Multa por descumprimento'
      } else if (value.includes('total')) {
        type = 'total'
        description = 'Valor total do contrato'
      } else {
        type = 'salario'
        description = 'Valor monetário do contrato'
      }
    }

    return { value, type, description }
  })
}

export function enrichClauses(clauses: string[]): EnrichedClause[] {
  return clauses.map(clause => {
    let type: EnrichedClause['type'] = 'outro'
    let description = ''
    let risk: EnrichedClause['risk'] = 'baixo'

    const lowerClause = clause.toLowerCase()

    if (lowerClause.includes('confidencialidade') || lowerClause.includes('sigilo')) {
      type = 'confidencialidade'
      description = 'Obrigação de manter sigilo sobre informações'
      risk = 'medio'
    } else if (lowerClause.includes('multa') || lowerClause.includes('penalidade')) {
      type = 'multa'
      description = 'Penalidades por descumprimento'
      risk = 'alto'
    } else if (lowerClause.includes('rescisão') || lowerClause.includes('rescisao') || lowerClause.includes('término') || lowerClause.includes('termino')) {
      type = 'rescisao'
      description = 'Condições para encerramento do contrato'
      risk = 'alto'
    } else if (lowerClause.includes('pagamento') || lowerClause.includes('remuneração') || lowerClause.includes('remuneracao')) {
      type = 'pagamento'
      description = 'Termos e condições de pagamento'
      risk = 'alto'
    } else if (lowerClause.includes('lgpd') || lowerClause.includes('proteção de dados') || lowerClause.includes('protecao de dados')) {
      type = 'lgpd'
      description = 'Conformidade com Lei Geral de Proteção de Dados'
      risk = 'alto'
    }

    return { value: clause, type, description, risk }
  })
}

export function getRiskColor(risk: 'baixo' | 'medio' | 'alto'): string {
  switch (risk) {
    case 'baixo':
      return 'bg-green-50 border-green-200'
    case 'medio':
      return 'bg-yellow-50 border-yellow-200'
    case 'alto':
      return 'bg-red-50 border-red-200'
    default:
      return 'bg-gray-50 border-gray-200'
  }
}

export function getRiskBadgeColor(risk: 'baixo' | 'medio' | 'alto'): string {
  switch (risk) {
    case 'baixo':
      return 'bg-green-100 text-green-800'
    case 'medio':
      return 'bg-yellow-100 text-yellow-800'
    case 'alto':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export function formatDate(dateStr: string): string {
  // Tentar converter para formato mais legível
  const datePattern = /(\d{1,2})\/(\d{1,2})\/(\d{4})/
  const match = dateStr.match(datePattern)
  
  if (match) {
    const [, day, month, year] = match
    const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day))
    return date.toLocaleDateString('pt-BR', { 
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  return dateStr
}
