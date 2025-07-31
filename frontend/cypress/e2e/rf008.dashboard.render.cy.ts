describe("Dashboard - Renderização", () => {
  beforeEach(() => {
    
    cy.intercept("GET", "http://localhost:5000/dashboard/municipio/**").as("getDashboard");

    
    cy.visit("http://localhost:3000/dashboard");

    
    cy.wait("@getDashboard");
  });

  it("Deve exibir o título da página e todos os blocos principais", () => {
 
    cy.contains("h1, h2", "Dashboard do Município").should("be.visible");

    
    cy.contains("Ranking Top 5 Média de Alunos", { timeout: 20000 }).should("be.visible");
    cy.contains("Média por Turma", { timeout: 20000 }).should("be.visible");
    cy.contains("Média por Escola", { timeout: 20000 }).should("be.visible");
    cy.contains("Ranking de Professores por Média", { timeout: 20000 }).should("be.visible");
    cy.contains("IA", { timeout: 20000 }).should("be.visible");
  });
});
