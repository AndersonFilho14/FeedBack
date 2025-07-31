

describe("Dashboard do Município", () => {
  
  beforeEach(() => {
    cy.visit("http://localhost:3000/dashboard"); 
  });


  it("deve falhar se o título principal for alterado para um valor incorreto", () => {
    
    cy.get("h1.font-\\[Jomolhari\\]")
     
      .should("contain.text", "Dashboard do Município")
      
      .and("not.contain.text", "Relatório Geral");
  });

 
});