// Tradutor simples para português e inglês

export type Language = 'pt-BR' | 'en-US'

export const translations: Record<string, Record<Language, string>> = {
  // Partes
  'contratante': {
    'pt-BR': 'Contratante (quem contrata)',
    'en-US': 'Contractor (who hires)'
  },
  'contratada': {
    'pt-BR': 'Contratada (prestadora)',
    'en-US': 'Contractor (service provider)'
  },
  
  // Tipos de Data
  'inicio': {
    'pt-BR': 'Início',
    'en-US': 'Start'
  },
  'termino': {
    'pt-BR': 'Término',
    'en-US': 'End'
  },
  'renovacao': {
    'pt-BR': 'Renovação',
    'en-US': 'Renewal'
  },
  'prazo': {
    'pt-BR': 'Prazo',
    'en-US': 'Deadline'
  },
  
  // Tipos de Valor
  'salario_mensal': {
    'pt-BR': 'Salário Mensal',
    'en-US': 'Monthly Salary'
  },
  'salario_total': {
    'pt-BR': 'Salário Total',
    'en-US': 'Total Salary'
  },
  'multa': {
    'pt-BR': 'Multa',
    'en-US': 'Penalty'
  },
  'taxa': {
    'pt-BR': 'Taxa',
    'en-US': 'Rate'
  },
  
  // Tipos de Cláusula
  'confidencialidade': {
    'pt-BR': 'Confidencialidade',
    'en-US': 'Confidentiality'
  },
  'rescisao': {
    'pt-BR': 'Rescisão',
    'en-US': 'Termination'
  },
  'pagamento': {
    'pt-BR': 'Pagamento',
    'en-US': 'Payment'
  },
  'lgpd': {
    'pt-BR': 'LGPD',
    'en-US': 'GDPR'
  },
  
  // Risco
  'baixo': {
    'pt-BR': 'Baixo Risco',
    'en-US': 'Low Risk'
  },
  'medio': {
    'pt-BR': 'Risco Médio',
    'en-US': 'Medium Risk'
  },
  'alto': {
    'pt-BR': 'Alto Risco',
    'en-US': 'High Risk'
  }
}

export function translate(key: string, language: Language): string {
  const lowerKey = key.toLowerCase()
  return translations[lowerKey]?.[language] || key
}

export function translateText(text: string, language: Language): string {
  // Se o texto contém underscores, é um tipo
  if (text.includes('_')) {
    return translate(text, language)
  }
  // Caso contrário, retorna o texto original
  return text
}
