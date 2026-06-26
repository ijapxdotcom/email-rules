import re
from typing import Dict

def classificar_email(remetente: str, assunto: str, corpo: str = "") -> Dict[str, str]:
    """
    Motor Determinístico de RuleOps (Fase 1).
    Avalia remetente, assunto e corpo do e-mail para roteamento corporativo.
    Retorna um dicionário padronizado pronto para consumo de APIs ou Agentes MCP.
    """
    
    # Normalização de dados para o Regex
    remetente = remetente.lower()
    texto_completo = f"{assunto} {corpo}".lower()

    # ==========================================
    # BLOCO 1: PRIORIDADE MÁXIMA (RISCOS E GOVERNO)
    # ==========================================
    
    # Regra 3: Risco Contratual e Prazos
    if re.search(r'(notifica[cç][aã]o de atraso|prorroga[cç][aã]o de prazo|cronograma|of[ií]cio)', texto_completo):
        return {
            "categoria": "Risco Contratual e Prazos",
            "destino": "Engenharia / Gestão de Contas (Aloisio)",
            "prioridade": "MÁXIMA",
            "acao": "Rotear para Aloisio montar resposta executiva/técnica para mitigar risco financeiro."
        }

    # Regra 6: Oportunidades Gov (Portais)
    if re.search(r'(cota[cç][aã]o eletr[oô]nica|dispensa de licita[cç][aã]o|comprasnet|14\.133)', texto_completo):
        return {
            "categoria": "Oportunidades Gov. (COMPRASNET/14.133)",
            "destino": "Comercial / Licitações",
            "prioridade": "ALTA - CRÍTICO",
            "acao": "Analisar objeto, verificar período oficial de disputa e preparar proposta."
        }

    # Regra 7: Licitações Estatais
    if re.search(r'(licita[cç][aã]o eletr[oô]nica aberta|copasa|envio de propostas)', texto_completo):
        return {
            "categoria": "Licitações Estatais",
            "destino": "Comercial / Licitações",
            "prioridade": "ALTA - CRÍTICO",
            "acao": "Acessar portal da estatal, baixar edital e analisar viabilidade técnica."
        }

    # Regra 8: Pesquisa de Preços Judiciária
    if re.search(r'(pesquisa de pre[cç]os|prorroga[cç][aã]o da vig[eê]ncia|solicita[cç][aã]o de or[cç]amento|tst)', texto_completo):
        return {
            "categoria": "Pesquisa de Preços Judiciária",
            "destino": "Comercial / Gestão de Contas",
            "prioridade": "ALTA - CRÍTICO",
            "acao": "Analisar viabilidade de prorrogação e emitir proposta assinada."
        }

    # ==========================================
    # BLOCO 2: CORE BUSINESS (CFTV, SCA, ENGENHARIA)
    # ==========================================

    # Regra 9: Projetos Técnicos (Core Business)
    if re.search(r'(cftv|sca|c[aâ]meras|controle de acesso|v[ií]deomonitoramento)', texto_completo):
        return {
            "categoria": "Projetos Técnicos (Core)",
            "destino": "Engenharia / Pré-Vendas",
            "prioridade": "ALTA",
            "acao": "Analisar escopo técnico, levantar quantitativos e preparar viabilidade."
        }

    # Regra 11: Gestão de Contratos e CREA
    if re.search(r'(art|crea|pendente de aprova[cç][aã]o|apostilamento|aditivo de replanilhamento)', texto_completo):
        return {
            "categoria": "Gestão de Contratos e CREA",
            "destino": "Licitações e Contratos / Engenharia (Kevin Diego)",
            "prioridade": "ALTA - TRAVA FATURAMENTO",
            "acao": "Analisar pendência no CREA e validar necessidade de ART de substituição."
        }

    # Regra 10: Assinaturas Externas Governamentais
    if re.search(r'(assinatura externa|disponibilizada para a assinatura)', texto_completo):
        return {
            "categoria": "Assinaturas Externas Governamentais",
            "destino": "Diretoria / Administrativo (Marcelo de Almeida)",
            "prioridade": "ALTA",
            "acao": "Acessar portal do órgão (ex: SEI) e notificar diretoria para assinatura digital."
        }

    # ==========================================
    # BLOCO 3: OPERAÇÃO COMERCIAL E SUPRIMENTOS
    # ==========================================

    # Regra 2: Cotações e Contratos Gerais
    if re.search(r'(cota[cç][aã]o de pre[cç]o|contratos|aditivos)', texto_completo):
        return {
            "categoria": "Cotações e Contratos",
            "destino": "Gestão de Contas (Aloisio)",
            "prioridade": "ALTA",
            "acao": "Marcar com status 'Novo' e atribuir responsabilidade direta ao Aloisio."
        }

    # Regra 5: Fornecimento e Faturamento
    if re.search(r'(faturamento|faturar|cnpj|proposta para fornecimento|cadastro)', texto_completo):
        return {
            "categoria": "Fornecimento e Faturamento",
            "destino": "Compras / Financeiro (Aloisio)",
            "prioridade": "MÉDIA",
            "acao": "Alinhamento de negociação técnica e correção de dados fiscais com o fornecedor."
        }

    # Regra 13: Fornecedores Técnicos
    if re.search(r'(invenzi|intelbras|dahua)', texto_completo) or re.search(r'(invenzi|intelbras|dahua)', remetente):
        return {
            "categoria": "Fornecedores Técnicos",
            "destino": "Engenharia / Suprimentos",
            "prioridade": "MÉDIA",
            "acao": "Analisar documentação técnica e cotações de hardware."
        }

    # Regra 12: Pipeline Comercial e CRM
    if re.search(r'(oportunidades de licita[cç][aã]o|status atual|aguardando publica[cç][aã]o|crm)', texto_completo):
        return {
            "categoria": "Pipeline Comercial e CRM",
            "destino": "Comercial / Gestão de Contas (Igor / Luana)",
            "prioridade": "MÉDIA",
            "acao": "Atualizar status dos projetos no CRM interno."
        }

    # Regra 4: Conselhos e Protocolos
    if re.search(r'(conselho regional|crt|baixa de registro|sinceti)', texto_completo):
        return {
            "categoria": "Conselhos e Protocolos",
            "destino": "Suporte Técnico / Administrativo (Alessandro)",
            "prioridade": "MÉDIA",
            "acao": "Verificar credenciais e andamento no sistema do respectivo Conselho."
        }

    # ==========================================
    # BLOCO 4: LIXO ELETRÔNICO E FALLBACK
    # ==========================================

    # Regra 1: Informativo / Descarte
    if re.search(r'(sigeo|documentos fiscais devolvidos)', texto_completo):
        return {
            "categoria": "Informativo / Descarte",
            "destino": "Nenhuma",
            "prioridade": "BAIXA",
            "acao": "Arquivar automaticamente sem acionar a equipe comercial."
        }

    # Fallback: E-mails não mapeados
    return {
        "categoria": "Não Classificado",
        "destino": "Triagem Manual",
        "prioridade": "DESCONHECIDA",
        "acao": "Requer análise humana e possível criação de nova regra (RuleOps)."
    }
