describe("Dashboard - Geração de PDF", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/dashboard");
  });

  it("Deve permitir clicar no botão de gerar PDF e conter o conteúdo a ser exportado", () => {
    cy.get("button")
      .contains("Baixar PDF")
      .should("be.visible")
      .and("not.be.disabled")
      .click();

    cy.get("#relatorio-completo").should("exist").and("not.be.empty");
  });
});
