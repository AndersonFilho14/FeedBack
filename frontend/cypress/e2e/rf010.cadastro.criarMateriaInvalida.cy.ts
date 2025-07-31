
describe('RF010 - Validação ao tentar cadastrar matéria sem nome', () => {
  it('Deve exibir erro ao tentar cadastrar matéria sem preencher o nome', () => {
    cy.visit('http://localhost:3000/materia/form');

  
    cy.get('button[name="Cadastrar"]').click();

   
    cy.get('input[name="nome"]:invalid').should('exist');
    
   
  });
});
