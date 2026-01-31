class MetaAdFields:
    ID = 'id'
    PERIODO_INICIO = 'veiculacao_inicio'
    PERIODO_FIM = 'veiculacao_fim'
    TAMANHO_PUBLICO = 'tamanho_estimado_publico'
    VALOR_GASTO = 'valor_gasto_medio_brl'
    IMPRESSOES = 'impressoes_media'
    PAGO_POR = 'pago_por'
    TEXTO = 'texto'

    @staticmethod
    def fields() -> list[str]:
        return [
            MetaAdFields.ID,
            MetaAdFields.PERIODO_INICIO,
            MetaAdFields.PERIODO_FIM,
            MetaAdFields.TAMANHO_PUBLICO,
            MetaAdFields.VALOR_GASTO,
            MetaAdFields.IMPRESSOES,
            MetaAdFields.PAGO_POR,
            MetaAdFields.TEXTO
        ]

