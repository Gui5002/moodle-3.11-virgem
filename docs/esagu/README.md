# Isolamento do tema EVAGU — etapa de refatoração para homologação

## Estado da entrega

Esta branch parte de `branch_esagu` e transfere alterações visuais comprovadas para
`theme/evagu`. **Não é uma versão pronta para produção nem uma migração concluída
para Moodle 4.x/5.x. O núcleo ainda contém alterações funcionais e visuais pendentes.**
Não atualizar o ambiente de produção com base apenas nesta refatoração.

Comparação completa dos snapshots Git: 50 arquivos modificados, 6.953 adicionados e
21 removidos (sem detecção de renomeação). A versão em `version.php` é igual nas duas
branches; isso não comprova que os plugins e o banco correspondam à mesma distribuição.
Os SHAs exatos estão em `restored-core-files.json`. `main` é a referência fornecida
pelo proprietário, não uma distribuição upstream validada nesta entrega.

## Implementação

22 arquivos voltaram byte a byte à referência `main`. Nenhuma tabela, configuração,
matrícula ou conta foi alterada por esta entrega. O nome/componente `theme_evagu` foi
mantido para preservar as configurações e os arquivos vinculados a ele no banco.

| Origem | Destino/decisão |
| --- | --- |
| CSS de myprofile, navigation e settings | `theme/evagu/style/esagu-core-overrides.css` |
| CSS de mídia, notas e feedback | Mesmo arquivo do tema |
| CSS do CodeMirror (fonte e build do Atto) | Mesmo arquivo do tema |
| Cor de hover dos cards no CSS compilado do Boost | Mesmo arquivo do tema |
| Classe `btn-block` removida do bloco login | Override CSS com escopo `.block_login` |
| `lib/templates/loginform.mustache` | Restaurado: o EVAGU já tem override próprio com o botão personalizado |
| Ícones de conclusão em `pix/i` | `theme/evagu/pix_core/i` (bytes preservados) |
| Mapeamentos catálogo/acadêmico em classe do núcleo | `theme/evagu/classes/output/icon_system_fontawesome.php` |
| Templates administrativos e myprofile, outline, YUI e dois CSS H5P | Restauradas diferenças de formatação sem mudança funcional identificada |

Os ícones catálogo/acadêmico usam `fa-check-circle` e `fa-question-circle`, nomes
compatíveis com o Font Awesome 4 presente no tema, em vez dos nomes de versão posterior.
O CSS extra é carregado antes dos estilos próprios já existentes do EVAGU. Isso evita
sobrepor deliberadamente o estilo final do tema; a cascata ainda exige teste visual.
Não copiamos o CSS completo do Boost para dentro do EVAGU.

## O que ainda impede afirmar que o núcleo está desacoplado

`core-audit.json` lista todos os arquivos modificados/removidos e sua situação.
`added-files.txt` lista os 6.953 arquivos adicionados, incluindo plugins e arquivos
fora das pastas esperadas. Ter `version.php` não basta para um diretório ser um plugin
válido: foram encontrados arquivos desse tipo até em `lib/guzzle`.

| Área pendente | Evidência / caminho de migração |
| --- | --- |
| Autenticação e cadastro | `lib/authlib.php` inclui `webservice/wspessoa.php` e valida CPF; migrar integração para plugin de autenticação/local com configuração e tratamento de falhas |
| Modelo de usuário | `lib/classes/user.php`, `user/editlib.php`, `login/signup_form.php`, `user/edit_form.php`, `user/editadvanced.php`; campos como CPF, cargo, lotação, SIAPE e `user_cargo` dependem do esquema real |
| Perfil público | `lib/myprofilelib.php` apresenta dados institucionais; migrar usando campos de perfil/callbacks com as mesmas regras de visibilidade |
| Matrículas, backup e mensagens | Diferenças em `lib/enrollib.php`, `lib/moodlelib.php`, `backup/moodle2/backup_stepslib.php` e `message/externallib.php`; auditar sem assumir que são apenas reformatação |
| Regras de cursos | Limites de nome breve diferentes na edição (15) e cópia (10), além de limite de nome completo (75); definir regra e ponto de extensão suportado |
| Busca e blog | Restrição de busca a administrador em `course/search.php`; publicação pública desativada em `blog/locallib.php`; manter até migrar política conscientemente |
| Menu e tradução | `admin/settings/appearance.php`, `lang/en/moodle.php` e pacote `lang/pt_br`; migrar para configuração de menu, strings de plugins e personalização de idioma em moodledata |
| Outros estilos | Classic, diálogos TinyMCE e exportação de privacidade ainda possuem diferenças; CSS do tema não alcança automaticamente documentos independentes/iframes |
| Busca/renderização | `course/renderer.php` e template de busca têm alterações de escape; auditar conjuntamente, sem retirar possível proteção como se fosse estilo |
| Recursos adicionais | Inventariar plugins EVA, OIDC/Office365, certificados, relatórios, endpoints e arquivos fora de plugins antes de substituir o core |

O próprio `theme/evagu/version.php` declara `$plugin->incompatible = 400`.
Essa restrição **não foi removida**: mudar o número não torna as APIs e templates
compatíveis com Moodle 4.0+. Há também numeração de versão legada atípica no plugin;
normalizá-la exige verificar a versão instalada no banco para não causar downgrade.

## Validação executada e limites

- `python3 tools/esagu/check_isolation.py`: verifica os 22 arquivos restaurados,
  proveniência dos dois SVGs, registro do CSS e preservação do template de login.
- `git diff --check`: passou nos arquivos novos/editados; a restauração literal de
  `lib/yuilib/3.17.2/assets/skin/sam/skin.css` reintroduz whitespace já presente na
  referência `main`, mantido para preservar a igualdade byte a byte.
- Revisão das diferenças CSS normalizadas para separar mudanças de estilo de formatação.
- Não foi executado Moodle, PHP lint, PHPUnit, Behat, comparação de screenshots ou
  atualização de banco. O ambiente de trabalho não dispõe de PHP/Moodle configurado.
- Arquivos do Git não incluem as configurações de aparência do banco, blocos instanciados,
  imagens enviadas e todo o conteúdo de moodledata. Portanto, identidade visual completa
  e compatibilidade funcional ainda não foram comprovadas.

## Como homologar

1. Criar cópia isolada do banco e moodledata, com backup restaurável e `config.php`
   próprio; desativar e-mails, cron e chamadas a integrações de produção nessa cópia.
2. Usar esta branch na homologação, mantendo `theme_evagu` e os plugins necessários.
3. Limpar caches: `php admin/cli/purge_caches.php`. Abrir também uma sessão anônima.
4. Comparar antes/depois nas mesmas páginas, usuários e tamanhos de tela: home, login
   (incluindo SSO), painel, catálogo, curso, perfil, administração, notas, feedback,
   vídeos, editor Atto e ícones de conclusão. Verificar teclado e contraste.
5. Testar cadastro, CPF, login institucional, edição de perfil, matrícula, conclusão,
   certificados, backup/restauração e relatórios. Registrar qualquer divergência.
6. Somente após migrar os itens pendentes para extensões e validar a versão de destino,
   ensaiar o caminho de atualização suportado em outra cópia. Confirmar requisitos de
   PHP/banco e compatibilidade individual de todos os plugins para essa versão.

Para reverter esta etapa, retornar ao commit de origem indicado no manifesto e limpar
caches. Isso só é reversão de código; uma futura atualização de banco exigirá restaurar
backup correspondente, não apenas trocar de branch.

## Informações necessárias para a próxima etapa

- Versão Moodle de destino e versões de PHP/banco disponíveis.
- Esquema anonimizado das tabelas/colunas institucionais e scripts de instalação usados;
  não enviar senhas, tokens, CPFs ou dados pessoais de produção.
- Configurações de aparência e blocos, mais referência visual das páginas na homologação.
- Contrato da integração de pessoas e comportamento esperado de CPF, cargo e matrícula.

## Referências técnicas

- https://moodledev.io/docs/5.1/apis/plugintypes/theme
- https://docs.moodle.org/dev/Templates
- A implementação de `lib/outputlib.php` do próprio Moodle 3.11 confirma a resolução
  de ícones em `pix_core`; `theme/evagu/config.php` já usa a fábrica de renderers do tema.

As referências modernas descrevem os mecanismos; esta branch continua destinada
à validação no Moodle 3.11 e não declara compatibilidade com essas versões modernas.
