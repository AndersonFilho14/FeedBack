from typing import Optional

class ValidadorCampos:
    
    def validar_campos_preenchidos(campos: list) -> Optional[str]:
        """ Verifica se todos os campos obrigatórios foram preenchidos."""
        
        if any(valor in [None, ""] for valor in campos):
            return "Todos os campos obrigatórios devem ser preenchidos."
        return None