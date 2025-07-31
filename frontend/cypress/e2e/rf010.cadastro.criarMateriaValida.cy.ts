// cypress/e2e/materia/criarMateriaValida.cy.ts



describe('RF010 - Cadastro de nova matéria com dados válidos', () => {
  const materiaNome = 'Materia Teste Cypress';

  it('Deve cadastrar nova matéria com sucesso', () => {
   
    cy.visit('http://localhost:3000/materia/form');

   
    cy.get('form').should('exist');
    cy.get('input[name="nome"]').should('be.visible');

   
    cy.get('input[name="nome"]').type(materiaNome);
    cy.get('button[name="Cadastrar"]').click();

    cy.contains('Matéria criada com sucesso').should('be.visible');

   
    cy.visit('http://localhost:3000/materia');
    cy.contains(materiaNome).should('exist');
  });
});



