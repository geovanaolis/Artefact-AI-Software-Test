import sys
import os

# Adiciona a pasta raiz do projeto ao PATH do Python para importar o agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import run_agent

def test_empório_assistant():
    print("=" * 70)
    print("🤖 INICIANDO SUÍTE DE TESTES AUTOMATIZADOS - EMPÓRIO DA MÚSICA")
    print("=" * 70)

    # Lista de cenários de teste (RAG, SQL e Perguntas Combinadas)
    test_cases = [
        {
            "category": "RAG (Políticas da Loja - PDF)",
            "query": "Qual é o endereço físico da loja e qual o horário de funcionamento nos sábados?"
        },
        {
            "category": "RAG (Políticas da Loja - PDF)",
            "query": "Qual é a política de trocas e devoluções para instrumentos com defeito?"
        },
        {
            "category": "SQL (Consulta ao Banco Operacional)",
            "query": "Quais são os produtos disponíveis da categoria de Cordas e quais seus respectivos preços e estoques?"
        },
        {
            "category": "SQL (Consulta ao Banco Operacional)",
            "query": "Existem promoções ativas no momento? Liste o nome da promoção e o desconto."
        },
        {
            "category": "Combinado (SQL + RAG)",
            "query": "Quero comprar um violão Yamaha. Qual é o preço dele em estoque e quais são as opções de parcelamento permitidas pela loja?"
        }
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\n[Teste {i}/{len(test_cases)}] {test['category']}")
        print(f"📌 Pergunta: {test['query']}")
        print("-" * 50)
        
        try:
            response = run_agent(test['query'])
            print(f"🤖 Resposta do Agente:\n{response}\n")
            print("✅ Status: PASCOU")
            passed += 1
        except Exception as e:
            print(f"❌ Status: FALHOU com erro -> {str(e)}")
            failed += 1
        print("=" * 70)

    print(f"\n📊 RESUMO DOS TESTES: {passed} APROVADOS | {failed} FALHAS")

if __name__ == "__main__":
    test_empório_assistant()