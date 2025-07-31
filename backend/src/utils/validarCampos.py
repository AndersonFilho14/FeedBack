from typing import Optional

class ValidadorCampos:
    
    def validar_campos_preenchidos(campos: list) -> Optional[str]:
        """ Verifica se todos os campos obrigatórios foram preenchidos."""
        
        if any(valor in [None, ""] for valor in campos):
            return "Todos os campos obrigatórios devem ser preenchidos."
        return None
    
    def validar_cpf(cpf: str) -> Optional[str]:
        """ Valida o CPF informado."""
        
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return "CPF inválido. Deve conter 11 dígitos numéricos."
        return None
    
    def validar_telefone(telefone: str) -> Optional[str]:
        """ Valida o formato do telefone informado."""
        
        if not telefone or len(telefone) < 10 or not telefone.isdigit():
            return "Telefone inválido. Deve conter pelo menos 10 dígitos numéricos."
        return None
    
    def validar_email(email: str) -> Optional[str]:
        """ Valida o formato do email informado."""
        
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            return "Email inválido. Deve conter um formato válido."
        return None