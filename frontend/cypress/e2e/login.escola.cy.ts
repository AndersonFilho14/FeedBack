//O sistema deve permitir login com autenticação por perfil (professor, gestor, …).
describe('Teste de Login de escola', () => {
  it('login válido redireciona para /MunicipioMain', () => {
    cy.intercept('GET', '**/acesso/municipio_alfa/senha123', {
      statusCode: 200,
      body: {
                id_user: 1,
                nome: "Cidade Alpha",
                cargo: "Municipio",
                token: "Q2lkYWRlIEFscGhh"
        },
    });
    cy.visit('http://localhost:3000/Login');
    cy.get('input[name="User"]').type('municipio_alfa');
    cy.get('input[name="password"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/MunicipioMain');
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
