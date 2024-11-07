# Sistema de Reservas para Condomínio - Salão e Churrasqueira

Este sistema de reservas foi desenvolvido para gerenciar reservas de espaços comuns em um condomínio (ex.: salão de festas e churrasqueiras). O sistema permite a criação, visualização, atualização e cancelamento de reservas com controle de conflitos, mensagens de erro adequadas, e persistência de dados. A aplicação utiliza padrões de projeto estruturais `Facade` e `Proxy` para simplificar a interação e garantir segurança nas operações de reservas.

## Funcionalidades

1. **Cadastro de Reservas (Create)**:
   - O usuário escolhe o espaço e a data para a reserva.
   - O sistema verifica se o espaço está disponível para a data escolhida.
   - Em caso positivo, a reserva é criada com um ID único e salva em um arquivo JSON.
   - Caso o espaço já esteja reservado, o sistema retorna uma mensagem de erro.

2. **Visualização de Reservas (Read)**:
   - Permite que os moradores vejam suas reservas e visualizem todas as reservas de um espaço em uma data específica.
   - Possui filtros por morador, data e espaço para facilitar a busca.

3. **Atualização de Reservas (Update)**:
   - Permite que o morador atualize a data ou o espaço de uma reserva existente, desde que haja disponibilidade.
   - A atualização verifica se o ID da reserva existe e se o usuário é o criador da reserva.
   - Caso contrário, uma mensagem de erro é exibida.

4. **Cancelamento de Reservas (Delete)**:
   - Permite que o morador cancele sua reserva, verificando a identidade do usuário.
   - Remove a reserva do banco de dados se as condições forem atendidas.

5. **Controle de Conflitos e Mensagens de Erro**:
   - Mensagens de erro claras são retornadas quando há conflitos de disponibilidade ou permissões de acesso.
   
6. **Persistência e Sincronização dos Dados**:
   - As operações de criação, atualização e exclusão são salvas em um arquivo JSON para garantir a persistência dos dados.
   - Ao iniciar a aplicação, os dados são carregados do arquivo para sincronizar o estado atual.

## Padrões de Projeto Utilizados

### Facade
O padrão `Facade` é utilizado para simplificar o acesso às funcionalidades principais do sistema (criação, visualização, atualização e cancelamento de reservas). Em vez de interagir diretamente com várias classes e métodos de verificação, o usuário utiliza uma interface única para todas as operações. O `Facade` centraliza a lógica do sistema, facilitando o uso e a manutenção do código.

### Proxy
O padrão `Proxy` é implementado para garantir a segurança e a integridade das reservas. Esse padrão é utilizado nas operações de **atualização** e **cancelamento** de reservas, onde o sistema verifica se o usuário que está realizando a ação é o criador da reserva. Caso contrário, o `Proxy` bloqueia a ação e retorna uma mensagem de "Acesso negado", garantindo que apenas o proprietário da reserva possa modificá-la ou excluí-la.

## Tecnologias Utilizadas

- **Linguagem**: JavaScript
- **Armazenamento de Dados**: Arquivo JSON
- **Frameworks/Bibliotecas**: Nenhum (código simples para iniciantes)

## Como Executar a Aplicação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/nome-do-repositorio.git
