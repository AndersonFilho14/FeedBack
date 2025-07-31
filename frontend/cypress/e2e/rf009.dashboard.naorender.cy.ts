

describe("Dashboard do Município", () => {
  // Antes de cada teste, visita a página do dashboard.
  // Certifique-se de atualizar '/dashboard' para a rota real da sua página.
  beforeEach(() => {
    cy.visit("http://localhost:3000/dashboard"); 
  });


  it("deve falhar se o título principal for alterado para um valor incorreto", () => {
    // Obtemos o título principal da página.
    // O nome da classe contém caracteres especiais '[' e ']', então precisamos escapá-los.
    cy.get("h1.font-\\[Jomolhari\\]")
      // Primeiro, confirmamos que ele contém o texto CORRETO para garantir que selecionamos o elemento certo.
      .should("contain.text", "Dashboard do Município")
      // AGORA, INVALIDAMOS: Afirmamos que o título NÃO deve conter um texto incorreto.
      // Este teste PASSA se o título estiver correto.
      // Ele FALHA se alguém alterar o título para "Relatório Geral", capturando a regressão.
      .and("not.contain.text", "Relatório Geral");
  });

 
});