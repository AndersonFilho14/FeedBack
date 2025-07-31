
describe('Teste de Login', () => {
  it('login válido redireciona para /InicialProfessor', () => {
    cy.intercept('GET', '**/acesso/prof_alfa/senha123', {
      statusCode: 200,
      body: {
        id_user: 1,
        nome: "Prof. Ana Silva",
        cargo: "Professor",
        token: "UHJvZi4gQW5hIFNpbHZh"
      },
    });
    cy.visit('http://localhost:3000/Login');
    cy.get('input[name="User"]').type('prof_alfa');
    cy.get('input[name="password"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/InicialProfessor');
  });

  it('login inválido exibe mensagem de erro', () => {
    cy.intercept('GET', '**/acesso/usuario_errado/senha_errada', {
      statusCode: 401,
      body: {},
    });
    cy.visit('http://localhost:3000/Login');
    cy.get('input[name="User"]').type('usuario_errado');
    cy.get('input[name="password"]').type('senha_errada');
    cy.get('button[type="submit"]').click();
    cy.contains('Usuário ou senha inválidos.').should('be.visible');
  });
});
