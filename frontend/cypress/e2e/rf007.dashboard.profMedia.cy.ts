describe("RF007 - Melhores notas por professor", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/dashboard/municipio/**").as("getDashboard");
    cy.visit("/dashboard/municipio/1");
    cy.wait("@getDashboard");
  });

  it("Deve mostrar a seção 'Média por Professor' com professores e médias visíveis", () => {
    cy.contains("Média por Professor", { timeout: 20000 }).should("be.visible");

    // Verifica que existe pelo menos um professor listado
    cy.get('[data-testid="media-professor"]').should("have.length.greaterThan", 0);

    cy.get('[data-testid="media-professor"]').first().within(() => {
      cy.get(".professor-nome").should("not.be.empty");
      cy.get(".professor-media").should("not.be.empty");
    });
  });

  it("Deve falhar porque espera que não haja professores listados", () => {
    cy.contains("Média por Professor", { timeout: 20000 }).should("be.visible");

    // Aqui esperamos explicitamente que não haja nenhum professor listado, o que deve falhar
    cy.get('[data-testid="media-professor"]').should("have.length", 0);
  });
});
