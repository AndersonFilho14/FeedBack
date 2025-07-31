describe("Dashboard - Renderização", () => {
  beforeEach(() => {
    // Intercepta a requisição dos dados do dashboard
    cy.intercept("GET", "http://localhost:5000/dashboard/municipio/**").as("getDashboard");

    // Visita a página
    cy.visit("http://localhost:3000/dashboard");

    // Aguarda a requisição do dashboard ser concluída
    cy.wait("@getDashboard");
  });

  it("Deve exibir o título da página e todos os blocos principais", () => {
    // Título principal
    cy.contains("h1, h2", "Dashboard do Município").should("be.visible");

    // Blocos de dados com timeout estendido para garantir carregamento
    cy.contains("Ranking Top 5 Média de Alunos", { timeout: 20000 }).should("be.visible");
    cy.contains("Média por Turma", { timeout: 20000 }).should("be.visible");
    cy.contains("Média por Escola", { timeout: 20000 }).should("be.visible");
    cy.contains("Ranking de Professores por Média", { timeout: 20000 }).should("be.visible");
    cy.contains("IA", { timeout: 20000 }).should("be.visible");
  });
});
